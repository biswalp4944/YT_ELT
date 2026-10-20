import json
from datetime import date
import logging
#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_path():

    file_path = f"data/yt_api_data_{date.today()}.json"
    try:
        logger.info(f"Processing file: YT_data_{date.today()}")
        with open(file_path, 'r',encoding='utf-8') as json_file:
            data = json.load(json_file)
            logger.info(f"Successfully loaded data from {file_path}")
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {file_path}")
        raise  