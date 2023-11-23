import sqlite3


class SQLite:
  db_file = 'data/user.sql'
  # db_file = 'data/user.db'
  conn = None
  cur = None

  def __init__(self, user_id, name, temp_thr, humid_thr, lightintensity_thr):
    self.user_id = user_id
    self.name = name
    self.temp_thr = temp_thr
    self.humid_thr = humid_thr
    self.lightintensity_thr = lightintensity_thr

  def connect(self):
    SQLite.conn = sqlite3.connect(SQLite.db_file)
    SQLite.cur = SQLite.conn.cursor()
    SQLite.cur.execute('''
      CREATE TABLE IF NOT EXISTS user (
        user_id int,
        name text,
        temp_thr real,
        humid_thr real,
        lightintensity_thr real,
        PRIMARY KEY(user_id)
      )
    ''')
    SQLite.conn.commit()

  def isConnected(self):
    if (self.conn is None or self.cur is None):
      return False
    return True

  def createUser(self):
    if (not self.isConnected()):
      return False
    SQLite.cur.execute(
        '''
      INSERT INTO user (user_id, name, temp_thr, humid_thr, lightintensity_thr) VALUES
      (?, ?, ?, ?, ?)
    ''', [
            self.user_id, self.name, self.temp_thr, self.humid_thr,
            self.lightintensity_thr
        ])
    SQLite.conn.commit()
    return SQLite.cur.lastrowid

  def deleteUser(self):
    if (not self.isConnected()):
      return False
    SQLite.cur.execute('''
      DELETE FROM user WHERE user_id = ?
    ''', [self.user_id])
    SQLite.conn.commit()
    return SQLite.cur.lastrowid

  def updateUser(self):
    if (not self.isConnected()):
      return False
    SQLite.cur.execute(
        '''
        UPDATE user SET name=?,temp_thr=?,humid_thr=?,lightintensity_thr=? WHERE user_id=?
      ''', [
            self.name, self.temp_thr, self.humid_thr, self.lightintensity_thr,
            self.user_id
        ])
    SQLite.conn.commit()
    return SQLite.cur.lastrowid

  def getUser(self):
    if (not self.isConnected()):
      return False
    SQLite.cur.execute('''
      SELECT * FROM user WHERE user_id=?
    ''', [self.user_id])
    SQLite.conn.commit()
    return SQLite.cur.fetchone()
  
  def getAll(self):
    if (not self.isConnected()):
      return False
    SQLite.cur.execute('''
      SELECT * FROM user
    ''')
    SQLite.conn.commit()
    return SQLite.cur.fetchall()

  def close(self):
    SQLite.conn.close()


if __name__ == '__main__':
  user = SQLite(2, 'user', 20, 20, 20)
  user.connect()
  if(user.getUser() == None):
    user.createUser()
  # user.name = 'name'
  # user.updateUser()
  # user.deleteUser()
  data = user.getAll()
  # data = user.getUser()
  print(data)
