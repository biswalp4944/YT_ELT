from airflow import DAG
import pendulum
from datetime import timedelta,datetime
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json

#define the local timezone
local_tz = pendulum.timezone("Asia/Kolkata")

#default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'email':'biswalp4944@yopmail.com',
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'max_active_runs':1,
    'dagrun_timeout': timedelta(minutes=60),
    'start_date': datetime(2026, 1, 1, tzinfo=local_tz),
    #'end_date': datetime(2030, 1, 1, tzinfo=local_tz),
}

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='A DAG to extract video data from YouTube API and save it to a JSON file',
    schedule_interval='15 1 * * *',  # Run daily at 2PM IST
    catchup=False,
) as dag:
    # Define the tasks in the DAG
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extracted_data = extract_video_data(video_ids)
    save_to_json_task=save_to_json(extracted_data)

    #define task dependencies
    playlist_id >> video_ids >> extracted_data >> save_to_json_task