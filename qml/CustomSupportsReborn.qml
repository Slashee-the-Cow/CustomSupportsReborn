//-----------------------------------------------------------------------------
// Copyright (c) 2022 5@xes
// Reborn version copyright 2025 Slashee the Cow
// 
// proterties values
//   "supportSize"               : Support Size in mm
//   "supportSizeMax"            : Support Maximum Size in mm
//   "supportSizeInner"          : Support Interior Size in mm
//   "supportAngle"              : Support Angle in °
//   "supportYDirection"         : Support Y direction (Abutment)
//   "abutmentEqualizeHeights"   : Equalize heights (Abutment)
//   "modelScaleMain"            : Scale Main direction (Model)
//   "supportType"               : Support Type ( Cylinder/Tube/Cube/Abutment/Line/Model ) 
//   "supportSubtype"            : Support model Type ( Cross/Section/Pillar/Bridge/Custom ) 
//   "modelOrient"               : Support Automatic Orientation for model Type
//   "modelMirror"               : Support Mirror for model Type
//   "panelRemoveAllText"        : Text for the Remove All Button
//-----------------------------------------------------------------------------

import QtQuick 6.0
import QtQuick.Controls 6.0

import UM 1.7 as UM
import Cura 1.0 as Cura
import CustomSupportsReborn 1.0

/*function withActiveTool(callback, defaultValue){
        if (typeof(defaultValue) === "undefined"){
            defaultValue = "";
        }
        if (UM.Controller.getActiveTool()){
            return callback(UM.Controller.getActiveTool());
        } else {
            return defaultValue;
    }*/

Item
{
    id: root

    UM.I18nCatalog {id: catalog; name: "customsupportsreborn"}

    // property var curaController: Cura.application ? Cura.application.controller : null
    /*function withActiveTool(callback, defaultValue){
        console.log("curaController is: ", curaController)
        console.log("curaController.activeTool is:", curaController.activeTool)
        if (typeof(defaultValue) === "undefined"){
            defaultValue = "";
        }
        if (curaController && curaController.activeTool){
            return callback(curaController.activeTool);
        } else {
            return defaultValue;
        }
    }*/
    


    width: childrenRect.width
    height: childrenRect.height
    
    
    property var support_size: UM.ActiveTool.properties.getValue("SupportSize")
    property int localwidth: 110

    function setSupportType(type)
    {
        // set checked state of mesh type buttons
        cylinderButton.checked = type === SupportTypes.CYLINDER
        tubeButton.checked = type === SupportTypes.TUBE
        cubeButton.checked = type === SupportTypes.CUBE
        abutmentButton.checked = type === SupportTypes.ABUTMENT
        lineButton.checked = type === SupportTypes.LINE
        modelButton.checked = type === SupportTypes.MODEL
        withActiveTool(function(tool) {tool.supportType = type})
    }
    
    Column
    {
        id: supportTypeButtons
        anchors.top: parent.top
        anchors.left: parent.left
        spacing: UM.Theme.getSize("default_margin").height

        Row // Mesh type buttons
        {
            id: supportTypeButtonsUpper
            spacing: UM.Theme.getSize("default_margin").width

            UM.ToolbarButton
            {
                id: cylinderButton
                text: catalog.i18nc("@label:shape", "Cylinder")
                toolItem: UM.ColorImage
                {
                    source: Qt.resolvedUrl("type_cylinder.svg")
                    color: "red"
                }
                property bool needBorder: true
                checkable:true
                onClicked: setSupportType(SupportTypes.CYLINDER)
                Binding{
                    target:cylinderButton
                    property: "checked"
                    value: withActiveTool(function(tool) {return tool.supportType === SupportTypes.CYLINDER})
                }
                //checked: withActiveTool(function(tool) {return tool.supportType}) === SupportTypes.CYLINDER
                z: 3 // Depth position 
            }

            UM.ToolbarButton
            {
                id: tubeButton
                text: catalog.i18nc("@label:shape", "Tube")
                toolItem: UM.ColorImage
                {
                    source: Qt.resolvedUrl("type_tube.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable:true
                onClicked: setSupportType(SupportTypes.TUBE)
                Binding{
                    target:tubeButton
                    property: "checked"
                    value: withActiveTool(function(tool) {return tool.supportType === SupportTypes.TUBE})
                }
                //checked: withActiveTool(function(tool) {return tool.supportType}) === SupportTypes.TUBE
                z: 2 // Depth position 
            }
            
            UM.ToolbarButton
            {
                id: cubeButton
                text: catalog.i18nc("@label:shape", "Cube")
                toolItem: UM.ColorImage
                {
                    source: Qt.resolvedUrl("type_cube.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable: true
                onClicked: setSupportType(SupportTypes.CUBE)
                Binding{
                    target:cubeButton
                    property: "checked"
                    value: withActiveTool(function(tool) {return tool.supportType === SupportTypes.CUBE})
                }
                //checked: withActiveTool(function(tool) {return tool.supportType}) === SupportTypes.CUBE
                z: 1 // Depth position 
            }


        }
        Row // Mesh type buttons
        {
            id: supportTypeButtonsLower
            spacing: UM.Theme.getSize("default_margin").width
            
            UM.ToolbarButton
            {
                id: abutmentButton
                text: catalog.i18nc("@label:shape", "Abutment")
                toolItem: UM.ColorImage
                {
                    source: Qt.resolvedUrl("type_abutment.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable: true
                onClicked: setSupportType(SupportTypes.ABUTMENT)
                Binding{
                    target:abutmentButton
                    property: "checked"
                    value: withActiveTool(function(tool) {return tool.supportType === SupportTypes.ABUTMENT})
                }
                //checked: withActiveTool(function(tool) {return tool.supportType}) === SupportTypes.ABUTMENT
                z: 3 // Depth position 
            }

            UM.ToolbarButton
            {
                id: lineButton
                text: catalog.i18nc("@label:shape", "Line")
                toolItem: UM.ColorImage
                {
                    source: Qt.resolvedUrl("type_line.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable:true
                onClicked: setSupportType(SupportTypes.LINE)
                Binding{
                    target:lineButton
                    property: "checked"
                    value: withActiveTool(function(tool) {return tool.supportType === SupportTypes.LINE})
                }
                //checked: withActiveTool(function(tool) {return tool.supportType}) === SupportTypes.LINE
                z: 2 // Depth position 
            }

            UM.ToolbarButton
            {
                id: modelButton
                text: catalog.i18nc("@label:shape", "Model")
                toolItem: UM.ColorImage
                {
                    source: Qt.resolvedUrl("type_model.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable:true
                onClicked: setSupportType(SupportTypes.MODEL)
                checked: UM.Controller.properties.getValue("SupportType") === SupportTypes.MODEL
                //checked: withActiveTool(function(tool) {return tool.supportType}) === SupportTypes.MODEL
                z: 1 // Depth position 
            }
        }
    }
    
    Grid
    {
        id: textfields
        anchors.leftMargin: UM.Theme.getSize("default_margin").width
        anchors.top: supportTypeButtons.bottom
        anchors.topMargin: UM.Theme.getSize("default_margin").height

        columns: 2
        flow: Grid.TopToBottom
        spacing: Math.round(UM.Theme.getSize("default_margin").width / 2)

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("panel:size", "Size")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }
 
        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("panel:max_size", "Max Size")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            visible: !modelButton.checked
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("panel:model", "Model")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            visible: modelButton.checked
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

    
        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("panel:inner-size", "Inner Size")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            visible: tubeButton.checked
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }
        
        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("panel:angle", "Angle")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            visible: !modelButton.checked
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }
        
        UM.TextFieldWithUnit
        {
            id: supportSizeTextField
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "mm"
            text: UM.Controller.properties.getValue("SupportSize")
            validator: DoubleValidator
            {
                decimals: 2
                bottom: 0.1
                locale: "en_US"
            }

            onEditingFinished:
            {
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                withActiveTool(function(tool) {tool.supportSize = modified_text})
            }
        }

        UM.TextFieldWithUnit
        {
            id: supportSizeMaxTextField
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "mm"
            visible: !modelButton.checked
            text: UM.Controller.properties.getValue("SupportSizeMax")
            validator: DoubleValidator
            {
                decimals: 2
                bottom: 0
                locale: "en_US"
            }

            onEditingFinished:
            {
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                withActiveTool(function(bool) {tool.supportSizeMax = modified_text})
            }
        }

        ComboBox {
            id: modelComboType
            objectName: "Support_Subtype"
            model: ListModel {
               id: cbItems
               ListElement { text: "cross"}
               ListElement { text: "section"}
               ListElement { text: "pillar"}
               ListElement { text: "bridge"}
               ListElement { text: "arch-buttress"}
               ListElement { text: "t-support"}
               ListElement { text: "custom"}
            }
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            visible: modelButton.checked
            Component.onCompleted: currentIndex = find(withActiveTool(function(tool) {return tool.supportSubtype}))
            
            onCurrentIndexChanged: 
            { 
                withActiveTool(function(tool) {tool.supportSubtype = cbItems.get(currentIndex).text})
            }
        }    
                
        UM.TextFieldWithUnit
        {
            id: supportSizeInnerTextField
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "mm"
            visible: tubeButton.checked
            text: UM.Controller.properties.getValue("SupportSizeInner")
            validator: DoubleValidator
            {
                decimals: 2
                top: support_size
                bottom: 0.1
                locale: "en_US"
            }

            onEditingFinished:
            {
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                withActiveTool(function(tool) {tool.supportSizeInner = modified_text})
            }
        }
        
        UM.TextFieldWithUnit
        {
            id: supportAngleTextField
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "°"
            visible: !modelButton.checked
            text: UM.Controller.properties.getValue("SupportAngle")
            validator: IntValidator
            {
                bottom: 0
            }

            onEditingFinished:
            {
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                withActiveTool(function(tool) {tool.supportAngle = modified_text})
            }
        }
    }
    
    Item
    {
        id: baseCheckBox
        width: childrenRect.width
        height: !modelButton.checked && !abutmentButton.checked && !cylinderButton.checked ?  0 : cylinderButton.checked ? UM.Theme.getSize("setting_control").height : abutmentButton.checked ? (UM.Theme.getSize("setting_control").height*2+UM.Theme.getSize("default_margin").height): childrenRect.height
        anchors.leftMargin: UM.Theme.getSize("default_margin").width
        anchors.top: textfields.bottom
        anchors.topMargin: UM.Theme.getSize("default_margin").height
        
        UM.CheckBox
        {
            id: supportYDirectionCheckbox
            anchors.top: baseCheckBox.top
            // anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: !modelOrientCheckbox.checked || abutmentButton.checked ? catalog.i18nc("panel:set_on_y", "Set on Y Direction") : catalog.i18nc("panel:set_on_main", "Set on Main Direction")
            visible: abutmentButton.checked || modelButton.checked 

            checked: withActiveTool(function(tool) {return tool.supportYDirection})
            onClicked: withActiveTool(function(tool) {tool.supportYDirection = checked})
        }
        
        UM.CheckBox
        {
            id: modelMirrorCheckbox
            anchors.top: supportYDirectionCheckbox.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: catalog.i18nc("panel:model_mirror", "Rotate 180")
            visible: modelButton.checked && !modelOrientCheckbox.checked

            checked: withActiveTool(function(tool) {return tool.modelMirror})
            onClicked: withActiveTool(function(tool) {tool.modelMirror = checked})
            
        }        
        UM.CheckBox
        {
            id: modelOrientCheckbox
            anchors.top: modelMirrorCheckbox.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: catalog.i18nc("panel:model_auto_orientate", "Auto Orientate")
            visible: modelButton.checked

            checked: withActiveTool(function(tool) {return tool.modelOrient})
            onClicked: withActiveTool(function(tool) {tool.modelOrient = checked})
            
        }    
        UM.CheckBox
        {
            id: modelScaleMainCheckbox
            anchors.top: modelOrientCheckbox.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: catalog.i18nc("panel:model_scale_main", "Scale Main Direction")
            visible: modelButton.checked

            checked: withActiveTool(function(tool) {return tool.modelScaleMain})
            onClicked: withActiveTool(function(tool) {tool.modelScaleMain = checked})
        }    
        UM.CheckBox
        {
            id: abutmentEqualizeHeightsCheckbox
            anchors.top: supportYDirectionCheckbox.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: catalog.i18nc("panel:abutment_equalize_heights", "Equalize Heights")
            visible: abutmentButton.checked

            checked: withActiveTool(function(tool) {return abutmentEqualizeHeights})
            onClicked: withActiveTool(function(tool) {abutmentEqualizeHeights = checked})
        }
        

    }

    Rectangle {
        id: rightRect
        anchors.top: baseCheckBox.bottom
        //color: UM.Theme.getColor("toolbar_background")
        color: "#00000000"
        width: UM.Theme.getSize("setting_control").width * 1.3
        height: UM.Theme.getSize("setting_control").height 
        anchors.left: parent.left
        anchors.topMargin: UM.Theme.getSize("default_margin").height
    }
    
    Cura.SecondaryButton
    {
        id: removeAllButton
        anchors.centerIn: rightRect
        spacing: UM.Theme.getSize("default_margin").height
        width: UM.Theme.getSize("setting_control").width
        height: UM.Theme.getSize("setting_control").height        
        text: catalog.i18nc("panel:remove_all", "Remove All")
        onClicked: withActiveTool(function(tool) {tool.removeAllSupportMesh()})
    }
}
