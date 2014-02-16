from PySide import QtCore


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None, *args):
        super(TableModel, self).__init__(parent, *args)
        
    def setTable(self, table):
        self.table = table

    def rowCount(self, parent=None):
        return self.table.rowCount

    def columnCount(self, parent=None):
        return self.table.columnCount

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.table.getData(index.row(), index.column())

    def headerData(self, index, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        result = None
        if (orientation == QtCore.Qt.Horizontal):
            header = self.table.getHorizontalHeader(index)
            if header is not None:
                result = header
            else:
                result = index + 1
        elif (orientation == QtCore.Qt.Vertical):
            header = self.table.getVerticalHeader(index)
            if header is not None:
                result = header
            else:
                result = index + 1
        return result

    
class Table(object):

    def __init__(self, horizontalHeader=None, verticalHeader=None):
        self.horizontalHeader = horizontalHeader
        self.verticalHeader = verticalHeader
        self.data = []

    def addRow(self, row, header=None):
        if (len(row) == len(self.horizontalHeader)):
            self.data.append(row)
            if header is not None and self.verticalHeader is not None:
                self.verticalHeader.append(header)

    def getData(self, row, column):
        return self.data[row][column]

    def getHorizontalHeader(self, column):
        header = self.horizontalHeader
        return header[column] if header is not None else None
        
    def getVerticalHeader(self, row):
        header = self.verticalHeader
        return header[row] if header is not None else None

    def getColumnCount(self):
        return len(self.horizontalHeader)

    columnCount = property(getColumnCount)

    def getRowCount(self):
        return len(self.data)

    rowCount = property(getRowCount)


if __name__ == '__main__':
    table = Table(['time'])
    for hour in range(0, 24):
        for minute in range(0, 60, 30):
            time = '{0:02d}:{1:02d}'.format(hour, minute)
            table.addRow(time)
