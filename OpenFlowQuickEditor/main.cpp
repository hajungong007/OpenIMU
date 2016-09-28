#include <QApplication>
#include <QQmlApplicationEngine>
#include <QQuickView>
#include <qqmlcontext.h>
#include <qqml.h>
#include "canevalayoutmodel.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QQmlApplicationEngine engine;

    CanevaLayoutModel model;
    model.addBlock(Block(100,100, "Blue"));
    model.addBlock(Block(100,200, "Red"));
    model.addBlock(Block(200,100, "Yellow"));
    model.addBlock(Block(200,200, "Green"));

    /*QQuickView viewer;
    viewer.engine()->rootContext()->setContextProperty("canevaLayoutModel", &model);
    viewer.setSource(QStringLiteral("qrc:/main.qml"));
    viewer.show();*/
    engine.rootContext()->setContextProperty("canevaLayoutModel", &model);
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    return app.exec();
}
