import QtQuick 2.0

import QtQuick.Controls 1.4
import QtQuick.Layouts 1.2


ColumnLayout {
    id: availableListView
    spacing: 6

    Component {
        id: highlightBar
        Rectangle {
            width: 200; height: 50
            color: "Cyan"
            y: blockList.currentItem.y;
            Behavior on y { SpringAnimation { spring: 5; damping: 0.5 } }
        }
    }

    ListView {
        id: blockList
        width: 200;
        Layout.fillHeight: true
        focus: true

        model: BlockListModel {
            id: blockListModel
        }
        delegate: BlockListDelegate {
            id: blockListDelegate
        }

        // Set the highlight delegate. Note we must also set highlightFollowsCurrentItem
        // to false so the highlight delegate can control how the highlight is moved.
        highlight: highlightBar
        highlightFollowsCurrentItem: false
    }

    TextArea {
        id: availableListViewBlockDescription
        text: "Description of the selected block in the list."
        Layout.maximumWidth: 300
        font.pointSize: 10
        verticalAlignment: Text.AlignBottom
        wrapMode: Text.WordWrap
    }
}
