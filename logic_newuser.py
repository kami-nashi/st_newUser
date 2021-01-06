import configparser as conf
import pymysql

def baseConfig():
    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)
    appConfig = configParser.get('appKey', 'secret')
    return appConfig

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

def createUser(userJSON):
    print('connecting ...')

    # Get the MAX ID, have SQL add 1 to it, use it for the uSkaterUUID in all other tables
    getLastID = "select (MAX(ID) + 1) as lii from uSkaterConfig"
    nextID =  newSkaterStart(getLastID)
    LII = nextID[0]['lii']

    print("Next User ID will be",LII)

    # Populates the uSkaterConfig table with a new row, where we begin.
    creStep1 = "INSERT INTO uSkaterConfig (uSkaterUUID, uSkaterFname, uSkaterLname, uSkaterUFSAid, uSkateComboIce, uSkateComboOff, uSkaterCity, uSkaterState, uSkaterMaintPref, uSkaterType, activeCoach) VALUES (%s, 'fName', 'lName', 1, 1, 2, 1, 1, 1, 1, 1);"

    dumb_tuple = (LII,LII)

    # Create a set of boots for on and off ice for the new user's ID
    creStep3 = "INSERT INTO uSkaterBoots (bootsName, bootsModel, bootsSize, bootsPurchDate, bootsPurchAmount, uSkaterUUID, bootID) VALUES ('Generic', 'Generic', 0, CURDATE(), 0, %s, 1);"
    creStep4 = "INSERT INTO uSkaterBoots (bootsName, bootsModel, bootsSize, bootsPurchDate, bootsPurchAmount, uSkaterUUID, bootID) VALUES ('Generic', 'Generic', 0, CURDATE(), 0, %s, 2);"

    # Create a set of blades and frames for the new user's ID
    creStep5 = "INSERT INTO uSkaterBlades (bladesName, bladesModel, bladesSize, bladesPurchDate, bladesPurchAmount, uSkaterUUID, bladeID) VALUES ('Generic', 'Generic', 0, CURDATE(), 0, %s, 1);"
    creStep6 = "INSERT INTO uSkaterBlades (bladesName, bladesModel, bladesSize, bladesPurchDate, bladesPurchAmount, uSkaterUUID, bladeID) VALUES ('Generic', 'Generic', 0, CURDATE(), 0, %s, 2);"

    # Create an off and on ice skate from the above configs. One each. Set them to Active, assign to the new user ID
    creStep7 = "INSERT INTO uSkateConfig (uSkaterUUID, uSkaterBladesID, uSkaterBootsID, sType, sActive, aSkateConfigID) VALUES (%s, 1, 1, 1, 1, 1)"
    creStep8 = "INSERT INTO uSkateConfig (uSkaterUUID, uSkaterBladesID, uSkaterBootsID, sType, sActive, aSkateConfigID) VALUES (%s, 2, 2, 2, 1, 2)"

    # Create an initial entry in ice_time, required for the whole thing to work for some reason. Must be assigned to new user ID
    creStep9 = "INSERT INTO ice_time (date, ice_time, ice_cost, skate_type, coach_time, coach_id, rink_id, has_video, has_notes, uSkaterUUID, uSkaterConfig) VALUES (CURDATE(), 0, 0, 1, 0, 0, 0, 0, 0, %s, 1)"

    # Create an inital in the maintenance table, also required for things to work for some reason. Must be assigned to new user ID
    creStep10 = "INSERT INTO maintenance (m_date, m_hours_on, m_cost, m_location, conf_id, notes, uSkaterUUID) VALUES (CURDATE(), 0, 0, 0, 1, 0, %s)"

    # If we made it to this point, create a login/password referenced by the user's ID in the aUserTable
    creStep11 = "INSERT INTO aUserTable (uSkaterUUID, uLoginID, uHash) VALUES (%s, 'login', 'password')"

    newSkaterBulk(creStep1, LII)
    print('step 1... done')
    newSkaterBulk(creStep3, LII)
    print('step 3... done')
    newSkaterBulk(creStep4, LII)
    print('step 4... done')
    newSkaterBulk(creStep5, LII)
    print('step 5... done')
    newSkaterBulk(creStep6, LII)
    print('step 6... done')
    newSkaterBulk(creStep7, LII)
    print('step 7... done')
    newSkaterBulk(creStep8, LII)
    print('step 8... done')
    newSkaterBulk(creStep9, LII)
    print('step 9... done')
    newSkaterBulk(creStep10, LII)
    print('step 10... done')
    newSkaterBulk(creStep11, LII)
    print('step 11... done')

    print('complete! Check User ID', LII)

    return
