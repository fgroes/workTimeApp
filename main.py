from database import *
from tableModel import *
from PySide import QtGui, QtCore
import sys


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.database = TaskTimeDatabase('data.db')
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
        self.topLayout = QtGui.QGridLayout()
        self.centralLayout.addLayout(self.topLayout)
        self.calendar = QtGui.QCalendarWidget(parent=self)
        self.calendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.topLayout.addWidget(self.calendar, 0, 0)
        self.topLayout.setColumnStretch(0, 1)
        self.topRightLayout = QtGui.QVBoxLayout()
        self.addUserButton = QtGui.QPushButton('Add User')
        self.addUserButton.clicked.connect(self.addUser)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.userComboBox = QtGui.QComboBox()
        self.setUsers()
        self.topRightLayout.addWidget(self.userComboBox)
        self.topRightLayout.addLayout(self.formLayout)
        self.firstNameText = QtGui.QLineEdit()
        self.lastNameText = QtGui.QLineEdit()
        self.userComboBox.currentIndexChanged.connect(self.userIndexChanged)
        self.formLayout.addRow('First name:', self.firstNameText)
        self.formLayout.addRow('Last name:', self.lastNameText)
        self.topRightLayout.addWidget(self.addUserButton)
        self.topRightLayout.addStretch()
        self.topLayout.addLayout(self.topRightLayout, 0, 1)
        self.topLayout.setColumnStretch(1, 1)
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
            
    def addUser(self):
        firstName = self.firstNameText.text()
        lastName = self.lastNameText.text()
        if firstName != '' and lastName != '':
            self.database.addUser(firstName, lastName)
        self.setUsers()
        self.userComboBox.setCurrentIndex(len(self.users) - 1)
            
    def setUsers(self):
        self.users, self.ids = self.database.getUsers()
        currentIndex = self.userComboBox.currentIndex()
        self.userComboBox.clear()
        self.userComboBox.addItems(self.users)
        self.userComboBox.setCurrentIndex(currentIndex)
        
    def userIndexChanged(self, index):
        user = self.database.getUser(self.ids[index])
        self.firstNameText.setText(user.firstName)
        self.lastNameText.setText(user.lastName)


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
