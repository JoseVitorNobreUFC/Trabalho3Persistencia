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

def create_id(id: str):
    return ObjectId(id)

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

def get_user_id(id: int) -> str:
    _ids = [
    "687d9f367d19253f7c53928d",
    "687d9f367d19253f7c53928e",
    "687d9f367d19253f7c53928f",
    "687d9f367d19253f7c539290",
    "687d9f367d19253f7c539291",
    "687d9f367d19253f7c539292",
    "687d9f367d19253f7c539293",
    "687d9f367d19253f7c539294",
    "687d9f367d19253f7c539295",
    "687d9f367d19253f7c539296",
    "687d9f367d19253f7c539297",
    "687d9f367d19253f7c539298",
    "687d9f367d19253f7c539299",
    "687d9f367d19253f7c53929a",
    "687d9f367d19253f7c53929b",
    "687d9f367d19253f7c53929c",
    "687d9f367d19253f7c53929d",
    "687d9f367d19253f7c53929e",
    "687d9f367d19253f7c53929f",
    "687d9f367d19253f7c5392a0",
    "687d9f367d19253f7c5392a1",
    "687d9f367d19253f7c5392a2",
    "687d9f367d19253f7c5392a3",
    "687d9f367d19253f7c5392a4",
    "687d9f367d19253f7c5392a5",
    "687d9f367d19253f7c5392a6",
    "687d9f367d19253f7c5392a7",
    "687d9f367d19253f7c5392a8",
    "687d9f367d19253f7c5392a9",
    "687d9f367d19253f7c5392aa"
]
    return _ids[id]

def get_family_id(id: int) -> str:
    _ids = [
    "687d9fd634988e8641806a68",
    "687d9fd634988e8641806a69",
    "687d9fd634988e8641806a6a",
    "687d9fd634988e8641806a6b",
    "687d9fd634988e8641806a6c",
    "687d9fd634988e8641806a6d",
    "687d9fd634988e8641806a6e",
    "687d9fd634988e8641806a6f"
    ]
    return _ids[id]