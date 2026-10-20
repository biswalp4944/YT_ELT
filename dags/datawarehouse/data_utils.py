from  airflow.providers.postgres.hooks.postgres import PostgresHook
from pyscope2.extras import RealDictCursor
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
    cursor.execute(schema_sql)
    conn.commit()
    close_conn_cursor(conn, cursor)

def create_table(schema, table):
    conn, cursor = get_conn_cursor()
    if schema=='staging':
        table_sql = f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                "video_id" VARCHAR(11) PRIMARY KEY NOT NULL,
                "video_title" TEXT NOT NULL,
                "Upload_date" TIMESTAMP NOT NULL,
                "Duration" VARCHAR(20) NOT NULL,
                "Video_views" INT,
                "Video_likes" INT,
                "Video_comments" INT,

            )
        """
    else:
        table_sql = f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                "video_id" VARCHAR(11) PRIMARY KEY NOT NULL,
                "video_title" TEXT NOT NULL,
                "Upload_date" TIMESTAMP NOT NULL,
                "Duration" VARCHAR(20) NOT NULL,
                "Video_views" INT,
                "Video_likes" INT,
                "Video_comments" INT,
            
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
    