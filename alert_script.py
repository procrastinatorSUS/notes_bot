import sqlite3 as sq
import time
import requests


def checktime():
    while True:
        time.sleep(1)
        with sq.connect('users.db') as db:
            cursor = db.execute('SELECT id, user_id, txt, unixepoch(date) - unixepoch(datetime(CURRENT_TIMESTAMP, "localtime")) from notes')
            check = cursor.fetchall()
            for i in check:
                if int(i[3]) < 0:
                    db.execute('INSERT INTO notifications(user_id, txt) VALUES(?, ?)',(i[1],i[2]))
                    db.execute(f'DELETE FROM notes WHERE id = {i[0]}')
                    db.commit()
def notice():
    while True:    
        with sq.connect('users.db') as db:
            time.sleep(10)
            cursor = db.execute('SELECT id, user_id, txt from notifications')
            alert = cursor.fetchall()
            for i in alert:
                requests.get(f"https://api.telegram.org/bot6552323918:AAHexHWmhL-khv6iL1J_6Mc2BQB-pXqeS5o/sendMessage?chat_id={i[1]}&text={i[2]}\n\nЧтобы отключить отправку сообщений напишите команду /stopnotifications")

if __name__ == '__main__':
    checktime()