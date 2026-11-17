from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's question")
    prompt_version: Literal["v1", "v2"] = Field("v2", description="Which task prompt to use")


class ChatResponse(BaseModel):
    answer: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    follow_up: str
