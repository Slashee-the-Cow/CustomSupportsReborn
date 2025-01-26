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

Item
{
    id: root

    readonly property string supportTypeCylinder: "cylinder"
    readonly property string supportTypeTube: "tube"
    readonly property string supportTypeCube: "cube"
    readonly property string supportTypeAbutment: "abutment"
    readonly property string supportTypeLine: "line"
    readonly property string supportTypeModel: "model"

    UM.I18nCatalog {id: catalog; name: "customsupportsreborn"}

    width: childrenRect.width
    height: childrenRect.height

    property real supportSizeValue: 0
    property real supportSizeMaxValue: 0
    property real supportSizeInnerValue: 0
    property real supportAngleValue: 0

    Component.onCompleted: {
        // Pretty sure the buttons need their checked values done too. Can't hurt anyway. I hope.
        cylinderButton.checked = UM.Controller.properties.getValue("SupportType") === supportTypeCylinder
        tubeButton.checked = UM.Controller.properties.getValue("SupportType") === supportTypeTube
        cubeButton.checked = UM.Controller.properties.getValue("SupportType") === supportTypeCube
        abutmentButton.checked = UM.Controller.properties.getValue("SupportType") === supportTypeAbutment
        lineButton.checked = UM.Controller.properties.getValue("SupportType") === supportTypeLine
        modelButton.checked = UM.Controller.properties.getValue("SupportType") === supportTypeModel

        supportSizeMaxValue = UM.Controller.properties.getValue("SupportSizeMax")
        supportSizeValue = UM.Controller.properties.getValue("SupportSize")
        supportSizeTextField.validator.top = supportSizeMaxValue
        supportSizeInnerValue = UM.Controller.properties.getValue("SupportSizeInner")
        supportSizeInnerTextField.validator.top = supportSizeValue - 0.01
        supportAngleValue = UM.Controller.properties.getValue("SupportAngle")

        supportYDirectionCheckbox.checked = UM.Controller.properties.getValue("SupportYDirection")
        modelMirrorCheckbox.checked = UM.Controller.properties.getValue("ModelMirror")
        modelOrientCheckbox.checked = UM.Controller.properties.getValue("ModelOrient")
        modelScaleMainCheckbox.checked = UM.Controller.properties.getValue("ModelScaleMain")
        abutmentEqualizeHeightsCheckbox.checked = UM.Controller.properties.getValue("AbutmentEqualizeHeights")
    }
    
    
    //property var support_size: UM.Controller.properties.getValue("SupportSize")
    property int localwidth: 110

    function setSupportType(type)
    {
        // set checked state of mesh type buttons
        cylinderButton.checked = type === supportTypeCylinder
        tubeButton.checked = type === supportTypeTube
        cubeButton.checked = type === supportTypeCube
        abutmentButton.checked = type === supportTypeAbutment
        lineButton.checked = type === supportTypeLine
        modelButton.checked = type === supportTypeModel
        UM.Controller.setProperty("SupportType", type)
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
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable:true
                onClicked: setSupportType(supportTypeCylinder)
                //checked: UM.Controller.properties.getValue("SupportType") === supportTypeCylinder
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
                onClicked: setSupportType(supportTypeTube)
                //checked: UM.Controller.properties.getValue("SupportType") === supportTypeTube
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
                onClicked: setSupportType(supportTypeCube)
                //checked: UM.Controller.properties.getValue("SupportType") === supportTypeCube
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
                onClicked: setSupportType(supportTypeAbutment)
                //checked: UM.Controller.properties.getValue("SupportType") === supportTypeAbutment
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
                onClicked: setSupportType(supportTypeLine)
                //checked: UM.Controller.properties.getValue("SupportType") === supportTypeLine
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
                onClicked: setSupportType(supportTypeModel)
                //checked: UM.Controller.properties.getValue("SupportType") === supportTypeModel
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
            property string displaySupportSize: "0"
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "mm"
            text: displaySupportSize
            Connections{
                target: root
                function onSupportSizeMaxValueChanged() {
                    supportSizeTextField.validator.top = root.supportSizeMaxValue;
                    if(root.supportSizeValue > root.supportSizeMaxValue){
                        root.supportSizeValue = root.supportSizeMaxValue;
                        supportSizeTextField.displaySupportSize = root.supportSizeValue.toString();
                        UM.Controller.setProperty("SupportSize", root.supportSizeValue)
                    }
                }
            }
            Component.onCompleted: {
                displaySupportSize = root.supportSizeValue.toString()
            }

            validator: DoubleValidator
            {
                decimals: 2
                bottom: 0.1
                locale: "en_US"
                notation: DoubleValidator.StandardNotation
            }

            onFocusChanged:
            {
                if(focus){
                    return;
                }
                var modified_text = supportSizeTextField.text.replace(",", ".") // User convenience. We use dots for decimal values
                if(modified_text === ""){
                    displaySupportSize = ""
                    displaySupportSize = root.supportSizeValue.toString();
                } else {
                    var text_as_num = parseFloat(modified_text)
                    if (isNaN(text_as_num)){
                        displaySupportSize = ""
                        displaySupportSize = root.supportSizeValue.toString()
                        return
                    } else if(text_as_num == 0){
                        displaySupportSize = ""
                        displaySupportSize = root.supportSizeValue.toString()
                        return
                    } else if(text_as_num > root.supportSizeMaxValue) {
                        displaySupportSize = ""
                        displaySupportSize = root.supportSizeMaxValue.toString()
                        text_as_num = root.supportSizeMaxValue
                    } else {
                        root.supportSizeValue = text_as_num;
                        UM.Controller.setProperty("SupportSize", text_as_num);
                        displaySupportSize = text_as_num.toString();
                    }
                }
            }
        }

        UM.TextFieldWithUnit
        {
            id: supportSizeMaxTextField
            property string displaySupportSizeMax: "0"
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "mm"
            visible: !modelButton.checked
            text: displaySupportSizeMax
            Component.onCompleted: {
                displaySupportSizeMax = root.supportSizeMaxValue.toString()
            }

            validator: DoubleValidator
            {
                decimals: 2
                bottom: 0.01
                locale: "en_US"
                notation: DoubleValidator.StandardNotation
            }

            onFocusChanged:
            {
                if(focus){
                    return;
                }
                console.log("supportSizeMaxTextField onEditingFinish")
                var modified_text = supportSizeMaxTextField.text.replace(",", ".") // User convenience. We use dots for decimal values
                if (modified_text === ""){
                    displaySupportSizeMax = ""
                    displaySupportSizeMax = root.supportSizeMaxValue.toString();
                    return
                } else {}
                    var text_as_num = parseFloat(modified_text)
                    if (isNaN(text_as_num)){
                        displaySupportSizeMax = ""
                        displaySupportSizeMax = root.supportSizeMaxValue.toString();
                        return
                    } else if(text_as_num == 0) {
                        displaySupportSizeMax = ""
                        displaySupportSizeMax = root.supportSizeMaxValue.toString()
                        return
                    } {
                        root.supportSizeMaxValue = text_as_num
                        UM.Controller.setProperty("SupportSizeMax", text_as_num)
                        displaySupportSizeMax = text_as_num.toString()
                    }
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
            Component.onCompleted: currentIndex = find(UM.Controller.properties.getValue("SupportSubtype"))
            
            onCurrentIndexChanged: 
            { 
                UM.Controller.setProperty("SupportSubtype", cbItems.get(currentIndex).text)
            }
        }    
                
        UM.TextFieldWithUnit
        {
            id: supportSizeInnerTextField
            property string displaySupportSizeInner: "0"
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "mm"
            visible: tubeButton.checked
            text: displaySupportSizeInner
            
            Connections{
                target: root
                function onSupportSizeValueChanged() {
                    supportSizeInnerTextField.validator.top = root.supportSizeValue - 0.01
                    if(root.supportSizeInnerValue >= root.supportSizeValue){
                        root.supportSizeInnerValue = root.supportSizeValue - 0.01;
                        supportSizeInnerTextField.displaySupportSizeInner = root.supportSizeInnerValue.toString();
                        UM.Controller.setProperty("SupportSizeInner", root.supportSizeInnerValue)
                    }
                }
            }

            Component.onCompleted: {
                displaySupportSizeInner = root.supportSizeInnerValue.toString()
            }
            validator: DoubleValidator
            {
                decimals: 2
                top: 10
                bottom: 0.1
                locale: "en_US"
                notation: DoubleValidator.StandardNotation
            }

            onFocusChanged:
            {
                if(focus){
                    return;
                }
                var modified_text = supportSizeInnerTextField.text.replace(",", ".") // User convenience. We use dots for decimal values
                if(modified_text === ""){
                    displaySupportSizeInner = ""
                    displaySupportSizeInner = root.supportSizeInnerValue.toString()
                    return
                } else {
                    var text_as_num = parseFloat(modified_text)
                    if(isNaN(text_as_num)){
                        displaySupportSizeInner = ""
                        displaySupportSize = root.supportSizeInnerValue.toString()
                        return
                    } else {
                        if(text_as_num == 0){
                            displaySupportSizeInner = ""
                            displaySupportSizeInner = root.supportSizeInnerValue.toString()
                            return
                        } else if(text_as_num > root.supportSizeValue - 0.01){
                            displaySupportSizeInner = ""
                            text_as_num = root.supportSizeValue - 0.01
                        }
                        root.supportSizeInnerValue = text_as_num
                        UM.Controller.setProperty("SupportSizeInner", text_as_num)
                        displaySupportSizeInner = text_as_num.toString()
                    }
                }
            }
        }
        
        UM.TextFieldWithUnit
        {
            id: supportAngleTextField
            property string displaySupportAngle: "0"

            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "°"
            visible: !modelButton.checked
            text: displaySupportAngle

            Component.onCompleted:{
                displaySupportAngle = root.supportAngleValue.toString()
            }

            validator: IntValidator
            {
                bottom: 0
                top: 89
            }

            onFocusChanged:
            {
                if(focus){
                    return;
                }
                var modified_text = supportAngleTextField.text.replace(",", ".") // User convenience. We use dots for decimal values
                if (modified_text === ""){
                    displaySupportAngle = ""
                    displaySupportAngle = root.supportAngleValue.toString()
                } else {
                    var text_as_num = parseFloat(modified_text)
                    if(isNaN(text_as_num)){
                        displaySupportAngle = ""
                        displaySupportAngle = root.supportAngleValue.toString()
                    } else {
                        root.supportAngleValue = text_as_num
                        UM.Controller.setProperty("SupportAngle", text_as_num)
                        displaySupportAngle = text_as_num.toString()
                    }
                }
            }
        }
    }
    
    Item
    {
        id: baseCheckBox
        width: childrenRect.width
        height: !modelButton.checked && !abutmentButton.checked ? 0 : abutmentButton.checked ? (UM.Theme.getSize("setting_control").height*2+UM.Theme.getSize("default_margin").height): childrenRect.height
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

            //checked: withActiveTool(function(tool) {return tool.supportYDirection})
            onClicked: UM.Controller.setProperty("SupportYDirection", checked)
        }
        
        UM.CheckBox
        {
            id: modelMirrorCheckbox
            anchors.top: supportYDirectionCheckbox.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: catalog.i18nc("panel:model_mirror", "Rotate 180°")
            visible: modelButton.checked && !modelOrientCheckbox.checked

            //checked: withActiveTool(function(tool) {return tool.modelMirror})
            onClicked: UM.Controller.setProperty("ModelMirror", checked)
            
        }        
        UM.CheckBox
        {
            id: modelOrientCheckbox
            anchors.top: modelMirrorCheckbox.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: catalog.i18nc("panel:model_auto_orientate", "Auto Orientate")
            visible: modelButton.checked

            //checked: withActiveTool(function(tool) {return tool.modelOrient})
            onClicked: UM.Controller.setProperty("ModelOrient", checked)
            
        }    
        UM.CheckBox
        {
            id: modelScaleMainCheckbox
            anchors.top: modelOrientCheckbox.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: catalog.i18nc("panel:model_scale_main", "Scale Main Direction")
            visible: modelButton.checked

            //checked: withActiveTool(function(tool) {return tool.modelScaleMain})
            onClicked: UM.Controller.setProperty("ModelScaleMain", checked)
        }    
        UM.CheckBox
        {
            id: abutmentEqualizeHeightsCheckbox
            anchors.top: supportYDirectionCheckbox.bottom
            anchors.topMargin: UM.Theme.getSize("default_margin").height
            anchors.left: parent.left
            text: catalog.i18nc("panel:abutment_equalize_heights", "Equalize Heights")
            visible: abutmentButton.checked

            //checked: withActiveTool(function(tool) {return abutmentEqualizeHeights})
            onClicked: UM.Controller.setProperty("AbutmentEqualizeHeights", checked)
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
        onClicked: UM.Controller.triggerAction("removeAllSupportMesh")
    }
}
