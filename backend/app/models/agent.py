from pydantic import BaseModel, Field
from typing import List, Optional


class AgentModel(BaseModel):
    """Represents an AI agent configuration."""

    id: str = Field(..., description="Unique identifier for the agent")
    name: str = Field(..., description="Human-readable name")
    type: str = Field(..., description="Type of agent (e.g., 'rag', 'code', 'chat')")
    description: str = Field(..., description="Detailed description of the agent")
    capabilities: Optional[List[str]] = Field(
        default_factory=list, description="Agent capabilities"
    )

    model_config = {"extra": "ignore"}
