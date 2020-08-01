import cProfile
import pstats

import pytest

from mutant_validator.backend.validator import is_mutant


def test_valid_DNA_sequence_horizontal_first_occurence():
    assert is_mutant(["AAAATGA", "AAAAAAA"]) is True


def test_valid_DNA_sequence_horizontal_second_occurence():
    assert is_mutant(["TAAAAGA", "AAAAAAA"]) is True


def test_valid_DNA_sequence_horizontal_third_occurence():
    assert is_mutant(["TGAAAAA", "AAAAAAA"]) is True


def test_valid_DNA_sequence_horizontal_fourth_occurence():
    assert is_mutant(["TGTAAAA", "AAAAAAA"]) is True


def test_valid_DNA_sequence_horizontal_not_mutant():
    assert is_mutant(["TGTAAAT", "AAAAAAA"]) is False


def test_valid_DNA_sequence_horizontal_too_short():
    assert is_mutant(["T"]) is False


def test_valid_DNA_sequence_horizontal_long_enough():
    assert is_mutant(["TTTT", "AAAA"]) is True


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


def test_valid_DNA_sequence_diagonal_forward_middle(mutant_diagonal_forward_dna_middle):
    assert is_mutant(mutant_diagonal_forward_dna_middle) is True


def test_valid_DNA_sequence_diagonal_forward_middle_up(
    mutant_diagonal_forward_dna_middle_up,
):
    assert is_mutant(mutant_diagonal_forward_dna_middle_up) is True


def test_valid_DNA_sequence_diagonal_forward_middle_down(
    mutant_diagonal_forward_dna_middle_down,
):
    assert is_mutant(mutant_diagonal_forward_dna_middle_down) is True


def test_valid_DNA_sequence_diagonal_backward_middle(
    mutant_diagonal_backward_dna_middle,
):
    assert is_mutant(mutant_diagonal_backward_dna_middle) is True


def test_valid_DNA_sequence_diagonal_backward_middle_up(
    mutant_diagonal_backward_dna_middle_up,
):
    assert is_mutant(mutant_diagonal_backward_dna_middle_up) is True


def test_valid_DNA_sequence_diagonal_backward_middle_down(
    mutant_diagonal_backward_dna_middle_down,
):
    assert is_mutant(mutant_diagonal_backward_dna_middle_down) is True


def test_valid_DNA_sequence_diagonal_backward_middle_small_vertical(
    mutant_diagonal_backward_dna_middle_small_vertical,
):
    assert is_mutant(mutant_diagonal_backward_dna_middle_small_vertical) is True


def test_valid_DNA_sequence_diagonal_backward_middle_small_horizontal(
    mutant_diagonal_backward_dna_middle_small_horizontal,
):
    assert is_mutant(mutant_diagonal_backward_dna_middle_small_horizontal) is True


def test_performance_valid_DNA_sequence_human(gigantic_human_dna):
    with cProfile.Profile() as pr:
        assert is_mutant(gigantic_human_dna) is False
    pstats.Stats(pr).sort_stats("cumtime").print_stats()
