from typing import List, Callable
import pytest


@pytest.fixture
def generate_vertical_dna(column: int = 1, line: int = 1) -> Callable:
    def _generate(column: int = 1, line: int = 1) -> List[str]:
        dna = [
            "GTGTGTG",
            "TCTCTCT",
            "GTGTGTG",
            "TCTCTCT",
            "GTGTGTG",
            "TCTCTCT",
            "GTGTGTG",
        ]
        if column == 0 and line == 0:
            return dna

        for li in range(line - 1, line + 3):
            dna[li] = f"{dna[li][:column - 1]}A{dna[li][column:]}"

        return dna

    return _generate


@pytest.fixture
def mutant_diagonal_forward_dna() -> List[str]:
    return [
        "GTGTGTG",
        "TCTCTCT",
        "GTCTGTG",
        "TCTCTCT",
        "GTGTCTG",
        "TCTCTCT",
        "GTGTGTG",
    ]


@pytest.fixture
def mutant_diagonal_backward_dna() -> List[str]:
    return [
        "GTGTGTG",
        "TCTCTCT",
        "GTCTGTG",
        "TCTCTCT",
        "CTGTGTG",
        "TCTCTCT",
        "GTGTGTG",
    ]
