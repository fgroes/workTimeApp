from PySide import QtSql, QtCore


class Database(object):

    def __init__(self, fileName):
        self.fileName = fileName
        
    def connect(self):
        if hasattr(self, 'connection'):
            if not self.connection.isOpen():
                self.connection.open()
        else:
            try:
                self.connection = QtSql.QSqlDatabase('QSQLITE')
                self.connection.setDatabaseName(self.fileName)
                if not self.connection.isOpen():
                    self.connection.open()
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
    
    def query(self, command):
        self.connect()
        return self.connection.exec_(command)
        
    def _getMaxId(self, tableName, columnName):
        self.connect()
        query = QtSql.QSqlQuery(self.connection)
        query.prepare(
            'SELECT MAX({1}) FROM {0}'.format(tableName, columnName))
        query.exec_()
        query.next()
        value = query.value(0)
        return int(value) if value != '' else None
        
        
class TaskTimeDatabase(Database):
    
    def __init__(self, fileName):
        super(TaskTimeDatabase, self).__init__(fileName)
        self.userColumns = ['id', 'firstName', 'lastName']
        self.taskColumns = ['taskId', 'userId', 'dateTime', 'task']
        self.addTable('users', self.userColumns)
        self.addTable('tasks', self.taskColumns)
                      
    def addUser(self, firstName, lastName):
        self.connect()
        query = QtSql.QSqlQuery(self.connection)
        query.prepare(
            'INSERT INTO users ({0}) VALUES (?, ?, ?)'.format(
                ', '.join(self.userColumns)))
        maxId = self._maxUserId
        query.bindValue(0, maxId + 1 if maxId is not None else 0)
        query.bindValue(1, firstName.capitalize())
        query.bindValue(2, lastName.capitalize())
        query.exec_()
        self.close()
                    
    def addTask(self, userId, dateTime, task):
        self.connect()
        query = QtSql.QSqlQuery(self.connection)
        query.prepare(
            'INSERT INTO tasks ({0}) VALUES (?, ?, ?, ?)'.format(
                ', '.join(self.taskColumns)))
        maxId = self._maxTaskId
        query.bindValue(0, maxId + 1 if maxId is not None else 0)
        query.bindValue(1, userId)
        query.bindValue(2, dateTime)
        query.bindValue(3, task)
        query.exec_()
        self.close()
        
    def _getMaxUserId(self):
        return self._getMaxId('users', 'id')
     
    _maxUserId = property(_getMaxUserId)
            
    def _getMaxTaskId(self):
        return self._getMaxId('tasks', 'taskId')
     
    _maxTaskId = property(_getMaxTaskId)


if __name__ == '__main__':
    db = TaskTimeDatabase('taskTime.db')
    db.addUser('fritz', 'groes')
    db.addUser('franz', 'goeth')
    dateTime = QtCore.QDateTime.currentDateTime()
    db.addTask(0, dateTime, 'stuff')