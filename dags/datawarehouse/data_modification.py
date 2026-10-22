import logging

logger = logging.getLogger(__name__)
table="yt_api"
def insert_data(cursor, conn, row, schema):
    try:

        if schema=='staging':
             video_id='video_id'

             cursor.execute(
                f"""INSERT INTO {schema}.{table} (video_id, title, published_at, duration, view_count, like_count, comment_count)
                VALUES (%(video_id)s, %(title)s, %(published_at)s, %(duration)s, %(view_count)s, %(like_count)s, %(comment_count)s)""", row)
        else:
            video_id='video_id'

            cursor.execute(
                  f"""INSERT INTO {schema}.{table} (video_id, title, published_at, duration, video_type, view_count, like_count, comment_count)
                    VALUES (%(video_id)s, %(title)s, %(published_at)s, %(duration)s, %(video_type)s, %(view_count)s, %(like_count)s, %(comment_count)s)""", row)
        conn.commit()
        logger.info(f"Inserted data for video_id: {row['video_id']}")
    except Exception as e:
        logger.error(f"Error inserting data for video_id: {row['video_id']}")
        raise e
def update_row(cursor, conn, row, schema):
    try:
        if schema == 'staging':
            cursor.execute(
                f"""UPDATE {schema}.{table} SET title=%(title)s, published_at=%(published_at)s, duration=%(duration)s, view_count=%(view_count)s, like_count=%(like_count)s, comment_count=%(comment_count)s WHERE video_id=%(video_id)s""", row)
        else:
            cursor.execute(
                f"""UPDATE {schema}.{table} SET title=%(title)s, published_at=%(published_at)s, duration=%(duration)s, video_type=%(video_type)s, view_count=%(view_count)s, like_count=%(like_count)s, comment_count=%(comment_count)s WHERE video_id=%(video_id)s""", row)
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
        