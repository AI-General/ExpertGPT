from datetime import datetime
from secrets import token_hex
from uuid import uuid4

from asyncpg import UniqueViolationError
import psycopg2

from models.settings import get_postgres_conn
from models.users import User


def create_api_key(current_user: User):
    new_key_id = uuid4()
    new_api_key = token_hex(16)
    api_key_inserted = False

    while not api_key_inserted:
        try:
            conn = get_postgres_conn()
            cur = conn.cursor()

            cur.execute("INSERT INTO api_keys(key_id, user_id, api_key, creation_time, is_active) VALUES(%s, %s, %s, %s, %s)", (str(new_key_id), str(current_user.id), str(new_api_key), datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), True))
            api_key_inserted = True
            conn.commit()

        except UniqueViolationError:
            # Generate a new API key if the current one is already in use
            new_api_key = token_hex(16)
        except Exception as e:
            print(f"Error creating new API key: {e}")
            return {"api_key": "Error creating new API key."}
    print(f"Created new API key for user {current_user.email}.")

    return {"api_key": new_api_key, "key_id": str(new_key_id)}

def delete_api_key(key_id, user_id):
    conn = None
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("""UPDATE api_keys 
                SET is_active = %s, deleted_time = %s
                WHERE key_id = %s AND user_id = %s""",
                (False, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), str(key_id), str(user_id)))
        conn.commit()
        print(f"API key with id {key_id} for user {user_id} has been deactivated.")
        message = {"message": "API key deleted."}

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
        message = {"message": "Error deleting API key."}
    finally:
        if conn is not None:
            conn.close()
    return message

def get_api_keys_by_user_id(userid):
    conn = None
    rows = []
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM api_keys WHERE user_id = %s AND is_active = true", (str(userid), ))
        rows = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return [{"key_id": row[0], "creation_time": str(row[3])} for row in rows]
