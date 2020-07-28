from typing import (
    Callable,
    List,
)

import pytest


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
