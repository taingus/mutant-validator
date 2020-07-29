from hashlib import sha256
from typing import (
    Any,
    Optional,
)

from databases import Database
from sqlalchemy import (
    func,
    select,
)

from mutant_validator.backend.models import validated_dna


async def add_validated_dna(
    database: Database, dna: str, mutant: bool
) -> Optional[Any]:
    encoded_dna = dna.encode()
    dna_sha = sha256(encoded_dna).hexdigest()

    exists = await database.fetch_one(
        validated_dna.select().where(validated_dna.c.sha == dna_sha)
    )
    if exists:
        return None

    return await database.execute(
        validated_dna.insert().values(sha=dna_sha, dna=encoded_dna, mutant=mutant)
    )


async def get_mutant_to_human_stats(database: Database):
    return await database.fetch_all(
        select([func.count(), validated_dna.c.mutant])
        .group_by(validated_dna.c.mutant)
        .select_from(validated_dna)
    )
