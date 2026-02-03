import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from tests.fixtures import evaluation_agent, mock_datasets, mock_metrics, mock_scenarios, mock_agents


class TestEvaluationAgent:
    """Tests for the EvaluationAgent class."""

    @pytest.mark.asyncio
    async def test_agent_initializes_client(self, evaluation_agent):
        """Test that the agent initializes the OpenAI client."""
        with patch("app.agents.evaluation_agent.AsyncOpenAI") as mock_openai:
            await evaluation_agent.initialize()
            mock_openai.assert_called_once()

    @pytest.mark.asyncio
    async def test_build_context_with_empty_lists(self, evaluation_agent):
        """Test context building with empty resource lists."""
        context = evaluation_agent._build_context([], [], [], [])
        assert "AVAILABLE RESOURCES:" in context
        assert "DATASETS:" in context
        assert "METRICS:" in context
        assert "SCENARIOS:" in context
        assert "AGENTS:" in context

    @pytest.mark.asyncio
    async def test_build_context_with_data(
        self, evaluation_agent, mock_datasets, mock_metrics, mock_scenarios, mock_agents
    ):
        """Test context building with actual data."""
        context = evaluation_agent._build_context(
            mock_datasets, mock_metrics, mock_scenarios, mock_agents
        )
        assert "ds-001" in context
        assert "Test Dataset" in context
        assert "Accuracy" in context
        assert "Test Scenario" in context
        assert "Test Agent" in context

    @pytest.mark.asyncio
    async def test_build_recommendation_with_valid_result(
        self, evaluation_agent, mock_datasets, mock_metrics, mock_scenarios, mock_agents
    ):
        """Test recommendation building with valid LLM result."""
        result = {
            "intent": "rag_safety",
            "dataset_id": "ds-001",
            "metric_ids": ["m-001"],
            "scenario_id": "s-001",
            "agent_id": "a-001",
            "reason": "Test reason",
        }

        recommendation = evaluation_agent._build_recommendation(
            result, mock_datasets, mock_metrics, mock_scenarios, mock_agents
        )

        assert recommendation is not None
        assert recommendation.dataset.id == "ds-001"
        assert len(recommendation.metrics) == 1
        assert recommendation.metrics[0].id == "m-001"
        assert recommendation.scenario.id == "s-001"
        assert recommendation.agent.id == "a-001"
        assert recommendation.reason == "Test reason"

    @pytest.mark.asyncio
    async def test_build_recommendation_falls_back_to_first_item(
        self, evaluation_agent, mock_datasets, mock_metrics, mock_scenarios, mock_agents
    ):
        """Test recommendation building falls back to first item when ID not found."""
        result = {
            "intent": "general",
            "dataset_id": "nonexistent",
            "metric_ids": [],
            "scenario_id": "nonexistent",
            "agent_id": "nonexistent",
            "reason": "Test",
        }

        recommendation = evaluation_agent._build_recommendation(
            result, mock_datasets, mock_metrics, mock_scenarios, mock_agents
        )

        assert recommendation is not None
        assert recommendation.dataset.id == "ds-001"  # Falls back to first
        assert recommendation.scenario.id == "s-001"
        assert recommendation.agent.id == "a-001"

    @pytest.mark.asyncio
    async def test_generate_response_for_rag_safety(self, evaluation_agent):
        """Test response generation for RAG safety intent."""
        result = {"intent": "rag_safety"}
        response = evaluation_agent._generate_response(result, None)
        assert "safety" in response.lower()

    @pytest.mark.asyncio
    async def test_generate_response_for_code_eval(self, evaluation_agent):
        """Test response generation for code evaluation intent."""
        result = {"intent": "code_eval"}
        response = evaluation_agent._generate_response(result, None)
        assert "code" in response.lower()

    @pytest.mark.asyncio
    async def test_generate_response_with_recommendation(self, evaluation_agent):
        """Test response generation includes recommendation reason."""
        from app.models.recommendation import Recommendation

        mock_recommendation = MagicMock(spec=Recommendation)
        mock_recommendation.reason = "Custom test reason"

        result = {"intent": "general"}
        response = evaluation_agent._generate_response(result, mock_recommendation)
        assert "Custom test reason" in response

    @pytest.mark.asyncio
    async def test_generate_response_unknown_intent(self, evaluation_agent):
        """Test response generation for unknown intent."""
        result = {"intent": "unknown_intent"}
        response = evaluation_agent._generate_response(result, None)
        assert "recommendation" in response.lower()
