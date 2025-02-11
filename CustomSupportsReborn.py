#--------------------------------------------------------------------------------------------
# Initial Copyright(c) 2018 Ultimaker B.V.
# Copyright (c) 2022 5axes
# Reborn version Copyright 2025 Slashee the Cow
#--------------------------------------------------------------------------------------------
# Based on the SupportBlocker plugin by Ultimaker B.V., and licensed under LGPLv3 or higher.
##  https://github.com/Ultimaker/Cura/tree/master/plugins/SupportEraser
##--------------------------------------------------------------------------------------------
# All modifications 15 April-2020 to 13 March 2023 Copyright(c) 5@xes 
#--------------------------------------------------------------------------------------------
# First release 05-18-2020  to change the initial plugin into cylindric support
# Modif 0.01 : Cylinder length -> Pick Point to base plate height
# Modif 0.02 : Using  support_tower_diameter as variable to define the cylinder
# Modif 0.03 : Using a special parameter  diameter_custom_support as variable to define the cylinder
# Modif 0.04 : Add a text field to define the diameter
# Modif 0.05 : Add checkbox and option to switch between Cube / Cylinder
# Modif 0.06 : Symplify code and store defaut size support in Preference "customsupportcylinder/s_size" default value 5
# V0.9.0 05-20-2020
# V1.0.0 06-01-2020 catalog.i18nc("@label","Size") on QML
# V1.0.1 06-20-2020 Add Angle for conical support
# V2.0.0 07-04-2020 Add Button and custom support type
# V2.0.1 
# V2.1.0 10-04-2020 Add Abutment support type
# V2.2.0 10-05-2020 Add Tube support type
# V2.3.0 10-18-2020 Add Y direction and Equalize heights for Abutment support type
# V2.4.0 01-21-2021 New option Max size to limit the size of the base
# V2.4.1 01-24-2021 By default support are not define with the property support_mesh_drop_down = True
# V2.5.0 03-07-2021 Freeform (Cross/Section/Pillar/Custom)
# V2.5.1 03-08-2021 Mirror & Rotate freeform support
# V2.5.2 03-09-2021 Bridge freeform support Bridge and rename Pillar
# V2.5.3 03-10-2021 Add "arch-buttress" type
# V2.5.5 03-11-2021 Minor modification on freeform design
#
# V2.6.0 03-05-2022 Update for Cura 5.0
# V2.6.1 18-05-2022 Update for Cura 5.0 QML with UM.ToolbarButton
# V2.6.2 19-05-2022 Scale Also in Main direction
# V2.6.3 25-05-2022 Temporary ? solution for the Toolbar height in QT6
# V2.6.4 31-05-2022 Add Button Remove All
#                   Increase the Increment angle for Cylinder and Tube from 2° to 10°
# V2.6.5 11-07-2022 Change Style of Button for Cura 5.0  5.1
# V2.6.6 07-08-2022 Internal modification for Maximum Z height
# V2.7.0 18-01-2023 Prepare translation
# V2.7.1 02-02-2023 Replace Rotation 180° / Auto Orientation for FreeForm Model
#
# V2.8.0 09-02-2023 Add Define As Model For Cylindrical Model
#--------------------------------------------------------------------------------------------
# Release history for Reborn version by Slashee the Cow 2025-
#--------------------------------------------------------------------------------------------
# v1.0.0 - Initial release.
#   Reverted everything to v2.8.0 manually as the version in the master branch seems to contain some "work in progress" stuff.
#   Renamed everything. Including internally so it doesn't compete with 5@xes' verison if you still have that installed.
#   Futzed around with the translation system and ended up with basically the same thing. If someone wants to translate it, get in touch!
#   Removed support for Qt 5 and bumped minimum Cura version to 5.0 so I'm not doing things twice and can use newer Python features if I need.
#   Cleaned up the code a little bit and tried to give some variables more readable names.
#   Changed the icon to illustrate it does more than cylinders. Now it looks like it does rockets.
#   Renamed "Freeform" to "Model" and "Custom" to "Line" and swapped their positions.
#   Input validation in the text fields! Resetting if you put in something invalid! Preventing bugs from conflicting settings!
# v1.0.1 - 2025-02-05
#   Fixed control panel for Cura versions < 5.7.
#   Control panel input validation now a little less strict. You can set the support size to above the max size now and it'll change the max size to match.
# v1.1.0
#   Headline: now you can taper inwards!
#   -   The inner part of a tube also tapers now!
#   Changed icons for abutment and model support types.
#   Model combo box now remembers what model you had selected.

from PyQt6.QtCore import Qt, QTimer, QObject, QVariant, pyqtProperty
from PyQt6.QtQml import qmlRegisterType
from PyQt6.QtWidgets import QApplication

import math
import numpy
import os.path
import trimesh

from cura.CuraApplication import CuraApplication
from cura.PickingPass import PickingPass
from cura.Operations.SetParentOperation import SetParentOperation
from cura.Scene.SliceableObjectDecorator import SliceableObjectDecorator
from cura.Scene.BuildPlateDecorator import BuildPlateDecorator
from cura.Scene.CuraSceneNode import CuraSceneNode

from UM.Controller import Controller
from UM.Logger import Logger
from UM.Message import Message
from UM.Math.Matrix import Matrix
from UM.Math.Vector import Vector
from UM.Tool import Tool
from UM.Event import Event, MouseEvent
from UM.Mesh.MeshBuilder import MeshBuilder
from UM.Mesh.MeshData import MeshData, calculateNormalsFromIndexedVertices

from UM.Operations.GroupedOperation import GroupedOperation
from UM.Operations.AddSceneNodeOperation import AddSceneNodeOperation
from UM.Operations.RemoveSceneNodeOperation import RemoveSceneNodeOperation
from UM.Scene.Iterator.DepthFirstIterator import DepthFirstIterator
from UM.Scene.Selection import Selection
from UM.Scene.SceneNode import SceneNode
from UM.Tool import Tool
from UM.Settings.SettingInstance import SettingInstance
from UM.Resources import Resources
from UM.i18n import i18nCatalog

#Resources.addSearchPath(
#    os.path.join(os.path.abspath(os.path.dirname(__file__)))
#)  # Plugin translation file import

i18n_catalog = i18nCatalog("customsupportsreborn")

#if i18n_catalog.hasTranslationLoaded():
#    Logger.log("i", "Custom Supports Reborn translation loaded")

DEBUG_MODE = True

def log(level, message):
    """Wrapper function for logging messages using Cura's Logger, but with debug mode so as not to spam you."""
    if level == "d" and DEBUG_MODE:
        Logger.log("d", message)
    elif level == "i":
        Logger.log("i", message)
    elif level == "w":
        Logger.log("w", message)
    elif level == "e":
        Logger.log("e", message)
    elif level == "c":
        Logger.log("c", message)
    elif DEBUG_MODE:
        Logger.log("w", f"Invalid log level: {level} for message {message}")

SUPPORT_TYPE_CYLINDER = "cylinder"
SUPPORT_TYPE_TUBE = "tube"
SUPPORT_TYPE_CUBE = "cube"
SUPPORT_TYPE_ABUTMENT = "abutment"
SUPPORT_TYPE_LINE = "line"
SUPPORT_TYPE_MODEL = "model"

class CustomSupportsReborn(Tool):

    #_translations = CustomSupportsRebornTranslations()
    #plugin_name = "@CustomSupportsReborn:"

    def __init__(self):
       
        super().__init__()

        Resources.addSearchPath(os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "resources"
        )))  # Plugin translation file import

        self._catalog = i18nCatalog("customsupportsreborn")

        self.setExposedProperties("SupportType", "ModelSubtype", "SupportSize", "SupportSizeMax", "SupportSizeInner", "SupportAngle", "SupportYDirection", "AbutmentEqualizeHeights", "ModelScaleMain", "ModelOrient", "ModelMirror", "PanelRemoveAllText")

        self._supports_created: list[SceneNode] = []
        
        self._line_points: int = 0  
        self._support_heights: float = 0.0
        
        # variable for menu dialog        
        self._support_size: float = 2.0
        self._support_size_max: float = 10.0
        self._support_size_inner: float = 0.0
        self._support_angle: float = 0.0
        self._support_y_direction: bool = False
        self._abutment_equalize_heights: bool = True
        self._model_scale_main: bool = True
        self._model_orient: bool = False
        self._model_mirror: bool = False
        self._support_type: str = SUPPORT_TYPE_CYLINDER
        self._model_subtype: str = "cross"
        self._model_hide_message:bool = False # To avoid message 
        self._panel_remove_all_text: str = self._catalog.i18nc("panel:remove_all", "Remove All")

        # Shortcut
        self._shortcut_key: Qt.Key = Qt.Key.Key_F
            
        self._controller: Controller = self.getController()
        self._application: CuraApplication = CuraApplication.getInstance()

        self._custom_point_location: Vector = Vector(0,0,0)
        self._selection_pass: SceneNode = None

        self._taper_direction = ""
        self._effective_taper_angle = 0
        
        
        # Note: if the selection is cleared with this tool active, there is no way to switch to
        # another tool than to reselect an object (by clicking it) because the tool buttons in the
        # toolbar will have been disabled. That is why we need to ignore the first press event
        # after the selection has been cleared.
        Selection.selectionChanged.connect(self._onSelectionChanged)
        self._had_selection = False
        self._skip_press = False

        self._had_selection_timer = QTimer()
        self._had_selection_timer.setInterval(0)
        self._had_selection_timer.setSingleShot(True)
        self._had_selection_timer.timeout.connect(self._selectionChangeDelay)
        
        # set the preferences to store the default value
        self._preferences = CuraApplication.getInstance().getPreferences()
        self._preferences.addPreference("customsupportsreborn/support_size", 5)
        self._preferences.addPreference("customsupportsreborn/support_size_max", 10)
        self._preferences.addPreference("customsupportsreborn/support_size_inner", 2)
        self._preferences.addPreference("customsupportsreborn/support_angle", 0)
        self._preferences.addPreference("customsupportsreborn/support_y_direction", False)
        self._preferences.addPreference("customsupportsreborn/abutment_equalize_heights", True)
        self._preferences.addPreference("customsupportsreborn/model_scale_main", True)
        self._preferences.addPreference("customsupportsreborn/model_orient", False)
        self._preferences.addPreference("customsupportsreborn/model_mirror", False)
        self._preferences.addPreference("customsupportsreborn/support_type", SUPPORT_TYPE_CYLINDER)
        self._preferences.addPreference("customsupportsreborn/model_subtype", "cross")
        
        # convert as float to avoid further issue
        self._support_size = float(self._preferences.getValue("customsupportsreborn/support_size"))
        self._support_size_max = float(self._preferences.getValue("customsupportsreborn/support_size_max"))
        self._support_size_inner = float(self._preferences.getValue("customsupportsreborn/support_size_inner"))
        self._support_angle = float(self._preferences.getValue("customsupportsreborn/support_angle"))
        # convert as boolean to avoid further issue
        self._support_y_direction = bool(self._preferences.getValue("customsupportsreborn/support_y_direction"))
        self._abutment_equalize_heights = bool(self._preferences.getValue("customsupportsreborn/abutment_equalize_heights"))
        self._model_scale_main = bool(self._preferences.getValue("customsupportsreborn/model_scale_main"))
        self._model_orient = bool(self._preferences.getValue("customsupportsreborn/model_orient"))
        self._model_mirror = bool(self._preferences.getValue("customsupportsreborn/model_mirror"))
        # convert as string to avoid further issue
        self._support_type = str(self._preferences.getValue("customsupportsreborn/support_type"))
        # Sub type for Free Form support
        self._model_subtype = str(self._preferences.getValue("customsupportsreborn/model_subtype"))

        self._setEffectiveTaperAngle()

                
    def event(self, event):
        super().event(event)
        modifiers = QApplication.keyboardModifiers()
        ctrl_is_active = modifiers & Qt.KeyboardModifier.ControlModifier
        # shift_is_active = modifiers & Qt.KeyboardModifier.ShiftModifier
        alt_is_active = modifiers & Qt.KeyboardModifier.AltModifier

        
        if event.type == Event.MousePressEvent and MouseEvent.LeftButton in event.buttons and self._controller.getToolsEnabled():
            if ctrl_is_active:
                self._controller.setActiveTool("TranslateTool")
                return

            if alt_is_active:
                self._controller.setActiveTool("RotateTool")
                return
                
            if self._skip_press:
                # The selection was previously cleared, do not add/remove an support mesh but
                # use this click for selection and reactivating this tool only.
                self._skip_press = False
                self._support_heights=0
                return

            if self._selection_pass is None:
                # The selection renderpass is used to identify objects in the current view
                self._selection_pass = CuraApplication.getInstance().getRenderer().getRenderPass("selection")
                
            picked_node = self._controller.getScene().findObject(self._selection_pass.getIdAtPosition(event.x, event.y))
            
            
            if not picked_node:
                # There is no slicable object at the picked location
                return

            node_stack = picked_node.callDecoration("getStack")
            if node_stack:
                if node_stack.getProperty("support_mesh", "value") and not alt_is_active:
                    self._removeSupportMesh(picked_node)
                    self._support_heights=0
                    return

                elif node_stack.getProperty("anti_overhang_mesh", "value") or node_stack.getProperty("infill_mesh", "value") or node_stack.getProperty("cutting_mesh", "value"):
                    # Only "normal" meshes can have support_mesh added to them
                    return

            # Create a pass for picking a world-space location from the mouse location
            active_camera = self._controller.getScene().getActiveCamera()
            picking_pass = PickingPass(active_camera.getViewportWidth(), active_camera.getViewportHeight())
            picking_pass.render()
            
            
            if self._support_type == 'line': 
                self._line_points += 1
                if self._line_points == 2 :
                    picked_position =  self._line_point_location 
                    picked_position_b = picking_pass.getPickedPosition(event.x, event.y)
                    self._line_point_location = picked_position_b
                    self._line_points = 0
                    # Add the support_mesh cube at the picked location
                    self._createSupportMesh(picked_node, picked_position,picked_position_b)
                else:
                    self._line_point_location = picking_pass.getPickedPosition(event.x, event.y)
            
            else:
                self._line_points = 0
                picked_position =  picking_pass.getPickedPosition(event.x, event.y)
                picked_position_b = picking_pass.getPickedPosition(event.x, event.y)
                self._line_point_location = picked_position_b
                    
                # Add the support_mesh cube at the picked location
                self._createSupportMesh(picked_node, picked_position,picked_position_b)


    def _createSupportMesh(self, parent: CuraSceneNode, position_start: Vector , position_end: Vector):
        node = CuraSceneNode()
        node_name = parent.getName()

        node_bounds = parent.getBoundingBox()
        self._nodeHeight = node_bounds.height
        
        # Logger.log("d", "Height Model= %s", str(node_bounds.height))
        
        if self._support_type == SUPPORT_TYPE_CYLINDER:
            node.setName(self._catalog.i18nc("nodeNames:cylinder", "CustomSupportCylinder"))
        elif self._support_type == SUPPORT_TYPE_TUBE:
            node.setName(self._catalog.i18nc("nodeNames:tube", "CustomSupportTube"))
        elif self._support_type == SUPPORT_TYPE_CUBE:
            node.setName(self._catalog.i18nc("nodeNames:cube", "CustomSupportCube"))
        elif self._support_type == SUPPORT_TYPE_ABUTMENT:
            node.setName(self._catalog.i18nc("nodeNames:abutment", "CustomSupportAbutment"))
        elif self._support_type == SUPPORT_TYPE_LINE:
            node.setName(self._catalog.i18nc("nodeNames:line", "CustomSupportLine"))
        elif self._support_type == SUPPORT_TYPE_MODEL:
            node.setName(self._catalog.i18nc("nodeNames:model", "CustomSupportModel"))
        else:
            node.setName(self._catalog.i18nc("@errors:node_support_type"), "CustomSupportError")
            self._logger.log("w", "CustomSupportsReborn: Creating a node without a valid support_type")
            
        node.setSelectable(True)

        # Prevent big circus tents.
        use_support_angle = self._effective_taper_angle if self._support_size != self._support_size_max else 0
        
        # long=Support Height
        self._length=position_start.y
        # Logger.log("d", "Long Support= %s", str(self._long))
        
        # Limitation for support height to Node Height
        # For Cube/Cylinder/Tube
        # Test with 0.5 because the precision on the clic poisition is not very thight 
        if self._length >= (self._nodeHeight-0.5) :
            # additionale length
            self._top_added_height = 0
        else :
            if self._support_type == SUPPORT_TYPE_CUBE:
                self._top_added_height = self._support_size*0.5
            elif self._support_type == SUPPORT_TYPE_ABUTMENT:
                self._top_added_height = self._support_size
            else :
                self._top_added_height = self._support_size*0.1
                
        # Logger.log("d", "Additional Long Support = %s", str(self._long+self._Sup))    
            
        if self._support_type == SUPPORT_TYPE_CYLINDER:
            # Cylinder creation Diameter , Maximum diameter , Increment angle 10°, length , top Additional Height, Angle of the support
            mesh = self._createCylinder(self._support_size, self._support_size_max, 10, self._length, self._top_added_height, use_support_angle, self._taper_direction)
        elif self._support_type == SUPPORT_TYPE_TUBE:
            # Tube creation Diameter ,Maximum diameter , Diameter Int, Increment angle 10°, length, top Additional Height , Angle of the support
            mesh =  self._createTube(self._support_size, self._support_size_max, self._support_size_inner, 10, self._length, self._top_added_height, use_support_angle, self._taper_direction)
        elif self._support_type == SUPPORT_TYPE_CUBE:
            # Cube creation Size,Maximum Size , length , top Additional Height, Angle of the support
            mesh =  self._createCube(self._support_size, self._support_size_max, self._length, self._top_added_height, use_support_angle, self._taper_direction)
        elif self._support_type == SUPPORT_TYPE_MODEL:
            # Cube creation Size , length
            mesh = MeshBuilder()  
            model_definition_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", self._model_subtype + ".stl")
            # Logger.log('d', 'Model_definition_path : ' + str(model_definition_path)) 
            load_mesh = trimesh.load(model_definition_path)
            origin = [0, 0, 0]
            DirX = [1, 0, 0]
            DirY = [0, 1, 0]
            DirZ = [0, 0, 1]
            
            # Solution must be tested ( other solution just on the X Axis)
            if self._model_scale_main :
                if (self._length * 0.5 ) < self._support_size :
                    Scale = self._support_size
                else :
                    Scale = self._length * 0.5
                load_mesh.apply_transform(trimesh.transformations.scale_matrix(Scale, origin, DirX))
                load_mesh.apply_transform(trimesh.transformations.scale_matrix(Scale, origin, DirY))
            else :
                load_mesh.apply_transform(trimesh.transformations.scale_matrix(self._support_size, origin, DirX))
                load_mesh.apply_transform(trimesh.transformations.scale_matrix(self._support_size, origin, DirY))
                
            # load_mesh.apply_transform(trimesh.transformations.scale_matrix(self._UseSize, origin, DirY))
 
            load_mesh.apply_transform(trimesh.transformations.scale_matrix(self._length, origin, DirZ)) 
            
            # Logger.log('d', "Info Orient Support --> " + str(self._OrientSupport))
            if self._model_orient:
                # This function can be triggered in the middle of a machine change, so do not proceed if the machine change has not done yet.
                global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()
                adhesion_key = "adhesion_type"
                adhesion_value=global_container_stack.getProperty(adhesion_key, "value")
                   
                if adhesion_value == 'none' :
                    adhesion_options = global_container_stack.getProperty(adhesion_key, "options")

                    global_container_stack.setProperty("adhesion_type", "value", "skirt")
                    log('d', "Info adhesion_type --> " + str(adhesion_value)) 
                    if not self._model_hide_message :
                        try:
                            translated_skirt_label = adhesion_options["skirt"]
                        except:
                            translated_skirt_label = "Skirt"  # Fallback if "skirt" is not in options (unlikely but good practice)
                            Logger.log("w", "Setting adhesion_type does not have 'skirt' as an option")
                        adhesion_label=global_container_stack.getProperty("adhesion_type", "label") 
                        warning_string = f"{self._catalog.i18nc('model_warning_dialog:start', 'Had to change setting')} {adhesion_label} {self._catalog.i18nc('model_warning_dialog:middle', 'to')} {translated_skirt_label} {self._catalog.i18nc('model_warning_dialog:end','for calculation purposes. You may want to change it back to its previous value.')}"
                        Message(text = warning_string, title = self._catalog.i18nc("model_warning_dialog:title", "WARNING: Custom Supports Reborn").show())
                        self._model_hide_message = True
                    # Define temporary adhesion_type=skirt to force boundary calculation ?
                _angle = self.defineAngle(node_name,position_start)
                if self._support_y_direction:
                    _angle = self.mainAngle(_angle)
                log('d', 'Angle : ' + str(_angle))
                load_mesh.apply_transform(trimesh.transformations.rotation_matrix(_angle, [0, 0, 1]))
            
            elif self._support_y_direction:
                load_mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(90), [0, 0, 1]))

            if self._model_mirror and not self._model_orient:
                load_mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(180), [0, 0, 1]))
                
            mesh =  self._toMeshData(load_mesh)
            
        elif self._support_type == SUPPORT_TYPE_ABUTMENT:
            # Abutement creation Size , length , top
            if self._abutment_equalize_heights :
                # Logger.log('d', 'SHeights : ' + str(self._SHeights)) 
                if self._support_heights==0 :
                    self._support_heights=position_start.y

                self._top=self._top_added_height+(self._support_heights-position_start.y)
                
            else:
                self._top=self._top_added_height
                self._support_heights=0
            
            # 
            log('d', 'Abutment top : ' + str(self._top))
            # Logger.log('d', 'MaxSize : ' + str(self._MaxSize))
            
            mesh =  self._createAbutment(self._support_size,self._support_size_max,self._length,self._top,use_support_angle,self._support_y_direction)
        else:           
            # Custom creation Size , P1 as vector P2 as vector
            # Get support_interface_height as extra distance 
            extruder_stack = self._application.getExtruderManager().getActiveExtruderStacks()[0]
            if self._top_added_height == 0 :
                extra_top = 0
            else :
                extra_top=extruder_stack.getProperty("support_interface_height", "value")            
            mesh =  self._createLine(self._support_size,self._support_size_max,position_start,position_end,use_support_angle,extra_top)

        # Mesh Model are loaded via trimesh doesn't aheve the Build method
        if self._support_type != 'model':
            node.setMeshData(mesh.build())
        else:
            node.setMeshData(mesh)

        # test for init position
        node_transform = Matrix()
        node_transform.setToIdentity()
        node.setTransformation(node_transform)
        
        active_build_plate = CuraApplication.getInstance().getMultiBuildPlateModel().activeBuildPlate
        node.addDecorator(BuildPlateDecorator(active_build_plate))
        node.addDecorator(SliceableObjectDecorator())
              
        stack = node.callDecoration("getStack") # created by SettingOverrideDecorator that is automatically added to CuraSceneNode

        settings = stack.getTop()

        # Define the new mesh as "support_mesh" or "support_mesh_drop_down"
        # Must be set for this 2 types
        # for key in ["support_mesh", "support_mesh_drop_down"]:
        # Don't fix
        
        definition = stack.getSettingDefinition("support_mesh")
        new_instance = SettingInstance(definition, settings)
        new_instance.setProperty("value", True)
        new_instance.resetState()  # Ensure that the state is not seen as a user state.
        settings.addInstance(new_instance)

        definition = stack.getSettingDefinition("support_mesh_drop_down")
        new_instance = SettingInstance(definition, settings)
        new_instance.setProperty("value", False)
        new_instance.resetState()  # Ensure that the state is not seen as a user state.
        settings.addInstance(new_instance)

        global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()    
        
        support_placement = global_container_stack.getProperty("support_type", "value")
        support_placement_label = global_container_stack.getProperty("support_type", "label")
        if support_placement ==  'buildplate' :
            support_placement_options = global_container_stack.getProperty("support_type", "options")
            if support_placement_options is not None:
                try:
                    translated_support_placement = support_placement_options["everywhere"]
                except KeyError:
                    translated_support_placement = "Everywhere"
                    Logger.log("w", "Setting support_type does not have 'everywhere' as an option")
            else:
                translated_support_placement = "Everywhere"
                log("w", "Setting support_type does not have any options defined") # Log if no options are defined
            Message(text = f"{self._catalog.i18nc('support_placement_warning:dialog:start', 'Had to change setting')} {support_placement_label} {self._catalog.i18nc('support_placement_warning:middle', 'to')} {translated_support_placement} {self._catalog.i18nc('support_placement_warning:end', 'for support to work.')}", title = self._catalog.i18nc("support_placement_warning:title", "WARNING: Custom Supports Reborn")).show()
            log('d', 'Support_type different from everywhere : ' + str(support_placement))
            # Define support_type=everywhere
            global_container_stack.setProperty("support_type", "value", 'everywhere')
            
        op = GroupedOperation()
        # First add node to the scene at the correct position/scale, before parenting, so the support mesh does not get scaled with the parent
        op.addOperation(AddSceneNodeOperation(node, self._controller.getScene().getRoot()))
        op.addOperation(SetParentOperation(node, parent))
        op.push()
        node.setPosition(position_start, CuraSceneNode.TransformSpace.World)
        self._supports_created.append(node)
        self._panel_remove_all_text = self._catalog.i18nc("panel:remove_last", "Remove Last")
        self.propertyChanged.emit()
        
        CuraApplication.getInstance().getController().getScene().sceneChanged.emit(node)

    # Source code from MeshTools Plugin 
    # Copyright (c) 2020 Aldo Hoeben / fieldOfView
    def _getAllSelectedNodes(self) -> list[SceneNode]:
        selection = Selection.getAllSelectedObjects()[:]
        if selection:
            deep_selection = []  # type: list[SceneNode]
            for selected_node in selection:
                if selected_node.hasChildren():
                    deep_selection = deep_selection + selected_node.getAllChildren()
                if selected_node.getMeshData() != None:
                    deep_selection.append(selected_node)
            if deep_selection:
                return deep_selection

        # Message(catalog.i18nc("@info:status", "Please select one or more models first"))

        return []
 

    def mainAngle(self, radian : float) -> float:
        degree = math.degrees(radian)
        degree = round(degree / 90) * 90
        return math.radians(degree)   
    
    def defineAngle(self, mesh_name : str, act_position: Vector) -> float:
        angle = 0
        min_distance = float("inf")
        # Set on the build plate for distance
        projected_event_position = Vector(act_position.x, 0, act_position.z)
        # Logger.log('d', "Mesh : {}".format(Cname))
        # Logger.log('d', "Position : {}".format(calc_position))

        nodes_list = self._getAllSelectedNodes()
        if not nodes_list:
            nodes_list = DepthFirstIterator(self._application.getController().getScene().getRoot())
         
        for node in nodes_list:
            if node.callDecoration("isSliceable"):
                # Logger.log('d', "isSliceable : {}".format(node.getName()))
                node_stack=node.callDecoration("getStack")           
                if node_stack:                    
                    if node.getName()==mesh_name :
                        # Logger.log('d', "Mesh : {}".format(node.getName()))
                        
                        hull_polygon = node.callDecoration("getAdhesionArea")
                        # hull_polygon = node.callDecoration("getConvexHull")
                        # hull_polygon = node.callDecoration("getConvexHullBoundary")
                        # hull_polygon = node.callDecoration("_compute2DConvexHull")
                                   
                        if not hull_polygon or hull_polygon.getPoints is None:
                            Logger.log("w", "Object {} cannot be calculated because it has no convex hull.".format(node.getName()))
                            return 0
                            
                        points=hull_polygon.getPoints()
                        # nb_pt = point[0] / point[1] must be divided by 2
                        # Angle Ref for angle / Y Dir
                        reference_angle = Vector(0, 0, 1)
                        id=0
                        start_id=0
                        end_id=0
                        for point in points:                               
                            # Logger.log('d', "X : {}".format(point[0]))
                            # Logger.log('d', "Point : {}".format(point))
                            new_position = Vector(point[0], 0, point[1])
                            distance_vector = projected_event_position - new_position
                            # Logger.log('d', "Lg : {}".format(lg))
                            # lght = lg.length()
                            distance = round(distance_vector.length(),0)

                            if distance < min_distance and distance > 0:
                                min_distance=distance
                                start_id=id
                                normalized_distance = distance_vector.normalized()
                                # Logger.log('d', "unit_vector2 : {}".format(unit_vector2))
                                angle_sin = math.asin(reference_angle.dot(normalized_distance))
                                # LeCos = math.acos(ref.dot(unit_vector2))
                                
                                if normalized_distance.x>=0 :
                                    # Logger.log('d', "Angle Pos 1a")
                                    angle = math.pi-angle_sin  #angle in radian
                                else :
                                    # Logger.log('d', "Angle Pos 2a")
                                    angle = angle_sin                                    
                                    
                            if distance==min_distance and distance>0 :
                                if id > end_id+1 :
                                    start_id=id
                                    end_id=id
                                else :
                                    end_id=id
                                    
                            id+=1
                        
                        # Could be the case with automatic .. rarely in pickpoint   
                        if start_id != end_id :
                            # Logger.log('d', "Possibility   : {} / {}".format(Start_Id,End_Id))
                            id=int(start_id+0.5*(end_id-start_id))
                            # Logger.log('d', "Id   : {}".format(Id))
                            new_position = Vector(points[id][0], 0, points[id][1])
                            distance_vector=projected_event_position-new_position                            
                            normalized_distance = distance_vector.normalized()
                            # Logger.log('d', "unit_vector2 : {}".format(unit_vector2))
                            angle_sin = math.asin(reference_angle.dot(normalized_distance))
                            # LeCos = math.acos(ref.dot(unit_vector2))
                            
                            if normalized_distance.x >=0 :
                                # Logger.log('d', "Angle Pos 1b")
                                angle = math.pi-angle_sin  #angle in radian
                                
                            else :
                                # Logger.log('d', "Angle Pos 2b")
                                angle = angle_sin
                                
                            
                            # Modification / Spoon not ne same start orientation
                            
                        # Logger.log('d', "Pick_position   : {}".format(calc_position))
                        # Logger.log('d', "Close_position  : {}".format(Select_position))
                        # Logger.log('d', "Unit_vector2    : {}".format(unit_vector2))
                        # Logger.log('d', "Angle Sinus     : {}".format(math.degrees(LeSin)))
                        # Logger.log('d', "Angle Cosinus   : {}".format(math.degrees(LeCos)))
                        # Logger.log('d', "Chose Angle     : {}".format(math.degrees(Angle)))
        return angle
    
    def _removeSupportMesh(self, node: CuraSceneNode):
        parent = node.getParent()
        if parent == self._controller.getScene().getRoot():
            parent = None

        op = RemoveSceneNodeOperation(node)
        op.push()

        if parent and not Selection.isSelected(parent):
            Selection.add(parent)

        CuraApplication.getInstance().getController().getScene().sceneChanged.emit(node)

    def _updateEnabled(self):
        plugin_enabled = False

        global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()
        if global_container_stack:
            plugin_enabled = global_container_stack.getProperty("support_mesh", "enabled")

        CuraApplication.getInstance().getController().toolEnabledChanged.emit(self._plugin_id, plugin_enabled)
    
    def _onSelectionChanged(self):
        # When selection is passed from one object to another object, first the selection is cleared
        # and then it is set to the new object. We are only interested in the change from no selection
        # to a selection or vice-versa, not in a change from one object to another. A timer is used to
        # "merge" a possible clear/select action in a single frame
        if Selection.hasSelection() != self._had_selection:
            self._had_selection_timer.start()

    def _selectionChangeDelay(self):
        has_selection = Selection.hasSelection()
        if not has_selection and self._had_selection:
            self._skip_press = True
        else:
            self._skip_press = False

        self._had_selection = has_selection
 
    # Initial Source code from fieldOfView
    def _toMeshData(self, tri_node: trimesh.base.Trimesh) -> MeshData:
        # Rotate the part to laydown on the build plate
        # Modification from 5@xes
        tri_node.apply_transform(trimesh.transformations.rotation_matrix(math.radians(90), [-1, 0, 0]))
        tri_faces = tri_node.faces
        tri_vertices = tri_node.vertices
        # Following code from fieldOfView
        # https://github.com/fieldOfView/Cura-SimpleShapes/blob/bac9133a2ddfbf1ca6a3c27aca1cfdd26e847221/SimpleShapes.py#L45

        indices = []
        vertices = []

        index_count = 0
        face_count = 0
        for tri_face in tri_faces:
            face = []
            for tri_index in tri_face:
                vertices.append(tri_vertices[tri_index])
                face.append(index_count)
                index_count += 1
            indices.append(face)
            face_count += 1

        vertices = numpy.asarray(vertices, dtype=numpy.float32)
        indices = numpy.asarray(indices, dtype=numpy.int32)
        normals = calculateNormalsFromIndexedVertices(vertices, indices, face_count)

        mesh_data = MeshData(vertices=vertices, indices=indices, normals=normals)

        return mesh_data
        
    # Cube Creation
    def _createCube(self, base_side, minmax_side, length, top_additional_height, taper_angle, taper_direction):
        mesh = MeshBuilder()

        half_base_side = base_side / 2
        half_minmax_side = minmax_side / 2
        total_height = length # Renamed total_height to length for consistency
        top_offset = top_additional_height # Renamed top_offset to top_additional_height for consistency

        if taper_angle > 0 or taper_direction == "outward": # Outward taper (positive angle OR explicit "outward")
            bottom_width_tapered = half_base_side + math.tan(math.radians(taper_angle)) * (total_height + top_offset)
            bottom_width_tapered = min(bottom_width_tapered, half_minmax_side) # Limit by minmax_side if outward taper

        elif taper_angle < 0 or taper_direction == "inward": # Inward taper (negative angle OR explicit "inward")
            bottom_width_tapered = half_base_side - math.tan(math.radians(abs(taper_angle))) * (total_height + top_offset) # Subtract for inward taper
            bottom_width_tapered = max(bottom_width_tapered, half_minmax_side) # Limit by minmax_side if inward taper - MINIMUM size

        else: # No taper (taper_angle == 0 or taper_direction == "none" or default)
            bottom_width_tapered = half_base_side # Straight cube

        if half_minmax_side > half_base_side and taper_angle!=0: # Taper length calculation - outward taper
            taper_length_val = (half_minmax_side - half_base_side) / math.tan(math.radians(taper_angle))
            taper_length = min(taper_length_val, total_height)
        elif half_minmax_side < half_base_side and taper_angle!=0: # Taper length calculation - inward taper
             taper_length_val = (half_base_side - half_minmax_side) / math.tan(math.radians(abs(taper_angle))) # Use abs for angle
             taper_length = min(taper_length_val, total_height)
        else:
            taper_length = total_height


        negative_length = -total_height
        taper_negative_length = -taper_length

        top_face_vertices = []
        bottom_face_vertices_taper = []
        bottom_face_vertices_straight = [] # Might be used later

        if taper_length <= total_height and taper_length > 0: # Tapered case
            # 1. Generate vertices for top face (square, side base_side) - SAME AS BEFORE
            y_top = top_additional_height
            half_side_top = half_base_side
            top_face_vertices.extend([
                [-half_side_top, y_top, half_side_top],
                [half_side_top, y_top, half_side_top],
                [half_side_top, y_top, -half_side_top],
                [-half_side_top, y_top, -half_side_top]
            ])

            # 2. Generate vertices for bottom face of tapered section (square, side bottom_width_tapered) - SAME AS BEFORE
            y_bottom_taper = taper_negative_length
            half_side_bottom_taper = bottom_width_tapered
            bottom_face_vertices_taper.extend([
                [-half_side_bottom_taper, y_bottom_taper, half_side_bottom_taper],
                [half_side_bottom_taper, y_bottom_taper, half_side_bottom_taper],
                [half_side_bottom_taper, y_bottom_taper, -half_side_bottom_taper],
                [-half_side_bottom_taper, y_bottom_taper, -half_side_bottom_taper]
            ])

            # 3. Generate vertices for bottom face of STRAIGHT section (square, side bottom_width_tapered) - NEW for straight section below taper
            y_bottom_straight = negative_length # Bottom of straight section is at negative_length
            half_side_bottom_straight = bottom_width_tapered # Straight section has same width as bottom of taper
            bottom_face_vertices_straight.extend([
                [-half_side_bottom_straight, y_bottom_straight, half_side_bottom_straight],
                [half_side_bottom_straight, y_bottom_straight, half_side_bottom_straight],
                [half_side_bottom_straight, y_bottom_straight, -half_side_bottom_straight],
                [-half_side_bottom_straight, y_bottom_straight, -half_side_bottom_straight]
            ])


            vertices = [] # Will store vertices for faces
            indices = [] # Will store indices

            # Face Construction for Tapered Sides - SAME AS BEFORE
            for i in range(4): # 4 sides of the square
                v_index_current = i
                v_index_next = (i + 1) % 4

                # Side Face 'i' of Tapered Section
                # Triangle 1
                vertices.append(top_face_vertices[v_index_current])
                vertices.append(top_face_vertices[v_index_next])
                vertices.append(bottom_face_vertices_taper[v_index_next])
                # Triangle 2
                vertices.append(bottom_face_vertices_taper[v_index_next])
                vertices.append(bottom_face_vertices_taper[v_index_current])
                vertices.append(top_face_vertices[v_index_current])

            # Top Face - using top_face_vertices - SAME AS BEFORE
            # Triangle 1 (Top Face)
            vertices.append(top_face_vertices[0])
            vertices.append(top_face_vertices[2])
            vertices.append(top_face_vertices[1])
            # Triangle 2 (Top Face)
            vertices.append(top_face_vertices[0])
            vertices.append(top_face_vertices[3])
            vertices.append(top_face_vertices[2])

            # Face Construction for STRAIGHT Section Sides - NEW for straight section below taper
            for i in range(4):
                v_index_current = i
                v_index_next = (i + 1) % 4

                # Side Face 'i' of STRAIGHT Section - Connect bottom of tapered section to bottom of straight section
                # Triangle 1
                vertices.append(bottom_face_vertices_taper[v_index_current]) # Top of straight side (bottom of tapered)
                vertices.append(bottom_face_vertices_taper[v_index_next])   # Top of straight side (bottom of tapered)
                vertices.append(bottom_face_vertices_straight[v_index_next])# Bottom of straight side
                # Triangle 2
                vertices.append(bottom_face_vertices_straight[v_index_next])# Bottom of straight side
                vertices.append(bottom_face_vertices_straight[v_index_current])# Bottom of straight side
                vertices.append(bottom_face_vertices_taper[v_index_current]) # Top of straight side (bottom of tapered)


            # Conditional Bottom Face - INSIDE IF BLOCK NOW, with condition for full vs partial taper
            if taper_length == total_height: # Full Taper - Bottom face is at bottom of TAPERED section
                # Bottom Face - using bottom_face_vertices_taper (reversed vertex order for bottom face)
                # Triangle 1 (Bottom Face - Full Taper)
                vertices.append(bottom_face_vertices_taper[0])
                vertices.append(bottom_face_vertices_taper[1])
                vertices.append(bottom_face_vertices_taper[2])
                # Triangle 2 (Bottom Face - Full Taper)
                vertices.append(bottom_face_vertices_taper[2])
                vertices.append(bottom_face_vertices_taper[3])
                vertices.append(bottom_face_vertices_taper[0])
            else: # Partial Taper - Bottom face is at bottom of STRAIGHT section
                # Bottom Face of STRAIGHT Section
                # Triangle 1 (Bottom Face - Partial Taper)
                vertices.append(bottom_face_vertices_straight[0])
                vertices.append(bottom_face_vertices_straight[1])
                vertices.append(bottom_face_vertices_straight[2])
                # Triangle 2 (Bottom Face - Partial Taper)
                vertices.append(bottom_face_vertices_straight[2])
                vertices.append(bottom_face_vertices_straight[3])
                vertices.append(bottom_face_vertices_straight[0])


        else: # Straight cube case (or rectangular prism)
            half_side_straight = bottom_width_tapered # Use bottom_width_tapered as side for straight cube (it will be equal to half_base_side in straight case)
            top_face_vertices_straight = []
            bottom_face_vertices_straight = [] # Reusing this list name, but now for straight cube bottom face

            # 1. Generate vertices for top face (square, side half_side_straight)
            y_top = top_additional_height
            half_side_top = half_side_straight # Side of top face is same as bottom for straight cube
            top_face_vertices_straight.extend([
                [-half_side_top, y_top, half_side_top],  # TLF - 0
                [half_side_top, y_top, half_side_top],   # TRF - 1
                [half_side_top, y_top, -half_side_top],  # TRB - 2
                [-half_side_top, y_top, -half_side_top]   # TLB - 3
            ])

            # 2. Generate vertices for bottom face (square, side half_side_straight)
            y_bottom_straight = negative_length # Bottom at negative_length
            half_side_bottom_straight = half_side_straight # Side of bottom face is same as top for straight cube
            bottom_face_vertices_straight.extend([
                [-half_side_bottom_straight, y_bottom_straight, half_side_bottom_straight],  # BLF - 0
                [half_side_bottom_straight, y_bottom_straight, half_side_bottom_straight],   # BRF - 1
                [half_side_bottom_straight, y_bottom_straight, -half_side_bottom_straight],  # BRB - 2
                [-half_side_bottom_straight, y_bottom_straight, -half_side_bottom_straight]   # BLB - 3
            ])

            vertices = [] # Will store vertices for faces

            # Face Construction for Straight Cube - 6 faces
            for i in range(4): # 4 sides
                v_index_current = i
                v_index_next = (i + 1) % 4

                # Side Face 'i' - Triangles to form a quad - connecting top and bottom straight faces
                # Triangle 1
                vertices.append(top_face_vertices_straight[v_index_current])
                vertices.append(top_face_vertices_straight[v_index_next])
                vertices.append(bottom_face_vertices_straight[v_index_next])
                # Triangle 2
                vertices.append(bottom_face_vertices_straight[v_index_next])
                vertices.append(bottom_face_vertices_straight[v_index_current])
                vertices.append(top_face_vertices_straight[v_index_current])

            # Top Face - using top_face_vertices_straight
            # Triangle 1 (Top Face)
            vertices.append(top_face_vertices_straight[0]) # TLF
            vertices.append(top_face_vertices_straight[2]) # TRB
            vertices.append(top_face_vertices_straight[1]) # TRF
            # Triangle 2 (Top Face)
            vertices.append(top_face_vertices_straight[0]) # TLF
            vertices.append(top_face_vertices_straight[3]) # TLB
            vertices.append(top_face_vertices_straight[2]) # TRB

            # Bottom Face - using bottom_face_vertices_straight (reversed vertex order for bottom face)
            # Triangle 1 (Bottom Face)
            vertices.append(bottom_face_vertices_straight[0]) # BLF
            vertices.append(bottom_face_vertices_straight[1]) # BRF
            vertices.append(bottom_face_vertices_straight[2]) # BRB
            # Triangle 2 (Bottom Face)
            vertices.append(bottom_face_vertices_straight[2]) # BRB
            vertices.append(bottom_face_vertices_straight[3]) # BLB
            vertices.append(bottom_face_vertices_straight[0]) # BLF

        mesh.setVertices(numpy.asarray(vertices, dtype=numpy.float32)) # Vertices will be added in face construction
        indices = [] # Generate indices
        for i in range(0, len(vertices), 3):
            indices.append([i, i+1, i+2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))
        mesh.calculateNormals()
        return mesh
        
    # Abutment Creation
    def _createAbutment(self, top_width, minmax_width, total_height, top_offset, taper_angle, rotate_90_degrees):
        """Creates an abutment mesh.

        Args:
        top_width: The width of the top rectangular face.
        bottom_width: The maximum diameter of the base (for tapered abutments). (Original name 'max_diameter' meaning clarified)
        total_height: The height of the main body of the abutment.
        top_offset: The additional height added to the top of the abutment.
        taper_angle: The angle of the taper.
        rotate_90_degrees: Whether to rotate the abutment by 90 degrees in the XY plane ("Horizontal Orientation" in UI). (Renamed from y_mirrored, UI label to be updated)
        """
        # Logger.log('d', 'Ydir : ' + str(ydir))
        mesh = MeshBuilder()

        radius = top_width / 2 # Using 'top_width' for 'diameter' parameter name meaning
        max_radius = minmax_width / 2 # Using 'bottom_width' for 'max_diameter' parameter name meaning
        bottom_diameter = math.tan(math.radians(taper_angle)) * (total_height + top_offset) + (2 * radius) # Original formula for bottom_diameter

        if max_radius > radius and taper_angle != 0:
            taper_length = (max_radius - radius) / math.tan(math.radians(taper_angle))
        else:
            taper_length = total_height
        
        
        # Debug Log Lines
        # Logger.log('d', 's_inf : ' + str(s_inf))
        # Logger.log('d', 'l_max : ' + str(l_max)) 
        # Logger.log('d', 'l : ' + str(l))
        
        # Difference between Standart Abutment and Abutment + max base size

        # Debug Log Lines
        # Logger.log('d', 's_inf : ' + str(s_inf))
        # Logger.log('d', 'l_max : ' + str(l_max)) 
        # Logger.log('d', 'l : ' + str(l))
        
        # Difference between Standart Abutment and Abutment + max base size
        if taper_length < total_height and taper_length > 0:
            vertices_per_segment = 40
            if not rotate_90_degrees: # "Vertical" Orientation (rotate_90_degrees == False)
                vertices = [  # 10 faces with 4 corners each - ORIGINAL VERTEX LIST RESTORED
                    [-radius, -taper_length, max_radius], [-radius, top_offset, 2 * radius], [radius, top_offset, 2 * radius], [radius, -taper_length, max_radius],
                    [-radius, top_offset, -2 * radius], [-radius, -taper_length, -max_radius], [radius, -taper_length, -max_radius], [radius, top_offset, -2 * radius],
                    [-radius, -total_height, max_radius], [-radius, -taper_length, max_radius], [radius, -taper_length, max_radius], [radius, -total_height, max_radius],
                    [-radius, -taper_length, -max_radius], [-radius, -total_height, -max_radius], [radius, -total_height, -max_radius], [radius, -taper_length, -max_radius],
                    [radius, -total_height, -max_radius], [-radius, -total_height, -max_radius], [-radius, -total_height, max_radius], [radius, -total_height, max_radius],
                    [-radius, top_offset, -2 * radius], [radius, top_offset, -2 * radius], [radius, top_offset, 2 * radius], [-radius, top_offset, 2 * radius],
                    [-radius, -taper_length, max_radius], [-radius, -taper_length, -max_radius], [-radius, top_offset, -2 * radius], [-radius, top_offset, 2 * radius],
                    [radius, -taper_length, -max_radius], [radius, -taper_length, max_radius], [radius, top_offset, 2 * radius], [radius, top_offset, -2 * radius],
                    [-radius, -total_height, max_radius], [-radius, -total_height, -max_radius], [-radius, -taper_length, -max_radius], [-radius, -taper_length, max_radius],
                    [radius, -total_height, -max_radius], [radius, -total_height, max_radius], [radius, -taper_length, max_radius], [radius, -taper_length, -max_radius]
                ]
            else:  # "Horizontal" Orientation (rotate_90_degrees == True)
                vertices = [  # 10 faces with 4 corners each - ORIGINAL VERTEX LIST RESTORED
                    [-max_radius, -taper_length, radius], [-2 * radius, top_offset, radius], [2 * radius, top_offset, radius], [max_radius, -taper_length, radius],
                    [-2 * radius, top_offset, -radius], [-max_radius, -taper_length, -radius], [max_radius, -taper_length, -radius], [2 * radius, top_offset, -radius],
                    [-max_radius, -total_height, radius], [-max_radius, -taper_length, radius], [max_radius, -taper_length, radius], [max_radius, -total_height, radius],
                    [-max_radius, -taper_length, -radius], [-max_radius, -total_height, -radius], [max_radius, -total_height, -radius], [max_radius, -taper_length, -radius],
                    [max_radius, -total_height, -radius], [-max_radius, -total_height, -radius], [-max_radius, -total_height, radius], [max_radius, -total_height, radius],
                    [-2 * radius, top_offset, -radius], [2 * radius, top_offset, -radius], [2 * radius, top_offset, radius], [-2 * radius, top_offset, radius],
                    [-max_radius, -taper_length, radius], [-max_radius, -taper_length, -radius], [-2 * radius, top_offset, -radius], [-2 * radius, top_offset, radius],
                    [max_radius, -taper_length, -radius], [max_radius, -taper_length, radius], [2 * radius, top_offset, radius], [2 * radius, top_offset, -radius],
                    [-max_radius, -total_height, radius], [-max_radius, -total_height, -radius], [-max_radius, -taper_length, -radius], [-max_radius, -taper_length, radius],
                    [max_radius, -total_height, -radius], [max_radius, -total_height, radius], [max_radius, -taper_length, radius], [max_radius, -taper_length, -radius]
                ]

        else:  # Straight abutment (no taper)
            vertices_per_segment = 24
            if not rotate_90_degrees: # "Vertical" Orientation (rotate_90_degrees == False)
                vertices = [  # 6 faces with 4 corners each - ORIGINAL VERTEX LIST RESTORED
                    [-radius, -total_height, bottom_diameter], [-radius, top_offset, 2 * radius], [radius, top_offset, 2 * radius], [radius, -total_height, bottom_diameter],
                    [-radius, top_offset, -2 * radius], [-radius, -total_height, -bottom_diameter], [radius, -total_height, -bottom_diameter], [radius, top_offset, -2 * radius],
                    [radius, -total_height, -bottom_diameter], [-radius, -total_height, -bottom_diameter], [-radius, -total_height, bottom_diameter], [radius, -total_height, bottom_diameter],
                    [-radius, top_offset, -2 * radius], [radius, top_offset, -2 * radius], [radius, top_offset, 2 * radius], [-radius, top_offset, 2 * radius],
                    [-radius, -total_height, bottom_diameter], [-radius, -total_height, -bottom_diameter], [-radius, top_offset, -2 * radius], [-radius, top_offset, 2 * radius],
                    [radius, -total_height, -bottom_diameter], [radius, -total_height, bottom_diameter], [radius, top_offset, 2 * radius], [radius, top_offset, -2 * radius]
                ]
            else:  # "Horizontal" Orientation (rotate_90_degrees == True)
                vertices = [  # 6 faces with 4 corners each - ORIGINAL VERTEX LIST RESTORED
                    [-bottom_diameter, -total_height, radius], [-2 * radius, top_offset, radius], [2 * radius, top_offset, radius], [bottom_diameter, -total_height, radius],
                    [-2 * radius, top_offset, -radius], [-bottom_diameter, -total_height, -radius], [bottom_diameter, -total_height, -radius], [2 * radius, top_offset, -radius],
                    [bottom_diameter, -total_height, -radius], [-bottom_diameter, -total_height, -radius], [-bottom_diameter, -total_height, radius], [bottom_diameter, -total_height, radius],
                    [-2 * radius, top_offset, -radius], [2 * radius, top_offset, -radius], [2 * radius, top_offset, radius], [-2 * radius, top_offset, radius],
                    [-bottom_diameter, -total_height, radius], [-bottom_diameter, -total_height, -radius], [-2 * radius, top_offset, -radius], [-2 * radius, top_offset, radius],
                    [bottom_diameter, -total_height, -radius], [bottom_diameter, -total_height, radius], [2 * radius, top_offset, radius], [2 * radius, top_offset, -radius]
                ]

        mesh.setVertices(numpy.asarray(vertices, dtype=numpy.float32))

        indices = []
        for i in range(0, vertices_per_segment, 4):  # All quads (12 triangles - or 6 for straight)
            indices.append([i, i + 2, i + 1])
            indices.append([i, i + 3, i + 2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))

        mesh.calculateNormals()
        return mesh
        
    # Cylinder creation
    def _createCylinder(self, diameter, minmax_diameter, circle_segments, length, top_additional_height, taper_angle, taper_direction):
        mesh = MeshBuilder()
        # Per-vertex normals require duplication of vertices
        radius = diameter / 2
        minmax_radius = minmax_diameter / 2

        negative_length = -length
        num_segments = int(360 / circle_segments)
        angle_increment_radians = math.radians(circle_segments)
        
        if taper_angle > 0 or taper_direction == "outward":
            bottom_radius = math.tan(math.radians(taper_angle)) * length + radius
            bottom_radius = min(bottom_radius, minmax_radius)
            if minmax_radius > radius and taper_angle != 0: # minmax_radius is max_radius in this case
                taper_length_calculated = (minmax_radius-radius) / math.tan(math.radians(taper_angle))
                taper_length = min(taper_length_calculated, length) # **MODIFIED: Cap taper_length at 'length'**
            else :
                taper_length = negative_length

        elif taper_angle < 0 or taper_direction == "inward":
            taper_angle = abs(taper_angle)
            bottom_radius = radius - math.tan(math.radians(taper_angle)) * length
            bottom_radius = max(bottom_radius, minmax_radius) # minmax_radius is min_radius in this case, ensure bottom_radius doesn't go below min_radius
            if radius > minmax_radius and taper_angle != 0: # Check if inward taper is actually possible/needed
                 taper_length_calculated = (radius - minmax_radius) / math.tan(math.radians(taper_angle))
                 taper_length = min(taper_length_calculated, length) # **MODIFIED: Cap taper_length at 'length'**
            else:
                taper_length = negative_length
        else:  # If tapering is no longer cool
            bottom_radius = radius
            taper_length = negative_length
            
        #Logger.log('d', 'lg : ' + str(lg))
        #Logger.log('d', 'l_max : ' + str(l_max)) 

        log('d', f'taper_length: {taper_length}')
        log('d', f'length: {length}') # ADDED: Log length value
        log('d', f'Condition (taper_length < length and taper_length > 0): {taper_length < length and taper_length > 0}')

        
        vertices = []
        if taper_length <= length and taper_length > 0:
            num_segments = int(360 / circle_segments)
            angle_increment_radians = math.radians(circle_segments)

            top_circle_vertices_taper = [] # Top circle vertices for TAPERED section
            bottom_circle_vertices_taper = [] # Bottom circle vertices for TAPERED section
            bottom_circle_vertices_straight = [] # Bottom circle vertices for STRAIGHT section (below taper)


            # 1. Generate vertices for the top and bottom circles of the TAPERED SECTION (SHARED vertices)
            for i in range(num_segments):
                angle = i * angle_increment_radians
                x_top = radius * math.cos(angle)
                z_top = radius * math.sin(angle)
                top_circle_vertices_taper.append([x_top, top_additional_height, z_top])

                x_bottom_taper = minmax_radius * math.cos(angle) # Using minmax_radius (max_radius for outward, min_radius for inward)
                z_bottom_taper = minmax_radius * math.sin(angle) # Using minmax_radius
                bottom_circle_vertices_taper.append([x_bottom_taper, -taper_length, z_bottom_taper])


            # 2. Generate vertices for the bottom circle of the STRAIGHT SECTION (SHARED vertices)
            for i in range(num_segments):
                angle = i * angle_increment_radians
                x_bottom_straight = minmax_radius * math.cos(angle) # Radius is now minmax_radius for straight section
                z_bottom_straight = minmax_radius * math.sin(angle) # Radius is minmax_radius
                bottom_circle_vertices_straight.append([x_bottom_straight, negative_length, z_bottom_straight])


            vertices = [] # Clear vertices list

            for i in range(num_segments):
                v_index_current = i
                v_index_next = (i + 1) % num_segments

                # Top Cap (same as before, using vertices of top circle of tapered section)
                vertices.append([0, top_additional_height, 0])
                vertices.append(top_circle_vertices_taper[v_index_next])
                vertices.append(top_circle_vertices_taper[v_index_current])

                # Side 1a (TAPERED SECTION - using SHARED vertices for tapered part)
                vertices.append(top_circle_vertices_taper[v_index_current])      # Top-Left
                vertices.append(top_circle_vertices_taper[v_index_next])      # Top-Right
                vertices.append(bottom_circle_vertices_taper[v_index_next])   # Bottom-Right (of TAPERED section)

                # Side 1b (TAPERED SECTION - using SHARED vertices for tapered part)
                vertices.append(bottom_circle_vertices_taper[v_index_next])   # Bottom-Right (of TAPERED section)
                vertices.append(bottom_circle_vertices_taper[v_index_current])  # Bottom-Left (of TAPERED section)
                vertices.append(top_circle_vertices_taper[v_index_current])      # Top-Left

                # Side 2a (STRAIGHT SECTION - using SHARED vertices for straight part)
                vertices.append(bottom_circle_vertices_taper[v_index_current])   # Top-Left  (which is BOTTOM of tapered section)
                vertices.append(bottom_circle_vertices_taper[v_index_next])   # Top-Right  (which is BOTTOM of tapered section)
                vertices.append(bottom_circle_vertices_straight[v_index_next]) # Bottom-Right (of STRAIGHT section)

                # Side 2b (STRAIGHT SECTION - using SHARED vertices for straight part)
                vertices.append(bottom_circle_vertices_straight[v_index_next]) # Bottom-Right (of STRAIGHT section)
                vertices.append(bottom_circle_vertices_straight[v_index_current])# Bottom-Left  (of STRAIGHT section)
                vertices.append(bottom_circle_vertices_taper[v_index_current])   # Top-Left  (which is BOTTOM of tapered section)


                # Bottom Cap (using vertices of bottom circle of straight section)
                vertices.append([0, negative_length, 0])
                vertices.append(bottom_circle_vertices_straight[v_index_current])
                vertices.append(bottom_circle_vertices_straight[v_index_next])

        else: # STRAIGHT CYLINDER CASE - Using Shared Vertices
            num_segments = int(360 / circle_segments)
            angle_increment_radians = math.radians(circle_segments)

            bottom_radius = radius
            
            top_circle_vertices = [] # List to store vertices of the top circle
            bottom_circle_vertices = [] # List to store vertices of the bottom circle

            # 1. Generate vertices for the top and bottom circles (SHARED vertices)
            for i in range(num_segments):
                angle = i * angle_increment_radians
                x = radius * math.cos(angle)
                z = radius * math.sin(angle)
                top_circle_vertices.append([x, top_additional_height, z])
                bottom_circle_vertices.append([x, negative_length, z])

            vertices = [] # Clear the vertices list

            for i in range(num_segments):
                # Get vertex indices for this segment, wrapping around for the last segment
                v_index_current = i
                v_index_next = (i + 1) % num_segments # Wrap around to 0 for the last segment

                # Top Triangle
                vertices.append([0, top_additional_height, 0]) # Center of top
                vertices.append(top_circle_vertices[v_index_next]) # Vertex on top circle (next)
                vertices.append(top_circle_vertices[v_index_current]) # Vertex on top circle (current)

                # Side 1a (using SHARED vertices from top and bottom circles)
                vertices.append(top_circle_vertices[v_index_current])     # Top-Left  (vertex i on top circle)
                vertices.append(top_circle_vertices[v_index_next])     # Top-Right (vertex i+1 on top circle)
                vertices.append(bottom_circle_vertices[v_index_next])  # Bottom-Right (vertex i+1 on bottom circle)

                # Side 1b (using SHARED vertices from top and bottom circles)
                vertices.append(bottom_circle_vertices[v_index_next])  # Bottom-Right (vertex i+1 on bottom circle)
                vertices.append(bottom_circle_vertices[v_index_current]) # Bottom-Left  (vertex i on bottom circle)
                vertices.append(top_circle_vertices[v_index_current])     # Top-Left  (vertex i on top circle)

                # Bottom Triangle
                vertices.append([0, negative_length, 0]) # Center of bottom
                vertices.append(bottom_circle_vertices[v_index_current]) # Vertex on bottom circle (current)
                vertices.append(bottom_circle_vertices[v_index_next]) # Vertex on bottom circle (next)
        
        mesh.setVertices(numpy.asarray(vertices, dtype=numpy.float32))

        indices = []
        for i in range(0, len(vertices), 3):
            indices.append([i, i+1, i+2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))

        mesh.calculateNormals()
        return mesh
 
   # Tube creation
    def _createTube(self, outer_diameter, minmax_diameter, wall_width, circle_segments, length, top_additional_height, taper_angle, taper_direction):
        # Logger.log('d', 'isize : ' + str(isize)) 
        mesh = MeshBuilder()
        outer_radius = outer_diameter / 2
        minmax_outer_radius = minmax_diameter / 2
        inner_radius = outer_radius - wall_width  # Calculate inner radius based on wall_width
        inner_radius = max(0, inner_radius) # Clamp inner_radius to be at least 0 - PREVENT HOURGLASS

        negative_length = -length
        num_segments = int(360 / circle_segments)
        angle_increment_radians = math.radians(circle_segments)

        if taper_angle > 0 or taper_direction == "outward":
            bottom_outer_radius = math.tan(math.radians(taper_angle)) * length + outer_radius
            bottom_outer_radius = min(bottom_outer_radius, minmax_outer_radius)
            bottom_inner_radius = bottom_outer_radius - wall_width # Inner radius also tapers outwards, maintaining wall_width
            if minmax_outer_radius > outer_radius and taper_angle != 0:
                taper_length = (minmax_outer_radius - outer_radius) / math.tan(math.radians(taper_angle))
                taper_length = min(taper_length, length)
            else:
                taper_length = negative_length

        elif taper_angle < 0 or taper_direction == "inward":
            bottom_outer_radius = outer_radius - math.tan(math.radians(taper_angle)) * length
            bottom_outer_radius = max(bottom_outer_radius, minmax_outer_radius)
            bottom_inner_radius = bottom_outer_radius - wall_width # Inner radius also tapers inwards, maintaining wall_width
            if outer_radius > minmax_outer_radius and taper_angle != 0:
                taper_length = (outer_radius - minmax_outer_radius) / math.tan(math.radians(taper_angle))
                taper_length = min(taper_length, length)
            else:
                taper_length = negative_length
        else: # No taper
            bottom_outer_radius = outer_radius
            bottom_inner_radius = inner_radius # No taper for inner cylinder either
            taper_length = negative_length
            
        vertices = []
        if taper_length <= length and taper_length > 0:
            outer_top_vertices_taper = [] # Top circle vertices for TAPERED section
            outer_bottom_vertices_taper = [] # Bottom circle vertices for TAPERED section
            inner_top_vertices_taper = [] # Top inner circle vertices for TAPERED section
            inner_bottom_vertices_taper = [] # Bottom inner circle vertices for TAPERED section
            outer_bottom_vertices_straight = [] # Bottom circle vertices for STRAIGHT section (below taper)
            inner_bottom_vertices_straight = [] # Bottom inner circle vertices for STRAIGHT section (below taper)ottom inner circle vertices for STRAIGHT section (below taper)

            taper_negative_length = -taper_length # Define negative taper length

            for i in range(num_segments):
                angle = i * angle_increment_radians
                x_top = outer_radius * math.cos(angle)
                z_top = outer_radius * math.sin(angle)
                outer_top_vertices_taper.append([x_top, top_additional_height, z_top]) # Top outer vertices of TAPERED section
                inner_top_vertices_taper.append([x_top * (inner_radius / outer_radius), top_additional_height, z_top * (inner_radius / outer_radius)]) # Top inner vertices of TAPERED section

                x_bottom_taper = bottom_outer_radius * math.cos(angle) # X,Z for bottom of tapered section
                z_bottom_taper = bottom_outer_radius * math.sin(angle) # X,Z for bottom of tapered section
                outer_bottom_vertices_taper.append([x_bottom_taper, taper_negative_length, z_bottom_taper]) # Bottom outer vertices of TAPERED section
                inner_bottom_vertices_taper.append([x_bottom_taper * (bottom_inner_radius / bottom_outer_radius), taper_negative_length, z_bottom_taper * (bottom_inner_radius / bottom_outer_radius)]) # Bottom inner vertices of TAPERED section


                x_bottom_straight = bottom_outer_radius * math.cos(angle) # Radius is constant for straight section
                z_bottom_straight = bottom_outer_radius * math.sin(angle) # Radius is constant for straight section
                outer_bottom_vertices_straight.append([x_bottom_straight, negative_length, z_bottom_straight]) # Bottom outer vertices of STRAIGHT section
                inner_bottom_vertices_straight.append([x_bottom_straight * (bottom_inner_radius / bottom_outer_radius), negative_length, z_bottom_straight * (bottom_inner_radius / bottom_outer_radius)]) # Bottom inner vertices of STRAIGHT section


            vertices = [] # Clear vertices list
            indices = []

            for i in range(num_segments):
                v_index_current = i
                v_index_next = (i + 1) % num_segments

                # --- Top Cap Ring (Tapered Section Top) ---
                # Triangle 1 (Top Cap Ring)
                vertices.append(inner_top_vertices_taper[v_index_current])
                vertices.append(outer_top_vertices_taper[v_index_next])
                vertices.append(outer_top_vertices_taper[v_index_current])
                # Triangle 2 (Top Cap Ring)
                vertices.append(inner_top_vertices_taper[v_index_next])
                vertices.append(outer_top_vertices_taper[v_index_next])
                vertices.append(inner_top_vertices_taper[v_index_current])


                # --- Outer Side Faces (TAPERED SECTION) ---
                # Side 1a (Outer Tapered)
                vertices.append(outer_top_vertices_taper[v_index_current])
                vertices.append(outer_top_vertices_taper[v_index_next])
                vertices.append(outer_bottom_vertices_taper[v_index_next])
                # Side 1b (Outer Tapered)
                vertices.append(outer_bottom_vertices_taper[v_index_next])
                vertices.append(outer_bottom_vertices_taper[v_index_current])
                vertices.append(outer_top_vertices_taper[v_index_current])


                # --- Inner Side Faces (TAPERED SECTION) ---
                # Side 2a (Inner Tapered)
                vertices.append(inner_top_vertices_taper[v_index_current])
                vertices.append(inner_bottom_vertices_taper[v_index_next])
                vertices.append(inner_top_vertices_taper[v_index_next])
                # Side 2b (Inner Tapered)
                vertices.append(inner_bottom_vertices_taper[v_index_next])
                vertices.append(inner_bottom_vertices_taper[v_index_current])
                vertices.append(inner_top_vertices_taper[v_index_current])


                # --- Outer Side Faces (STRAIGHT SECTION - below taper) ---
                # Side 3a (Outer Straight)
                vertices.append(outer_bottom_vertices_taper[v_index_current]) # Top of straight section
                vertices.append(outer_bottom_vertices_taper[v_index_next]) # Top of straight section
                vertices.append(outer_bottom_vertices_straight[v_index_next]) # Bottom of straight section
                # Side 3b (Outer Straight)
                vertices.append(outer_bottom_vertices_straight[v_index_next]) # Bottom of straight section
                vertices.append(outer_bottom_vertices_straight[v_index_current])# Bottom of straight section
                vertices.append(outer_bottom_vertices_taper[v_index_current]) # Top of straight section


                # --- Inner Side Faces (STRAIGHT SECTION - below taper) ---
                # Side 4a (Inner Straight)
                vertices.append(inner_bottom_vertices_taper[v_index_current]) # Top of straight section
                vertices.append(inner_bottom_vertices_straight[v_index_next]) # Bottom of straight section
                vertices.append(inner_bottom_vertices_taper[v_index_next]) # Top of straight section
                # Side 4b (Inner Straight)
                vertices.append(inner_bottom_vertices_straight[v_index_next]) # Bottom of straight section
                vertices.append(inner_bottom_vertices_straight[v_index_current])# Bottom of straight section
                vertices.append(inner_bottom_vertices_taper[v_index_current]) # Top of straight section


                # --- Bottom Cap Ring (Straight Section Bottom) ---
                # Triangle 1 (Bottom Cap Ring)
                vertices.append(inner_bottom_vertices_straight[v_index_current])
                vertices.append(outer_bottom_vertices_straight[v_index_current])
                vertices.append(outer_bottom_vertices_straight[v_index_next])
                # Triangle 2 (Bottom Cap Ring)
                vertices.append(inner_bottom_vertices_straight[v_index_next])
                vertices.append(outer_bottom_vertices_straight[v_index_next])
                vertices.append(inner_bottom_vertices_straight[v_index_current])
                
        else:
            outer_top_vertices = []   # Array for top outer circle vertices
            outer_bottom_vertices = []  # Array for bottom outer circle vertices
            inner_top_vertices = []   # Array for top inner circle vertices
            inner_bottom_vertices = []  # Array for bottom inner circle vertices

            for i in range(num_segments):
                angle = i * angle_increment_radians
                x = outer_radius * math.cos(angle)  # Calculate X and Z based on outer radius
                z = outer_radius * math.sin(angle)

                # Top Outer Circle Vertices (using shared X, Z and outer_radius)
                outer_top_vertices.append([x, top_additional_height, z])
                # Bottom Outer Circle Vertices (using shared X, Z and bottom_outer_radius)
                outer_bottom_vertices.append([x * (bottom_outer_radius / outer_radius) , negative_length, z * (bottom_outer_radius / outer_radius)]) # Scale X and Z for bottom_outer_radius
                # Top Inner Circle Vertices (using shared X, Z and inner_radius)
                inner_top_vertices.append([x * (inner_radius / outer_radius), top_additional_height, z * (inner_radius / outer_radius)]) # Scale X and Z for inner_radius
                # Bottom Inner Circle Vertices (using shared X, Z and bottom_inner_radius)
                inner_bottom_vertices.append([x * (bottom_inner_radius / outer_radius), negative_length, z * (bottom_inner_radius / outer_radius)]) # Scale X and Z for bottom_inner_radius and bottom_outer_radius

            vertices = []
            for i in range(num_segments):
                # Get vertex indices for this segment, wrapping around
                v_index_current = i
                v_index_next = (i + 1) % num_segments

                # --- Outer Side Faces ---
                # Side 1a (Outer)
                vertices.append(outer_top_vertices[v_index_current])
                vertices.append(outer_top_vertices[v_index_next])
                vertices.append(outer_bottom_vertices[v_index_next])

                # Side 1b (Outer)
                vertices.append(outer_bottom_vertices[v_index_next])
                vertices.append(outer_bottom_vertices[v_index_current])
                vertices.append(outer_top_vertices[v_index_current])

                # --- Inner Side Faces ---
                # Side 2a (Inner) - Note reversed vertex order for inward facing
                vertices.append(inner_top_vertices[v_index_current])
                vertices.append(inner_bottom_vertices[v_index_next])
                vertices.append(inner_top_vertices[v_index_next])

                # Side 2b (Inner) - Note reversed vertex order for inward facing
                vertices.append(inner_bottom_vertices[v_index_next])
                vertices.append(inner_bottom_vertices[v_index_current])
                vertices.append(inner_top_vertices[v_index_current])

                # --- Top Cap Ring (Connecting outer and inner top circles) ---
                # Triangle 1 (Top Cap Ring)
                vertices.append(inner_top_vertices[v_index_current])
                vertices.append(outer_top_vertices[v_index_next])
                vertices.append(outer_top_vertices[v_index_current])

                # Triangle 2 (Top Cap Ring)
                vertices.append(inner_top_vertices[v_index_next])
                vertices.append(outer_top_vertices[v_index_next])
                vertices.append(inner_top_vertices[v_index_current])


                # --- Bottom Cap Ring (Connecting outer and inner bottom circles) ---
                # Triangle 1 (Bottom Cap Ring)
                vertices.append(inner_bottom_vertices[v_index_current])
                vertices.append(outer_bottom_vertices[v_index_current])
                vertices.append(outer_bottom_vertices[v_index_next])

                # Triangle 2 (Bottom Cap Ring)
                vertices.append(inner_bottom_vertices[v_index_next])
                vertices.append(outer_bottom_vertices[v_index_next])
                vertices.append(inner_bottom_vertices[v_index_current])


        mesh.setVertices(numpy.asarray(vertices, dtype=numpy.float32))

        indices = [] # Generate indices based on vertex order (simple sequential indexing)
        for i in range(0, len(vertices), 3):
            indices.append([i, i+1, i+2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))

        mesh.calculateNormals()
        return mesh
        
    # Line Support Creation
    def _createLine(self, top_diameter, minmax_diameter, start_position , end_position, taper_angle, top_offset):
        mesh = MeshBuilder()

        start_point = Vector(start_position.x,start_position.z,start_position.y)
        end_point = Vector(end_position.x,end_position.z,end_position.y)

        line_direction = end_point - start_point

        # Calculate vector
        radius = top_diameter / 2
        max_radius = minmax_diameter / 2
        start_height = start_position.y 
        start_bottom_radius=math.tan(math.radians(taper_angle))*start_height+radius
        end_height = end_position.y 
        end_bottom_radius=math.tan(math.radians(taper_angle))*end_height+radius
 
        if max_radius > radius and taper_angle != 0:
            start_taper_length = (max_radius - radius) / math.tan(math.radians(taper_angle))
            end_taper_length = (max_radius - radius) / math.tan(math.radians(taper_angle))
        else :
            start_taper_length=start_height
            end_taper_length=end_height
 
        top_offset_vector = Vector(0,0,top_offset)
        radius_vector = Vector(0,0,radius)
        start_height_vector = Vector(0,0,-start_height)
        end_height_vector = Vector(0,0,-end_height)
        
        normal_vector = Vector.cross(line_direction, radius_vector).normalized()
        outer_radius_offset = Vector(normal_vector.x*radius,normal_vector.y*radius,normal_vector.z*radius)
            
        if start_taper_length < start_height and end_taper_length < end_height and start_taper_length > 0 and end_taper_length > 0: 
            vertices_per_segment=40
            
            start_max_radius_offset = Vector(normal_vector.x*max_radius,normal_vector.y*max_radius,normal_vector.z*max_radius)
            end_max_radius_offset = Vector(normal_vector.x*max_radius,normal_vector.y*max_radius,normal_vector.z*max_radius)

            start_max_taper_height_vector = Vector(0,0,-start_taper_length)
            end_max_taper_height_vector = Vector(0,0,-end_taper_length)
        
            # X Z Y
            point_1_top = top_offset_vector + outer_radius_offset
            point_2_top = top_offset_vector-outer_radius_offset
            point_3_top = line_direction+top_offset_vector+outer_radius_offset
            point_4_top = line_direction+top_offset_vector-outer_radius_offset
 
            point_1_start_max_taper = start_max_taper_height_vector+start_max_radius_offset
            point_2_start_max_taper = start_max_taper_height_vector-start_max_radius_offset
            point_3_end_max_taper = end_max_taper_height_vector+line_direction+end_max_radius_offset
            point_4_end_max_taper = end_max_taper_height_vector+line_direction-end_max_radius_offset
            
            point_1_start_inner = start_height_vector+start_max_radius_offset
            point_2_start_inner = start_height_vector-start_max_radius_offset
            point_3_end_inner = end_height_vector+line_direction+end_max_radius_offset
            point_4_end_inner = end_height_vector+line_direction-end_max_radius_offset

            """
            1) Top
            2) Front
            3) Left
            4) Right
            5) Back 
            6) Front inf
            7) Left inf
            8) Right inf
            9) Back inf
            10) Bottom
            """
            verts = [ # 10 faces with 4 corners each
                [point_1_top.x, point_1_top.z, point_1_top.y], [point_2_top.x, point_2_top.z, point_2_top.y], [point_4_top.x, point_4_top.z, point_4_top.y], [point_3_top.x, point_3_top.z, point_3_top.y],              
                [point_1_top.x, point_1_top.z, point_1_top.y], [point_3_top.x, point_3_top.z, point_3_top.y], [point_3_end_max_taper.x, point_3_end_max_taper.z, point_3_end_max_taper.y], [point_1_start_max_taper.x, point_1_start_max_taper.z, point_1_start_max_taper.y],
                [point_2_top.x, point_2_top.z, point_2_top.y], [point_1_top.x, point_1_top.z, point_1_top.y], [point_1_start_max_taper.x, point_1_start_max_taper.z, point_1_start_max_taper.y], [point_2_start_max_taper.x, point_2_start_max_taper.z, point_2_start_max_taper.y],
                [point_3_top.x, point_3_top.z, point_3_top.y], [point_4_top.x, point_4_top.z, point_4_top.y], [point_4_end_max_taper.x, point_4_end_max_taper.z, point_4_end_max_taper.y], [point_3_end_max_taper.x, point_3_end_max_taper.z, point_3_end_max_taper.y],
                [point_4_top.x, point_4_top.z, point_4_top.y], [point_2_top.x, point_2_top.z, point_2_top.y], [point_2_start_max_taper.x, point_2_start_max_taper.z, point_2_start_max_taper.y], [point_4_end_max_taper.x, point_4_end_max_taper.z, point_4_end_max_taper.y],
                [point_1_start_max_taper.x, point_1_start_max_taper.z, point_1_start_max_taper.y], [point_3_end_max_taper.x, point_3_end_max_taper.z, point_3_end_max_taper.y], [point_3_end_inner.x, point_3_end_inner.z, point_3_end_inner.y], [point_1_start_inner.x, point_1_start_inner.z, point_1_start_inner.y],
                [point_2_start_max_taper.x, point_2_start_max_taper.z, point_2_start_max_taper.y], [point_1_start_max_taper.x, point_1_start_max_taper.z, point_1_start_max_taper.y], [point_1_start_inner.x, point_1_start_inner.z, point_1_start_inner.y], [point_2_start_inner.x, point_2_start_inner.z, point_2_start_inner.y],
                [point_3_end_max_taper.x, point_3_end_max_taper.z, point_3_end_max_taper.y], [point_4_end_max_taper.x, point_4_end_max_taper.z, point_4_end_max_taper.y], [point_4_end_inner.x, point_4_end_inner.z, point_4_end_inner.y], [point_3_end_inner.x, point_3_end_inner.z, point_3_end_inner.y],
                [point_4_end_max_taper.x, point_4_end_max_taper.z, point_4_end_max_taper.y], [point_2_start_max_taper.x, point_2_start_max_taper.z, point_2_start_max_taper.y], [point_2_start_inner.x, point_2_start_inner.z, point_2_start_inner.y], [point_4_end_inner.x, point_4_end_inner.z, point_4_end_inner.y],
                [point_1_start_inner.x, point_1_start_inner.z, point_1_start_inner.y], [point_2_start_inner.x, point_2_start_inner.z, point_2_start_inner.y], [point_4_end_inner.x, point_4_end_inner.z, point_4_end_inner.y], [point_3_end_inner.x, point_3_end_inner.z, point_3_end_inner.y]
            ]
            
        else:
            vertices_per_segment=24

            start_max_radius_offset = Vector(normal_vector.x*start_bottom_radius,normal_vector.y*start_bottom_radius,normal_vector.z*start_bottom_radius)
            end_max_radius_offset = Vector(normal_vector.x*end_bottom_radius,normal_vector.y*end_bottom_radius,normal_vector.z*end_bottom_radius)

            # X Z Y
            point_1_top = top_offset_vector+outer_radius_offset
            point_2_top = top_offset_vector-outer_radius_offset
            point_3_top = line_direction+top_offset_vector+outer_radius_offset
            point_4_top = line_direction+top_offset_vector-outer_radius_offset
     
            point_1_start_inner = start_height_vector+start_max_radius_offset
            point_2_start_inner = start_height_vector-start_max_radius_offset
            point_3_end_inner = end_height_vector+line_direction+end_max_radius_offset
            point_4_end_inner = end_height_vector+line_direction-end_max_radius_offset

            """
            1) Top
            2) Front
            3) Left
            4) Right
            5) Back 
            6) Bottom
            """
            verts = [ # 6 faces with 4 corners each
                [point_1_top.x, point_1_top.z, point_1_top.y], [point_2_top.x, point_2_top.z, point_2_top.y], [point_4_top.x, point_4_top.z, point_4_top.y], [point_3_top.x, point_3_top.z, point_3_top.y],
                [point_1_top.x, point_1_top.z, point_1_top.y], [point_3_top.x, point_3_top.z, point_3_top.y], [point_3_end_inner.x, point_3_end_inner.z, point_3_end_inner.y], [point_1_start_inner.x, point_1_start_inner.z, point_1_start_inner.y],
                [point_2_top.x, point_2_top.z, point_2_top.y], [point_1_top.x, point_1_top.z, point_1_top.y], [point_1_start_inner.x, point_1_start_inner.z, point_1_start_inner.y], [point_2_start_inner.x, point_2_start_inner.z, point_2_start_inner.y],
                [point_3_top.x, point_3_top.z, point_3_top.y], [point_4_top.x, point_4_top.z, point_4_top.y], [point_4_end_inner.x, point_4_end_inner.z, point_4_end_inner.y], [point_3_end_inner.x, point_3_end_inner.z, point_3_end_inner.y],
                [point_4_top.x, point_4_top.z, point_4_top.y], [point_2_top.x, point_2_top.z, point_2_top.y], [point_2_start_inner.x, point_2_start_inner.z, point_2_start_inner.y], [point_4_end_inner.x, point_4_end_inner.z, point_4_end_inner.y],
                [point_1_start_inner.x, point_1_start_inner.z, point_1_start_inner.y], [point_2_start_inner.x, point_2_start_inner.z, point_2_start_inner.y], [point_4_end_inner.x, point_4_end_inner.z, point_4_end_inner.y], [point_3_end_inner.x, point_3_end_inner.z, point_3_end_inner.y]
            ]
        
        mesh.setVertices(numpy.asarray(verts, dtype=numpy.float32))

        indices = []
        for i in range(0, vertices_per_segment, 4): # All 6 quads (12 triangles)
            indices.append([i, i+2, i+1])
            indices.append([i, i+3, i+2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))

        mesh.calculateNormals()
        return mesh

    def removeAllSupportMesh(self):
        if self._supports_created:
            for node in self._supports_created:
                node_stack = node.callDecoration("getStack")
                if node_stack.getProperty("support_mesh", "value"):
                    self._removeSupportMesh(node)
            self._supports_created = []
            self._panel_remove_all_text = self._catalog.i18nc("panel:remove_all", "Remove All")
            self.propertyChanged.emit()
        else:        
            for node in DepthFirstIterator(self._application.getController().getScene().getRoot()):
                if node.callDecoration("isSliceable"):
                    # N_Name=node.getName()
                    # Logger.log('d', 'isSliceable : ' + str(N_Name))
                    node_stack=node.callDecoration("getStack")           
                    if node_stack:        
                        if node_stack.getProperty("support_mesh", "value"):
                            # N_Name=node.getName()
                            # Logger.log('d', 'support_mesh : ' + str(N_Name)) 
                            self._removeSupportMesh(node)
        
    def getSupportSize(self) -> float:
        return self._support_size
  
    def setSupportSize(self, new_size: str) -> None:
        try:
            new_value = float(new_size)
        except ValueError:
            return

        if new_value <= 0:
            return
        
        self._support_size = new_value
        self._preferences.setValue("customsupportsreborn/support_size", new_value)
        log("d", f"CustomSupportsReborn._support_size being set to {new_value}")
        self.propertyChanged.emit()
    
    #supportSize = property(getSupportSize, setSupportSize)

    def getSupportSizeMax(self) -> float:
        return self._support_size_max
  
    def setSupportSizeMax(self, new_size: str) -> None:
        try:
            new_value = float(new_size)
        except ValueError:
            return

        if new_value < 0:
            log("i", "Tried to set SupportSizeMax to < 0")
            return
        
        self._support_size_max = new_value
        self._preferences.setValue("customsupportsreborn/support_size_max", new_value)
        log("d", f"CustomSupportsReborn._support_size_max being set to {new_value}")
        self.propertyChanged.emit()
    
    #supportSizeMax = property(getSupportSizeMax, setSupportSizeMax)
        
    def getSupportSizeInner(self) -> float:
        return self._support_size_inner
  
    def setSupportSizeInner(self, new_size: str) -> None:
        try:
            new_value = float(new_size)
        except ValueError:
            return

        if new_value <= 0:
            return
        if new_value >= self._support_size:
            new_value = self._support_size
        
        #Logger.log('d', 's_value : ' + str(s_value))        
        self._support_size_inner = new_value
        self._preferences.setValue("customsupportsreborn/support_size_inner", new_value)
        log("d", f"CustomSupportsReborn._support_size_inner being set to {new_value}")
        self.propertyChanged.emit()
    
    #supportSizeInner = property(getSupportSizeInner, setSupportSizeInner)
        
    def getSupportAngle(self) -> float:
        return self._support_angle
  
    def setSupportAngle(self, new_angle: str) -> None:
        try:
            new_value = float(new_angle)
        except ValueError:
            return

        # Logger.log('d', 's_value : ' + str(s_value))        
        self._support_angle = new_value
        self._preferences.setValue("customsupportsreborn/support_angle", new_value)
        log("d", f"CustomSupportsReborn._support_angle being set to {new_value}")
        self.propertyChanged.emit()
        self._setEffectiveTaperAngle()

    def _setEffectiveTaperAngle(self) -> None:
        if self._support_angle == 0:
            self._effective_taper_angle = 0
            self._taper_direction = ""
        elif self._support_angle > 0:
            self._effective_taper_angle = self._support_angle
            self._taper_direction = "outward"
        else:
            self._effective_taper_angle = self._support_angle
            self._taper_direction = "inward"

    #supportAngle = property(getSupportAngle, setSupportAngle)
 
    def getPanelRemoveAllText(self) -> str:
        return self._panel_remove_all_text
    
    def setPanelRemoveAllText(self, new_text: str) -> None:
        self._panel_remove_all_text = str(new_text)
        log("d", f"CustomSupporsReborn._panel_remove_all_text being set to {new_text}")
        self.propertyChanged.emit()

    #panelRemoveAllText = property(getPanelRemoveAllText, setPanelRemoveAllText)
        
    def getSupportType(self) -> str:
        return self._support_type
    
    def setSupportType(self, new_type: str) -> None:
        self._support_type = new_type
        log("d", f"CustomSupportsReborn._support_type being set to {new_type}")
        self._preferences.setValue("customsupportsreborn/support_type", new_type)
        self.propertyChanged.emit()

    #supportType = property(getSupportType, setSupportType)
 
    def getModelSubtype(self) -> str:
        # Logger.log('d', 'Set SubType : ' + str(self._SubType))  
        return self._model_subtype
    
    def setModelSubtype(self, new_type: str) -> None:
        self._model_subtype = new_type
        # Logger.log('d', 'Get SubType : ' + str(SubType))   
        self._preferences.setValue("customsupportsreborn/model_subtype", new_type)
        log("d", f"CustomSupportsReborn._model_subtype being set to {new_type}")
        self.propertyChanged.emit()

    # modelSubtype = property(getModelSubtype, setModelSubtype)

    """def getModelSubtypeIndex(self) -> int:
        log_stack(f"CustomSupportsReborn: Stack for _model_subtype_index being read as {self._model_subtype_index}")
        return self._model_subtype_index
    
    def setModelSubtypeIndex(self, new_index: int) -> None:
        self._model_subtype_index = new_index
        # Logger.log('d', 'Get SubType : ' + str(SubType))   
        # log("d", f"_model_subtype_index being set to {new_index}")
        log_stack(f"CustomSupportsReborn: Stack for _model_subtype_index being set to {new_index}")
        self._preferences.setValue("customsupportsreborn/model_subtype_index", new_index)
        self.propertyChanged.emit()

    modelSubtypeIndex = property(getModelSubtypeIndex, setModelSubtypeIndex)"""
        
    def getSupportYDirection(self) -> bool:
        return self._support_y_direction
    
    def setSupportYDirection(self, YDirection: bool) -> None:
        try:
            new_value = bool(YDirection)
        except ValueError:
            return
        
        self._support_y_direction = new_value
        self._preferences.setValue("customsupportsreborn/support_y_direction", new_value)
        log("d", f"CustomSupportsReborn._support_y_direction being set to {new_value}")
        self.propertyChanged.emit()

    #supportYDirection = property(getSupportYDirection, setSupportYDirection)
 
    def getAbutmentEqualizeHeights(self) -> bool:
        return self._abutment_equalize_heights
  
    def setAbutmentEqualizeHeights(self, equalize: bool) -> None:
        try:
            new_value = bool(equalize)
        except ValueError:
            return

        self._abutment_equalize_heights = new_value
        self._preferences.setValue("customsupportsreborn/abutment_equalize_heights", new_value)
        log("d", f"CustomSupportsReborn._abutment_equalize_heights being set to {new_value}")
        self.propertyChanged.emit()

    #abutmentEqualizeHeights = property(getAbutmentEqualizeHeights, setAbutmentEqualizeHeights)
 
    def getModelScaleMain(self) -> bool:
        return self._model_scale_main
  
    def setModelScaleMain(self, scale: bool) -> None:
        try:
            new_value = bool(scale)
        except ValueError:
            return

        self._model_scale_main = new_value
        self._preferences.setValue("customsupportsreborn/model_scale_main", new_value)
        log("d", f"CustomSupportsReborn._model_scale_main being set to {new_value}")
        self.propertyChanged.emit()

    #modelScaleMain = property(getModelScaleMain, setModelScaleMain)
        
    def getModelOrient(self) -> bool:
        return self._model_orient
  
    def setModelOrient(self, orient: bool) -> None:
        try:
            new_value = bool(orient)
        except ValueError:
            return

        self._model_orient = new_value
        self._preferences.setValue("customsupportsreborn/model_orient", new_value)
        log("d", f"CustomSupportsReborn._model_orient being set to {new_value}")
        self.propertyChanged.emit()
    
    #modelOrient = property(getModelOrient, setModelOrient)
    
    def getModelMirror(self) -> bool:
        return self._model_mirror
  
    def setModelMirror(self, mirror: bool) -> None:
        try:
            new_value = bool(mirror)
        except ValueError:
            return

        self._model_mirror = new_value
        self._preferences.setValue("customsupportsreborn/model_mirror", new_value)
        log("d", f"CustomSupportsReborn._model_mirror being set to {new_value}")
        self.propertyChanged.emit()

    #modelMirror = property(getModelMirror, setModelMirror)