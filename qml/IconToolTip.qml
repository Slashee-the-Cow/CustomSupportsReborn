import QtQuick 6.0
import QtQuick.Controls 6.0
import QtQuick.Layouts 6.0

import UM 1.6 as UM

Item {
    id: container
    property alias imageSource: iconImage.source
    property string toolTipText: ""
    property alias iconColor: iconImage.color
    

    height: UM.Theme.getSize("setting_control").height
    width: UM.Theme.getSize("setting_control").height
    
    
    
    Pane {
        id: toolTipPane
        hoverEnabled: true
        background: Rectangle {color: "green"}

        property bool toolTipVisible: true

        UM.ColorImage {
            id: iconImage
            anchors.centerIn: parent
            source: ""
            color: UM.Theme.getColor("icon")
        }

        visible: toolTipText !== ""

        ToolTip.text: toolTipText
        ToolTip.visible: hovered && toolTipVisible
        //ToolTip.timeout: 1000
    }
}