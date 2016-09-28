import QtQuick 2.0

MouseArea {
    id: editorDelegate

    width: 80; height: 80
    drag.target: icon

    Rectangle {
        id: icon
        width: 72; height: 72
        anchors {
            horizontalCenter: parent.horizontalCenter;
            verticalCenter: parent.verticalCenter
        }
        color: model.color
        radius: 3

        Drag.active: editorDelegate.drag.active
        Drag.source: editorDelegate
        Drag.hotSpot.x: 36
        Drag.hotSpot.y: 36

        states: [
            State {
                when: icon.Drag.active
                ParentChange {
                    target: icon
                    parent: editor
                }

                AnchorChanges {
                    target: icon;
                    anchors.horizontalCenter: undefined;
                    anchors.verticalCenter: undefined
                }
            }
        ]
    }

    DropArea {
        anchors { fill: parent; margins: 15 }

        onEntered: visualModel.items.move(drag.source.visualIndex, editorDelegate.visualIndex)
    }
}
