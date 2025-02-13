//-----------------------------------------------------------------------------
// Copyright (c) 2022 5@xes
// Reborn version copyright 2025 Slashee the Cow
// 
// proterties values
//   "supportSize"               : Support size in mm
//   "supportSizeTapered"        : Tapered support size in mm
//   "wallWidth"                 : Tube wall width in mm
//   "taperAngle"                : Taoer angle in °
//   "supportYDirection"         : Support Y direction (Abutment)
//   "abutmentEqualizeHeights"   : Equalize heights (Abutment)
//   "modelScaleMain"            : Scale Main direction (Model)
//   "supportType"               : Support Type ( Cylinder/Tube/Cube/Abutment/Line/Model ) 
//   "modelSubtype"              : Support model Type ( Cross/Section/Pillar/Bridge/Custom ) 
//   "modelOrient"               : Support Automatic Orientation for model Type
//   "modelMirror"               : Support Mirror for model Type
//   "panelRemoveAllText"        : Text for the Remove All Button
//-----------------------------------------------------------------------------

import QtQuick 6.0
import QtQuick.Controls 6.0
import QtQuick.Layouts 6.0

import UM 1.6 as UM
import Cura 1.1 as Cura

import ".."

Item
{
    id: root

    readonly property string supportTypeCylinder: "cylinder"
    readonly property string supportTypeTube: "tube"
    readonly property string supportTypeCube: "cube"
    readonly property string supportTypeAbutment: "abutment"
    readonly property string supportTypeLine: "line"
    readonly property string supportTypeModel: "model"

    readonly property string iconWarning: "icon_warning.svg"
    readonly property string iconInfo: "icon_info.svg"
    readonly property string iconBlank: ""

    UM.I18nCatalog {id: catalog; name: "customsupportsreborn"}

    width: childrenRect.width
    height: childrenRect.height

    property real supportSizeValue: 0
    property real supportSizeTaperedValue: 0
    property real wallWidthValue: 0
    property real taperAngleValue: 0

    property string supportSizeIconToolTipText: ""
    property string supportSizeIconImage: ""

    property string supportSizeTaperedIconToolTipText: ""
    property string supportSizeTaperedIconImage: ""

    property string wallWidthIconToolTipText: ""
    property string wallWidthIconImage: ""

    property string taperAngleIconToolTipText: ""
    property string taperAngleIconImage: ""

    property string modelSubtypeIconToolTipText: ""
    property string modelSubtypeIconImage: ""

    function getCuraVersion(){
        if(CuraApplication.version){
            return CuraApplication.version()
        } else {
            return UM.Application.version
        }
    }

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
        //let version = CuraApplication ? CuraApplication.version() : (UM.Application ? UM.Application.version : null);
        let version = getCuraVersion()
        if(version){
            return compareVersions(version, "5.7.0") >= 0;
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


    function updateUI(){
        // Pretty sure the buttons need their checked values done too. Can't hurt anyway. I hope.

        cylinderButton.checked = getProperty("SupportType") === supportTypeCylinder
        tubeButton.checked = getProperty("SupportType") === supportTypeTube
        cubeButton.checked = getProperty("SupportType") === supportTypeCube
        abutmentButton.checked = getProperty("SupportType") === supportTypeAbutment
        lineButton.checked = getProperty("SupportType") === supportTypeLine
        modelButton.checked = getProperty("SupportType") === supportTypeModel

        supportSizeValue = getProperty("SupportSize")
        supportSizeTaperedValue = getProperty("SupportSizeTapered")
        wallWidthValue = getProperty("WallWidth")
        taperAngleValue = getProperty("TaperAngle")

        supportYDirectionCheckbox.checked = getProperty("SupportYDirection")
        modelMirrorCheckbox.checked = getProperty("ModelMirror")
        modelOrientCheckbox.checked = getProperty("ModelOrient")
        modelScaleMainCheckbox.checked = getProperty("ModelScaleMain")
        abutmentEqualizeHeightsCheckbox.checked = getProperty("AbutmentEqualizeHeights")
        modelSubtype.currentIndex = modelSubtype.find(getProperty("ModelSubtype"))
    }
    
    Component.onCompleted: {    
        updateUI();
        //supportSizeIconImage = "icon_warning.svg"
        //supportSizeIconTooltipText = "WARNING: This is a test."
        //supportSizeIcon.visible = false
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

    //property int labelWidth: 60
    property int labelWidth = Math.max(supportSizeLabel.contentWidth, wallWidthLabel.contentWidth, taperAngleLabel.contentWidth, modelSubtypeLabel.contentWidth, supportSizeTaperedLabel.contentWidth)
    property int textFieldWidth: 110
    property int textFieldHeight: UM.Theme.getSize("setting_control").height
    property int iconWidth: UM.Theme.getSize("setting_control").height
    property int iconHeight: UM.Theme.getSize("setting_control").height
    ColumnLayout {
        id: inputTextFields
        anchors.top: supportTypeButtons.bottom
        spacing: UM.Theme.getSize("default_margin").height / 2
        RowLayout {
            id: supportSizeRow
            spacing: UM.Theme.getSize("default_margin").width
            
            UM.Label {
                id: supportSizeLabel
                text: catalog.i18nc("panel:size", "Size")
                Layout.preferredWidth: labelWidth
            }

            UM.TextFieldWithUnit {
                id: supportSizeTextField
                property string displaySupportSize: "0"
                Layout.preferredWidth: textFieldWidth
                height: textFieldHeight
                unit: "mm"
                text: displaySupportSize
                Connections{
                    target: root
                    function onSupportSizeTaperedValueChanged() {
                        //supportSizeTextField.validator.top = root.supportSizeTaperedValue;
                        /*if(root.supportSizeValue > root.supportSizeTaperedValue){
                            root.supportSizeValue = root.supportSizeTaperedValue;
                            supportSizeTextField.displaySupportSize = root.supportSizeValue.toString();
                            setProperty("SupportSize", root.supportSizeValue)
                        }*/
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
                        } else {
                            root.supportSizeValue = text_as_num;
                            setProperty("SupportSize", text_as_num);
                            displaySupportSize = text_as_num.toString();
                        }
                    }
                }
            }

            IconToolTip {
                id: supportSizeIconToolTip
                imageSource: supportSizeIconImage
                toolTipText: supportSizeIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
            }
        }
        RowLayout {
            spacing: UM.Theme.getSize("default_margin").width
            id: wallWidthRow
            visible: tubeButton.checked

            UM.Label {
                id: wallWidthLabel
                text: catalog.i18nc("panel:wall-width", "Wall Width")
                Layout.preferredWidth: labelWidth
            }

            UM.TextFieldWithUnit {
                id: wallWidthTextField
                property string displayWallWidth: "0"
                Layout.preferredWidth: textFieldWidth
                height: textFieldHeight
                unit: "mm"
                text: displayWallWidth
                
                Connections{
                    target: root
                    function onSupportSizeValueChanged() {
                        wallWidthTextField.validator.top = root.supportSizeValue / 2 - 0.01
                        if(root.wallWidthValue >= root.supportSizeValue / 2){
                            root.wallWidthValue = root.supportSizeValue / 2 - 0.01;
                            wallWidthTextField.displayWallWidth = root.wallWidthValue.toString();
                            setProperty("WallWidth", root.wallWidthValue)
                        }
                    }
                }

                Component.onCompleted: {
                    displayWallWidth = root.wallWidthValue.toString()
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
                    var modified_text = wallWidthTextField.text.replace(",", ".") // User convenience. We use dots for decimal values
                    if(modified_text === ""){
                        displayWallWidth = ""
                        displayWallWidth = root.wallWidthValue.toString()
                        return
                    } else {
                        var text_as_num = parseFloat(modified_text)
                        if(isNaN(text_as_num)){
                            displayWallWidth = ""
                            displayWallWidth = root.wallWidthValue.toString()
                            return
                        } else {
                            if(text_as_num == 0){
                                displayWallWidth = ""
                                displayWallWidth = root.wallWidthValue.toString()
                                return
                            } else if(text_as_num > root.supportSizeValue - 0.01){
                                displayWallWidth = ""
                                text_as_num = root.supportSizeValue - 0.01
                            }
                            root.wallWidthValue = text_as_num
                            setProperty("WallWidth", text_as_num)
                            displayWallWidth = text_as_num.toString()
                        }
                    }
                }
            }

            IconToolTip {
                id: wallWidthIconToolTip
                imageSource: wallWidthIconImage
                toolTipText: wallWidthIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
            }
        }

        RowLayout {
            spacing: UM.Theme.getSize("default_margin").width
            id: taperAngleRow
            visible: !modelButton.checked
            
            UM.Label {
                id: taperAngleLabel
                text: catalog.i18nc("panel:angle", "Taper Angle")
                Layout.preferredWidth: labelWidth
            }

            UM.TextFieldWithUnit {
                id: taperAngleTextField
                property string displayTaperAngle: "0"

                Layout.preferredWidth: textFieldWidth
                height: textFieldHeight
                unit: "°"
                text: displayTaperAngle

                Component.onCompleted:{
                    displayTaperAngle = root.taperAngleValue.toString()
                }

                validator: IntValidator
                {
                    bottom: -89
                    top: 89
                }

                onFocusChanged:
                {
                    if(focus){
                        return;
                    }
                    var modified_text = taperAngleTextField.text.replace(",", ".") // User convenience. We use dots for decimal values
                    if (modified_text === ""){
                        displayTaperAngle = ""
                        displayTaperAngle = root.taperAngleValue.toString()
                    } else {
                        var text_as_num = parseFloat(modified_text)
                        if(isNaN(text_as_num)){
                            displayTaperAngle = ""
                            displayTaperAngle = root.taperAngleValue.toString()
                        } else {
                            root.taperAngleValue = text_as_num
                            setProperty("TaperAngle", text_as_num)
                            displayTaperAngle = text_as_num.toString()
                       }
                   }
                }
            }
            IconToolTip {
                id: taperAngleIconToolTip
                imageSource: taperAngleIconImage
                toolTipText: taperAngleIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
            }
        }

        RowLayout {
            id modelSubtypeRow
            spacing: UM.Theme.getSize("default_margin").width
            visible: modelButton.checked
            UM.Label {
                id: modelSubtypeLabel
                text: catalog.i18nc("panel:model", "Model")
                Layout.preferredWidth: labelWidth
            }
            ComboBox {
            id: modelSubtype
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
                Layout.preferredWidth: localwidth
                height: UM.Theme.getSize("setting_control").height
                Component.onCompleted: {
                }
                
                onActivated: {
                    setProperty("ModelSubtype", subtypeItems.get(currentIndex).text);
                }
            }
        }

        IconToolTip {
            id: modelSubtypeIconToolTip
            imageSource: modelSubtypeIconImage
            toolTipText: modelSubtypeIconToolTipText
            Layout.preferredWidth: iconWidth
            Layout.preferredHeight: iconHeight
        }

        RowLayout {
            id: supportSizeTaperedSizeRow
            spacing: UM.Theme.getSize("default_margin").width
            visible: taperAngleValue != 0
            UM.Label {
                id: supportSizeTaperedSizeLabel
                text: catalog.i18nc("panel:tapered_size", "Tapered Size ")
                Layout.preferredWidth: labelWidth
            }
            UM.TextFieldWithUnit {
                id: supportSizeTaperedTextField
                property string displaySupportSizeTapered: "0"
                Layout.preferredWidth: textFieldWidth
                height: textFieldHeight
                unit: "mm"
                text: displaySupportSizeTapered

                Component.onCompleted: {
                    displaySupportSizeTapered = root.supportSizeTaperedValue.toString()
                }

                validator: DoubleValidator {
                    decimals: 2
                    bottom: 0.01
                    locale: "en_US"
                    notation: DoubleValidator.StandardNotation
                }

                onFocusChanged: {
                    if(focus){
                        return;
                    }
                    console.log("supportSizeTaperedTextField onEditingFinish")
                    var modified_text = supportSizeTaperedTextField.text.replace(",", ".") // User convenience. We use dots for decimal values
                    if (modified_text === ""){
                        displaySupportSizeTapered = ""
                        displaySupportSizeTapered = root.supportSizeTaperedValue.toString();
                        return
                    } else {
                        var text_as_num = parseFloat(modified_text)
                        if (isNaN(text_as_num)){
                            displaySupportSizeTapered = ""
                            displaySupportSizeTapered = root.supportSizeTaperedValue.toString();
                            return
                        } else if(text_as_num == 0) {
                            displaySupportSizeTapered = ""
                            displaySupportSizeTapered = root.supportSizeTaperedValue.toString()
                            return
                        } {
                            root.supportSizeTaperedValue = text_as_num
                            setProperty("SupportSizeTapered", text_as_num)
                            displaySupportSizeTapered = text_as_num.toString()
                        }
                    }
                }
            }
            IconToolTip{
                id: supportSizeTaperedIconToolTip
                imageSource: supportSizeTaperedIconImage
                toolTipText: supportSizeTaperedIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
            }
        }
    }

    function validateInputs(){
        let support_size = root.supportSizeValue
        let taper_angle = root.taperAngleValue
        let support_size_tapered = root.supportSizeTaperedValue

        let returnValid = true

        let minimum_distance = 0.01

        if (taper_angle < 0){
            SupportSizeTaperedTextField.validator.top = supportSizeValue - minimum_distance
            SupportSizeTaperedTextField.validator.bottom = Infinity
            if (!supportSizeTaperedTextField.acceptableInput){
                supportSizeTaperedIconImage = iconWarning
                supportSizeTaperedIconToolTipText = catalog.i18nc("panel_warning_over_min", "Tapered size must be under support size with negative taper.")
            } else {
                supportSizeTaperedIconImage = iconBlank
                supportSizeTaperedIconToolTipText = ""
            }
        } elif (taper_angle > 0){
            supportSizeTaperedTextField.validator.top = Infinity
            SupportSizeTaperedTextField.validator.bottom = supportSizeValue + minimum_distance
            if (!supportSizeTaperedTextField.acceptableInput){
                supportSizeTaperedIconImage = iconWarning
                supportSizeTaperedIconToolTipText = catalog.i18nc("panel_warning_over_min", "Tapered size must be higher than support size with positive taper.")
            } else {
                supportSizeTaperedIconImage = iconBlank
                supportSizeTaperedIconToolTipText = ""
            }
        } else {
            supportSizeTaperedIconImage = iconBlank
            supportSizeTaperedIconToolTipText = ""
        }
    }

    /*function showErrorToolTip(textField, icon, message) {
        // Find the corresponding IconToolTip (you'll need to adjust this based on how you associate tooltips with fields)
        let toolTip = findToolTipForField(textField); // Implement this function
        if (toolTip) {
            toolTip.text = message;
            toolTip.visible = true;
        }
    }

    function hideErrorToolTip(textField) {
        let toolTip = findToolTipForField(textField);
        if (toolTip) {
            toolTip.visible = false;
            toolTip.text = "";
        }
    }

    function findToolTipForField(textField) {
        //Find the IconToolTip associated with the given TextField
        return textField.parent.children.find(child => child instanceof IconToolTip);
    }*/

    /*Grid
    {
        id: textfields
        anchors.leftMargin: UM.Theme.getSize("default_margin").width
        anchors.top: inputTextFields.bottom
        anchors.topMargin: UM.Theme.getSize("default_margin").height

        columns: 2
        flow: Grid.LeftToRight
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
 
        UM.TextFieldWithUnit
        {
            id: supportSizeTextFieldGrid
            property string displaySupportSize: "0"
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "mm"
            text: displaySupportSize
            Connections{
                target: root
                function onSupportSizeMaxValueChanged() {
                    //supportSizeTextField.validator.top = root.supportSizeMaxValue;
                    /*if(root.supportSizeValue > root.supportSizeMaxValue){
                        root.supportSizeValue = root.supportSizeMaxValue;
                        supportSizeTextField.displaySupportSize = root.supportSizeValue.toString();
                        setProperty("SupportSize", root.supportSizeValue)
                    }*/
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
                    } else {
                        root.supportSizeValue = text_as_num;
                        setProperty("SupportSize", text_as_num);
                        displaySupportSize = text_as_num.toString();
                    }
                }
            }
        }
        Item {
            IconToolTip {
                id: supportSizeIconToolTipGrid
                imageSource: supportSizeIconImage
                toolTipText: supportSizeIconToolTipText
            }
        }
        
        Label {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("panel:max_size", "Min/Max Size")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            visible: !modelButton.checked
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        UM.TextFieldWithUnit
        {
            id: supportSizeMaxTextFieldGrid
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
        
        Item{

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
        ComboBox {
            id: modelSubtypeGrid
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
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            visible: modelButton.checked
            Component.onCompleted: {
            }
            
            onActivated: {
                setProperty("ModelSubtype", subtypeItems.get(currentIndex).text);
            }
        }
        
        Item{

        }
    
        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("panel:wall-width", "Wall Width")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            visible: tubeButton.checked
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }
        UM.TextFieldWithUnit
        {
            id: supportSizeInnerTextFieldGrid
            property string displaySupportSizeInner: "0"
            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "mm"
            visible: tubeButton.checked
            text: displaySupportSizeInner
            
            Connections{
                target: root
                function onSupportSizeValueChanged() {
                    supportSizeInnerTextField.validator.top = root.supportSizeValue / 2 - 0.01
                    if(root.supportSizeInnerValue >= root.supportSizeValue / 2){
                        root.supportSizeInnerValue = root.supportSizeValue / 2 - 0.01;
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
        
        Item{

        }
        
        Label {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("panel:angle", "Taper Angle")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            visible: !modelButton.checked
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        
        UM.TextFieldWithUnit {
            id: supportAngleTextFieldGrid
            property string displaySupportAngle: "0"

            width: localwidth
            height: UM.Theme.getSize("setting_control").height
            unit: "°"
            visible: !modelButton.checked
            text: displaySupportAngle

            Component.onCompleted:{
                displaySupportAngle = root.taperAngleValue.toString()
            }

            validator: IntValidator
            {
                bottom: -89
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
                    displaySupportAngle = root.taperAngleValue.toString()
                } else {
                    var text_as_num = parseFloat(modified_text)
                    if(isNaN(text_as_num)){
                        displaySupportAngle = ""
                        displaySupportAngle = root.taperAngleValue.toString()
                    } else {
                        root.taperAngleValue = text_as_num
                        setProperty("SupportAngle", text_as_num)
                        displaySupportAngle = text_as_num.toString()
                    }
                }
            }
        }

        Item {

        }*/
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
            text: !modelOrientCheckbox.checked || abutmentButton.checked ? catalog.i18nc("panel:set_on_opposite", "Set on Opposite Direction") : catalog.i18nc("panel:set_on_main", "Set on Main Direction")
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
