#include "Utilities.h"

using namespace std;

const QString Utilities::m_successColour = "#2ECC71 ";
const QString Utilities::m_errorColour = "#E84C3C ";
const QString Utilities::m_warningColour = "#F1C40F";
const QString Utilities::m_defaultColour = "#2C3E50";

QString Utilities::capitalizeFirstCharacter(QString myString)
{
    return myString.at(0).toUpper() + myString.mid(1);
}

QString Utilities::capitalizeFirstCharacter(string myString)
{
    QString myQString = QString::fromStdString(myString);
    return myQString.at(0).toUpper() + myQString.mid(1);
}

QString Utilities::getColourFromEnum(MessageStatus status)
{
    switch(status)
    {
    case success:
        return m_successColour;
    case warning:
        return m_warningColour;
    case error:
        return m_errorColour;
    default:
        return m_defaultColour;
    }
}





