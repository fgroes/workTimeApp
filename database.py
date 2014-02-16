from PySide import QtSql


class Database(object):

    def __init__(self, fileName):
        self.fileName = fileName
        
    def connect(self):
        if hasattr(self, 'connection'):
            if not self.connection.open():
                self.connection.open()
        else:
            try:
                self.connection = QtSql.QSqlDatabase('QSQLITE')
                self.connection.setDatabaseName(self.fileName)
                if not self.connection.open():
                    raise Exception()
            except:
                print('cannot establish a database connection')
                        
    def close(self):
        self.connection.close()
            
    def getTables(self):
        self.connect()
        if hasattr(self, 'connection'):
            return self.connection.tables()
        else:
            return None

    tables = property(getTables)

    def addTable(self, tableName, columnNames):
        self.connect()
        if tableName not in self.tables:
            if hasattr(self, 'connection'):
                command = 'CREATE TABLE {0}({1})'.format(
                    tableName, ', '.join(columnNames))
                self.connection.exec_(command)


if __name__ == '__main__':
    db = Database('test.db')
    db.addTable('workers', ['firstName', 'lastName', 'Age'])
    print(db.tables)