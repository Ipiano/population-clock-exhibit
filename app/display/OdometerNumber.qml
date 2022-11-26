import QtQuick 2.15

Item {
    id: root
    clip: true

    property font font: Qt.font({ family: 'Encode Sans' })
    property int value: 0

    Component {
        id: delegate
        Text {
            width: root.width
            height: root.height

            text: index

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter

            fontSizeMode: Text.Fit
            minimumPointSize: 10

            font: root.font
        }
    }

    PathView {
        id: view
        anchors.fill: parent

        model: 10
        delegate: delegate
        currentIndex: value

        preferredHighlightBegin: 0.5
        preferredHighlightEnd: 0.5
        highlightRangeMode: PathView.StrictlyEnforceRange

        path: Path {
            startX: width/2.0; startY: (0 + height/2.0) - height * 5
            PathLine { x: width/2.0; y: (0 + height/2.0) + height * 5}
        }
    }
}
