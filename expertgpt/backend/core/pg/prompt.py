import uuid

import psycopg2
from models.settings import get_postgres_conn
from models.databases.pg.prompts import CreatePromptProperties, Prompt


def create_prompt(prompt: CreatePromptProperties) -> Prompt:
    id = uuid.uuid4()
    conn = None
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("INSERT INTO prompts(id, title, content, status) VALUES(%s, %s, %s, %s)", (str(id), prompt.title, prompt.content, prompt.status))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return Prompt(id=id, **prompt)