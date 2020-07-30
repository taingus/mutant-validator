from fastapi import status


def test_validate_mutant_dna_ok_response(client):
    response = client.post("/mutant", json={"dna": ["AAAA"]})

    assert response.status_code == status.HTTP_200_OK


def test_validate_mutant_dna_forbidden_response(client):
    response = client.post("/mutant", json={"dna": ["ACTG"]})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_mutant_stats_with_no_data(client):
    response = client.get("/stats").json()

    assert response["count_mutant_dna"] == 0
    assert response["count_human_dna"] == 0
    assert response["ratio"] == 0.0


def test_get_mutant_stats_with_one_human(client, db_human):
    response = client.get("/stats").json()

    assert response["count_mutant_dna"] == 0
    assert response["count_human_dna"] == 1
    assert response["ratio"] == 0.0


def test_get_mutant_stats_with_one_mutant(client, db_mutant):
    response = client.get("/stats").json()

    assert response["count_mutant_dna"] == 1
    assert response["count_human_dna"] == 0
    assert response["ratio"] == 0.0


def test_get_mutant_stats_with_one_mutant_and_one_human(client, db_mutant, db_human):
    response = client.get("/stats").json()

    assert response["count_mutant_dna"] == 1
    assert response["count_human_dna"] == 1
    assert response["ratio"] == 1.0


def test_get_mutant_stats_with_one_mutant_and_two_human(client, db_mutant, db_human):
    response = client.post("/mutant", json={"dna": ["ctag"]})
    response = client.get("/stats").json()

    assert response["count_mutant_dna"] == 1
    assert response["count_human_dna"] == 2
    assert response["ratio"] == 0.5
