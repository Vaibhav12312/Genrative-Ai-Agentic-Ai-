from pydantic import BaseModel, Field


class RecordCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)
    category: str = Field(default="general", min_length=1, max_length=80)
    legacy_id: str | None = Field(default=None, max_length=80)


class RecordOut(BaseModel):
    id: int
    title: str
    content: str
    category: str
    created_at: str
    legacy_id: str | None = None


class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)


class AskResponse(BaseModel):
    answer: str
    sources: list[int] = Field(default_factory=list)
    source_details: list[dict] = Field(default_factory=list)
