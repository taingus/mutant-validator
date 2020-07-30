import re
from typing import List

from pydantic import (
    BaseModel,
    validator,
)

DNA_VALID_REGEX = re.compile(r"[^ACGT]+?", re.IGNORECASE)


class Node(BaseModel):
    v: str = ""
    h: str = ""
    f: str = ""
    b: str = ""

    skip_v_check: bool = False
    skip_h_check: bool = False

    gen_length: int = 4

    def is_mutant(self) -> bool:
        return any(
            (
                self._check_line(self.v, self.skip_v_check),
                self._check_line(self.h, self.skip_h_check),
                self._check_line(self.f),
                self._check_line(self.b),
            )
        )

    def _check_line(self, line: str, skip: bool = False) -> bool:
        return not skip and any(
            line[pos] == line[pos + 1] == line[pos + 2] == line[pos + 3]
            for pos in range(0, (len(line) - (self.gen_length - 1)))
        )


class DNASequence(str):
    def validate(self) -> bool:
        return not DNA_VALID_REGEX.search(self)


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
