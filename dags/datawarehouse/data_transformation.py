from datetime import timedelta, datetime
from isodate import parse_duration as parse_iso_duration # type: ignore

def parse_duration(duration_str):
    return parse_iso_duration(duration_str)

    components = ['D', 'H', 'M', 'S']
    values= {'D': 0, 'H': 0, 'M': 0, 'S': 0}

    for component in components:
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            values[component] = int(value)

    total_duration = timedelta(
        days=values['D'], hours=values['H'], minutes=values['M'], seconds=values['S'])
    
    return total_duration

def transform_data(row):
    row = row.copy()  # Create a copy of the row to avoid modifying the original
    duration_td= parse_duration(row['duration'])
    row['duration'] = (datetime.min + duration_td).time()
    row['video_type'] ='shorts' if duration_td.total_seconds() <= 60 else 'Normal'
    return row