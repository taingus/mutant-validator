from fastapi import FastAPI, Response, status
from mutant_validator.backend.database import database, migrate
from mutant_validator.backend.containers import DNA
from mutant_validator.backend.validator import is_mutant
from mutant_validator.backend.query import add_validated_dna

app = FastAPI(
    title="Mutant Validator",
    description="Validates if any given valid DNA chain contains mutant genes",
)


@app.on_event("startup")
async def startup():
    migrate()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/mutant")
async def validate_mutant_dna(dna: DNA, response: Response):
    mutant = is_mutant(dna)
    response.status_code = status.HTTP_200_OK if mutant else status.HTTP_403_FORBIDDEN
    await add_validated_dna(database, dna=str(dna.dna), mutant=mutant)
    return response
