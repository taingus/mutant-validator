from mutant_validator.backend.containers import DNASequence
from mutant_validator.backend.validator import is_mutant


def test_valid_DNA_sequence_horizontal_first_occurence():
    assert is_mutant(["AAAATGA"]) is True


def test_valid_DNA_sequence_horizontal_second_occurence():
    assert is_mutant(["TAAAAGA"]) is True


def test_valid_DNA_sequence_horizontal_third_occurence():
    assert is_mutant(["TGAAAAA"]) is True


def test_valid_DNA_sequence_horizontal_fourth_occurence():
    assert is_mutant(["TGTAAAA"]) is True


def test_valid_DNA_sequence_horizontal_not_mutant():
    assert is_mutant(["TGTAAAT"]) is False


def test_valid_DNA_sequence_vertical():
    pass


def test_valid_DNA_sequence_diagonal_forward():
    pass


def test_valid_DNA_sequence_diagonal_backwards():
    pass
