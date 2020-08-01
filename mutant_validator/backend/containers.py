from typing import List

from pydantic import (
    BaseModel,
    validator,
)

from mutant_validator.config import (
    DNA_VALID_REGEX,
    MUTANT_DNA_CHAINS,
)


class Node(BaseModel):
    v: str = ""
    h: str = ""
    f: str = ""
    b: str = ""

    skip_v_check: bool = False
    skip_h_check: bool = False

    gen_length: int = 4

    def count_mutant_genes(self) -> int:
        return sum(
            (
                self._check_line(self.v, self.skip_v_check),
                self._check_line(self.h, self.skip_h_check),
                self._check_line(self.f),
                self._check_line(self.b),
            )
        )

    def _check_line(self, line: str, skip: bool = False) -> bool:
        return not skip and any(x in line for x in MUTANT_DNA_CHAINS)


class DNA(BaseModel):
    dna: List[str]

    @validator("dna")
    def valid_chain(cls, v: List[str]) -> List[str]:
        if len(v) == 0:
            raise ValueError("Empty DNA sequence")

        max_len = len(v[0])
        for pos, line in enumerate(v):
            if len(line) != max_len or DNA_VALID_REGEX.search(line):
                raise ValueError("Invalid DNA sequence")
            v[pos] = line.upper()
        return v


class DNAStats(BaseModel):
    count_mutant_dna: int = 0
    count_human_dna: int = 0
    ratio: float = 0
