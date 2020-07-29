import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///mutant_validator/db.sqlite3")
