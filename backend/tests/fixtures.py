import pytest
from app.agents.evaluation_agent import EvaluationAgent
from app.services.data_service import DataService
from app.models.dataset import Dataset
from app.models.metric import Metric
from app.models.scenario import Scenario
from app.models.agent import AgentModel


@pytest.fixture
async def evaluation_agent():
    """Fixture providing an initialized evaluation agent."""
    agent = EvaluationAgent()
    # Note: This will fail without proper API key in test environment
    # In real tests, you'd mock the OpenAI client
    # await agent.initialize()
    return agent


@pytest.fixture
def data_service():
    """Fixture providing a data service instance."""
    return DataService()


@pytest.fixture
def mock_datasets():
    """Fixture providing mock dataset data."""
    return [
        Dataset(
            id="ds-001",
            name="Test Dataset",
            description="A test dataset",
            tags=["test"],
            size="100",
            file_format="json",
            metadata_quality_score=0.9,
        )
    ]


@pytest.fixture
def mock_metrics():
    """Fixture providing mock metric data."""
    return [
        Metric(
            id="m-001",
            name="Accuracy",
            category="accuracy",
            description="Measures accuracy",
            cost="Low",
        )
    ]


@pytest.fixture
def mock_scenarios():
    """Fixture providing mock scenario data."""
    return [
        Scenario(
            id="s-001",
            name="Test Scenario",
            description="A test scenario",
        )
    ]


@pytest.fixture
def mock_agents():
    """Fixture providing mock agent data."""
    return [
        AgentModel(
            id="a-001",
            name="Test Agent",
            type="test",
            description="A test agent",
        )
    ]
