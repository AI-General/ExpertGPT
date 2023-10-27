from datetime import datetime
from uuid import UUID
import uuid

import psycopg2
from models.settings import get_postgres_conn

def is_user_in_db (email: str):
    conn = None
    try: 
        conn = get_postgres_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        print("Query executed successfully")
        rows = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    if len(rows) == 1:
        return True
    else:
        return False

def add_user_in_db (email: str, hashed_password: str):
    user_id = uuid.uuid4()
    conn = None
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("INSERT INTO users(user_id, email, password, date, requests_count) VALUES(%s, %s, %s, %s, %s)", (str(user_id), email, hashed_password, str(datetime.now()), 0))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return user_id
