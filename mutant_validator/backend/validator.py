from typing import (
    List,
    Union,
)

from .containers import DNASequence


def is_mutant(sequence: List[Union[DNASequence, str]]):
    if isinstance(sequence, str):
        sequence = DNASequence(str)
