import configparser as conf
import pymysql

def newSkaterStart(sql):
   configParser = conf.RawConfigParser()
   configFilePath = r'/etc/skatetrax/settings.conf'
   configParser.read(configFilePath)

   host = configParser.get('dbconf', 'host')
   user = configParser.get('dbconf', 'user')
   password = configParser.get('dbconf', 'password')
   db = configParser.get('dbconf', 'db')

   con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
   cur = con.cursor()
   cur.execute(sql)
   tables = cur.fetchall()
   cur.connection.commit()
   con.close()
   return tables

def newSkaterBulk(sql,newSkater):
   configParser = conf.RawConfigParser()
   configFilePath = r'/etc/skatetrax/settings.conf'
   configParser.read(configFilePath)

   host = configParser.get('dbconf', 'host')
   user = configParser.get('dbconf', 'user')
   password = configParser.get('dbconf', 'password')
   db = configParser.get('dbconf', 'db')

   con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
   cur = con.cursor()
   cur.execute(sql,newSkater)
   tables = cur.fetchall()
   cur.connection.commit()
   con.close()
   return tables

def createUser():
    print('connecting ...')
    getLastID = "select (MAX(ID) + 1) as lii from uSkaterConfig"
    nextID =  newSkaterStart(getLastID)
    print('Last Inserted ID is', nextID)

    return

createUser()
