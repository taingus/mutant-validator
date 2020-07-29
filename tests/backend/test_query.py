import pytest

from mutant_validator.backend.query import (
    add_validated_dna,
    get_mutant_to_human_stats,
)


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


@pytest.mark.asyncio
async def test_mutant_to_human_stats_with_empty_data(db):
    result = await get_mutant_to_human_stats(db)

    assert result == []


@pytest.mark.asyncio
async def test_mutant_to_human_stats_with_one_human(db):
    await add_validated_dna(database=db, dna="human", mutant=False)
    result = await get_mutant_to_human_stats(db)

    assert result[0][0] == 1
    assert result[0][1] is False


@pytest.mark.asyncio
async def test_mutant_to_human_stats_with_one_mutant(db):
    await add_validated_dna(database=db, dna="mutant", mutant=True)
    result = await get_mutant_to_human_stats(db)

    assert result[0][0] == 1
    assert result[0][1] is True


@pytest.mark.asyncio
async def test_mutant_to_human_stats_with_one_mutant_and_one_human(db):
    await add_validated_dna(database=db, dna="mutant", mutant=True)
    await add_validated_dna(database=db, dna="human", mutant=False)
    result = await get_mutant_to_human_stats(db)

    assert result[0][0] == 1
    assert result[0][1] is False

    assert result[1][0] == 1
    assert result[1][1] is True
