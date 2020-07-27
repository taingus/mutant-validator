from pydantic import BaseModel, validator
import re

DNA_VALID_REGEX = re.compile(r"[^ATCG]+?", re.IGNORECASE)


class Node(BaseModel):
    v: str = ""
    h: str = ""
    f: str = ""
    b: str = ""

    skip_v_check: bool = False
    skip_h_check: bool = False

    gen_length: int = 4

    @validator("v", "h", "f", "b")
    def valid_chain(cls, v):
        if DNA_VALID_REGEX.search(v):
            raise ValueError("Invalid DNA sequence")
        return v.upper()
