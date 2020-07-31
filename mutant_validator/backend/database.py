import databases
import sqlalchemy

from mutant_validator.config import DATABASE_URL

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)


def migrate():
    # Acts as a hack for migrations, not scalable
    metadata.create_all(engine)


def get_db() -> databases.Database:
    return database
