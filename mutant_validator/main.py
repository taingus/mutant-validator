from fastapi import FastAPI, Response, status
from mutant_validator.backend.containers import DNA
from mutant_validator.backend.validator import is_mutant

app = FastAPI(
    title="Mutant Validator",
    description="Validates if any given valid DNA chain contains mutant genes",
)


@app.post("/mutant")
async def validate_mutant_dna(dna: DNA, response: Response):
    response.status_code = (
        status.HTTP_200_OK if is_mutant(dna) else status.HTTP_403_FORBIDDEN
    )
    return response
