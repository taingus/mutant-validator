from pytest import raises

from mutant_validator.backend.containers import (
    DNASequence,
    Node,
)


def test_node_with_valid_DNA_sequence():
    result = Node(v="AAAAAA")

    assert result.v == "AAAAAA"


def test_node_with_valid_DNA_sequence_is_capitalized():
    result = Node(v="aaaaaa")

    assert result.v == "AAAAAA"


def test_node_fails_with_invalid_DNA_sequence():
    with raises(ValueError) as result:
        Node(v="invaliddnasequence")

    assert result.value.errors()[0]["msg"] == "Invalid DNA sequence"


def test_dna_with_valid_DNA_sequence():
    result = DNASequence("AAAAAA")

    assert result.validate() is True


def test_dna_with_valid_DNA_sequence_is_capitalized():
    result = DNASequence("aaaaaa")

    assert result.validate() is True


def test_dna_fails_with_invalid_DNA_sequence():
    result = DNASequence("invaliddnasequence")

    assert result.validate() is False
