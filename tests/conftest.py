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
from mutant_validator.backend.models import validated_dna
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
            "TTTTTTT",
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
        "CGAAAAC",
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
        "CGAAAAC",
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
        "CGAAAAC",
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
        "CGAAAAA",
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
        "CGAAAAA",
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
        "CGAAAAA",
        "CGTCGTC",
        "GTCGTCG",
        "GTCGTCA",
        "TCGTCAT",
        "TCGTAGT",
        "CGTAGTC",
    ]


@pytest.fixture
def mutant_diagonal_backward_dna_middle_small_horizontal() -> List[str]:
    return [
        "GTCGTC",
        "GTCGTC",
        "TCAAAA",
        "TCGTCA",
        "CGTCAT",
        "CGTAGT",
        "GTAGTC",
    ]


@pytest.fixture
def mutant_diagonal_backward_dna_middle_small_vertical() -> List[str]:
    return [
        "GTCGGTAAA",
        "GTCGTCAGA",
        "TCGTCGAAT",
        "AGGTCTACA",
        "TGGTCACAA",
    ]


@pytest.fixture
def gigantic_human_dna() -> List[str]:
    return [
        "CGTCGTC" * 1000,
        "CGTCGTC" * 1000,
        "GTCGTCG" * 1000,
        "GTCGTCG" * 1000,
    ] * 1000


@pytest.fixture
async def db_mutant(db) -> None:
    await db.execute(
        validated_dna.insert().values(sha="sha_mutant", dna="mutant", mutant=True)
    )


@pytest.fixture
async def db_human(db) -> None:
    await db.execute(
        validated_dna.insert().values(sha="sha_human", dna="human", mutant=False)
    )
