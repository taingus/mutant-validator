from databases import Database
from fastapi import (
    Depends,
    FastAPI,
    Response,
    status,
)

from mutant_validator.backend.containers import (
    DNA,
    DNAStats,
)
from mutant_validator.backend.database import (
    get_db,
    migrate,
)
from mutant_validator.backend.query import (
    add_validated_dna,
    get_mutant_to_human_stats,
)
from mutant_validator.backend.validator import is_mutant

app = FastAPI(
    title="Mutant Validator",
    description="Validates if any given valid DNA chain contains mutant genes",
)


@app.on_event("startup")
async def startup():
    migrate()
    await get_db().connect()


@app.on_event("shutdown")
async def shutdown():
    await get_db().disconnect()


@app.post(
    "/mutant",
    responses={status.HTTP_403_FORBIDDEN: {"description": "Human not allowed"}},
)
async def validate_mutant_dna(
    dna: DNA, response: Response, db: Database = Depends(get_db)
):
    mutant = is_mutant(dna.dna)
    response.status_code = status.HTTP_200_OK if mutant else status.HTTP_403_FORBIDDEN
    await add_validated_dna(db, dna=str(dna.dna), mutant=mutant)
    return response


@app.get("/stats", response_model=DNAStats)
async def get_processed_dna_stats(db: Database = Depends(get_db)):
    response = DNAStats()
    result = await get_mutant_to_human_stats(db)

    for count, mutant in result:
        if mutant is True:
            response.count_mutant_dna = count
        else:
            response.count_human_dna = count

    if response.count_mutant_dna > 0 and response.count_human_dna > 0:
        response.ratio = response.count_mutant_dna / response.count_human_dna
    return response
