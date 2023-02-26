import sqlite3
from sqlite3 import Error
from datetime import datetime
import os
from venv import create
import matplotlib.pyplot as plt
import numpy as np

con = sqlite3.connect('strikes.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        return conn
    except Error as e:
        print(e)
    return conn

def add_strike(user):
    con = create_connection('strikes.db')
    cur = con.cursor()

    # create table, insert value if didn't exist and update by 1
    cur.execute("CREATE TABLE IF NOT EXISTS user_table (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT UNIQUE, strikes INTEGER)")
    cur.execute("INSERT OR IGNORE INTO user_table (username, strikes) VALUES (?, 0)", (user,))
    cur.execute("UPDATE user_table SET strikes = strikes + 1 WHERE username=?", (user,))
    
    con.commit()
    con.close()
    
def remove_strike(user):
    con = create_connection('strikes.db')
    cur = con.cursor()
    cur.execute("UPDATE user_table SET strikes = strikes - 1 WHERE username=?", (user,))
    con.commit()
    con.close()

    
def show_strike_graph():
    con = create_connection('strikes.db')
    cur = con.cursor()
    
    cur.execute("SELECT username, strikes FROM user_table")
    strike_pair = cur.fetchall()

    fig = plt.figure(figsize = (10, 5))
 
    user_list = [tup[0] for tup in strike_pair]
    strike_list = [tup[1] for tup in strike_pair]

    
    #creating the bar plot 
    plt.barh(user_list, strike_list)
 
    for index, value in enumerate(strike_list):
        plt.text(value, index,
                str(value))
    
    plt.xlabel("User")
    plt.ylabel("Strikes")
    plt.title("Strikes for Discord User")
    
    plt.savefig('./images/strikegraph.png')
    # plt.show()
    con.close()

    
# def remove_row():