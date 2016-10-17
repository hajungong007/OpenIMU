#include "RecordsWidget.h"

RecordsWidget::RecordsWidget()
{

}

RecordsWidget::RecordsWidget(WimuAcquisition data, RecordInfo rcd)
{
    layout = new QGridLayout;
    this->setLayout(layout);

    acceleroData = data;
    record = rcd;

    recordTitle = new QLabel("Nom de l'enregistrement: "+ QString::fromStdString(record.m_recordName));
    recordDate = new QLabel(QString::fromStdString("Journée d'enregistrement: ")+ QString::fromStdString(acceleroData.getDates().back().date));
    imuType = new QLabel("Centralle inertielle: "+ QString::fromStdString("Wimu")); //TODO: add in bd
    positionImu = new QLabel("Position IMU: "+ QString::fromStdString("Poignet")); //TODO: add in bd
    seeFullGraphBtn = new QPushButton("Graphique détaillé");
    goToNextStep = new QPushButton("Choisir Algorithme");

    AccDataDisplay *dataDisplay = new AccDataDisplay(acceleroData);
    dataDisplay->showSimplfiedDataDisplay();

    layout->addWidget(recordTitle,0,0);
    layout->addWidget(recordDate,1,0);
    layout->addWidget(imuType,2,0);
    layout->addWidget(positionImu,3,0);
    layout->addWidget(dataDisplay,4,0,1,4);
    layout->addWidget(seeFullGraphBtn,5,0);
    layout->addWidget(goToNextStep,5,3);

    this->setStyleSheet( "QPushButton{"
                         "background-color: rgba(230, 233, 239,0.6);"
                         "border-style: inset;"
                         "border-width: 2px;"
                         "border-radius: 10px;"
                         "border-color: white;"
                         "font: 12px;"
                         "min-width: 10em;"
                         "padding: 6px; }"
     );
}

RecordsWidget::~RecordsWidget()
{

}
