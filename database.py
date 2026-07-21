# database.py

import sqlite3

DB_NAME = "data.db"


def connect():

    conn = sqlite3.connect(
        DB_NAME,
        timeout=30
    )

    conn.execute(
        "PRAGMA busy_timeout = 30000"
    )

    return conn



def setup_database():

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS groups(
        chat_id INTEGER PRIMARY KEY,
        title TEXT
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        photo TEXT,
        minutes INTEGER
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS subscribers(
        user_id INTEGER PRIMARY KEY
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        user_id INTEGER PRIMARY KEY
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        id INTEGER PRIMARY KEY,
        enabled INTEGER,
        current_post INTEGER,
        welcome TEXT,
        send_private INTEGER
    )
    """)


    cur.execute("""
    INSERT OR IGNORE INTO settings
    (
        id,
        enabled,
        current_post,
        welcome,
        send_private
    )
    VALUES
    (
        1,
        0,
        0,
        '👋 Welcome to {group_name}!\n\n🤖 Bot is ready.',
        0
    )
    """)


    conn.commit()
    conn.close()



# ================= GROUP =================


def add_group(chat_id, title):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO groups(chat_id,title) VALUES(?,?)",
        (chat_id,title)
    )

    conn.commit()
    conn.close()



def get_groups():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT chat_id,title FROM groups"
    )

    data = cur.fetchall()

    conn.close()

    return data



def remove_group(chat_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM groups WHERE chat_id=?",
        (chat_id,)
    )

    conn.commit()
    conn.close()



# ================= POSTS =================


def add_post(text, photo, minutes):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO posts
        (text,photo,minutes)
        VALUES(?,?,?)
        """,
        (text,photo,minutes)
    )

    conn.commit()
    conn.close()



def get_posts():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id,text,photo,minutes FROM posts"
    )

    data = cur.fetchall()

    conn.close()

    return data



# ================= SUBSCRIBERS =================


def add_subscriber(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO subscribers(user_id) VALUES(?)",
        (user_id,)
    )

    conn.commit()
    conn.close()



def get_subscribers():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM subscribers"
    )

    data = cur.fetchall()

    conn.close()

    return data



# ================= ADMINS =================


def add_admin(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO admins(user_id) VALUES(?)",
        (user_id,)
    )

    conn.commit()
    conn.close()



def get_admins():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM admins"
    )

    data = cur.fetchall()

    conn.close()

    return data



def remove_admin(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM admins WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()



# ================= SETTINGS =================


def get_settings():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT enabled,current_post,welcome,send_private
        FROM settings
        WHERE id=1
        """
    )

    data = cur.fetchone()

    conn.close()

    return data



def update_settings(
    enabled=None,
    current_post=None,
    welcome=None,
    send_private=None
):

    conn = connect()
    cur = conn.cursor()


    if enabled is not None:

        cur.execute(
            "UPDATE settings SET enabled=? WHERE id=1",
            (enabled,)
        )


    if current_post is not None:

        cur.execute(
            "UPDATE settings SET current_post=? WHERE id=1",
            (current_post,)
        )


    if welcome is not None:

        cur.execute(
            "UPDATE settings SET welcome=? WHERE id=1",
            (welcome,)
        )


    if send_private is not None:

        cur.execute(
            "UPDATE settings SET send_private=? WHERE id=1",
            (send_private,)
        )


    conn.commit()
    conn.close()



def update_current_post(post_id):

    update_settings(
        current_post=post_id
    )