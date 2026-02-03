from pydantic import BaseModel, Field
from typing import List, Optional


class Scenario(BaseModel):
    """Represents an evaluation scenario configuration."""

    id: str = Field(..., description="Unique identifier for the scenario")
    name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Detailed description of the scenario")
    recommended_metrics: Optional[List[str]] = Field(
        default_factory=list, description="Recommended metric IDs"
    )

    model_config = {"extra": "ignore"}
