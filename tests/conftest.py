from typing import List, Callable
import pytest


@pytest.fixture
def generate_vertical_dna(column: int = 1, line: int = 1) -> Callable:
    def _generate(column: int = 1, line: int = 1) -> List[str]:
        dna = [
            "GTGTGTG",
            "TGTGTGT",
            "GTGTGTG",
            "TGTGTGT",
            "GTGTGTG",
            "TGTGTGT",
            "GTGTGTG",
        ]
        if column == 0 and line == 0:
            return dna

        for li in range(line - 1, line + 3):
            dna[li] = f"{dna[li][:column - 1]}A{dna[li][column:]}"

        return dna

    return _generate
