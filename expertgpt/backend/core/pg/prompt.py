import uuid
from uuid import UUID

import psycopg2
from models.settings import get_postgres_conn
from models.prompt import CreatePromptProperties, Prompt, PromptUpdatableProperties

def get_public_prompts() -> list[Prompt]:
    """
    List all public prompts
    """
    rows = []
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("SELECT * FROM prompts WHERE status = 'public'")
        rows = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    return [Prompt(id=row[0], title=row[1], content=row[2], status=row[3]) for row in rows]

def get_prompt_by_id(prompt_id: UUID) -> Prompt | None:
    """
    Get a prompt by its id

    Args:
        prompt_id (UUID): The id of the prompt

    Returns:
        Prompt: The prompt
    """
    row = None
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("SELECT * FROM prompts WHERE id = %s", (str(prompt_id), ))
        row = cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
    if row:
        return Prompt(id=row[0], title=row[1], content=row[2], status=row[3])
    else:
        return None

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
    return Prompt(id=id, **prompt.dict())

def update_prompt_by_id(
    prompt_id: UUID, prompt: PromptUpdatableProperties
) -> Prompt:
    conn = None
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        if prompt.title:
            cur.execute("UPDATE prompts SET title = %s WHERE id = %s", (prompt.title, str(prompt_id)))
            conn.commit()
        if prompt.content:
            cur.execute("UPDATE prompts SET content = %s WHERE id = %s", (prompt.content, str(prompt_id)))
            conn.commit()
        if prompt.status:
            cur.execute("UPDATE prompts SET status = %s WHERE id = %s", (prompt.status, str(prompt_id)))
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()

    return get_prompt_by_id(prompt_id)
