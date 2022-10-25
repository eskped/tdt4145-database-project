
import sqlite3
from sqlite3 import OperationalError

def createDatabaseWithData():
    executeScriptsFromFile("KaffeDB.sql")
    executeScriptsFromFile("KaffeDBfillData.sql")

def executeScriptsFromFile(filename):
    con = sqlite3.connect("Kaffe.db")
    cursor = con.cursor()
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    try:
        for command in sqlCommands:
            cursor.execute(command)
    except OperationalError as msg:
        print ("Command skipped: ", msg)
    con.commit()
    con.close()

createDatabaseWithData()