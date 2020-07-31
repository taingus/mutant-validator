import os
import re

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///mutant_validator/db.sqlite3")

DNA_VALID_REGEX = re.compile(r"[^ACGT]+?", re.IGNORECASE)
MUTANT_DNA_CHAINS = ("A" * 4, "C" * 4, "T" * 4, "G" * 4)
