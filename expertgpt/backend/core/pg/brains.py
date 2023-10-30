from uuid import UUID, uuid4

import psycopg2
from logger import get_logger
from models.brains import CreateBrainProperties
from models.brain_entity import BrainEntity, MinimalBrainEntity
from models.settings import get_postgres_conn

logger = get_logger(__name__)

def get_user_brains(user_id) -> list[MinimalBrainEntity]:
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("""
                SELECT brains_users.brain_id AS brain_id, rights, brains.name
                FROM brains_users
                INNER JOIN brains ON brains_users.brain_id = brains.brain_id
                WHERE brains_users.user_id = %s
                """, (str(user_id),))

        rows = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
        message = {"message": "Error deleting API key."}
    finally:
        if conn is not None:
            conn.close()

    user_brains: list[MinimalBrainEntity] = []
    for row in rows:
        user_brains.append(
            MinimalBrainEntity(
                id=row[0],
                name=row[2],
                rights=row[1],
            )
        )
    return user_brains


def get_brain_by_id(brain_id: UUID) -> BrainEntity | None:
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT brain_id, name, status, description, prompt_id, linkedin, extraversion, neuroticism, conscientiousness
            FROM brains
            WHERE brain_id = %s
            """, (str(brain_id), ))

        row = cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
        return None
    finally:
        if conn is not None:
            conn.close()

    return BrainEntity(id=row[0], name=row[1], status=row[2], description=row[3], prompt_id=row[4], linkedin=row[5], extraversion=row[6], neuroticism=row[7], conscientiousness=row[8])


def get_user_default_brain(user_id: UUID) -> BrainEntity | None:
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT brain_id
            FROM brains_users
            WHERE user_id = %s AND default_brain = %s
            """, (str(user_id), True))

        row = cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        conn.rollback()
        return None
    finally:
        if conn is not None:
            conn.close()

    if row is None:
        return None
    brain_id = row[0]
    if brain_id is None:
        return None

    logger.info(f"Default brain id: {brain_id}")

    return get_brain_by_id(brain_id)


def create_brain(brain: CreateBrainProperties):
    brain_id = uuid4()
    try:        
        conn = get_postgres_conn()
        cur = conn.cursor()

        fields ="brain_id, " + ", ".join(brain.dict().keys())
        values = "%s, " + ", ".join(["%s" for _ in brain.dict().values()])

        insert_query = f"INSERT INTO brains ({fields}) VALUES ({values}) RETURNING *;"
        cur.execute(insert_query, [str(brain_id)] + list(brain.dict().values()))
        conn.commit()
    except Exception as e:
        print(f"Error creating new API key: {e}")
        return {"api_key": "Error creating new API key."}
    
    if conn is not None:
        conn.close()

    return BrainEntity(brain_id=brain_id, **brain.dict())

def create_brain_user(user_id: UUID, brain_id, rights, is_default_brain: bool) -> None:
    try:
        conn = get_postgres_conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO brains_users (brain_id, user_id, rights, default_brain) VALUES (%s, %s, %s, %s) RETURNING *;
            """, (str(brain_id), str(user_id), rights, is_default_brain))
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while executing PostgreSQL", error)
        logger.error("Error while executing PostgreSQL", error)
        conn.rollback()
        return None
    finally:
        if conn is not None:
            conn.close()
            logger.info("Successfully inserted new brain user.")


