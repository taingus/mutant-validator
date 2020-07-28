import re
from typing import List

from pydantic import (
    BaseModel,
    validator,
)

DNA_VALID_REGEX = re.compile(r"[^ATCG]+?", re.IGNORECASE)


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
            [
                self._check_line(self.v, self.skip_v_check),
                self._check_line(self.h, self.skip_h_check),
                self._check_line(self.f),
                self._check_line(self.b),
            ]
        )

    def _check_line(self, line: str, skip: bool = False) -> bool:
        if not skip:
            for pos in range(0, (len(line) - (self.gen_length - 1))):
                if line[pos] == line[pos + 1] == line[pos + 2] == line[pos + 3]:
                    return True
        return False


class DNASequence(str):
    def validate(self) -> bool:
        return not DNA_VALID_REGEX.search(self)


class DNA(BaseModel):
    dna: List[str]

    @validator("dna", each_item=True)
    def valid_chain(cls, v: str) -> str:
        if DNA_VALID_REGEX.search(v):
            raise ValueError("Invalid DNA sequence")
        return v.upper()
