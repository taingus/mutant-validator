from pytest import raises

from mutant_validator.backend.containers import (
    Node,
    DNA,
    DNASequence,
)


def test_DNASequence_with_valid_DNA_sequence():
    result = DNASequence("AaaAAA")

    assert result.validate() is True


def test_DNASequence_fails_with_invalid_DNA_sequence():
    result = DNASequence("invaliddnasequence")

    assert result.validate() is False


def test_dna_with_valid_dna_sequence():
    result = DNA(dna=["AAAAAA"])

    assert result.dna[0] == "AAAAAA"


def test_dna_with_valid_DNA_sequence_is_capitalized():
    result = DNA(dna=["aaaaaa"])

    assert result.dna[0] == "AAAAAA"


def test_dna_fails_with_invalid_DNA_sequence():
    with raises(ValueError) as result:
        DNA(dna=["aaaa", "invaliddnasequence"])

    assert result.value.errors()[0]["msg"] == "Invalid DNA sequence"


def test_node_with_horizontal_string_found():
    string = "aagxxxxxxttt"
    node = Node(h=string)

    assert node.is_mutant() is True


def test_node_with_horizontal_string_not_found():
    string = "abcdefghiiikl"
    node = Node(h=string)

    assert node.is_mutant() is False


def test_node_with_vertical_string_found():
    string = "aagxxxxxxttt"
    node = Node(h=string)

    assert node.is_mutant() is True


def test_node_with_vertical_string_not_found():
    string = "abcdefghiiikl"
    node = Node(v=string)

    assert node.is_mutant() is False


def test_node_with_forward_diagonal_string_found():
    string = "aagxxxxxxttt"
    node = Node(f=string)

    assert node.is_mutant() is True


def test_node_with_forward_diagonal_string_not_found():
    string = "abcdefghiiikl"
    node = Node(f=string)

    assert node.is_mutant() is False


def test_node_with_backward_diagonal_string_found():
    string = "aagxxxxxxttt"
    node = Node(b=string)

    assert node.is_mutant() is True


def test_node_with_backward_diagonal_string_not_found():
    string = "abcdefghiiikl"
    node = Node(b=string)

    assert node.is_mutant() is False
