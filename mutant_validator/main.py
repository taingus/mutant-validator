from databases import Database
from fastapi import (
    Depends,
    FastAPI,
    Response,
    status,
)

from mutant_validator.backend.containers import DNA
from mutant_validator.backend.database import (
    get_db,
    migrate,
)
from mutant_validator.backend.query import add_validated_dna
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


@app.post("/mutant")
async def validate_mutant_dna(
    dna: DNA, response: Response, db: Database = Depends(get_db)
):
    mutant = is_mutant(dna)
    response.status_code = status.HTTP_200_OK if mutant else status.HTTP_403_FORBIDDEN
    await add_validated_dna(db, dna=str(dna.dna), mutant=mutant)
    return response
