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

import UM 1.6 as UM
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
    property int supportSubtypeIndex: 0

    function compareVersions(version1, version2) {
        const v1 = String(version1).split(".");
        const v2 = String(version2).split(".");

        for (let i = 0; i < Math.max(v1.length, v2.length); i++) {
            const num1 = parseInt(v1[i] || 0); // Handle missing components
            const num2 = parseInt(v2[i] || 0);

            if (num1 < num2) return -1;
            if (num1 > num2) return 1;
        }
        return 0; // Versions are equal
    }

    function isVersion57OrGreater(){
        let version = CuraApplication ? CuraApplication.version : (UM.Application ? UM.Application.version : null);
        if(version){
            return compareVersions(CuraApplication.version || (UM.Application && UM.Application.version), "5.7.0") >= 0;
        } else {
            return False
        }
        
    }
    

    function getProperty(propertyName){
        if(isVersion57OrGreater()){
            return UM.Controller.properties.getValue(propertyName);
        } else {
            return UM.ActiveTool.properties.getValue(propertyName);
        }
    }

    function setProperty(propertyName, value){
        if(isVersion57OrGreater()){
            return UM.Controller.setProperty(propertyName, value);
        } else {
            return UM.ActiveTool.setProperty(propertyName, value);
        }
    }

    function triggerAction(action){
        if(isVersion57OrGreater()){
            return UM.Controller.triggerAction(action)
        } else {
            return UM.ActiveTool.triggerAction(action)
        }
    }

    Component.onCompleted: {
        // Pretty sure the buttons need their checked values done too. Can't hurt anyway. I hope.
        cylinderButton.checked = getProperty("SupportType") === supportTypeCylinder
        tubeButton.checked = getProperty("SupportType") === supportTypeTube
        cubeButton.checked = getProperty("SupportType") === supportTypeCube
        abutmentButton.checked = getProperty("SupportType") === supportTypeAbutment
        lineButton.checked = getProperty("SupportType") === supportTypeLine
        modelButton.checked = getProperty("SupportType") === supportTypeModel

        supportSizeMaxValue = getProperty("SupportSizeMax")
        supportSizeValue = getProperty("SupportSize")
        //supportSizeTextField.validator.top = supportSizeMaxValue
        supportSizeInnerValue = getProperty("SupportSizeInner")
        supportSizeInnerTextField.validator.top = supportSizeValue - 0.01
        supportAngleValue = getProperty("SupportAngle")
        supportSubtypeIndex = getProperty("SupportSubtypeIndex")


        supportYDirectionCheckbox.checked = getProperty("SupportYDirection")
        modelMirrorCheckbox.checked = getProperty("ModelMirror")
        modelOrientCheckbox.checked = getProperty("ModelOrient")
        modelScaleMainCheckbox.checked = getProperty("ModelScaleMain")
        abutmentEqualizeHeightsCheckbox.checked = getProperty("AbutmentEqualizeHeights")
    }
    
    
    //property var support_size: getProperty("SupportSize")
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
        setProperty("SupportType", type)
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
                //checked: getProperty("SupportType") === supportTypeCylinder
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
                //checked: getProperty("SupportType") === supportTypeTube
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
                //checked: getProperty("SupportType") === supportTypeCube
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
                //checked: getProperty("SupportType") === supportTypeAbutment
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
                //checked: getProperty("SupportType") === supportTypeLine
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
                //checked: getProperty("SupportType") === supportTypeModel
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
                    //supportSizeTextField.validator.top = root.supportSizeMaxValue;
                    if(root.supportSizeValue > root.supportSizeMaxValue){
                        root.supportSizeValue = root.supportSizeMaxValue;
                        supportSizeTextField.displaySupportSize = root.supportSizeValue.toString();
                        setProperty("SupportSize", root.supportSizeValue)
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
                        root.supportSizeMaxValue = text_as_num;
                        supportSizeMaxTextField.displaySupportSizeMax = root.supportSizeMaxValue.toString();
                        setProperty("SupportSizeMax", root.supportSizeMaxValue)
                    } else {
                        root.supportSizeValue = text_as_num;
                        setProperty("SupportSize", text_as_num);
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
                        setProperty("SupportSizeMax", text_as_num)
                        displaySupportSizeMax = text_as_num.toString()
                    }
            }
        }

        ComboBox {
            id: modelSubtype
            property int currentIndexDisplay: 0
            model: ListModel {
               id: subtypeItems
               ListElement { text: "cross"}
               ListElement { text: "section"}
               ListElement { text: "pillar"}
               ListElement { text: "bridge"}
               ListElement { text: "arch-buttress"}
               ListElement { text: "t-support"}
               ListElement { text: "custom"}
            }
            currentIndex: currentIndexDisplay
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            visible: modelButton.checked
            Component.onCompleted: {
                modelSubtype.currentIndexDisplay = root.supportSubtypeIndex;
                modelSubtype.update()
            }
            
            onCurrentIndexChanged: 
            { 
                root.supportSubtypeIndex = modelSubtype.currentIndex
                modelSubtype.currentIndexDisplay = modelSubtype.currentIndex
                setProperty("SupportSubtype", subtypeItems.get(currentIndex).text)
                setProperty("SupportSubtypeIndex", modelSubtype.currentIndex)
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
                        setProperty("SupportSizeInner", root.supportSizeInnerValue)
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
                        setProperty("SupportSizeInner", text_as_num)
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
                        setProperty("SupportAngle", text_as_num)
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
            onClicked: setProperty("SupportYDirection", checked)
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
            onClicked: setProperty("ModelMirror", checked)
            
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
            onClicked: setProperty("ModelOrient", checked)
            
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
            onClicked: setProperty("ModelScaleMain", checked)
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
            onClicked: setProperty("AbutmentEqualizeHeights", checked)
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
        onClicked: triggerAction("removeAllSupportMesh")
    }
}
