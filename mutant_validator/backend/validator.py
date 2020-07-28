from typing import (
    List,
    Union,
)

from .containers import (
    DNA,
    Node,
)


def is_mutant(sequence: Union[List[str], DNA]):
    if isinstance(sequence, list):
        sequence = DNA(dna=sequence)

    for line in sequence.dna:
        node = Node(h=line)

        if node.is_mutant():
            return True

    for x in range(0, len(sequence.dna[0])):
        pass
    return False
