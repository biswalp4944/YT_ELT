from datawarehouse.data_loading import load_path
from datawarehouse.data_transformation import transform_data
from datawarehouse.data_modification import insert_data, update_row, delete_row
from datawarehouse.data_utils import get_conn_cursor,close_conn_cursor,create_schema,create_table,get_video_ids

import logging
from airflow.decorators import task # type: ignore

logger = logging.getLogger(__name__)
table="yt_api"

@task
def staging_table():
    schema='staging'
    conn,cursor=None,None

    try:
        conn, cursor = get_conn_cursor()
        YT_data=load_path()

        create_schema(schema)
        create_table(schema,table)

        table_ids=get_video_ids(cursor,schema)

        for row in YT_data:
            row = row.copy()  # Create a copy of the row to avoid modifying the original
            row=transform_data(row)
            if len(table_ids)==0:
                insert_data(cursor, conn, row, schema)

            else:
               

                if row['video_id'] in table_ids:
                    update_row(cursor, conn, row, schema)
                else:
                    insert_data(cursor, conn, row, schema)

        ids_in_json = {row['video_id'] for row in YT_data}
        ids_to_delete = set(table_ids) - ids_in_json

        if ids_to_delete:
            delete_row(cursor, conn, ids_to_delete, schema)

        logger.info(f"Schema '{schema}' table processing completed successfully.")
    except Exception as e:
        logger.error(f"Error processing schema '{schema}' table:{e}")
        raise e 
    finally:
        if conn and cursor:
            close_conn_cursor(conn, cursor)   

@task
def production_table():
    schema='production'
    conn,cursor=None,None

    try:
        conn, cursor = get_conn_cursor()

        create_schema(schema)
        create_table(schema,table)

        table_ids=get_video_ids(cursor,schema)

        current_video_ids=set()

        cursor.execute(f"SELECT *FROM STAGING.{table}" )
        rows =cursor.fetchall()
        for row in rows:
            current_video_ids.add(row['video_id'])
            if len(table_ids)==0:
                insert_data(cursor, conn, row, schema)

            else:
                if row['video_id'] in table_ids:
                    update_row(cursor, conn, row, schema)
                else:
                    insert_data(cursor, conn, row, schema)

        ids_to_delete = set(table_ids) - current_video_ids

        if ids_to_delete:
            delete_row(cursor, conn, ids_to_delete, schema)

        logger.info(f"Schema '{schema}' table updated successfully.")  

    except Exception as e:
        logger.error(f"Error processing schema '{schema}' table: {e}")
        raise e      