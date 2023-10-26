from uuid import UUID
from models.settings import get_postgres_conn

def is_user_in_db (email: str):
    conn = get_postgres_conn()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users WHERE email={email};')
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    if len(rows) == 1:
        return True
    else:
        return False

def add_user_in_db (email: str):
    user_id = UUID(bytes=email.encode(), version=4)
    conn = get_postgres_conn()
    cur = conn.cursor()

    cur.execute(f"INSERT INTO users(user_id, email) VALUES({user_id}, {email})")
    conn.commit()
    cur.close()
    conn.close()
    return user_id
