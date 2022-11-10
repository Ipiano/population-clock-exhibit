import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

ApplicationWindow {
    visible: true
    title: " "

    property bool fullscreen: population_provider.fullscreen

    width: fullscreen ? Screen.width : 600
    height: fullscreen ? Screen.height : 500
    x: fullscreen ? 0 : 100
    y: fullscreen ? 0 : 100

    flags: fullscreen ? Qt.Window | Qt.SplashScreen | Qt.FramelessWindowHint : Qt.Window
    visibility: fullscreen ? Window.FullScreen : Window.Windowed

    Text {
        anchors.left: parent.left
        anchors.right: parent.right
        width: parent.width
        height: parent.height

        text: population_provider.population ? population_provider.population : "Loading..."

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        fontSizeMode: Text.Fit
        minimumPointSize: 10
        font.pointSize: 1000

        focus: true
        Keys.onPressed: (event) => {
                if (event.key == Qt.Key_Q)
                    close()
                else if(event.key == Qt.Key_F)
                    population_provider.fullscreen = !fullscreen
            }
    }
}
