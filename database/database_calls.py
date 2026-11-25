import sqlite3

def username_in_db(username):
    con = sqlite3.connect("C:\\Users\miran\PycharmProjects\IM_NEA_prototypes\database\database.db")
    c = con.cursor()
    c.execute("SELECT * FROM account WHERE username = ?;", (username,))
    user_exists = bool(c.fetchone())
    con.close()
    return user_exists

def get_user(username):
    con = sqlite3.connect("C:\\Users\miran\PycharmProjects\IM_NEA_prototypes\database\database.db")
    c = con.cursor()
    c.execute("SELECT * FROM account WHERE username = ?;", (username,))
    account_id, username, email_address, hashed_password, salt, locked = c.fetchone()
    con.close()
    values_dict = {
        "username": username,
        "hashed_password": hashed_password,
        "salt": salt,
        "locked": locked
    }
    return values_dict

def add_user(username, email, hashed_password, salt):
    con = sqlite3.connect("C:\\Users\miran\PycharmProjects\IM_NEA_prototypes\database\database.db")
    c = con.cursor()
    c.execute("INSERT INTO account (username, email, hashed_password, salt, locked) VALUES (?, ?, ?, ?, False);",
              (username, email, hashed_password, salt))
    con.commit()
    con.close()