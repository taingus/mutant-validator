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

    v_len = len(sequence.dna)
    h_len = len(sequence.dna[0])

    total_mutant_sequences = 0

    if h_len > 3:
        for pos, line in enumerate(sequence.dna):
            f_line = ""
            b_line = ""
            if v_len > 3:
                f_line = "".join(
                    [
                        sequence.dna[pos + x][x]
                        for x in range(0, v_len - pos)
                        if pos + x < h_len and pos + x < v_len
                    ]
                )
                if pos > 2:
                    b_line = "".join(
                        [
                            sequence.dna[pos + x][v_len - 1 - x]
                            for x in range(0, v_len - pos)
                            if pos + x < h_len and pos + x < v_len
                        ]
                    )
            node = Node(h=line, f=f_line, b=b_line, skip_v_check=True)

            total_mutant_sequences += node.count_mutant_genes()
            if total_mutant_sequences > 1:
                return True

    if v_len > 3:
        for col in range(0, len(sequence.dna[0])):
            f_line = ""
            b_line = ""
            if h_len > 3:
                f_line = "".join(
                    [
                        sequence.dna[x][col + x]
                        for x in range(0, h_len - col)
                        if col + x < h_len and col + x < v_len
                    ]
                )
                if col > 2:
                    b_line = "".join(
                        [
                            sequence.dna[x][col - x]
                            for x in range(0, col + 1)
                            if h_len - x >= 0 and v_len - x >= 0 and col - x >= 0
                        ]
                    )

            v_line = "".join([sequence.dna[x][col] for x in range(0, v_len)])
            node = Node(v=v_line, f=f_line, b=b_line, skip_h_check=True)

            total_mutant_sequences += node.count_mutant_genes()
            if total_mutant_sequences > 1:
                return True

    return False
