#ifndef CANEVALAYOUTMODEL_H
#define CANEVALAYOUTMODEL_H

#include <QAbstractListModel>
#include <QStringList>


class Block
{
public:
    Block(int x, int y, const QString &color);

    int x() const;
    int y() const;
    QString color() const;

private:
    int m_x;
    int m_y;
    QString m_color;
};

class CanevaLayoutModel : public QAbstractListModel
{
    Q_OBJECT
public:
    enum BlockRoles {
        XRole = Qt::UserRole + 1,
        YRole,
        ColorRole
    };

    CanevaLayoutModel(QObject *parent = 0);
    void addBlock(const Block &block);

    int rowCount(const QModelIndex & parent = QModelIndex()) const;

    QVariant data(const QModelIndex & index, int role = Qt::DisplayRole) const;

protected:
    QHash<int, QByteArray> roleNames() const;
private:
    QList<Block> m_blocks;
};


#endif //CANEVALAYOUTMODEL_H
