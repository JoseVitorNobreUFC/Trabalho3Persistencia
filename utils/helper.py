from datetime import datetime, date
from bson.objectid import ObjectId

def convert_date_to_datetime(value: date | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.combine(value, datetime.min.time())

def parse_mongo_id(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    return doc

def generate_id() -> str:
    return ObjectId()

def get_game_id(id: int) -> str:
    _ids = [
    "68784fedf83530f11d7925c7",
    "68784fedf83530f11d7925c8",
    "68784fedf83530f11d7925c9",
    "68784fedf83530f11d7925ca",
    "68784fedf83530f11d7925cb",
    "68784fedf83530f11d7925cc",
    "68784fedf83530f11d7925cd",
    "68784fedf83530f11d7925ce",
    "68784fedf83530f11d7925cf",
    "68784fedf83530f11d7925d0",
    "68784fedf83530f11d7925d1",
    "68784fedf83530f11d7925d2",
    "68784fedf83530f11d7925d3",
    "68784fedf83530f11d7925d4",
    "68784fedf83530f11d7925d5",
    "68784fedf83530f11d7925d6",
    "68784fedf83530f11d7925d7",
    "68784fedf83530f11d7925d8",
    "68784fedf83530f11d7925d9",
    "68784fedf83530f11d7925da",
    "68784fedf83530f11d7925db",
    "68784fedf83530f11d7925dc",
    "68784fedf83530f11d7925dd",
    "68784fedf83530f11d7925de",
    "68784fedf83530f11d7925df",
    "68784fedf83530f11d7925e0",
    "68784fedf83530f11d7925e1",
    "68784fedf83530f11d7925e2",
    "68784fedf83530f11d7925e3",
    "68784fedf83530f11d7925e4"
]
    return _ids[id]