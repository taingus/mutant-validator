from databases import Database
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from mutant_validator.backend.database import (
    get_db,
    metadata,
)
from mutant_validator.main import app

TEST_DATABASE_URL = "sqlite:///mutant_validator/test_db.sqlite3"

db_test = Database(TEST_DATABASE_URL, force_rollback=True)
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

metadata.drop_all(engine)
metadata.create_all(engine)


def override_get_db() -> Database:
    return db_test


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_validate_mutant_dna_ok_response():
    response = client.post("/mutant", json={"dna": ["AAAA"]})

    assert response.status_code == status.HTTP_200_OK


def test_validate_mutant_dna_forbidden_response():
    response = client.post("/mutant", json={"dna": ["ACTG"]})

    assert response.status_code == status.HTTP_403_FORBIDDEN
