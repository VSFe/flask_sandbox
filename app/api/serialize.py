from datetime import date, datetime

def to_serializable(_dict):
    return { key : val.isoformat() if isinstance(val, (datetime, date)) \
        else val for key, val in _dict.items()}