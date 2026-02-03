from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from app.models.dataset import Dataset
from app.models.metric import Metric
from app.models.agent import AgentModel
from app.models.scenario import Scenario


class Recommendation(BaseModel):
    """Represents a complete evaluation configuration recommendation."""

    dataset: Dataset
    metrics: List[Metric]
    agent: AgentModel
    scenario: Scenario
    reason: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=10000)

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Validate message content."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    content: str
    recommendation: Optional[Recommendation] = None
    quick_replies: List[str] = Field(default_factory=list)
