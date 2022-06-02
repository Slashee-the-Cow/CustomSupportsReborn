//-----------------------------------------------------------------------------
// Copyright (c) 2022 5@xes
// 
// proterties values
//   "SSize"       : Support Size in mm
//   "MSize"       : Support Maximum Size in mm
//   "ISize"       : Support Interior Size in mm
//   "AAngle"      : Support Angle in °
//   "YDirection"  : Support Y direction (Abutment)
//   "EHeights"    : Equalize heights (Abutment)
//   "SMain"       : Scale Main direction (Freeform)
//   "SType"       : Support Type ( Cylinder/Tube/Cube/Abutment/Freeform/Custom ) 
//   "SubType"     : Support Freeform Type ( Cross/Section/Pillar/Bridge/Custom ) 
//   "SMirror"     : Support Mirror for Freeform Type
//-----------------------------------------------------------------------------

import QtQuick 2.2
import QtQuick.Controls 1.2

import UM 1.1 as UM

Item
{
    id: base
    width: childrenRect.width
    height: childrenRect.height
    UM.I18nCatalog { id: catalog; name: "cura"}

    property var s_size: UM.ActiveTool.properties.getValue("SSize")

    function setSType(type)
    {
        // set checked state of mesh type buttons
		cylinderButton.checked = type === 'cylinder'
		tubeButton.checked = type === 'tube'
        cubeButton.checked = type === 'cube'
		abutmentButton.checked = type === 'abutment'
		customButton.checked = type === 'custom'
		freeformButton.checked = type === 'freeform'
        UM.ActiveTool.setProperty("SType", type)
    }
	
    Column
    {
        id: sTypeItems
        anchors.top: parent.top;
        anchors.left: parent.left;
        spacing: UM.Theme.getSize("default_margin").height;

        Row // Mesh type buttons
        {
            id: sTypeButtons
            spacing: UM.Theme.getSize("default_margin").width

            Button
            {
                id: cylinderButton
                text: catalog.i18nc("@label", "Cylinder")
                iconSource: "type_cylinder.svg"
                property bool needBorder: true
                checkable:true
                onClicked: setSType('cylinder')
                style: UM.Theme.styles.tool_button
                checked: UM.ActiveTool.properties.getValue("SType") === 'cylinder'
                z: 6; // Depth position 
            }

            Button
            {
                id: tubeButton
                text: catalog.i18nc("@label", "Tube");
                iconSource: "type_tube.svg";
                property bool needBorder: true;
                checkable:true;
                onClicked: setSType('tube');
                style: UM.Theme.styles.tool_button;
                checked: UM.ActiveTool.properties.getValue("SType") === 'tube';
                z: 5; // Depth position 
            }
			
            Button
            {
                id: cubeButton;
                text: catalog.i18nc("@label", "Cube")
                iconSource: "type_cube.svg"
                property bool needBorder: true
                checkable: true
                onClicked: setSType('cube')
                style: UM.Theme.styles.tool_button
                checked: UM.ActiveTool.properties.getValue("SType") === 'cube'
                z: 4; // Depth position 
            }

            Button
            {
                id: abutmentButton
                text: catalog.i18nc("@label", "Abutment")
                iconSource: "type_abutment.svg"
                property bool needBorder: true
                checkable: true
                onClicked: setSType('abutment')
                style: UM.Theme.styles.tool_button
                checked: UM.ActiveTool.properties.getValue("SType") === 'abutment'
                z: 3; // Depth position 
            }

            Button
            {
                id: freeformButton
                text: catalog.i18nc("@label", "Freeform")
                iconSource: "type_freeform.svg"
                property bool needBorder: true
                checkable:true
                onClicked: setSType('freeform')
                style: UM.Theme.styles.tool_button
                checked: UM.ActiveTool.properties.getValue("SType") === 'freeform'
                z: 2; // Depth position 
            }
			
            Button
            {
                id: customButton
                text: catalog.i18nc("@label", "Custom")
                iconSource: "type_custom.svg"
                property bool needBorder: true
                checkable:true
                onClicked: setSType('custom')
                style: UM.Theme.styles.tool_button
                checked: UM.ActiveTool.properties.getValue("SType") === 'custom'
                z: 1; // Depth position 
            }
        }
    }
    Grid
    {
        id: textfields;
        anchors.leftMargin: UM.Theme.getSize("default_margin").width
        anchors.top: sTypeItems.bottom
		anchors.topMargin: UM.Theme.getSize("default_margin").height

        columns: 2
        flow: Grid.TopToBottom
        spacing: Math.round(UM.Theme.getSize("default_margin").width / 2)

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("@label","Size")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }
 
        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("@label","Max Size")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
			visible: !freeformButton.checked
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

        Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("@label","Type")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
			visible: freeformButton.checked
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }

		Label
        {
            height: UM.Theme.getSize("setting_control").height
            text: catalog.i18nc("@label","Interior size")
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
            text: catalog.i18nc("@label","Angle")
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            verticalAlignment: Text.AlignVCenter
			visible: !freeformButton.checked
            renderType: Text.NativeRendering
            width: Math.ceil(contentWidth) //Make sure that the grid cells have an integer width.
        }
		
        TextField
        {
            id: sizeTextField
            width: UM.Theme.getSize("setting_control").width
            height: UM.Theme.getSize("setting_control").height
            property string unit: "mm"
            style: UM.Theme.styles.text_field;
            text: UM.ActiveTool.properties.getValue("SSize")
            validator: DoubleValidator
            {
                decimals: 2
                bottom: 0.1
                locale: "en_US"
            }

            onEditingFinished:
            {
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                UM.ActiveTool.setProperty("SSize", modified_text)
            }
        }

        TextField
        {
            id: maxTextField
            width: UM.Theme.getSize("setting_control").width
            height: UM.Theme.getSize("setting_control").height
            property string unit: "mm"
            style: UM.Theme.styles.text_field
			visible: !freeformButton.checked
            text: UM.ActiveTool.properties.getValue("MSize")
            validator: DoubleValidator
            {
                decimals: 2
                bottom: 0
                locale: "en_US"
            }

            onEditingFinished:
            {
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                UM.ActiveTool.setProperty("MSize", modified_text);
            }
        }

		ComboBox {
			id: supportComboType
			objectName: "Support_Type"
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
			width: UM.Theme.getSize("setting_control").width
			height: UM.Theme.getSize("setting_control").height
			visible: freeformButton.checked
			Component.onCompleted: currentIndex = find(UM.ActiveTool.properties.getValue("SubType"))
			
			onCurrentIndexChanged: 
			{ 
				UM.ActiveTool.setProperty("SubType",cbItems.get(currentIndex).text);
			}
		}	
				
        TextField
        {
            id: sizeInteriorTextField
            width: UM.Theme.getSize("setting_control").width
            height: UM.Theme.getSize("setting_control").height
            property string unit: "mm"
            style: UM.Theme.styles.text_field
			visible: tubeButton.checked
            text: UM.ActiveTool.properties.getValue("ISize")
            validator: DoubleValidator
            {
                decimals: 2
				top: s_size
                bottom: 0.1
                locale: "en_US"
            }

            onEditingFinished:
            {
			    var cur_text = parseFloat(text)
				if ( cur_text >= s_size )
				{
				}
                var modified_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                UM.ActiveTool.setProperty("ISize", modified_text)
            }
        }
		
		TextField
        {
            id: angleTextField
            width: UM.Theme.getSize("setting_control").width
            height: UM.Theme.getSize("setting_control").height
            property string unit: "°"
            style: UM.Theme.styles.text_field
			visible: !freeformButton.checked
            text: UM.ActiveTool.properties.getValue("AAngle")
            validator: IntValidator
            {
                bottom: 0
            }

            onEditingFinished:
            {
                var modified_angle_text = text.replace(",", ".") // User convenience. We use dots for decimal values
                UM.ActiveTool.setProperty("AAngle", modified_angle_text)
            }
        }
    }
	Item
	{
		id: baseCheckBox
		width: childrenRect.width
		height: !freeformButton.checked && !abutmentButton.checked  ? 0 : (abutmentButton.checked ? (UM.Theme.getSize("setting_control").height*2+UM.Theme.getSize("default_margin").height): childrenRect.height)
		anchors.leftMargin: UM.Theme.getSize("default_margin").width
		anchors.top: textfields.bottom
		anchors.topMargin: UM.Theme.getSize("default_margin").height
		
		CheckBox
		{
			id: useYDirectionCheckbox
			anchors.top: baseCheckBox.top
			// anchors.topMargin: UM.Theme.getSize("default_margin").height
			anchors.left: parent.left
			text: catalog.i18nc("@option:check","Set on Y direction")
			style: UM.Theme.styles.partially_checkbox
			visible: abutmentButton.checked || freeformButton.checked

			checked: UM.ActiveTool.properties.getValue("YDirection")
			onClicked: UM.ActiveTool.setProperty("YDirection", checked)
			
		}
		CheckBox
		{
			id: mirrorCheckbox
			anchors.top: useYDirectionCheckbox.bottom
			anchors.topMargin: UM.Theme.getSize("default_margin").height
			anchors.left: parent.left
			text: catalog.i18nc("@option:check","Rotate 180°")
			style: UM.Theme.styles.partially_checkbox
			visible: freeformButton.checked

			checked: UM.ActiveTool.properties.getValue("SMirror")
			onClicked: UM.ActiveTool.setProperty("SMirror", checked)
			
		}	
		CheckBox
		{
			id: scaleMainDirectionCheckbox
			anchors.top: mirrorCheckbox.bottom
			anchors.topMargin: UM.Theme.getSize("default_margin").height
			anchors.left: parent.left
			text: catalog.i18nc("@option:check","Scaling also in main Directions")
			style: UM.Theme.styles.partially_checkbox
			visible: freeformButton.checked

			checked: UM.ActiveTool.properties.getValue("SMain")
			onClicked: UM.ActiveTool.setProperty("SMain", checked)
			
		}	
		CheckBox
		{
			id: equalizeHeightsCheckbox
			anchors.top: useYDirectionCheckbox.bottom
			anchors.topMargin: UM.Theme.getSize("default_margin").height
			anchors.left: parent.left
			text: catalog.i18nc("@option:check","Equalize heights")
			style: UM.Theme.styles.partially_checkbox
			visible: abutmentButton.checked

			checked: UM.ActiveTool.properties.getValue("EHeights")
			onClicked: UM.ActiveTool.setProperty("EHeights", checked)
		}
	}
	
	Rectangle {
        id: rightRect
        anchors.top: baseCheckBox.bottom
		//color: UM.Theme.getColor("toolbar_background")
		color: "#00000000"
		width: UM.Theme.getSize("setting_control").width * 1.8
		height: UM.Theme.getSize("setting_control").height 
        anchors.left: parent.left
		anchors.topMargin: UM.Theme.getSize("default_margin").height
    }
	
	Button
	{
		id: removeAllButton
		anchors.centerIn: rightRect
		width: UM.Theme.getSize("setting_control").width
		height: UM.Theme.getSize("setting_control").height	
		text: catalog.i18nc("@label", UM.ActiveTool.properties.getValue("SMsg"))
		onClicked: UM.ActiveTool.triggerAction("removeAllSupportMesh")
	}
}
