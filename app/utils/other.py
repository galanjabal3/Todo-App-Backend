import bcrypt
from typing import List, Dict, Any


def hash_string(value: str) -> str:
    """Hash string using bcrypt and return as string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(value.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_string(provided_value: str, stored_hash: str) -> bool:
    """Verify string against stored bcrypt hash."""
    return bcrypt.checkpw(
        provided_value.encode("utf-8"),
        stored_hash.encode("utf-8"),
    )

def list_filter_to_dict(filters: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {dfilter['field']: dfilter['value'] for dfilter in filters}

def list_filter_dict_to_list(filters: Dict[str, Any] = None):
    return [{'field': key, 'value': filters[key]} for key in (filters or {}).keys()]