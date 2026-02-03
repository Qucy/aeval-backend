from app.agents.evaluation_agent import EvaluationAgent
from app.services.data_service import DataService
from app.models.recommendation import ChatResponse


class ChatService:
    """Service that orchestrates chat interactions with the evaluation agent."""

    def __init__(self) -> None:
        """Initialize the chat service."""
        self.agent = EvaluationAgent()
        self.data_service = DataService()
        self._initialized = False

    async def ensure_initialized(self) -> None:
        """Ensure the agent is initialized."""
        if not self._initialized:
            await self.agent.initialize()
            self._initialized = True

    async def process_message(self, message: str) -> ChatResponse:
        """Process a user message and return response with recommendation.

        Args:
            message: User's input message

        Returns:
            ChatResponse with content, recommendation, and quick replies
        """
        await self.ensure_initialized()

        # Load all data
        datasets = await self.data_service.load_datasets()
        metrics = await self.data_service.load_metrics()
        scenarios = await self.data_service.load_scenarios()
        agents = await self.data_service.load_agents()

        # Process with agent
        content, recommendation = await self.agent.process_request(
            message, datasets, metrics, scenarios, agents
        )

        return ChatResponse(
            content=content,
            recommendation=recommendation,
            quick_replies=[
                "Accept and continue",
                "Make it cheaper",
                "Add more safety metrics",
            ],
        )


# Singleton instance
_chat_service = ChatService()


async def get_chat_service() -> ChatService:
    """Get the singleton chat service instance."""
    return _chat_service
