from pony.orm import Database
from app.config import config
from app.utils.logger import logger

_db = None

def dbcon():
    global _db
    
    if not _db:
        _db = Database()
        _db.bind(
            provider=config.PROVIDER,
            user=config.USER,
            password=config.PASSWORD,
            host=config.HOST,
            port=config.PORT,
            database=config.DBNAME,
            sslmode="require"
        )
    
    return _db


def init_db():
    db = dbcon()

    # import model
    import app.db.models

    db.generate_mapping(create_tables=False)

    logger.info("[DB] Pony ORM initialized")
