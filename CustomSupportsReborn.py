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
# V1.0.0 - Initial release.
#   Reverted everything to v2.8.0 manually as the version in the master branch seems to contain some "work in progress" stuff.
#   Renamed everything. Including internally so it doesn't compete with 5@xes' verison if you still have that installed.
#   Futzed around with the translation system and ended up with basically the same thing. 
#   Removed support for Qt 5 and bumped minimum Cura version to 5.0 so I'm not doing things twice and can use newer Python features if I need.
#   Cleaned up the code a little bit and tried to give some variables more readable names.
#   Changed the icon to illustrate it does more than cylinders. Now it looks like it does rockets.
#   Renamed "Freeform" to "Model" and "Custom" to "Line" and swapped their positions.

from PyQt6.QtCore import Qt, QTimer, QObject, QVariant, pyqtProperty
from PyQt6.QtQml import qmlRegisterType
from PyQt6.QtWidgets import QApplication

import math
import numpy
import os.path
import trimesh
import logging
from enum import Enum

from typing import Optional, List

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

#i18n_cura_catalog = i18nCatalog("cura")
#i18n_printer_catalog = i18nCatalog("fdmprinter.def.json")
#i18n_extrud_catalog = i18nCatalog("fdmextruder.def.json")

#Resources.addSearchPath(
#    os.path.join(os.path.abspath(os.path.dirname(__file__)))
#)  # Plugin translation file import

#i18n_catalog = i18nCatalog("customsupportsreborn")

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
    #propertyChanged = pyqtSignal(str)

    def __init__(self):
       
        super().__init__()

        Resources.addSearchPath(os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "resources"
        )))  # Plugin translation file import

        self._catalog = i18nCatalog("customsupportsreborn")

        self.setExposedProperties("SupportType", "SupportSubtype", "SupportSize", "SupportSizeMax", "SupportSizeInner", "SupportAngle", "SupportYDirection", "AbutmentEqualizeHeights", "ModelScaleMain", "ModelOrient", "ModelMirror", "PanelRemoveAllText")

        self._supports_created: List[SceneNode] = []
        
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
        self._support_type: str = 'cylinder'
        self._support_subtype: str = 'cross'
        self._model_hide_message:bool = False # To avoid message 
        self._panel_remove_all_text: str = self._catalog.i18nc("panel:remove_all", "Remove All")
        
        # Shortcut
        self._shortcut_key: Qt.Key = Qt.Key.Key_F
            
        self._controller: Controller = self.getController()
        self._application: CuraApplication = CuraApplication.getInstance()

        self._custom_point_location: Vector = Vector(0,0,0)
        self._selection_pass: SceneNode = None
        
        
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
        self._preferences.addPreference("customsupportsreborn/support_subtype", "cross")
        
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
        self._support_subtype = str(self._preferences.getValue("customsupportsreborn/support_subtype"))

                
    def event(self, event):
        super().event(event)
        modifiers = QApplication.keyboardModifiers()
        ctrl_is_active = modifiers & Qt.KeyboardModifier.ControlModifier
        shift_is_active = modifiers & Qt.KeyboardModifier.ShiftModifier
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


    def _createSupportMesh(self, parent: CuraSceneNode, position: Vector , position2: Vector):
        node = CuraSceneNode()
        EName = parent.getName()

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
        
        # long=Support Height
        self._long=position.y
        # Logger.log("d", "Long Support= %s", str(self._long))
        
        # Limitation for support height to Node Height
        # For Cube/Cylinder/Tube
        # Test with 0.5 because the precision on the clic poisition is not very thight 
        if self._long >= (self._nodeHeight-0.5) :
            # additionale length
            self._Sup = 0
        else :
            if self._support_type == SUPPORT_TYPE_CUBE:
                self._Sup = self._support_size*0.5
            elif self._support_type == SUPPORT_TYPE_ABUTMENT:
                self._Sup = self._support_size
            else :
                self._Sup = self._support_size*0.1
                
        # Logger.log("d", "Additional Long Support = %s", str(self._long+self._Sup))    
            
        if self._support_type == SUPPORT_TYPE_CYLINDER:
            # Cylinder creation Diameter , Maximum diameter , Increment angle 10°, length , top Additional Height, Angle of the support
            mesh = self._createCylinder(self._support_size,self._support_size_max,10,self._long,self._Sup,self._support_angle)
        elif self._support_type == SUPPORT_TYPE_TUBE:
            # Tube creation Diameter ,Maximum diameter , Diameter Int, Increment angle 10°, length, top Additional Height , Angle of the support
            mesh =  self._createTube(self._support_size,self._support_size_max,self._support_size_inner,10,self._long,self._Sup,self._support_angle)
        elif self._support_type == SUPPORT_TYPE_CUBE:
            # Cube creation Size,Maximum Size , length , top Additional Height, Angle of the support
            mesh =  self._createCube(self._support_size,self._support_size_max,self._long,self._Sup,self._support_angle)
        elif self._support_type == SUPPORT_TYPE_MODEL:
            # Cube creation Size , length
            mesh = MeshBuilder()  
            MName = self._support_subtype + ".stl"
            model_definition_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", MName)
            # Logger.log('d', 'Model_definition_path : ' + str(model_definition_path)) 
            load_mesh = trimesh.load(model_definition_path)
            origin = [0, 0, 0]
            DirX = [1, 0, 0]
            DirY = [0, 1, 0]
            DirZ = [0, 0, 1]
            
            # Solution must be tested ( other solution just on the X Axis)
            if self._model_scale_main :
                if (self._long * 0.5 ) < self._support_size :
                    Scale = self._support_size
                else :
                    Scale = self._long * 0.5
                load_mesh.apply_transform(trimesh.transformations.scale_matrix(Scale, origin, DirX))
                load_mesh.apply_transform(trimesh.transformations.scale_matrix(Scale, origin, DirY))
            else :
                load_mesh.apply_transform(trimesh.transformations.scale_matrix(self._support_size, origin, DirX))
                load_mesh.apply_transform(trimesh.transformations.scale_matrix(self._support_size, origin, DirY))
                
            # load_mesh.apply_transform(trimesh.transformations.scale_matrix(self._UseSize, origin, DirY))
 
            load_mesh.apply_transform(trimesh.transformations.scale_matrix(self._long, origin, DirZ)) 
            
            # Logger.log('d', "Info Orient Support --> " + str(self._OrientSupport))
            if self._model_orient == True :
                # This function can be triggered in the middle of a machine change, so do not proceed if the machine change has not done yet.
                global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()
                adhesion_key = "adhesion_type"
                adhesion_value=global_container_stack.getProperty(adhesion_key, "value")
                   
                if adhesion_value == 'none' :
                    adhesion_options = global_container_stack.getProperty(adhesion_key, "options")

                    global_container_stack.setProperty("adhesion_type", "value", "skirt")
                    Logger.log('d', "Info adhesion_type --> " + str(adhesion_value)) 
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
                _angle = self.defineAngle(EName,position)
                if self._support_y_direction == True :
                    _angle = self.mainAngle(_angle)
                Logger.log('d', 'Angle : ' + str(_angle))
                load_mesh.apply_transform(trimesh.transformations.rotation_matrix(_angle, [0, 0, 1]))
            
            elif self._support_y_direction == True :
                load_mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(90), [0, 0, 1]))

            if self._model_mirror == True and self._model_orient == False :   
                load_mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(180), [0, 0, 1]))
                
            mesh =  self._toMeshData(load_mesh)
            
        elif self._support_type == SUPPORT_TYPE_ABUTMENT:
            # Abutement creation Size , length , top
            if self._abutment_equalize_heights == True :
                # Logger.log('d', 'SHeights : ' + str(self._SHeights)) 
                if self._support_heights==0 :
                    self._support_heights=position.y
                    self._SSup=self._Sup

                self._top=self._SSup+(self._support_heights-position.y)
                
            else:
                self._top=self._Sup
                self._support_heights=0
            
            # 
            Logger.log('d', 'top : ' + str(self._top))
            # Logger.log('d', 'MaxSize : ' + str(self._MaxSize))
            
            mesh =  self._createAbutment(self._support_size,self._support_size_max,self._long,self._top,self._support_angle,self._support_y_direction)
        else:           
            # Custom creation Size , P1 as vector P2 as vector
            # Get support_interface_height as extra distance 
            extruder_stack = self._application.getExtruderManager().getActiveExtruderStacks()[0]
            if self._Sup == 0 :
                extra_top = 0
            else :
                extra_top=extruder_stack.getProperty("support_interface_height", "value")            
            mesh =  self._createLine(self._support_size,self._support_size_max,position,position2,self._support_angle,extra_top)

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
                Logger.log("w", "Setting support_type does not have any options defined") # Log if no options are defined
            Message(text = f"{self._catalog.i18nc('support_placement_warning:dialog:start', 'Had to change setting')} {support_placement_label} {self._catalog.i18nc('support_placement_warning:middle', 'to')} {translated_support_placement} {self._catalog.i18nc('support_placement_warning:end', 'for support to work.')}", title = self._catalog.i18nc("support_placement_warning:title", "WARNING: Custom Supports Reborn")).show()
            Logger.log('d', 'Support_type different from everywhere : ' + str(support_placement))
            # Define support_type=everywhere
            global_container_stack.setProperty("support_type", "value", 'everywhere')
            
        op = GroupedOperation()
        # First add node to the scene at the correct position/scale, before parenting, so the support mesh does not get scaled with the parent
        op.addOperation(AddSceneNodeOperation(node, self._controller.getScene().getRoot()))
        op.addOperation(SetParentOperation(node, parent))
        op.push()
        node.setPosition(position, CuraSceneNode.TransformSpace.World)
        self._supports_created.append(node)
        self._panel_remove_all_text = self._catalog.i18nc("panel:remove_last", "Remove Last")
        self.propertyChanged.emit()
        
        CuraApplication.getInstance().getController().getScene().sceneChanged.emit(node)

    # Source code from MeshTools Plugin 
    # Copyright (c) 2020 Aldo Hoeben / fieldOfView
    def _getAllSelectedNodes(self) -> List[SceneNode]:
        selection = Selection.getAllSelectedObjects()[:]
        if selection:
            deep_selection = []  # type: List[SceneNode]
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
    
    def defineAngle(self, Cname : str, act_position: Vector) -> float:
        Angle = 0
        min_lght = 9999999.999
        # Set on the build plate for distance
        calc_position = Vector(act_position.x, 0, act_position.z)
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
                    if node.getName()==Cname :
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
                        Id=0
                        Start_Id=0
                        End_Id=0
                        for point in points:                               
                            # Logger.log('d', "X : {}".format(point[0]))
                            # Logger.log('d', "Point : {}".format(point))
                            new_position = Vector(point[0], 0, point[1])
                            lg=calc_position-new_position
                            # Logger.log('d', "Lg : {}".format(lg))
                            # lght = lg.length()
                            lght = round(lg.length(),0)

                            if lght<min_lght and lght>0 :
                                min_lght=lght
                                Start_Id=Id
                                Select_position = new_position
                                unit_vector2 = lg.normalized()
                                # Logger.log('d', "unit_vector2 : {}".format(unit_vector2))
                                LeSin = math.asin(reference_angle.dot(unit_vector2))
                                # LeCos = math.acos(ref.dot(unit_vector2))
                                
                                if unit_vector2.x>=0 :
                                    # Logger.log('d', "Angle Pos 1a")
                                    Angle = math.pi-LeSin  #angle in radian
                                else :
                                    # Logger.log('d', "Angle Pos 2a")
                                    Angle = LeSin                                    
                                    
                            if lght==min_lght and lght>0 :
                                if Id > End_Id+1 :
                                    Start_Id=Id
                                    End_Id=Id
                                else :
                                    End_Id=Id
                                    
                            Id+=1
                        
                        # Could be the case with automatic .. rarely in pickpoint   
                        if Start_Id != End_Id :
                            # Logger.log('d', "Possibility   : {} / {}".format(Start_Id,End_Id))
                            Id=int(Start_Id+0.5*(End_Id-Start_Id))
                            # Logger.log('d', "Id   : {}".format(Id))
                            new_position = Vector(points[Id][0], 0, points[Id][1])
                            lg=calc_position-new_position                            
                            unit_vector2 = lg.normalized()
                            # Logger.log('d', "unit_vector2 : {}".format(unit_vector2))
                            LeSin = math.asin(reference_angle.dot(unit_vector2))
                            # LeCos = math.acos(ref.dot(unit_vector2))
                            
                            if unit_vector2.x >=0 :
                                # Logger.log('d', "Angle Pos 1b")
                                Angle = math.pi-LeSin  #angle in radian
                                
                            else :
                                # Logger.log('d', "Angle Pos 2b")
                                Angle = LeSin
                                
                            
                            # Modification / Spoon not ne same start orientation
                            
                        # Logger.log('d', "Pick_position   : {}".format(calc_position))
                        # Logger.log('d', "Close_position  : {}".format(Select_position))
                        # Logger.log('d', "Unit_vector2    : {}".format(unit_vector2))
                        # Logger.log('d', "Angle Sinus     : {}".format(math.degrees(LeSin)))
                        # Logger.log('d', "Angle Cosinus   : {}".format(math.degrees(LeCos)))
                        # Logger.log('d', "Chose Angle     : {}".format(math.degrees(Angle)))
        return Angle
        
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
    def _createCube(self, size, maxs, height, top, dep):
        mesh = MeshBuilder()

        # Intial Comment from Ultimaker B.V. I have never try to verify this point
        # Can't use MeshBuilder.addCube() because that does not get per-vertex normals
        # Per-vertex normals require duplication of vertices
        s = size / 2
        sm = maxs / 2
        l = height 
        s_inf=s+math.tan(math.radians(dep))*(l+top)
        
        if sm>s and dep!=0:
            l_max=(sm-s) / math.tan(math.radians(dep))
        else :
            l_max=l
        
        # Difference between Cone and Cone + max base size
        if l_max<l and l_max>0:
            nbv=40        
            verts = [ # 10 faces with 4 corners each
                [-sm, -l_max,  sm], [-s,  top,  s], [ s,  top,  s], [ sm, -l_max,  sm],
                [-s,  top, -s], [-sm, -l_max, -sm], [ sm, -l_max, -sm], [ s,  top, -s],
                [-sm, -l,  sm], [-sm,  -l_max,  sm], [ sm,  -l_max,  sm], [ sm, -l,  sm],
                [-sm,  -l_max, -sm], [-sm, -l, -sm], [ sm, -l, -sm], [ sm,  -l_max, -sm],
                [ sm, -l, -sm], [-sm, -l, -sm], [-sm, -l,  sm], [ sm, -l,  sm],
                [-s,  top, -s], [ s,  top, -s], [ s,  top,  s], [-s,  top,  s],
                [-sm, -l,  sm], [-sm, -l, -sm], [-sm,  -l_max, -sm], [-sm,  -l_max,  sm],
                [ sm, -l, -sm], [ sm, -l,  sm], [ sm,  -l_max,  sm], [ sm,  -l_max, -sm],  
                [-sm, -l_max,  sm], [-sm, -l_max, -sm], [-s,  top, -s], [-s,  top,  s],
                [ sm, -l_max, -sm], [ sm, -l_max,  sm], [ s,  top,  s], [ s,  top, -s]
            ]       
        else:
            nbv=24        
            verts = [ # 6 faces with 4 corners each
                [-s_inf, -l,  s_inf], [-s,  top,  s], [ s,  top,  s], [ s_inf, -l,  s_inf],
                [-s,  top, -s], [-s_inf, -l, -s_inf], [ s_inf, -l, -s_inf], [ s,  top, -s],
                [ s_inf, -l, -s_inf], [-s_inf, -l, -s_inf], [-s_inf, -l,  s_inf], [ s_inf, -l,  s_inf],
                [-s,  top, -s], [ s,  top, -s], [ s,  top,  s], [-s,  top,  s],
                [-s_inf, -l,  s_inf], [-s_inf, -l, -s_inf], [-s,  top, -s], [-s,  top,  s],
                [ s_inf, -l, -s_inf], [ s_inf, -l,  s_inf], [ s,  top,  s], [ s,  top, -s]
            ]
        mesh.setVertices(numpy.asarray(verts, dtype=numpy.float32))

        indices = []
        for i in range(0, nbv, 4): # All 6 quads (12 triangles)
            indices.append([i, i+2, i+1])
            indices.append([i, i+3, i+2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))

        mesh.calculateNormals()
        return mesh
        
    # Abutment Creation
    def _createAbutment(self, size, maxs, height, top, dep, ydir):
    
        # Logger.log('d', 'Ydir : ' + str(ydir)) 
        mesh = MeshBuilder()

        s = size / 2
        sm = maxs / 2
        l = height 
        s_inf=math.tan(math.radians(dep))*(l+top)+(2*s)
        
        if sm>s and dep!=0:
            l_max=(sm-s) / math.tan(math.radians(dep))
        else :
            l_max=l
        
        # Debug Log Lines
        # Logger.log('d', 's_inf : ' + str(s_inf))
        # Logger.log('d', 'l_max : ' + str(l_max)) 
        # Logger.log('d', 'l : ' + str(l))
        
        # Difference between Standart Abutment and Abutment + max base size
        if l_max<l and l_max>0:
            nbv=40  
            if ydir == False :
                verts = [ # 10 faces with 4 corners each
                    [-s, -l_max,  sm], [-s,  top,  2*s], [ s,  top,  2*s], [ s, -l_max,  sm],
                    [-s,  top, -2*s], [-s, -l_max, -sm], [ s, -l_max, -sm], [ s,  top, -2*s],
                    [-s, -l,  sm], [-s,  -l_max,  sm], [ s,  -l_max,  sm], [ s, -l,  sm],
                    [-s,  -l_max, -sm], [-s, -l, -sm], [ s, -l, -sm], [ s,  -l_max, -sm],                  
                    [ s, -l, -sm], [-s, -l, -sm], [-s, -l,  sm], [ s, -l,  sm],
                    [-s,  top, -2*s], [ s,  top, -2*s], [ s,  top,  2*s], [-s,  top,  2*s],
                    [-s, -l_max,  sm], [-s, -l_max, -sm], [-s,  top, -2*s], [-s,  top,  2*s],
                    [ s, -l_max, -sm], [ s, -l_max,  sm], [ s,  top,  2*s], [ s,  top, -2*s],                   
                    [-s, -l,  sm], [-s, -l, -sm], [-s,  -l_max, -sm], [-s,  -l_max,  sm],
                    [ s, -l, -sm], [ s, -l,  sm], [ s,  -l_max,  sm], [ s,  -l_max, -sm]
                ]
            else:
                verts = [ # 10 faces with 4 corners each
                    [-sm, -l_max,  s], [-2*s,  top,  s], [ 2*s,  top,  s], [ sm, -l_max,  s],
                    [-2*s,  top, -s], [-sm, -l_max, -s], [ sm, -l_max, -s], [ 2*s,  top, -s],                
                    [-sm, -l,  s], [-sm,  -l_max,  s], [ sm,  -l_max,  s], [ sm, -l,  s],
                    [-sm,  -l_max, -s], [-sm, -l, -s], [ sm, -l, -s], [ sm,  -l_max, -s],                         
                    [ sm, -l, -s], [-sm, -l, -s], [-sm, -l,  s], [ sm, -l,  s],
                    [-2*s,  top, -s], [ 2*s,  top, -s], [ 2*s,  top,  s], [-2*s,  top,  s],             
                    [-sm, -l_max,  s], [-sm, -l_max, -s], [-2*s,  top, -s], [-2*s,  top,  s],
                    [ sm, -l_max, -s], [ sm, -l_max,  s], [ 2*s,  top,  s], [ 2*s,  top, -s],                                  
                    [-sm, -l,  s], [-sm, -l, -s], [-sm,  -l_max, -s], [-sm,  -l_max,  s],
                    [ sm, -l, -s], [ sm, -l,  s], [ sm,  -l_max,  s], [ sm,  -l_max, -s]
                ]             
        else:
            nbv=24        
            if ydir == False :
                verts = [ # 6 faces with 4 corners each
                    [-s, -l,  s_inf], [-s,  top,  2*s], [ s,  top,  2*s], [ s, -l,  s_inf],
                    [-s,  top, -2*s], [-s, -l, -s_inf], [ s, -l, -s_inf], [ s,  top, -2*s],
                    [ s, -l, -s_inf], [-s, -l, -s_inf], [-s, -l,  s_inf], [ s, -l,  s_inf],
                    [-s,  top, -2*s], [ s,  top, -2*s], [ s,  top,  2*s], [-s,  top,  2*s],
                    [-s, -l,  s_inf], [-s, -l, -s_inf], [-s,  top, -2*s], [-s,  top,  2*s],
                    [ s, -l, -s_inf], [ s, -l,  s_inf], [ s,  top,  2*s], [ s,  top, -2*s]
                ]
            else:
                verts = [ # 6 faces with 4 corners each
                    [-s_inf, -l,  s], [-2*s,  top,  s], [ 2*s,  top,  s], [ s_inf, -l,  s],
                    [-2*s,  top, -s], [-s_inf, -l, -s], [ s_inf, -l, -s], [ 2*s,  top, -s],
                    [ s_inf, -l, -s], [-s_inf, -l, -s], [-s_inf, -l,  s], [ s_inf, -l,  s],
                    [-2*s,  top, -s], [ 2*s,  top, -s], [ 2*s,  top,  s], [-2*s,  top,  s],
                    [-s_inf, -l,  s], [-s_inf, -l, -s], [-2*s,  top, -s], [-2*s,  top,  s],
                    [ s_inf, -l, -s], [ s_inf, -l,  s], [ 2*s,  top,  s], [ 2*s,  top, -s]
                ]        
        mesh.setVertices(numpy.asarray(verts, dtype=numpy.float32))

        indices = []
        for i in range(0, nbv, 4): # All 6 quads (12 triangles)
            indices.append([i, i+2, i+1])
            indices.append([i, i+3, i+2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))

        mesh.calculateNormals()
        return mesh
        
    # Cylinder creation
    def _createCylinder(self, size, maxs, nb , lg , sup ,dep):
        mesh = MeshBuilder()
        # Per-vertex normals require duplication of vertices
        r = size / 2
        rm = maxs / 2

        l = -lg
        rng = int(360 / nb)
        ang = math.radians(nb)
        r_inf=math.tan(math.radians(dep))*lg+r
        if rm>r and dep!=0 :
            l_max=(rm-r) / math.tan(math.radians(dep))
        else :
            l_max=l
            
        #Logger.log('d', 'lg : ' + str(lg))
        #Logger.log('d', 'l_max : ' + str(l_max)) 
        
        verts = []
        if l_max<lg and l_max>0:
            nbv=18
            for i in range(0, rng):
                # Top
                verts.append([0, sup, 0])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                #Side 1a
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([rm*math.cos((i+1)*ang), -l_max, rm*math.sin((i+1)*ang)])
                #Side 1b
                verts.append([rm*math.cos((i+1)*ang), -l_max, rm*math.sin((i+1)*ang)])
                verts.append([rm*math.cos(i*ang), -l_max, rm*math.sin(i*ang)])
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                #Side 2a
                verts.append([rm*math.cos(i*ang), -l_max, rm*math.sin(i*ang)])
                verts.append([rm*math.cos((i+1)*ang), -l_max, rm*math.sin((i+1)*ang)])
                verts.append([rm*math.cos((i+1)*ang), l, rm*math.sin((i+1)*ang)])
                #Side 2b
                verts.append([rm*math.cos((i+1)*ang), l, rm*math.sin((i+1)*ang)])
                verts.append([rm*math.cos(i*ang), l, rm*math.sin(i*ang)])
                verts.append([rm*math.cos(i*ang), -l_max, rm*math.sin(i*ang)])
                #Bottom 
                verts.append([0, l, 0])
                verts.append([rm*math.cos(i*ang), l, rm*math.sin(i*ang)])
                verts.append([rm*math.cos((i+1)*ang), l, rm*math.sin((i+1)*ang)]) 
                
        else:
            nbv=12
            for i in range(0, rng):
                # Top
                verts.append([0, sup, 0])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                #Side 1a
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([r_inf*math.cos((i+1)*ang), l, r_inf*math.sin((i+1)*ang)])
                #Side 1b
                verts.append([r_inf*math.cos((i+1)*ang), l, r_inf*math.sin((i+1)*ang)])
                verts.append([r_inf*math.cos(i*ang), l, r_inf*math.sin(i*ang)])
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                #Bottom 
                verts.append([0, l, 0])
                verts.append([r_inf*math.cos(i*ang), l, r_inf*math.sin(i*ang)])
                verts.append([r_inf*math.cos((i+1)*ang), l, r_inf*math.sin((i+1)*ang)])
        
        mesh.setVertices(numpy.asarray(verts, dtype=numpy.float32))

        indices = []
        # for every angle increment nbv (12 or 18) Vertices
        tot = rng * nbv
        for i in range(0, tot, 3): # 
            indices.append([i, i+1, i+2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))

        mesh.calculateNormals()
        return mesh
 
   # Tube creation
    def _createTube(self, size, maxs, isize, nb , lg, sup ,dep):
        # Logger.log('d', 'isize : ' + str(isize)) 
        mesh = MeshBuilder()
        # Per-vertex normals require duplication of vertices
        r = size / 2
        ri = isize / 2
        rm = maxs / 2
        l = -lg
        rng = int(360 / nb)
        ang = math.radians(nb)
        r_inf=math.tan(math.radians(dep))*lg+r
        if rm>r and dep!=0:
            l_max=(rm-r) / math.tan(math.radians(dep))
        else :
            l_max=l
            
        verts = []
        if l_max<lg and l_max>0:
            nbv=30
            for i in range(0, rng):
                # Top
                verts.append([ri*math.cos(i*ang), sup, ri*math.sin(i*ang)])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                
                verts.append([ri*math.cos((i+1)*ang), sup, ri*math.sin((i+1)*ang)])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([ri*math.cos(i*ang), sup, ri*math.sin(i*ang)])

                #Side 1a
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([rm*math.cos((i+1)*ang), -l_max, rm*math.sin((i+1)*ang)])
                
                #Side 1b
                verts.append([rm*math.cos((i+1)*ang), -l_max, rm*math.sin((i+1)*ang)])
                verts.append([rm*math.cos(i*ang), -l_max, rm*math.sin(i*ang)])
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                
                #Side 2a
                verts.append([rm*math.cos(i*ang), -l_max, rm*math.sin(i*ang)])
                verts.append([rm*math.cos((i+1)*ang), -l_max, rm*math.sin((i+1)*ang)])
                verts.append([rm*math.cos((i+1)*ang), l, rm*math.sin((i+1)*ang)])
                
                #Side 2b
                verts.append([rm*math.cos((i+1)*ang), l, rm*math.sin((i+1)*ang)])
                verts.append([rm*math.cos(i*ang), l, rm*math.sin(i*ang)])
                verts.append([rm*math.cos(i*ang), -l_max, rm*math.sin(i*ang)])
                
                #Bottom 
                verts.append([ri*math.cos(i*ang), l, ri*math.sin(i*ang)])
                verts.append([rm*math.cos(i*ang), l, rm*math.sin(i*ang)])
                verts.append([rm*math.cos((i+1)*ang), l, rm*math.sin((i+1)*ang)]) 
                
                verts.append([ri*math.cos((i+1)*ang), l, ri*math.sin((i+1)*ang)])
                verts.append([ri*math.cos(i*ang), l, ri*math.sin(i*ang)])
                verts.append([rm*math.cos((i+1)*ang), l, rm*math.sin((i+1)*ang)]) 
                
                #Side Inta
                verts.append([ri*math.cos(i*ang), sup, ri*math.sin(i*ang)])
                verts.append([ri*math.cos((i+1)*ang), l, ri*math.sin((i+1)*ang)])
                verts.append([ri*math.cos((i+1)*ang), sup, ri*math.sin((i+1)*ang)])
                
                #Side Intb
                verts.append([ri*math.cos((i+1)*ang), l, ri*math.sin((i+1)*ang)])
                verts.append([ri*math.cos(i*ang), sup, ri*math.sin(i*ang)])
                verts.append([ri*math.cos(i*ang), l, ri*math.sin(i*ang)])
                
        else:
            nbv=24
            for i in range(0, rng):
                # Top
                verts.append([ri*math.cos(i*ang), sup, ri*math.sin(i*ang)])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                
                verts.append([ri*math.cos((i+1)*ang), sup, ri*math.sin((i+1)*ang)])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([ri*math.cos(i*ang), sup, ri*math.sin(i*ang)])
                
                #Side 1a
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                verts.append([r*math.cos((i+1)*ang), sup, r*math.sin((i+1)*ang)])
                verts.append([r_inf*math.cos((i+1)*ang), l, r_inf*math.sin((i+1)*ang)])
                
                #Side 1b
                verts.append([r_inf*math.cos((i+1)*ang), l, r_inf*math.sin((i+1)*ang)])
                verts.append([r_inf*math.cos(i*ang), l, r_inf*math.sin(i*ang)])
                verts.append([r*math.cos(i*ang), sup, r*math.sin(i*ang)])
                
                #Bottom 
                verts.append([ri*math.cos(i*ang), l, ri*math.sin(i*ang)])
                verts.append([r_inf*math.cos(i*ang), l, r_inf*math.sin(i*ang)])
                verts.append([r_inf*math.cos((i+1)*ang), l, r_inf*math.sin((i+1)*ang)]) 
                
                verts.append([ri*math.cos((i+1)*ang), l, ri*math.sin((i+1)*ang)])
                verts.append([ri*math.cos(i*ang), l, ri*math.sin(i*ang)])
                verts.append([r_inf*math.cos((i+1)*ang), l, r_inf*math.sin((i+1)*ang)]) 
                
                #Side Inta
                verts.append([ri*math.cos(i*ang), sup, ri*math.sin(i*ang)])
                verts.append([ri*math.cos((i+1)*ang), l, ri*math.sin((i+1)*ang)])
                verts.append([ri*math.cos((i+1)*ang), sup, ri*math.sin((i+1)*ang)])
                
                #Side Intb
                verts.append([ri*math.cos((i+1)*ang), l, ri*math.sin((i+1)*ang)])
                verts.append([ri*math.cos(i*ang), sup, ri*math.sin(i*ang)])
                verts.append([ri*math.cos(i*ang), l, ri*math.sin(i*ang)])

        mesh.setVertices(numpy.asarray(verts, dtype=numpy.float32))

        indices = []
        # for every angle increment ( 24  or 30 ) Vertices
        tot = rng * nbv
        for i in range(0, tot, 3): # 
            indices.append([i, i+1, i+2])
        mesh.setIndices(numpy.asarray(indices, dtype=numpy.int32))

        mesh.calculateNormals()
        return mesh
        
    # Line Support Creation
    def _createLine(self, size, maxs, pos1 , pos2, dep, ztop):
        mesh = MeshBuilder()
        # Init point
        Pt1 = Vector(pos1.x,pos1.z,pos1.y)
        Pt2 = Vector(pos2.x,pos2.z,pos2.y)

        V_Dir = Pt2 - Pt1

        # Calcul vecteur
        s = size / 2
        sm = maxs / 2
        l_a = pos1.y 
        s_infa=math.tan(math.radians(dep))*l_a+s
        l_b = pos2.y 
        s_infb=math.tan(math.radians(dep))*l_b+s
 
        if sm>s and dep!=0:
            l_max_a=(sm-s) / math.tan(math.radians(dep))
            l_max_b=(sm-s) / math.tan(math.radians(dep))
        else :
            l_max_a=l_a
            l_max_b=l_b
 
        Vtop = Vector(0,0,ztop)
        VZ = Vector(0,0,s)
        VZa = Vector(0,0,-l_a)
        VZb = Vector(0,0,-l_b)
        
        Norm=Vector.cross(V_Dir,VZ).normalized()
        Dec = Vector(Norm.x*s,Norm.y*s,Norm.z*s)
            
        if l_max_a<l_a and l_max_b<l_b and l_max_a>0 and l_max_b>0: 
            nbv=40
            
            Deca = Vector(Norm.x*sm,Norm.y*sm,Norm.z*sm)
            Decb = Vector(Norm.x*sm,Norm.y*sm,Norm.z*sm)

            VZam = Vector(0,0,-l_max_a)
            VZbm = Vector(0,0,-l_max_b)
        
            # X Z Y
            P_1t = Vtop+Dec
            P_2t = Vtop-Dec
            P_3t = V_Dir+Vtop+Dec
            P_4t = V_Dir+Vtop-Dec
 
            P_1m = VZam+Deca
            P_2m = VZam-Deca
            P_3m = VZbm+V_Dir+Decb
            P_4m = VZbm+V_Dir-Decb
            
            P_1i = VZa+Deca
            P_2i = VZa-Deca
            P_3i = VZb+V_Dir+Decb
            P_4i = VZb+V_Dir-Decb
             
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
                [P_1t.x, P_1t.z, P_1t.y], [P_2t.x, P_2t.z, P_2t.y], [P_4t.x, P_4t.z, P_4t.y], [P_3t.x, P_3t.z, P_3t.y],              
                [P_1t.x, P_1t.z, P_1t.y], [P_3t.x, P_3t.z, P_3t.y], [P_3m.x, P_3m.z, P_3m.y], [P_1m.x, P_1m.z, P_1m.y],
                [P_2t.x, P_2t.z, P_2t.y], [P_1t.x, P_1t.z, P_1t.y], [P_1m.x, P_1m.z, P_1m.y], [P_2m.x, P_2m.z, P_2m.y],
                [P_3t.x, P_3t.z, P_3t.y], [P_4t.x, P_4t.z, P_4t.y], [P_4m.x, P_4m.z, P_4m.y], [P_3m.x, P_3m.z, P_3m.y],
                [P_4t.x, P_4t.z, P_4t.y], [P_2t.x, P_2t.z, P_2t.y], [P_2m.x, P_2m.z, P_2m.y], [P_4m.x, P_4m.z, P_4m.y],
                [P_1m.x, P_1m.z, P_1m.y], [P_3m.x, P_3m.z, P_3m.y], [P_3i.x, P_3i.z, P_3i.y], [P_1i.x, P_1i.z, P_1i.y],
                [P_2m.x, P_2m.z, P_2m.y], [P_1m.x, P_1m.z, P_1m.y], [P_1i.x, P_1i.z, P_1i.y], [P_2i.x, P_2i.z, P_2i.y],
                [P_3m.x, P_3m.z, P_3m.y], [P_4m.x, P_4m.z, P_4m.y], [P_4i.x, P_4i.z, P_4i.y], [P_3i.x, P_3i.z, P_3i.y],
                [P_4m.x, P_4m.z, P_4m.y], [P_2m.x, P_2m.z, P_2m.y], [P_2i.x, P_2i.z, P_2i.y], [P_4i.x, P_4i.z, P_4i.y],
                [P_1i.x, P_1i.z, P_1i.y], [P_2i.x, P_2i.z, P_2i.y], [P_4i.x, P_4i.z, P_4i.y], [P_3i.x, P_3i.z, P_3i.y]
            ]
            
        else:
            nbv=24

            Deca = Vector(Norm.x*s_infa,Norm.y*s_infa,Norm.z*s_infa)
            Decb = Vector(Norm.x*s_infb,Norm.y*s_infb,Norm.z*s_infb)

            # X Z Y
            P_1t = Vtop+Dec
            P_2t = Vtop-Dec
            P_3t = V_Dir+Vtop+Dec
            P_4t = V_Dir+Vtop-Dec
     
            P_1i = VZa+Deca
            P_2i = VZa-Deca
            P_3i = VZb+V_Dir+Decb
            P_4i = VZb+V_Dir-Decb
             
            """
            1) Top
            2) Front
            3) Left
            4) Right
            5) Back 
            6) Bottom
            """
            verts = [ # 6 faces with 4 corners each
                [P_1t.x, P_1t.z, P_1t.y], [P_2t.x, P_2t.z, P_2t.y], [P_4t.x, P_4t.z, P_4t.y], [P_3t.x, P_3t.z, P_3t.y],
                [P_1t.x, P_1t.z, P_1t.y], [P_3t.x, P_3t.z, P_3t.y], [P_3i.x, P_3i.z, P_3i.y], [P_1i.x, P_1i.z, P_1i.y],
                [P_2t.x, P_2t.z, P_2t.y], [P_1t.x, P_1t.z, P_1t.y], [P_1i.x, P_1i.z, P_1i.y], [P_2i.x, P_2i.z, P_2i.y],
                [P_3t.x, P_3t.z, P_3t.y], [P_4t.x, P_4t.z, P_4t.y], [P_4i.x, P_4i.z, P_4i.y], [P_3i.x, P_3i.z, P_3i.y],
                [P_4t.x, P_4t.z, P_4t.y], [P_2t.x, P_2t.z, P_2t.y], [P_2i.x, P_2i.z, P_2i.y], [P_4i.x, P_4i.z, P_4i.y],
                [P_1i.x, P_1i.z, P_1i.y], [P_2i.x, P_2i.z, P_2i.y], [P_4i.x, P_4i.z, P_4i.y], [P_3i.x, P_3i.z, P_3i.y]
            ]
        
        mesh.setVertices(numpy.asarray(verts, dtype=numpy.float32))

        indices = []
        for i in range(0, nbv, 4): # All 6 quads (12 triangles)
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
        
        #Logger.log('d', 's_value : ' + str(s_value))        
        self._support_size = new_value
        self._preferences.setValue("customsupportsreborn/support_size", new_value)
        log("d", f"_support_size being set to {new_value}")
        self.propertyChanged.emit()
    
    supportSize = property(getSupportSize, setSupportSize)

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
        
        #Logger.log('d', 's_value : ' + str(s_value))        
        self._support_size_max = new_value
        self._preferences.setValue("customsupportsreborn/support_size_max", new_value)
        log("d", f"_support_size_max being set to {new_value}")
        self.propertyChanged.emit()
    
    supportSizeMax = property(getSupportSizeMax, setSupportSizeMax)
        
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
        log("d", f"_support_size_inner being set to {new_value}")
        self.propertyChanged.emit()
    
    supportSizeInner = property(getSupportSizeInner, setSupportSizeInner)
        
    def getSupportAngle(self) -> float:
        return self._support_angle
  
    def setSupportAngle(self, new_angle: str) -> None:
        try:
            new_value = float(new_angle)
        except ValueError:
            return

        if new_value < 0:
            return
        
        # Logger.log('d', 's_value : ' + str(s_value))        
        self._support_angle = new_value
        self._preferences.setValue("customsupportsreborn/support_angle", new_value)
        log("d", f"_support_angle being set to {new_value}")
        self.propertyChanged.emit()

    supportAngle = property(getSupportAngle, setSupportAngle)
 
    def getPanelRemoveAllText(self) -> str:
        return self._panel_remove_all_text
    
    def setPanelRemoveAllText(self, new_text: str) -> None:
        self._panel_remove_all_text = str(new_text)
        log("d", f"_panel_remove_all_text being set to {new_text}")
        self.propertyChanged.emit()

    panelRemoveAllText = property(getPanelRemoveAllText, setPanelRemoveAllText)
        
    def getSupportType(self) -> str:
        return self._support_type
    
    def setSupportType(self, new_type: str) -> None:
        self._support_type = new_type
        log("d", f"_support_type being set to {new_type}")
        self._preferences.setValue("customsupportsreborn/support_type", new_type)
        self.propertyChanged.emit()

    supportType = property(getSupportType, setSupportType)
 
    def getSupportSubtype(self) -> str:
        # Logger.log('d', 'Set SubType : ' + str(self._SubType))  
        return self._support_subtype
    
    def setSupportSubtype(self, new_type: str) -> None:
        self._support_subtype = new_type
        # Logger.log('d', 'Get SubType : ' + str(SubType))   
        self._preferences.setValue("customsupportsreborn/support_subtype", new_type)
        log("d", f"_support_subtype being set to {new_type}")
        self.propertyChanged.emit()

    supportSubtype = property(getSupportSubtype, setSupportSubtype)
        
    def getSupportYDirection(self) -> bool:
        return self._support_y_direction
    
    def setSupportYDirection(self, YDirection: bool) -> None:
        try:
            new_value = bool(YDirection)
        except ValueError:
            return
        
        self._support_y_direction = new_value
        self._preferences.setValue("customsupportsreborn/support_y_direction", new_value)
        log("d", f"_support_y_direction being set to {new_value}")
        self.propertyChanged.emit()

    supportYDirection = property(getSupportYDirection, setSupportYDirection)
 
    def getAbutmentEqualizeHeights(self) -> bool:
        return self._abutment_equalize_heights
  
    def setAbutmentEqualizeHeights(self, equalize: bool) -> None:
        try:
            new_value = bool(equalize)
        except ValueError:
            return

        self._abutment_equalize_heights = new_value
        self._preferences.setValue("customsupportsreborn/abutment_equalize_heights", new_value)
        log("d", f"_abutment_equalize_heights being set to {new_value}")
        self.propertyChanged.emit()

    abutmentEqualizeHeights = property(getAbutmentEqualizeHeights, setAbutmentEqualizeHeights)
 
    def getModelScaleMain(self) -> bool:
        return self._model_scale_main
  
    def setModelScaleMain(self, scale: bool) -> None:
        try:
            new_value = bool(scale)
        except ValueError:
            return

        self._model_scale_main = new_value
        self._preferences.setValue("customsupportsreborn/model_scale_main", new_value)
        log("d", f"_model_scale_main being set to {new_value}")
        self.propertyChanged.emit()

    modelScaleMain = property(getModelScaleMain, setModelScaleMain)
        
    def getModelOrient(self) -> bool:
        return self._model_orient
  
    def setModelOrient(self, orient: bool) -> None:
        try:
            new_value = bool(orient)
        except ValueError:
            return

        self._model_orient = new_value
        self._preferences.setValue("customsupportsreborn/model_orient", new_value)
        log("d", f"_model_orient being set to {new_value}")
        self.propertyChanged.emit()
    
    modelOrient = property(getModelOrient, setModelOrient)
    
    def getModelMirror(self) -> bool:
        return self._model_mirror
  
    def setModelMirror(self, mirror: bool) -> None:
        try:
            new_value = bool(mirror)
        except ValueError:
            return

        self._model_mirror = new_value
        self._preferences.setValue("customsupportsreborn/model_mirror", new_value)
        log("d", f"_model_mirror being set to {new_value}")
        self.propertyChanged.emit()

    modelMirror = property(getModelMirror, setModelMirror)