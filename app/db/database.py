from pony.orm import Database
from app.config import config

def dbcon(database=config.DBNAME):
    db = Database()
    db.bind(
        provider=config.PROVIDER,
        user=config.USER,
        password=config.PASSWORD,
        host=config.HOST,
        port=config.PORT,
        database=database,
        sslmode="require"
    )
    return db
