import sqlalchemy

from mutant_validator.backend.database import metadata

validated_dna = sqlalchemy.Table(
    "validated_dnas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("dna", sqlalchemy.String),
    sqlalchemy.Column("mutant", sqlalchemy.Boolean),
)
