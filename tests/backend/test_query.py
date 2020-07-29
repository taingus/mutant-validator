import pytest

from mutant_validator.backend.query import add_validated_dna


@pytest.mark.asyncio
async def test_insert_dna_sequence_works(db):
    result = await add_validated_dna(database=db, dna="DNA", mutant=True,)

    assert result is not None


@pytest.mark.asyncio
async def test_insert_duplicate_dna_sequence_does_not_work(db):
    await add_validated_dna(
        database=db, dna="DUPLICATE", mutant=True,
    )
    result = await add_validated_dna(database=db, dna="DUPLICATE", mutant=True)

    assert result is None
