from fastapi.testclient import TestClient
from fastapi import status
from mutant_validator.main import app

client = TestClient(app)


def test_validate_mutant_dna_ok_response():
    response = client.post("/mutant", json={"dna": ["AAAA"]})

    assert response.status_code == status.HTTP_200_OK


def test_validate_mutant_dna_forbidden_response():
    response = client.post("/mutant", json={"dna": ["ACTG"]})

    assert response.status_code == status.HTTP_403_FORBIDDEN
