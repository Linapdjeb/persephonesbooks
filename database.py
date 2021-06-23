
from helpers import error
import sqlite3
import os

currentdir = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(currentdir + "/PBooks.db", check_same_thread=False)
# conn.row_factory = sqlite3.Row


def select_user(username):
    c = conn.cursor()
    try:
        result = c.execute("SELECT * FROM users WHERE username = '" + username + "';")
    except:
        return error("something went wrong in the system", 400)
    result = result.fetchall()
    # result = [x[0] for x in c.fetchall()]
    conn.commit()
    c.close()
    return result


def get_user(id):
    c = conn.cursor()
    try:
        output = c.execute(f"SELECT * FROM users WHERE id = {id};")
    except:
        return error("something went wrong in the system", 400)
    result = output.fetchall()
    conn.commit()
    c.close()
    return result


def get_username(id):
    c = conn.cursor()
    try:
        output = c.execute(f"SELECT username FROM users WHERE id = {id};")
    except:
        return error("something went wrong in the system", 400)
    result = output.fetchall()
    conn.commit()
    c.close()
    return result


def get_users():
    c = conn.cursor()
    try:
        result = c.execute("SELECT * FROM users")
    except:
        return error("something went wrong in the system", 400)
    result = result.fetchall()
    # result = [x[0] for x in c.fetchall()]
    conn.commit()
    c.close()
    return result


def insert_user(username, hash, email):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, hash, email) values(?, ?, ?)", (username, hash, email))
        id = c.lastrowid
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return id


def update_userinfo(fullname, profession, address, pinfo, id):
    c = conn.cursor()
    try:
        c.execute(f"UPDATE userinfo SET fullname = '{fullname}', profession = '{profession}', address = '{address}', pinfo = '{pinfo}' WHERE user_id = '{id}';")
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return True


def insert_userinfo(fullname, profession, address, pinfo, id):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO userinfo (fullname, profession, address, pinfo, user_id) values(?, ?, ?, ?, ?);", (fullname, profession, address, pinfo, id))
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return True

def get_userinfo(id):
    c = conn.cursor()
    try:
        output = c.execute(f"SELECT * FROM userinfo WHERE user_id = {id};")
    except:
        return error("something went wrong in the system", 400)
    info = output.fetchall()
    conn.commit()
    c.close()
    return info


def update_password(password, id):
    c = conn.cursor()
    try:
        c.execute(f"UPDATE users SET hash = '{password}' WHERE id = {id};")
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return True



def insertpost(title, intro, mainbody, conclusion, author):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO posts (title, intro, mainbody, conclusion, date, author) values(?, ?, ?, ?, datetime('now','localtime'), ?);", (title, intro, mainbody, conclusion, author))
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return True


def get_posts():
    c = conn.cursor()
    try:
        # ORDER BY id DESC
        output = c.execute("SELECT * FROM posts ORDER BY id DESC;")
    except:
        return error("something went wrong in the system", 400)
    result = output.fetchall()
    conn.commit()
    c.close()
    return result


def getpost(title):
    c = conn.cursor()
    try:
        # ORDER BY id DESC
        output = c.execute(f"SELECT * FROM posts WHERE title = '{title}';")
    except:
        return error("something went wrong in the system", 400)
    result = output.fetchall()
    conn.commit()
    c.close()
    return result


def get_myposts(name):
    c = conn.cursor()
    try:
        output = c.execute(f"SELECT * FROM posts WHERE author = '{name}' ORDER BY id DESC;")
    except:
        return error("something went wrong in the system", 400)
    result = output.fetchall()
    conn.commit()
    c.close()
    return result


def deletepost(title, name):
    c = conn.cursor()
    try:
        c.execute(f"DELETE FROM posts WHERE author = '{name}' AND title = '{title}';")
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return True


def addnote(title, content, id):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO notebook (title, content, date, user_id) values(?, ?, datetime('now','localtime'), ?);", (title, content, id))
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return True


def getnotes(id):
    c = conn.cursor()
    try:
        output = c.execute(f"SELECT * FROM notebook WHERE user_id = {id} ORDER BY id DESC;")
    except:
        return error("something went wrong in the system", 400)
    result = output.fetchall()
    conn.commit()
    c.close()
    return result


def editnote(title, content, id):
    c = conn.cursor()
    try:
        c.execute(F"UPDATE notebook SET content = '{content}', date = datetime('now','localtime') WHERE title = '{title}' AND user_id = {id};")
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return True

def deletenote(title, id):
    c = conn.cursor()
    try:
        c.execute(f"DELETE FROM notebook WHERE user_id = {id} AND title = '{title}';")
    except:
        return error("something went wrong in the system", 400)
    conn.commit()
    c.close()
    return True