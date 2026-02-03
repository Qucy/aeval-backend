from pydantic import BaseModel, Field
from typing import Literal


class Metric(BaseModel):
    """Represents an evaluation metric."""

    id: str = Field(..., description="Unique identifier for the metric")
    name: str = Field(..., description="Human-readable name")
    category: str = Field(..., description="Category of metric (e.g., 'safety', 'accuracy')")
    description: str = Field(..., description="Detailed description of what the metric measures")
    cost: Literal["Low", "Medium", "High"] = Field(
        ..., description="Computational cost of the metric"
    )
