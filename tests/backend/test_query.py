from mutant_validator.backend.query import add_validated_dna
import pytest
from tests.test_main import override_get_db


@pytest.mark.asyncio
async def test_insert_dna_sequence_works():
    result = await add_validated_dna(
        database=override_get_db(), dna="DNA", mutant=True,
    )

    assert result is not None


@pytest.mark.asyncio
async def test_insert_duplicate_dna_sequence_does_not_work():
    await add_validated_dna(
        database=override_get_db(), dna="DUPLICATE", mutant=True,
    )
    result = await add_validated_dna(
        database=override_get_db(), dna="DUPLICATE", mutant=True,
    )

    assert result is None
