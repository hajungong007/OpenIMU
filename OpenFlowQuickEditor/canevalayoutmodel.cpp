#include "canevalayoutmodel.h"

Block::Block(int x, int y, const QString &color)
    : m_x(x), m_y(y), m_color(color)
{

}

int Block::x() const
{
    return m_x;
}

int Block::y() const
{
    return m_y;
}

QString Block::color() const
{
    return m_color;
}

CanevaLayoutModel::CanevaLayoutModel(QObject *parent)
    : QAbstractListModel(parent)
{
}

void CanevaLayoutModel::addBlock(const Block &block)
{
    beginInsertRows(QModelIndex(), rowCount(), rowCount());
    m_blocks << block;
    endInsertRows();
}

int CanevaLayoutModel::rowCount(const QModelIndex & parent) const {
    Q_UNUSED(parent);
    return m_blocks.count();
}

QVariant CanevaLayoutModel::data(const QModelIndex & index, int role) const {
    if (index.row() < 0 || index.row() >= m_blocks.count())
        return QVariant();

    const Block &block = m_blocks[index.row()];
    if (role == XRole)
        return block.x();
    else if (role == YRole)
        return block.y();
    else if (role == ColorRole)
        return block.color();
    return QVariant();
}

QHash<int, QByteArray> CanevaLayoutModel::roleNames() const {
    QHash<int, QByteArray> roles;
    roles[XRole] = "xBlock";
    roles[YRole] = "yBlock";
    roles[ColorRole] = "colorBlock";
    return roles;
}
