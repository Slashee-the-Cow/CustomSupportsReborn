import QtQuick 6.0
import QtQuick.Controls 6.0
import QtQuick.Layouts 6.0

import UM 1.6 as UM

Item {
    id: container
    property string imageSource: ""
    property string iconThemeColor: "icon"
    property string toolTipText: ""
    property bool toolTipVisible: true
    
    Pane {
        id: toolTipPane
        anchors.fill: parent
        hoverEnabled: true
        background: Rectangle {color: "transparent"}
        padding: 0
        

        UM.ColorImage {
            visible: true
            id: iconImage
            anchors.fill: parent
            source: Qt.resolvedUrl(imageSource)
            color: UM.Theme.getColor(iconThemeColor)
        }

        visible: toolTipText !== ""

        ToolTip.text: toolTipText
        ToolTip.visible: hovered && toolTipVisible
        //ToolTip.timeout: 1000
    }
}