from  airflow.providers.postgres.hooks.postgres import PostgresHook # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
table="yt_api"
def get_conn_cursor():
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db")
    conn = hook.get_conn()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cursor

def close_conn_cursor(conn, cursor):
    cursor.close()
    conn.close()

def create_schema(schema):
    conn, cursor = get_conn_cursor()
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    #cursor.execute(schema_sql) # type: ignore
    conn.commit()
    close_conn_cursor(conn, cursor)

def create_table(schema, table):
    conn, cursor = get_conn_cursor()
    if schema=='staging':
        table_sql = f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                "video_id" VARCHAR(11) PRIMARY KEY NOT NULL,
                "title" TEXT NOT NULL,
                "published_at" TIMESTAMP NOT NULL,
                "duration" VARCHAR(20) NOT NULL,
                "view_count" INT,
                "like_count" INT,
                "comment_count" INT,
                "video_type" VARCHAR(20) DEFAULT 'NA' NOT NULL

            )
        """
    else:
        table_sql = f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                "video_id" VARCHAR(11) PRIMARY KEY NOT NULL,
                "title" TEXT NOT NULL,
                "published_at" TIMESTAMP NOT NULL,
                "duration" VARCHAR(20) NOT NULL,
                "view_count" INT,
                "like_count" INT,
                "comment_count" INT,
                "video_type" VARCHAR(20) NOT NULL
            
            )
        """
    cursor.execute(table_sql)
    conn.commit()
    close_conn_cursor(conn, cursor)

def  get_video_ids(cursor,schema):
    cursor.execute(f"SELECT video_id FROM {schema}.{table}")
    ids = cursor.fetchall()

    video_ids=[row['video_id'] for row in ids]
    return video_ids
    