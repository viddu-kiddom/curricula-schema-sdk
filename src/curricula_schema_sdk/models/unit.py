from uuid import UUID

from curricula_schema_sdk.models.BaseCurriculaModel import BaseCurriculaModel


class Unit(BaseCurriculaModel):
    unit_number: UUID
