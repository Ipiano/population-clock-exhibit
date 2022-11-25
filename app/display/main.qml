import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick 2.15

ApplicationWindow {
    visible: true
    title: " "

    property bool fullscreen: population_provider.fullscreen
    property int height_hack: population_provider.height_hack
    property string population_value: population_provider.population ? population_provider.population : ""

    width: fullscreen ? Screen.width : 600
    height: fullscreen ? Screen.height : 500
    x: fullscreen ? 0 : 100
    y: fullscreen ? 0 : 100

    flags: fullscreen ? Qt.Window | Qt.SplashScreen | Qt.FramelessWindowHint : Qt.Window
    visibility: fullscreen ? Window.FullScreen : Window.Windowed

    Item {
        id: display_area

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: height_hack > 0 ? Math.min(height_hack, parent.height) : parent.height

        Rectangle {
            id: counter_area

            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            height: display_area.height * 0.9

            // Template for all text, setting the font and character
            // bounding box based on auto-resizing text
            Text {
                id: sample_text
                visible: false

                width: parent.width / population_value.length
                height: parent.height

                text: "0"

                fontSizeMode: Text.Fit
                minimumPointSize: 10

                font.pointSize: 1000
                font.family: "DejaVu Sans"
            }

            Row {
                visible: population_value
                anchors.centerIn: parent

                Repeater {
                    model: population_value.length

                    Item {
                        id: pop_digit

                        property string character: population_value[modelData]
                        property bool isComma: character == ","

                        width: isComma ? sample_text.contentWidth/2 : sample_text.contentWidth
                        height: sample_text.contentHeight

                        Component {
                            id: comma_component

                            Text {
                                text: character

                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter

                                fontSizeMode: Text.Fit
                                minimumPointSize: 10

                                font: sample_text.font
                            }
                        }

                        Component {
                            id: number_component

                            Text {
                                text: character

                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter

                                fontSizeMode: Text.Fit
                                minimumPointSize: 10

                                font: sample_text.font
                            }
                        }

                        Loader {
                            anchors.fill: parent
                            sourceComponent: isComma ? comma_component : number_component
                        }
                    }
                }
            }

            Text {
                id: pop_text
                anchors.fill: parent

                visible: !population_value

                text: "Loading..."

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter

                fontSizeMode: Text.Fit
                minimumPointSize: 10

                font: sample_text.font
            }
        }

        Text {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: counter_area.bottom
            anchors.bottom: parent.bottom

            text: population_provider.source ? "Source: " + population_provider.source : ""

            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignRight
        }

        focus: true
        Keys.onPressed: (event) => {
                if (event.key == Qt.Key_Q)
                    close()
                else if(event.key == Qt.Key_F)
                    population_provider.fullscreen = !fullscreen
            }
    }
}
