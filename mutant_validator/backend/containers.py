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
    v_len: int = 0
    h_len: int = 0

    def is_mutant(self) -> bool:
        return any([self._mutant_in_horizontal()])

    def _mutant_in_horizontal(self) -> bool:
        if not self.skip_h_check:
            for pos in range(0, (self.h_len - 3)):
                if self.h[pos] == self.h[pos + 1] == self.h[pos + 2] == self.h[pos + 3]:
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
