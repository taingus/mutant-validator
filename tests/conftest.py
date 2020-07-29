from typing import (
    Callable,
    Generator,
    List,
)

from databases import Database
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine

from mutant_validator.backend.database import (
    get_db,
    metadata,
)
from mutant_validator.main import app

TEST_DATABASE_URL = "sqlite:///mutant_validator/test_db.sqlite3"

db_test = Database(TEST_DATABASE_URL, force_rollback=True)
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


def override_get_db() -> Database:
    return db_test


@pytest.fixture()
def db() -> Generator:
    metadata.create_all(engine)
    yield db_test
    metadata.drop_all(engine)


@pytest.fixture()
def client() -> Generator:
    metadata.create_all(engine)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    metadata.drop_all(engine)


@pytest.fixture
def generate_vertical_dna(column: int = 1, line: int = 1) -> Callable:
    def _generate(column: int = 1, line: int = 1) -> List[str]:
        dna = [
            "CGTCGTC",
            "CGTCGTC",
            "GTCGTCG",
            "GTCGTCG",
            "TCGTCGT",
            "TCGTCGT",
            "CGTCGTC",
        ]
        if column == 0 and line == 0:
            return dna

        for li in range(line - 1, line + 3):
            dna[li] = f"{dna[li][:column - 1]}A{dna[li][column:]}"

        return dna

    return _generate


@pytest.fixture
def mutant_diagonal_forward_dna_middle() -> List[str]:
    return [
        "CGTCGTC",
        "CATCGTC",
        "GTAGTCG",
        "GTCATCG",
        "TCGTAGT",
        "TCGTCGT",
        "CGTCGTC",
    ]


@pytest.fixture
def mutant_diagonal_forward_dna_middle_down() -> List[str]:
    return [
        "CGTCGTC",
        "CGTCGTC",
        "GTCGTCG",
        "ATCGTCG",
        "TAGTCGT",
        "TCATCGT",
        "CGTAGTC",
    ]


@pytest.fixture
def mutant_diagonal_forward_dna_middle_up() -> List[str]:
    return [
        "CGTAGTC",
        "CGTCATC",
        "GTCGTAG",
        "GTCGTCA",
        "TCGTCGT",
        "TCGTCGT",
        "CGTCGTC",
    ]


@pytest.fixture
def mutant_diagonal_backward_dna_middle() -> List[str]:
    return [
        "CGTCGTA",
        "CGTCGAC",
        "GTCGACG",
        "GTCATCG",
        "TCGTCGT",
        "TCGTCGT",
        "CGTCGTC",
    ]


@pytest.fixture
def mutant_diagonal_backward_dna_middle_up() -> List[str]:
    return [
        "CGTAGTC",
        "CGACGTC",
        "GACGTCG",
        "ATCGTCG",
        "TCGTCGT",
        "TCGTCGT",
        "CGTCGTC",
    ]


@pytest.fixture
def mutant_diagonal_backward_dna_middle_down() -> List[str]:
    return [
        "CGTCGTC",
        "CGTCGTC",
        "GTCGTCG",
        "GTCGTCA",
        "TCGTCAT",
        "TCGTAGT",
        "CGTAGTC",
    ]
