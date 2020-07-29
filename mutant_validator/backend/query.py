from databases import Database
from mutant_validator.backend.models import validated_dna


async def add_validated_dna(database: Database, dna: str, mutant: bool):
    query = validated_dna.insert().values(dna=dna, mutant=mutant)
    return await database.execute(query)
