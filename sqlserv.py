import sqlite3
import asyncio
import aiosqlite as sq
# Connect to the database
try:
    con = sqlite3.connect("users.db")
    print("conected")
    cur = con.cursor()
    #cur.execute(f'DELETE FROM notes WHERE user_id = 705256742') #удалить все заметки по айдишнику
    #cur.execute("DROP TABLE notes")
    #cur.execute("DROP TABLE notifications")
    #cur.execute("CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY, user_id INT, txt char NOT NULL, date DATETIME)")
    #cur.execute("CREATE TABLE IF NOT EXISTS notifications(id INTEGER PRIMARY KEY, user_id INT, txt char NOT NULL)")
    #cur.execute("INSERT INTO notifications(user_id, txt) VALUES(?,?)", (31286767312, 'тест работы',))
    #cur.execute('INSERT INTO notes(user_id, txt, date) VALUES(?, ?, ?)', (321123123, "test", 20240209210000,))
    #print(cur.execute("SELECT txt FROM notes"))
    #now = cur.execute('SELECT date("now") FROM customers')
    #cur.execute(f"DELETE FROM customers WHERE id")
    #ndate = cur.execute(f"SELECT id, JULIANDAY(date) - JULIANDAY(date('now')) FROM customers")
    #print(ndate.fetchall())

    con.commit()
    con.close()  
except Exception as ex:
    print("Connection refused...")
    print(ex)

"""#cur.execute('ALTER TABLE customers DROP date')
    cur.execute("ALTER TABLE customers ADD id INT PRIMARY KEY NOT NULL")"""
"""try:
    with sqlite3.connect("users.db") as con:
        cur = con.cursor()
        #cur.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY, date DATETIME)")
        #cur.execute(f"INSERT INTO test(date) VALUES(trftime('%d','now'))")
        #p = (cur.execute("SELECT COUNT(*) FROM notes WHERE user_id = 1133461404"))
        #print (cur.fetchone()[0])
        #cur.execute(f'INSERT INTO notes(user_id, txt, date) VALUES(31286767312, "тест работы", {cur.execute('SELECT strftime("%Y","now")')}{cur.execute('SELECT strftime("%m","now")')}10151500)')
        #print(cur.execute('SELECT strftime("%Y","now")'))
except Exception as ex: 
    print("Connection refused...")
    print(ex)

"""

