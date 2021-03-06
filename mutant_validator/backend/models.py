import sqlalchemy

from mutant_validator.backend.database import metadata

validated_dna = sqlalchemy.Table(
    "validated_dnas",
    metadata,
    sqlalchemy.Column("sha", sqlalchemy.String(length=65), primary_key=True),
    sqlalchemy.Column("dna", sqlalchemy.Text),
    sqlalchemy.Column("mutant", sqlalchemy.Boolean),
)
