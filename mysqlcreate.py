import mysql.connector

def accounttable():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password',
        database='notler')

    mycursor = db.cursor()

    mycursor.execute("CREATE TABLE IF NOT EXISTS account(username VARCHAR(100) PRIMARY KEY, email_id VARCHAR(300), password VARCHAR(300))")

def notetable():
    db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='notler')

    mycursor = db.cursor()

    mycursor.execute("CREATE TABLE IF NOT EXISTS notes(username VARCHAR(100) PRIMARY KEY, note1 VARCHAR(1000), note2 VARCHAR(1000),\
                     note3 VARCHAR(1000), note4 VARCHAR(1000), note5 VARCHAR(1000))")

def notetittletable():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password',
        database='notler'
    )

    mycursor = db.cursor()

    mycursor.execute("CREATE TABLE IF NOT EXISTS notetittle(username VARCHAR(100) PRIMARY KEY, note1tittle VARCHAR(1000), note2tittle VARCHAR(1000), note3tittle VARCHAR(1000), note4tittle VARCHAR(1000), note5tittle VARCHAR(1000))")
