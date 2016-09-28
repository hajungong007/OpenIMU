import QtQuick 2.0

Component {
    Item {
        id: wrapper
        width: 180; height: 40
        MouseArea{
            id: mouseArea2
            anchors.fill: parent
            Row {
                id: row1
                anchors.verticalCenter: parent.verticalCenter
                Text {
                    width: 150
                    id:txt
                    text: blockDisplayName
                    anchors.verticalCenter: parent.verticalCenter
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                }
                MouseArea{
                    id: mouseArea1

                    width: 25
                    height: 25
                    anchors.verticalCenter: parent.verticalCenter

                    Text{
                        text: '+'
                        anchors.verticalCenter: parent.verticalCenter
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignRight
                        width: 25
                        height: 25
                    }
                    onClicked: {
                        canevaLayoutModel.addBlock(0,0,"magenta")
                    }
                }
            }
            onClicked: {
                availableListViewBlockDescription.text=description
                wrapper.ListView.view.currentIndex = index
            }
        }
        states: State {
            name: "Current"
            when: wrapper.ListView.isCurrentItem
            PropertyChanges { target: wrapper; x: 15 }
        }
        transitions: Transition {
            NumberAnimation { properties: "x"; duration: 200 }
        }
    }
}
