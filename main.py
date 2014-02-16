from database import *
from PySide import QtGui
import sys


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle('basic window')
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('&File')
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.triggered.connect(QtGui.qApp.quit)
        centralWidget = QtGui.QWidget()
        self.fileMenu.addAction(exitAction)
        self.centralLayout = QtGui.QVBoxLayout()
        self.centralLayout.addWidget(QtGui.QPushButton('Test'))
        self.tableView = QtGui.QTableView()
        self.setTable()
        self.tableView.setModel(self.tableModel)
        self.centralLayout.addWidget(self.tableView)
        centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(centralWidget)

    def setTable(self):
        table = Table(['Name', 'Age'])
        table.addRow(['fritz', '31'])
        table.addRow(['dominik', '28'])
        table.addRow(['andi', '26'])
        table.addRow(['franz', '34'])
        self.tableModel = TableModel()
        self.tableModel.setTable(table)


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
