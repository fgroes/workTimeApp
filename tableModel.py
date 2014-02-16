from PySide import QtCore


class TableModel(QtCore.QAbstractTableModel):

	def __init__(self, parent=None, *args):
		super(TableModel, self).__init__(parent, *args)
		
	def setTable(self, table):
		self.table = table

	def rowCount(self, parent):
		return self.table.rowCount

	def columnCount(self, parent):
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
			result = self.table.getHeader(index)
		elif (orientation == QtCore.Qt.Vertical):
			result = index + 1
		return result

	
class Table(object):

	def __init__(self, header):
		self.header = header
		self.data = []

	def addRow(self, row):
		if (len(row) == len(self.header)):
			self.data.append(row)

	def getData(self, row, column):
		return self.data[row][column]

	def getHeader(self, column):
		return self.header[column]

	def getColumnCount(self):
		return len(self.header)

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