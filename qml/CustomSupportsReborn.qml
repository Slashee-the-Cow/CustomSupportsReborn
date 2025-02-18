//-----------------------------------------------------------------------------
// Custom Support Cylinder Copyright (c) 2022 5@xes
// Custom Supports Reborn copyright 2025 Slashee the Cow
// 
//   "supportSize"               : Support size in mm
//   "TaperedSize"               : Tapered support size in mm
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
import QtQml 6.0

import UM 1.6 as UM
import Cura 1.1 as Cura

import ".."

Item {
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

    readonly property string colorNormal: "icon"
    readonly property string colorInfo: "icon"
    readonly property string colorError: "error"

    readonly property bool sizeWarnings: true
    readonly property real sizeWarningSize: 330

    UM.I18nCatalog {id: catalog; name: "customsupportsreborn"}

    width: childrenRect.width
    height: childrenRect.height

    property real supportSizeValue: 0
    property real supportSizeFocusValue: 0  // To restore it to the last value you used if you click the "Fix it" button, not the last valid entry
    property real taperedSizeValue: 0
    property real wallWidthValue: 0
    property real taperAngleValue: 0
    property string supportTypeValue: ""
    property string modelSubtypeValue: ""

    // Technically it's probably wrong to set these to true now. But they're set when the component is created.
    property bool supportSizeValueValid: true
    property bool taperedSizeValueValid: true
    property bool wallWidthValueValid: true
    property bool taperAngleValueValid: true
    property bool supportTypeValueValid: true  // It's loaded in the updateUI() run in the start and can only be changed to other valid values

    property string supportSizeIconToolTipText: ""
    property string supportSizeIconImage: ""
    property string supportSizeIconColor: ""

    property string taperedSizeIconToolTipText: ""
    property string taperedSizeIconImage: ""
    property string taperedSizeIconColor: ""

    property string wallWidthIconToolTipText: ""
    property string wallWidthIconImage: ""
    property string wallWidthIconColor: ""

    property string taperAngleIconToolTipText: ""
    property string taperAngleIconImage: ""
    property string taperAngleIconColor: ""

    property string modelSubtypeIconToolTipText: ""
    property string modelSubtypeIconImage: ""
    property string modelSubtypeIconColor: ""

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

    function getValidatedValue(text, min_value, max_value){
        var value = parseFloat(text.replace(",","."))
        
        if (isNaN(value)) {
            return { valid: false }; // Return an object with valid: false
        }

        // Clamping (not sure I'll want it, but seemed like a good idea at the time)
        if (min_value !== undefined && value < min_value) {
            value = min_value;
        }
        if (max_value !== undefined && value > max_value) {
            value = max_value;
        }

        return { valid: true, value: value }
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
        taperedSizeValue = getProperty("TaperedSize")
        wallWidthValue = getProperty("WallWidth")
        taperAngleValue = getProperty("TaperAngle")
        supportTypeValue = getProperty("SupportType")

        supportYDirectionCheckbox.checked = getProperty("SupportYDirection")
        modelMirrorCheckbox.checked = getProperty("ModelMirror")
        modelOrientCheckbox.checked = getProperty("ModelOrient")
        modelScaleMainCheckbox.checked = getProperty("ModelScaleMain")
        abutmentEqualizeHeightsCheckbox.checked = getProperty("AbutmentEqualizeHeights")
        modelSubtype.currentIndex = modelSubtype.find(getProperty("ModelSubtype"))
    }
    
    property bool uiInitialized: false  // Race conditions aren't as fun as they sound

    Component.onCompleted: {    
        updateUI();
        Qt.callLater(function(){
            uiInitialized = true
            validateInputs()
        })
    }
    
    //property var support_size: getProperty("SupportSize")
    //property int localwidth: 110

    function setSupportType(type) {
        // set checked state of mesh type buttons
        cylinderButton.checked = type === supportTypeCylinder
        tubeButton.checked = type === supportTypeTube
        cubeButton.checked = type === supportTypeCube
        abutmentButton.checked = type === supportTypeAbutment
        lineButton.checked = type === supportTypeLine
        modelButton.checked = type === supportTypeModel
        supportTypeValue = type
        setProperty("SupportType", type)
        validateInputs({
            supportSizeText: supportSizeTextField.text,
            taperAngleText: taperAngleTextField.text,
            taperedSizeText: taperedSizeTextField.text,
            wallWidthText: wallWidthTextField.text
        })
    }
    
    Column {
        id: supportTypeButtons
        anchors.top: parent.top
        anchors.left: parent.left
        spacing: UM.Theme.getSize("default_margin").height

        Row {  // Mesh type buttons
            id: supportTypeButtonsUpper
            spacing: UM.Theme.getSize("default_margin").width

            UM.ToolbarButton {
                id: cylinderButton
                text: catalog.i18nc("@label:shape", "Cylinder")
                toolItem: UM.ColorImage {
                    source: Qt.resolvedUrl("type_cylinder.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable:true
                onClicked: setSupportType(supportTypeCylinder)
                //checked: getProperty("SupportType") === supportTypeCylinder
                z: 3 // Depth position 
            }

            UM.ToolbarButton {
                id: tubeButton
                text: catalog.i18nc("@label:shape", "Tube")
                toolItem: UM.ColorImage {
                    source: Qt.resolvedUrl("type_tube.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable:true
                onClicked: setSupportType(supportTypeTube)
                //checked: getProperty("SupportType") === supportTypeTube
                z: 2 // Depth position 
            }
            
            UM.ToolbarButton {
                id: cubeButton
                text: catalog.i18nc("@label:shape", "Cube")
                toolItem: UM.ColorImage {
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
        Row { // Mesh type buttons
            id: supportTypeButtonsLower
            spacing: UM.Theme.getSize("default_margin").width
            
            UM.ToolbarButton {
                id: abutmentButton
                text: catalog.i18nc("@label:shape", "Abutment")
                toolItem: UM.ColorImage {
                    source: Qt.resolvedUrl("type_abutment.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable: true
                onClicked: setSupportType(supportTypeAbutment)
                //checked: getProperty("SupportType") === supportTypeAbutment
                z: 3 // Depth position 
            }

            UM.ToolbarButton {
                id: lineButton
                text: catalog.i18nc("@label:shape", "Line")
                toolItem: UM.ColorImage {
                    source: Qt.resolvedUrl("type_line.svg")
                    color: UM.Theme.getColor("icon")
                }
                property bool needBorder: true
                checkable:true
                onClicked: setSupportType(supportTypeLine)
                //checked: getProperty("SupportType") === supportTypeLine
                z: 2 // Depth position 
            }

            UM.ToolbarButton {
                id: modelButton
                text: catalog.i18nc("@label:shape", "Model")
                toolItem: UM.ColorImage {
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

    property int labelWidth: 70
    //property int labelWidth: Math.max(supportSizeLabel.contentWidth, wallWidthLabel.contentWidth, taperAngleLabel.contentWidth, modelSubtypeLabel.contentWidth, taperedSizeLabel.contentWidth)
    property int textFieldWidth: 110
    property int textFieldHeight: UM.Theme.getSize("setting_control").height
    property int iconWidth: UM.Theme.getSize("setting_control").height - UM.Theme.getSize("default_margin").height / 8
    property int iconHeight: iconWidth
    //property int iconHeight: UM.Theme.getSize("setting_control").height - UM.Theme.getSize("default_margin").height
    ColumnLayout {
        id: inputTextFields
        anchors.top: supportTypeButtons.bottom
        spacing: UM.Theme.getSize("default_margin").height
        
        RowLayout {
            id: invalidValuesWarningRow
            visible: false
            
            UM.Label {
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignCenter
                color: UM.Theme.getColor("error")
                text: catalog.i18nc("panel:invalid_values_warning", "Warning: Trying to create a support with an invalid input value will result in using previous valid values or failsafe defaults.")
                Layout.preferredWidth: iconWidth * 2 + textFieldWidth + labelWidth + UM.Theme.getSize("default_margin").width
                Layout.alignment: Qt.AlignHCenter
            }
        }

        RowLayout {
            id: supportSizeRow
            spacing: UM.Theme.getSize("default_margin").width
            
            UM.Label {
                id: supportSizeLabel
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignRight
                text: catalog.i18nc("panel:size", "Size")
                Layout.preferredWidth: labelWidth
            }

            UM.TextFieldWithUnit {
                id: supportSizeTextField
                property string displaySupportSize: ""
                Layout.preferredWidth: textFieldWidth
                height: textFieldHeight
                unit: "mm"
                text: displaySupportSize

                Component.onCompleted: {
                    displaySupportSize = root.supportSizeValue.toString()
                }

                validator: DoubleValidator {
                    decimals: 2
                    bottom: 1
                    locale: "en_US"
                    notation: DoubleValidator.StandardNotation
                }

                onTextChanged: {
                    validateInputs({supportSizeText: text})
                }

                onFocusChanged: {
                    if(focus) {return}

                    var result = getValidatedValue(text)
                    if (result.valid){
                        supportSizeFocusValue = result.value
                    }
                }
            }

            IconToolTip {
                id: supportSizeIconToolTip
                imageSource: supportSizeIconImage
                toolTipText: supportSizeIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: imageSource != iconBlank
            }

            Button {
                id: supportSizeFixItButton
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: false
                hoverEnabled: true
                ToolTip.text: catalog.i18nc("fixit_support_size", "Fix it! (Restore last used valid value)")
                ToolTip.visible: hovered
                background: Rectangle {color: "transparent"}
                UM.ColorImage {
                    source: Qt.resolvedUrl("icon_hammer.svg")
                    anchors.fill: parent
                    color: UM.Theme.getColor("icon")
                }
                property var fixFunction: null
                onClicked: {
                    if(fixFunction){
                        fixFunction()
                        visible = false
                    }
                }
            }
        }

        RowLayout {
            spacing: UM.Theme.getSize("default_margin").width
            id: wallWidthRow
            visible: tubeButton.checked

            UM.Label {
                id: wallWidthLabel
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignRight
                text: catalog.i18nc("panel:wall-width", "Wall Width")
                Layout.preferredWidth: labelWidth
            }

            UM.TextFieldWithUnit {
                id: wallWidthTextField
                property string displayWallWidth: ""
                Layout.preferredWidth: textFieldWidth
                height: textFieldHeight
                unit: "mm"
                text: displayWallWidth

                Component.onCompleted: {
                    displayWallWidth = root.wallWidthValue.toString()
                }
                validator: DoubleValidator {
                    decimals: 2
                    bottom: 0.1
                    locale: "en_US"
                    notation: DoubleValidator.StandardNotation
                }

                onTextChanged: {
                    validateInputs({wallWidthText: text})
                }
            }

            IconToolTip {
                id: wallWidthIconToolTip
                imageSource: wallWidthIconImage
                toolTipText: wallWidthIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: imageSource != iconBlank
            }

            Button {
                id: wallWidthFixItButton
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: false
                hoverEnabled: true
                ToolTip.text: catalog.i18nc("fixit_wall_width", "Fix it! (Set wall width to 25% of support size)")
                ToolTip.visible: hovered
                background: Rectangle {color: "transparent"}
                UM.ColorImage {
                    source: Qt.resolvedUrl("icon_hammer.svg")
                    anchors.fill: parent
                    color: UM.Theme.getColor("icon")
                }
                property var fixFunction: null
                onClicked: {
                    if(fixFunction){
                        if(fixFunction()){
                            visible = false
                        }
                    }
                }
            }
            
        }

        RowLayout {
            spacing: UM.Theme.getSize("default_margin").width
            id: taperAngleRow
            visible: !modelButton.checked
            
            UM.Label {
                id: taperAngleLabel
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignRight
                text: catalog.i18nc("panel:angle", "Taper Angle")
                Layout.preferredWidth: labelWidth
            }

            UM.TextFieldWithUnit {
                id: taperAngleTextField
                property string displayTaperAngle: ""

                Layout.preferredWidth: textFieldWidth
                height: textFieldHeight
                unit: "°"
                text: displayTaperAngle

                Component.onCompleted:{
                    displayTaperAngle = root.taperAngleValue.toString()
                }

                validator: IntValidator {
                    bottom: -89
                    top: 89
                }

                onTextChanged: {
                    validateInputs({taperAngleText: text})
                }
            }

            IconToolTip {
                id: taperAngleIconToolTip
                imageSource: taperAngleIconImage
                toolTipText: taperAngleIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: imageSource != iconBlank
            }

            Button {
                id: taperAngleFixItButton
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: false
                hoverEnabled: true
                ToolTip.text: catalog.i18nc("fixit_taper_angle", "Fix it! (Set taper angle to 0°)")
                ToolTip.visible: hovered
                background: Rectangle {color: "transparent"}
                UM.ColorImage {
                    source: Qt.resolvedUrl("icon_hammer.svg")
                    anchors.fill: parent
                    color: UM.Theme.getColor("icon")
                }
                property var fixFunction: null
                onClicked: {
                    if(fixFunction){
                        if(fixFunction()){
                            visible = false
                        }
                    }
                }
            }
        }

        RowLayout {
            id: modelSubtypeRow
            spacing: UM.Theme.getSize("default_margin").width
            visible: modelButton.checked
            UM.Label {
                id: modelSubtypeLabel
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignRight
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
                //ListElement { text: "custom"}
                }
                Layout.preferredWidth: textFieldWidth
                height: UM.Theme.getSize("setting_control").height
                Component.onCompleted: {
                }
                
                onActivated: {
                    setProperty("ModelSubtype", subtypeItems.get(currentIndex).text)
                    modelSubtypeValue = subtypeItems.get(currentIndex).text
                    if(!isVersion57OrGreater()){
                        setIconToolTip(modelSubtypeIconToolTip, iconInfo, "Currently selected model is " + modelSubtypeValue)
                    }
                    validateInputs()
                }
            }

            IconToolTip {
                id: modelSubtypeIconToolTip
                imageSource: modelSubtypeIconImage
                toolTipText: modelSubtypeIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: imageSource != iconBlank
            }

            // I don't see this one ever being used. But, y'know, consistency.
            Button {
                id: modelSubtypeFixItButton
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: false
                hoverEnabled: true
                ToolTip.text: catalog.i18nc("fixit_model_subtype", "Fix it! (Reset to default value)")
                ToolTip.visible: hovered
                background: Rectangle {color: "transparent"}
                UM.ColorImage {
                    source: Qt.resolvedUrl("icon_hammer.svg")
                    anchors.fill: parent
                    color: UM.Theme.getColor("icon")
                }
                property var fixFunction: function(){
                    setProperty(ModelSubtype, subtypeItems.get(0).text)
                    modelSubtypeValue = ModelSubtype, subtypeItems.get(0).text
                    return true
                }
                onClicked: {
                    if(fixFunction){
                        if(fixFunction()){
                            visible = false
                        }
                    }
                }
            }
        }

        RowLayout {
            id: taperedSizeRow
            spacing: UM.Theme.getSize("default_margin").width
            visible: taperAngleValue != 0 && !modelButton.checked && !abutmentButton.checked
            UM.Label {
                id: taperedSizeLabel
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignRight
                text: catalog.i18nc("panel:tapered_size", "Tapered Size")
                Layout.preferredWidth: labelWidth
            }
            UM.TextFieldWithUnit {
                id: taperedSizeTextField
                property string displaytaperedSize: ""
                Layout.preferredWidth: textFieldWidth
                height: textFieldHeight
                unit: "mm"
                text: displaytaperedSize
                hoverEnabled: true

                Component.onCompleted: {
                    displaytaperedSize = root.taperedSizeValue.toString()
                }

                validator: DoubleValidator {
                    decimals: 2
                    bottom: 1
                    locale: "en_US"
                    notation: DoubleValidator.StandardNotation
                }

                onTextChanged: {
                    validateInputs({taperedSizeText: text})
                }
            }

            IconToolTip {
                id: taperedSizeIconToolTip
                imageSource: taperedSizeIconImage
                toolTipText: taperedSizeIconToolTipText
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: imageSource != iconBlank
            }

            Button {
                id: taperedSizeFixItButton
                Layout.preferredWidth: iconWidth
                Layout.preferredHeight: iconHeight
                anchors.margins: 0
                visible: false
                hoverEnabled: true
                ToolTip.text: catalog.i18nc("fixit_tapered_size", "Fix it! (Sets tapered size to ±50% of normal size, depending on taper being positive or negative)")
                ToolTip.visible: hovered
                background: Rectangle {color: "transparent"}
                UM.ColorImage {
                    source: Qt.resolvedUrl("icon_hammer.svg")
                    anchors.fill: parent
                    color: UM.Theme.getColor("icon")
                }
                property var fixFunction: null
                onClicked: {
                    if(fixFunction){
                        fixFunction()
                        visible = false
                    }
                }
            }
        }
    }

    function setIconToolTip(icon_tool_tip, icon, message, icon_color = iconInfo){
        icon_tool_tip.imageSource = icon
        icon_tool_tip.toolTipText = message
        icon_tool_tip.iconThemeColor = icon_color
    }

    function clearIconToolTip(icon_tool_tip){
        setIconToolTip(icon_tool_tip, iconBlank, "", colorNormal)
    }

    function validateInputs(params){
        if (!uiInitialized) {return ;}
        const {
            supportSizeText = null,
            taperAngleText = null,
            taperedSizeText = null,
            wallWidthText = null
        } = params || {}

        let setSupportSize = null
        let setTaperAngle = null
        let setTaperedSize = null
        let setWallWidth = null
        
        let support_type = supportTypeValue
        // Do individual validation before dependent validation
        let support_fix_function = function(){
            supportSizeTextField.text = supportSizeFocusValue.toString()  // Set to the last valid value used, should trigger revalidation thanks to onTextChanged handler
            return true
        }
        if (supportSizeText !== null){
            const {valid: localIsValid, value: localSupportSizeValue} = getValidatedValue(supportSizeText)
            if (!localIsValid){  // Invalid text entry
                setIconToolTip(supportSizeIconToolTip, iconWarning, catalog.i18nc("validation:support_invalid_error", "Please enter a valid number."), colorError)
                supportSizeFixItButton.visible = true
                supportSizeFixItButton.fixFunction = support_fix_function
                supportSizeValueValid = false
            } else if (localSupportSizeValue < 1){  // Too small
                setIconToolTip(supportSizeIconToolTip, iconWarning, catalog.i18nc("validation:support_small_error", "Support size must be at least 1mm."), colorError)
                supportSizeFixItButton.visible = true
                supportSizeFixItButton.fixFunction = support_fix_function
                supportSizeValueValid = false
            } else if (sizeWarnings && localSupportSizeValue > sizeWarningSize){ // Just a warning, it's still valid.
                    setIconToolTip(supportSizeIconToolTip, iconInfo, catalog.i18nc("validation:support_size_warning", "The support size you have set is very high. Make sure it will fit in your printer's build volume."), iconInfo);
                    supportSizeFixItButton.visible = true
                    supportSizeFixItButton.fixFunction = support_fix_function
                    supportSizeValueValid = true
                    setSupportSize = localSupportSizeValue
            } else {  // We're all good
                clearIconToolTip(supportSizeIconToolTip)
                supportSizeFixItButton.visible = false
                supportSizeValueValid = true
                setSupportSize = localSupportSizeValue
            }
        }

        let taper_angle_fix_function = function(){
            taperAngleTextField.text = "0"
        }
        if (taperAngleText !== null){
            const {valid: localIsValid, value: localTaperAngleValue} = getValidatedValue(taperAngleText)
            if(!localIsValid){  // This should only happen if the user deletes all the text in the field, the intValidator makes it hard to screw up otherwise
                setIconToolTip(taperAngleIconToolTip, iconWarning, catalog.i18nc("validation:taper_angle_invalid_error", "Taper angle must be set between -89° and 89°"), colorError)
                taperAngleFixItButton.visible = true
                taperAngleFixItButton.fixFunction = taper_angle_fix_function
                taperAngleValueValid = false
            } else {
                clearIconToolTip(taperAngleIconToolTip)
                taperAngleFixItButton.visible = false
                taperAngleValueValid = true
                setTaperAngle = localTaperAngleValue
            }
        }
        
        let tapered_size_fix_function = function(){
            if (supportSizeFixItButton.visible){  // Set the regular size to a fixed size if it's bad
                supportSizeFixItButton.clicked()
            }
            if (taperAngleValue < 0){
                taperedSizeTextField.text = (supportSizeValue * 0.5).toString()
            } else if (taperAngleValue > 0){
                taperedSizeTextField.text = (supportSizeValue * 1.5).toString()
            } else {
                taperedSizeTextField.text = supportSizeValue.toString()
            }
            return true
        }
        if (taperedSizeText !== null){
            const {valid: localIsValid, value: localTaperedSizeValue} = getValidatedValue(taperedSizeText)
            if(!localIsValid){
                setIconToolTip(taperedSizeIconToolTip, iconWarning, catalog.i18nc("validation:tapered_size_invalid", "Please enter a valid number."), colorError)
                taperedSizeFixItButton.visible = true
                taperedSizeFixItButton.fixFunction = tapered_size_fix_function
                taperedSizeValueValid = false
            } else if (sizeWarnings && localTaperedSizeValue > sizeWarningSize){ // Just a warning, it's still valid.
                    setIconToolTip(supportSizeIconToolTip, iconInfo, catalog.i18nc("validation:support_size_warning", "The tapered support size you have set is very high. Make sure it will fit in your printer's build volume."), iconInfo);
                    taperedSizeFixItButton.visible = true
                    taperedSizeFixItButton.fixFunction = tapered_size_fix_function
                    taperedSizeValueValid = true
                    setTaperedSize = localTaperedSizeValue
            } else { // Comparing to start size is dependent so we get to that later
                clearIconToolTip(taperedSizeIconToolTip)
                taperedSizeFixItButton. visible = false
                taperedSizeValueValid = true
                setTaperedSize = localTaperedSizeValue
            }
        }

        let wall_width_fix_function = function(){
            if (supportSizeFixItButton.visible){  // Set the regular size to a fixed size if it's bad
                supportSizeFixItButton.clicked()
            }
            wallWidthTextField.text = (supportSizeValue * 0.25).toString()
            return true
        }
        if(support_type === supportTypeTube){  // Needs to be validated regardless or else its warning can disappear
            const {valid: localIsValid, value: localWallWidthValue} = getValidatedValue(wallWidthTextField.text)
            if(!localIsValid){
                setIconToolTip(wallWidthIconToolTip, iconWarning, catalog.i18nc("validation:wall_width_invalid", "Please enter a valid number."), colorError)
                wallWidthFixItButton.visible = true
                wallWidthFixItButton.fixFunction = wall_width_fix_function
                wallWidthValueValid = false
            } else {  // We'll get to comparing it to the support size in a minute
                clearIconToolTip(wallWidthIconToolTip)
                wallWidthFixItButton.visible = false
                wallWidthValueValid = true
                setWallWidth = localWallWidthValue
            }
        }


        let minimum_distance = 0.01

        let testTaperAngle = setTaperAngle ?? taperAngleValue
        let testTaperedSize = setTaperedSize ?? taperedSizeValue
        let testSupportSize = setSupportSize ?? supportSizeValue
        let testWallWidth = setWallWidth ?? wallWidthValue
        
        // Make sure tapered size is appropriately smaller or larger
        if (testTaperAngle < 0 && testTaperedSize > testSupportSize){
            setIconToolTip(taperedSizeIconToolTip, iconWarning, catalog.i18nc("validation:tapered_too_big", "Tapered size must be lower than support size when using a negative taper."), colorError)
            taperedSizeFixItButton.fixFunction = tapered_size_fix_function
            taperedSizeFixItButton.visible = true
            taperedSizeValueValid = false
            setTaperedSize = null
        } else if (testTaperAngle > 0 && testTaperedSize < testSupportSize){
            setIconToolTip(taperedSizeIconToolTip, iconWarning, catalog.i18nc("validation:tapered_too_small", "Tapered size must be larger than support size when using a positive taper."), colorError)
            taperedSizeFixItButton.fixFunction = tapered_size_fix_function
            taperedSizeFixItButton.visible = true
            taperedSizeValueValid = false
            setTaperedSize = null
        } else {  // Either angle is 0 or it *isn't* too big or small
            clearIconToolTip(taperedSizeIconToolTip)
            taperedSizeFixItButton.visible = false
            taperedSizeValueValid = true
        }
        
        // Tests for specific support types
        switch (support_type){
            case (supportTypeAbutment): {
                if (testTaperAngle < 0){  // This doesn't break it, this is just an info.
                    setIconToolTip(taperAngleIconToolTip, iconInfo, catalog.i18nc("validation:abutment_negative_taper", "Abutment support type does not support tapering inwards. A 0° taper will be used if the angle is set to negative."))
                    taperAngleFixItButton.visible = true
                    taperAngleFixItButton.fixFunction = function(){
                        taperAngleTextField.text = "0"
                        return true
                    }
                }
                break;
            }
            case (supportTypeTube): {
                if (testWallWidth >= testSupportSize / 2){
                    setIconToolTip(wallWidthIconToolTip, iconWarning, catalog.i18nc("validation:wall_width_thick", "Wall width must be under half of support size."), colorError)
                    wallWidthFixItButton.visible = true
                    wallWidthFixItButton.fixFunction = wall_width_fix_function
                    wallWidthValueValid = false
                    setWallWidth = null
                } else {
                    clearIconToolTip(wallWidthIconToolTip)
                    wallWidthFixItButton.visible = false
                    wallWidthValueValid = true
                }
                break;
            }
        }

        if (setSupportSize !== null){
            supportSizeValueValid = true
            supportSizeValue = setSupportSize
            setProperty("SupportSize", setSupportSize)
        }
        if (setTaperAngle !== null){
            taperAngleValueValid = true
            taperAngleValue = setTaperAngle
            setProperty("TaperAngle", setTaperAngle)
        }
        if (setTaperedSize !== null){
            taperedSizeValueValid = true
            taperedSizeValue = setTaperedSize
            setProperty("TaperedSize", setTaperedSize)
        }
        if (setWallWidth !== null){
            wallWidthValueValid = true
            wallWidthValue = setWallWidth
            setProperty("WallWidth", setWallWidth)
        }

        invalidValuesWarningRow.visible = checkInvalidRows()
    }

    function checkInvalidRows(){
            return !supportSizeValueValid ||  // Always visible so don't need to check for that
            (taperAngleRow.visible && !taperAngleValueValid) ||  // Should only be invalid if user directly clears field
            (taperedSizeRow.visible && !taperedSizeValueValid) ||
            (wallWidthRow.visible && !wallWidthValueValid)
    }
    
    ColumnLayout {
        id: checkBoxColumn
        anchors.top: inputTextFields.bottom
        anchors.topMargin: UM.Theme.getSize("default_margin").height
        spacing: UM.Theme.getSize("default_margin").height / 2
        
        UM.CheckBox {
            id: supportYDirectionCheckbox
            text: !modelOrientCheckbox.checked || abutmentButton.checked ? catalog.i18nc("panel:set_on_opposite", "Set on Opposite Direction") : catalog.i18nc("panel:set_on_main", "Set on Main Direction")
            visible: abutmentButton.checked || modelButton.checked 

            onClicked: setProperty("SupportYDirection", checked)
        }
        
        UM.CheckBox {
            id: modelMirrorCheckbox
            text: catalog.i18nc("panel:model_mirror", "Rotate 180°")
            visible: modelButton.checked && !modelOrientCheckbox.checked

            onClicked: setProperty("ModelMirror", checked)
        }

        UM.CheckBox {
            id: modelOrientCheckbox
            text: catalog.i18nc("panel:model_auto_orientate", "Auto Orientate")
            visible: modelButton.checked

            onClicked: setProperty("ModelOrient", checked)
        }

        UM.CheckBox {
            id: modelScaleMainCheckbox
            text: catalog.i18nc("panel:model_scale_main", "Scale Main Direction")
            visible: modelButton.checked

            onClicked: setProperty("ModelScaleMain", checked)
        }    
        UM.CheckBox {
            id: abutmentEqualizeHeightsCheckbox
            text: catalog.i18nc("panel:abutment_equalize_heights", "Equalize Heights")
            visible: abutmentButton.checked

            onClicked: setProperty("AbutmentEqualizeHeights", checked)
        }
        

    }

    Rectangle {
        id: rightRect
        anchors.top: checkBoxColumn.bottom
        //color: UM.Theme.getColor("toolbar_background")
        color: "#00000000"
        width: UM.Theme.getSize("setting_control").width * 1.3
        height: UM.Theme.getSize("setting_control").height 
        anchors.left: parent.left
        anchors.topMargin: UM.Theme.getSize("default_margin").height
    }
    
    Cura.SecondaryButton {
        id: removeAllButton
        anchors.centerIn: rightRect
        spacing: UM.Theme.getSize("default_margin").height
        width: UM.Theme.getSize("setting_control").width
        height: UM.Theme.getSize("setting_control").height        
        text: catalog.i18nc("panel:remove_all", "Remove All")
        onClicked: triggerAction("removeAllSupportMesh")
    }
}
