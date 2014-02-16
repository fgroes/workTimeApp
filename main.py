from tableModel import *
from PySide import QtGui, QtCore
import sys


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.show()      

    def initUI(self):
        self.setWindowTitle('basic window')
        self.setGeometry(100, 100, 1100, 900)
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('&File')
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.triggered.connect(QtGui.qApp.quit)
        centralWidget = QtGui.QWidget()
        self.fileMenu.addAction(exitAction)
        self.centralLayout = QtGui.QVBoxLayout()
        self.calendar = QtGui.QCalendarWidget(parent=self)
        self.calendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.centralLayout.addWidget(self.calendar)
        self.tableView = QtGui.QTableView()   
        #self.setTable()
        self.calendar.clicked.connect(self.setCurrentDate)
        self.setCurrentDate(QtCore.QDate.currentDate())
        self.centralLayout.addWidget(self.tableView)
        centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(centralWidget)
    
    def setCurrentDate(self, currentDate):      
        dateMonday = currentDate.addDays(1 - currentDate.dayOfWeek())
        datesOfWeek = []
        daysOfWeek = QtCore.Qt.DayOfWeek.values.keys()
        numberOfDaysInWeek = len(daysOfWeek)
        for i in range(numberOfDaysInWeek):
            date = dateMonday.addDays(i)
            datesOfWeek.append(date.toString('ddd dd.MM.yy'))
        table = Table(datesOfWeek, [])
        for hour in range(0, 24):
            for minute in range(0, 60, 30):
                time = '{0:02d}:{1:02d}'.format(hour, minute)
                table.addRow(
                    ['' for i in range(numberOfDaysInWeek)],
                    time)
        self.tableModel = TableModel()
        self.tableModel.setTable(table)
        self.tableView.setModel(self.tableModel)
        for i in range(self.tableModel.columnCount()):
            self.tableView.setColumnWidth(i, 200)


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
