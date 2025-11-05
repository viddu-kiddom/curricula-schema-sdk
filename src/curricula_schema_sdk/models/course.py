from uuid import UUID

from curricula_schema_sdk.models.BaseCurriculaModel import BaseCurriculaModel


class Course(BaseCurriculaModel):
    subject: str
    grade_level: str
    curricula_id: UUID
    language: str
    isbn: int
