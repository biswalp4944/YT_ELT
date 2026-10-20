import logging

logger = logging.getLogger(__name__)
table="yt_api"
def insert_data(cursor, conn, row, schema):
    try:

        if schema=='staging':
             video_id='video_id'

             cursor.execute(
                f"""INSERT INTO {schema}.{table} (video_id, video_title, Upload_date, Duration, Video_views, Video_likes, Video_comments)
                VALUES (%(video_id)s, %(video_title)s, %(Upload_date)s, %(Duration)s, %(Video_views)s, %(Video_likes)s, %(Video_comments)s)""", row)
        else:
            video_id='video_id'

            cursor.execute(
                  f"""INSERT INTO {schema}.{table} (video_id, video_title, Upload_date, Duration,Video_Type, Video_views, Video_likes, Video_comments)
                    VALUES (%(video_id)s, %(video_title)s, %(Upload_date)s, %(Duration)s, %(Video_Type)s, %(Video_views)s, %(Video_likes)s, %(Video_comments)s)""", row)
        conn.commit()
        logger.info(f"Inserted data for video_id: {row['video_id']}")
    except Exception as e:
        logger.error(f"Error inserting data for video_id: {row['video_id']}")
        raise e
def update_row(cursor, conn, row, schema):
    try:
        if schema == 'staging':
            cursor.execute(
                f"""UPDATE {schema}.{table} SET video_title=%(video_title)s, Upload_date=%(Upload_date)s, Duration=%(Duration)s, Video_views=%(Video_views)s, Video_likes=%(Video_likes)s, Video_comments=%(Video_comments)s WHERE video_id=%(video_id)s""", row)
        else:
            cursor.execute(
                f"""UPDATE {schema}.{table} SET video_title=%(video_title)s, Upload_date=%(Upload_date)s, Duration=%(Duration)s, Video_Type=%(Video_Type)s, Video_views=%(Video_views)s, Video_likes=%(Video_likes)s, Video_comments=%(Video_comments)s WHERE video_id=%(video_id)s""", row)
        conn.commit()
        logger.info(f"Updated data for video_id: {row['video_id']}")
    except Exception as e:
        logger.error(f"Error updating data for video_id: {row['video_id']}")
        raise e
    def delete_row(cursor, conn, ids_to_delete, schema):
        try:
            ids_to_delete=f"""{','.join([f"'{id}'" for id in ids_to_delete])}"""
            cursor.execute(f"""DELETE FROM {schema}.{table} WHERE video_id IN ({ids_to_delete})""")
            conn.commit()
            logger.info(f"Deleted data for video_ids: {ids_to_delete}")
        except Exception as e:
            logger.error(f"Error deleting data for video_ids: {ids_to_delete}")
            raise e
        