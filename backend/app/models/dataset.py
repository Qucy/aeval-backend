from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class Dataset(BaseModel):
    """Represents an evaluation dataset."""

    id: str = Field(..., description="Unique identifier for the dataset")
    name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Detailed description of the dataset")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    size: str = Field(..., description="Size of the dataset (e.g., '1000', '10K')")
    total_records: Optional[int] = Field(None, description="Total number of records")
    file_format: str = Field(..., description="File format (e.g., 'json', 'csv')")
    metadata_quality_score: float = Field(
        ..., ge=0.0, le=1.0, description="Quality score of metadata"
    )
    application_context: Optional[str] = Field(None, description="Application context")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")

    model_config = {"extra": "ignore"}
