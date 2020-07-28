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


def test_valid_DNA_sequence_vertical_first_column(generate_vertical_dna):
    assert is_mutant(generate_vertical_dna(column=1)) is True


def test_valid_DNA_sequence_vertical_second_column(generate_vertical_dna):
    assert is_mutant(generate_vertical_dna(column=2)) is True


def test_valid_DNA_sequence_vertical_third_column(generate_vertical_dna):
    assert is_mutant(generate_vertical_dna(column=3)) is True


def test_valid_DNA_sequence_vertical_first_column_second_line(generate_vertical_dna):
    assert is_mutant(generate_vertical_dna(column=1, line=2)) is True


def test_valid_DNA_sequence_vertical_second_column_third_line(generate_vertical_dna):
    assert is_mutant(generate_vertical_dna(column=2, line=3)) is True


def test_valid_DNA_sequence_vertical_third_column_fourth_line(generate_vertical_dna):
    assert is_mutant(generate_vertical_dna(column=3, line=4)) is True


def test_valid_DNA_sequence_no_mutant(generate_vertical_dna):
    assert is_mutant(generate_vertical_dna(column=0, line=0)) is False


def test_valid_DNA_sequence_diagonal_forward():
    pass


def test_valid_DNA_sequence_diagonal_backwards():
    pass
