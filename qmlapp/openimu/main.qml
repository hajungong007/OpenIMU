import QtQuick 2.0
import QtCharts 2.0
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.1


Rectangle {
    id: mainwindow
    visible: true
    width: 640
    height: 480

    ColumnLayout {
        id: layout
        Layout.fillHeight: true


        Text {
            id: text_scope
            text: "Scope"
            font.pointSize: 18
            color: "black"
        }

        Button {
            id: reset_zoom_button
            text: "Reset Zoom"
            font.pointSize: 18
            onPressed: {
                print('button pressed')
                chart.zoomReset()
            }
        }

        Item {
            id: item
            //anchors.fill: parent
            width: mainwindow.width
            height: 500

            //![1]
            ChartView {
                id: chart
                title: "Accelerometers"
                anchors.fill: parent
                legend.visible: false
                antialiasing: true
                animationOptions: ChartView.SeriesAnimations



                ValueAxis {
                    id: axisX
                    min: 0
                    max: 1000000
                    tickCount: 5
                }

                ValueAxis {
                    id: axisY
                    min: -1.5
                    max: 1.5
                }

                LineSeries {
                    id: series1
                    axisX: axisX
                    axisY: axisY
                    useOpenGL: true


                }


                Rectangle {
                    id: rectang
                    visible: false
                    x: 0
                    y: 0
                    z: 99
                    width: 0
                    height: 0
                    rotation: 0
                    color: "#5F227CEB"
                    border.width: 1
                    border.color: "#103A6E"
                    //transformOrigin: Item.TopLeft
                }
                MouseArea {

                    hoverEnabled: true
                    anchors.fill: parent
                    //acceptedButtons: Qt.AllButtons

                    onPressed: {rectang.x = mouseX; rectang.y = mouseY; rectang.visible = true}
                    onMouseXChanged: {rectang.width = mouseX - rectang.x}
                    onMouseYChanged: {rectang.height = mouseY - rectang.y}
                    onReleased: {
                        print(Qt.rect(rectang.x, rectang.y, rectang.width, rectang.height))
                        chart.zoomIn(Qt.rect(rectang.x, rectang.y, rectang.width, rectang.height))
                        rectang.visible = false;
                    }
                }

            } // ChartView




            // Add data dynamically to the series
            Component.onCompleted: {

                //chart.visible = false

                //Updating datasource
                print('updating datasource');
                dataSource.update(chart.series(0));
            }
        }

    }
}
