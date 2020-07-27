from mutant_validator.backend.validator import is_mutant
from mutant_validator.backend.containers import DNASequence


def test_valid_DNA_sequence_horizontal_first_occurence():
    assert is_mutant(DNASequence("AAAATGA")) is True


def test_valid_DNA_sequence_horizontal_second_occurence():
    assert is_mutant(DNASequence("TAAAAGA")) is True


def test_valid_DNA_sequence_horizontal_third_occurence():
    assert is_mutant(DNASequence("TGAAAAA")) is True


def test_valid_DNA_sequence_horizontal_fourth_occurence():
    assert is_mutant(DNASequence("TGTAAAA")) is True


def test_valid_DNA_sequence_horizontal_not_mutant():
    assert is_mutant(DNASequence("TGTAAAT")) is False


def test_valid_DNA_sequence_vertical():
    pass


def test_valid_DNA_sequence_diagonal_forward():
    pass


def test_valid_DNA_sequence_diagonal_backwards():
    pass
