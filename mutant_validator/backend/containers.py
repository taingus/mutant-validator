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
