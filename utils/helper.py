from datetime import datetime, date

def convert_date_to_datetime(value: date | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.combine(value, datetime.min.time())

def parse_mongo_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc