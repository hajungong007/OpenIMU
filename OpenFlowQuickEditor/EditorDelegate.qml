import QtQuick 2.0

Rectangle {
    id: editorDelegate
    width: 50
    height: 50
    z: mouseArea.drag.active ||  mouseArea.pressed ? 2 : 1
    color: colorBlock
    x: xBlock
    y: yBlock
    property point beginDrag
    property bool caught: true
    border { width:2; color: "white" }
    radius: 5
    Drag.active: mouseArea.drag.active

    Text {
        anchors.centerIn: parent
        text: index
        color: "white"
    }
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        drag.target: parent
        onPressed: {
            editorDelegate.beginDrag = Qt.point(editorDelegate.x, editorDelegate.y);
        }
        onReleased: {
            if(!editorDelegate.caught) {
                backAnimX.from = editorDelegate.x;
                backAnimX.to = beginDrag.x;
                backAnimY.from = editorDelegate.y;
                backAnimY.to = beginDrag.y;
                backAnim.start()
            }
        }

    }
    ParallelAnimation {
        id: backAnim
        SpringAnimation { id: backAnimX; target: editorDelegate; property: "x"; duration: 500; spring: 2; damping: 0.2 }
        SpringAnimation { id: backAnimY; target: editorDelegate; property: "y"; duration: 500; spring: 2; damping: 0.2 }
    }
}
