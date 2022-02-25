#!/usr/bin/env python2

import os
import sqlite3

def build_database(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE memos ( ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Title TEXT, Desc TEXT )")
    conn.commit()

def add_memo(conn):
    title = raw_input("Title: ")
    desc = raw_input("Description: ")
    
    cur = conn.cursor()
    cur.execute("INSERT INTO memos (Title, Desc) VALUES (?, ?)", (title, desc))
    conn.commit()

def rm_memo(conn):
    id = raw_input("ID: ")
    
    cur = conn.cursor()
    cur.execute("DELETE FROM memos WHERE ID=?", (id, ))
    conn.commit()

def list_memo(conn):
    cur = conn.cursor()
    for row in cur.execute("SELECT ID, Title FROM memos"):
        print row[0], ":", row[1]

def get_memo(conn):
    id = raw_input("ID: ")
    
    cur = conn.cursor()
    cur.execute("SELECT Title, Desc FROM memos WHERE ID=?", (id, ))
    row = cur.fetchone()
    
    if row is not None:
        print "Title:", row[0]
        print "Description:", row[1]

if __name__ == "__main__":
    conn = sqlite3.connect("database_test.db")
    command = None
    
    while True:
        try:
            command = raw_input("-> ")
            print
            
            if command == "rebuild":
                conn.rollback()
                conn.close()
                os.remove("database_test.db")
                conn = sqlite3.connect("database_test.db")
                build_database(conn)
            elif command == "add":
                add_memo(conn)
            elif command == "rm":
                rm_memo(conn)
            elif command == "list":
                list_memo(conn)
            elif command == "get":
                get_memo(conn)
            else:
                print "Bad Command!"
            
            print
        except EOFError:
            print
            break
    
    conn.commit()
    conn.close()
