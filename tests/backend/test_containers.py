from pytest import raises

from mutant_validator.backend.containers import (
    DNA,
    DNASequence,
)


def test_DNASequence_with_valid_DNA_sequence():
    result = DNASequence("AaaAAA")

    assert result.validate() is True


def test_DNASequence_fails_with_invalid_DNA_sequence():
    result = DNASequence("invaliddnasequence")

    assert result.validate() is False


def test_DNA_with_valid_dna_sequence():
    result = DNA(dna=["AAAAAA"])

    assert result.dna[0] == "AAAAAA"


def test_node_with_valid_DNA_sequence_is_capitalized():
    result = DNA(dna=["aaaaaa"])

    assert result.dna[0] == "AAAAAA"


def test_node_fails_with_invalid_DNA_sequence():
    with raises(ValueError) as result:
        DNA(dna=["aaaa", "invaliddnasequence"])

    assert result.value.errors()[0]["msg"] == "Invalid DNA sequence"
