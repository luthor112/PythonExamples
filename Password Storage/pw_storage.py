#!/usr/bin/env python2

import binascii
import getpass
import os
import os.path
import scrypt
import sqlite3

def build_database():
    database = sqlite3.connect("database.db")
    cur = database.cursor()
    
    cur.execute("CREATE TABLE passwords ( Name TEXT NOT NULL PRIMARY KEY UNIQUE, PasswordHash TEXT NOT NULL )")
    
    database.commit()
    database.close()

def add_user(database):
    username = raw_input("Name: ")
    password = getpass.getpass("Password: ")
    salt = os.urandom(8)
    password_hash = scrypt.hash(password, salt)
    
    cur = database.cursor()
    cur.execute("INSERT INTO passwords (Name, PasswordHash) VALUES (?, ?)", (username, binascii.hexlify(salt+password_hash)))
    database.commit()
    
    print "User created!"

def check_user(database):
    username = raw_input("Name: ")
    password = getpass.getpass("Password: ")
    
    cur = database.cursor()
    cur.execute("SELECT PasswordHash FROM passwords WHERE Name=?", (username, ))
    row = cur.fetchone()
    
    if row is not None:
        salt_and_hash = binascii.unhexlify(row[0])
        if scrypt.hash(password, salt_and_hash[:8]) == salt_and_hash[8:]:
            print "OK!"
        else:
            print "Invalid credentials!"
    else:
        print "User does not exist!"

if __name__ == "__main__":
    if not os.path.exists("database.db"):
        build_database()
    
    database = sqlite3.connect("database.db")
    command = None
    
    while True:
        try:
            command = raw_input("-> ")
            print
            
            if command == "new":
                add_user(database)
            elif command == "check":
                check_user(database)
            else:
                print "Bad Command!"
            
            print
        except EOFError:
            print
            break
    
    database.commit()
    database.close()
