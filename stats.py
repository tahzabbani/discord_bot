import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

con = sqlite3.connect('stats.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS user_time_table (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT UNIQUE, previous_time TIMESTAMP, timeshow TIMESTAMP, time_spent INTEGER)")
con.commit()
con.close()

#        minutes = divmod(now, 60)[0] 


def update_timestamp(user, time):
    con = sqlite3.connect('stats.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_time_table (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT UNIQUE, previous_time TIMESTAMP, timeshow TIMESTAMP, time_spent INTEGER)")

    cur.execute("INSERT OR IGNORE INTO user_time_table(username) VALUES ('" + user + "')")
    cur.execute("UPDATE user_time_table SET previous_time = timeshow WHERE username ='" + user + "'")
    cur.execute("UPDATE user_time_table SET timeshow ='" + str(time) + "'WHERE username ='" + user + "'")
    con.commit()
    con.close()

def update_time_diff(user, time):
    con = sqlite3.connect('stats.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_time_table (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT UNIQUE, previous_time TIMESTAMP, timeshow TIMESTAMP, time_spent INTEGER)")
    cur.execute("SELECT previous_time FROM user_time_table WHERE username ='" + user + "'")
    get_time = cur.fetchone()[0]
    if (get_time != None and get_time != 0):
        time_diff = time - get_time
    else:
        time_diff = 0
    cur.execute("SELECT time_spent FROM user_time_table WHERE username ='" + user + "'")
    get_db_total_time = cur.fetchone()[0]

    if (get_db_total_time == None):
        get_db_total_time = 0

    # minutes = (time_diff.seconds//60)%60

    if time_diff != 0:
        minutes = time_diff.seconds
    else:
        minutes = 0

    print(time)
    print(get_time)

    int(get_db_total_time)
    int(minutes)

    get_db_total_time += minutes
    cur.execute("UPDATE user_time_table SET time_spent =" + str(get_db_total_time) + " WHERE username ='" + user + "'")
    con.commit()
    con.close()
    return get_db_total_time
    # cur.execute("INSERT OR IGNORE INTO user_time_table(username, time_spent) VALUES (" + user + ", " + get_db_total_time + ")")

now = datetime.now()

# update_timestamp("tahseen", now)
# update_timestamp("mark", now)

# print(update_time_diff("tahseen", now))
# update_time_diff("mark", now)

def generate_graph():
    con = sqlite3.connect('stats.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_time_table (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT UNIQUE, previous_time TIMESTAMP, timeshow TIMESTAMP, time_spent INTEGER)")
    cur.execute("SELECT username FROM user_time_table")
    names = cur.fetchall()
    fig = plt.figure()
    cur.execute("SELECT time_spent FROM user_time_table")
    times = cur.fetchall()
    plt.bar([x for t in names for x in t], [y for t in times for y in t])
    plt.savefig("./images/mygraph.png")
    
generate_graph()

con = sqlite3.connect('stats.db',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cur = con.cursor()
cur.execute("SELECT * FROM user_time_table")
rows = cur.fetchall()
for row in rows:
    print(row)
con.commit()
con.close()