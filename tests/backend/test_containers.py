from pytest import raises

from mutant_validator.backend.containers import (
    DNA,
    Node,
)


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


def test_dna_fails_with_different_length_sequences():
    with raises(ValueError) as result:
        DNA(dna=["aaaa", "aaaaaa"])

    assert result.value.errors()[0]["msg"] == "Invalid DNA sequence"


def test_dna_fails_with_empty_sequence():
    with raises(ValueError) as result:
        DNA(dna=[])

    assert result.value.errors()[0]["msg"] == "Empty DNA sequence"


def test_node_with_horizontal_string_too_short():
    string = "AAA"
    node = Node(h=string)

    assert node.is_mutant() is False


def test_node_with_horizontal_string_long_enough_found():
    string = "AAAA"
    node = Node(h=string)

    assert node.is_mutant() is True


def test_node_with_horizontal_string_found():
    string = "AAGCCCCCCTTT"
    node = Node(h=string)

    assert node.is_mutant() is True


def test_node_with_horizontal_string_not_found():
    string = "ABCDEFGHIIIKL"
    node = Node(h=string)

    assert node.is_mutant() is False


def test_node_with_vertical_string_found():
    string = "AAGCCCCCCTTT"
    node = Node(h=string)

    assert node.is_mutant() is True


def test_node_with_vertical_string_not_found():
    string = "ABCDEFGHIIIKL"
    node = Node(v=string)

    assert node.is_mutant() is False


def test_node_with_forward_diagonal_string_found():
    string = "AAGCCCCCCTTT"
    node = Node(f=string)

    assert node.is_mutant() is True


def test_node_with_forward_diagonal_string_not_found():
    string = "ABCDEFGHIIIKL"
    node = Node(f=string)

    assert node.is_mutant() is False


def test_node_with_backward_diagonal_string_found():
    string = "AAGCCCCCCTTT"
    node = Node(b=string)

    assert node.is_mutant() is True


def test_node_with_backward_diagonal_string_not_found():
    string = "ABCDEFGHIIIKL"
    node = Node(b=string)

    assert node.is_mutant() is False
