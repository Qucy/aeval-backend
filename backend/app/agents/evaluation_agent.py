import json
import asyncio
from zhipuai import ZhipuAI

from app.config import settings
from app.models.dataset import Dataset
from app.models.metric import Metric
from app.models.scenario import Scenario
from app.models.agent import AgentModel
from app.models.recommendation import Recommendation
from typing import List, Optional, Tuple


class EvaluationAgent:
    """Agent that handles intent extraction and evaluation configuration recommendations.

    This single agent can process user requests and recommend appropriate
    datasets, metrics, scenarios, and agents based on intent classification.
    """

    SYSTEM_PROMPT = """You are an AI Evaluation Configuration Assistant. Your role is to:
1. Understand the user's evaluation goals
2. Classify their intent
3. Recommend appropriate datasets, metrics, and scenarios

AVAILABLE INTENTS:
- rag_safety: RAG system with focus on safety/hallucination/adversarial testing
- rag_accuracy: RAG system with focus on accuracy/faithfulness
- code_eval: Code generation and debugging evaluation
- general_chat: General conversational abilities
- safety: Safety and alignment testing

When responding to users:
1. Extract their intent
2. Recommend appropriate configuration
3. Explain your reasoning

Return responses in this JSON format:
{
    "intent": "<intent_category>",
    "dataset_id": "<dataset_id>",
    "metric_ids": ["<metric_id1>", "<metric_id2>"],
    "scenario_id": "<scenario_id>",
    "agent_id": "<agent_id>",
    "reason": "<explanation of recommendation>"
}"""

    def __init__(self) -> None:
        """Initialize the evaluation agent."""
        self.client: Optional[ZhipuAI] = None

    async def initialize(self) -> None:
        """Initialize the ZhipuAI client."""
        if self.client is None:
            self.client = ZhipuAI(api_key=settings.zai_api_key)

    async def process_request(
        self,
        user_input: str,
        datasets: List[Dataset],
        metrics: List[Metric],
        scenarios: List[Scenario],
        agents: List[AgentModel],
    ) -> Tuple[str, Optional[Recommendation]]:
        """Process user request and return response content + recommendation.

        Args:
            user_input: The user's message
            datasets: Available datasets
            metrics: Available metrics
            scenarios: Available scenarios
            agents: Available agents

        Returns:
            Tuple of (response_content, recommendation)

        Raises:
            ValueError: If LLM response is invalid or missing required fields
        """
        await self.initialize()

        # Build context for the LLM
        context = self._build_context(datasets, metrics, scenarios, agents)

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT + "\n\n" + context},
            {"role": "user", "content": user_input},
        ]

        try:
            # Run synchronous client call in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=settings.zai_model,
                messages=messages,
                temperature=settings.agent_temperature,
                max_tokens=settings.agent_max_tokens,
            )
        except Exception as e:
            raise ValueError(f"LLM API call failed: {e}")

        if not hasattr(response, 'choices') or len(response.choices) == 0:
            raise ValueError("LLM returned no choices")

        choice = response.choices[0]
        if not hasattr(choice, 'message'):
            raise ValueError("LLM choice has no message")

        message = choice.message
        content = message.content if hasattr(message, 'content') else None

        if not content:
            raise ValueError("LLM returned empty response")

        # Strip markdown code blocks if present (LLMs sometimes wrap JSON in ```json ... ```)
        if content.startswith("```"):
            lines = content.split("\n")
            # Remove first line (```json or ```)
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from LLM: {e}")

        # Validate required fields
        required_fields = ["intent", "dataset_id", "metric_ids", "scenario_id", "agent_id"]
        missing_fields = [f for f in required_fields if f not in result]
        if missing_fields:
            raise ValueError(f"LLM response missing required fields: {missing_fields}")

        # Build recommendation
        recommendation = self._build_recommendation(
            result, datasets, metrics, scenarios, agents
        )

        # Generate friendly response
        response_content = self._generate_response(result, recommendation)

        return response_content, recommendation

    def _build_context(
        self,
        datasets: List[Dataset],
        metrics: List[Metric],
        scenarios: List[Scenario],
        agents: List[AgentModel],
    ) -> str:
        """Build context string with available resources."""
        lines = ["AVAILABLE RESOURCES:"]

        lines.append("\nDATASETS:")
        for d in datasets:
            lines.append(f"  - {d.id}: {d.name}")
            lines.append(f"    Description: {d.description}")
            lines.append(f"    Tags: {', '.join(d.tags)}")

        lines.append("\nMETRICS:")
        for m in metrics:
            lines.append(f"  - {m.id}: {m.name} ({m.category})")
            lines.append(f"    Description: {m.description}")

        lines.append("\nSCENARIOS:")
        for s in scenarios:
            lines.append(f"  - {s.id}: {s.name}")
            lines.append(f"    Description: {s.description}")

        lines.append("\nAGENTS:")
        for a in agents:
            lines.append(f"  - {a.id}: {a.name} ({a.type})")

        return "\n".join(lines)

    def _build_recommendation(
        self,
        result: dict,
        datasets: List[Dataset],
        metrics: List[Metric],
        scenarios: List[Scenario],
        agents: List[AgentModel],
    ) -> Optional[Recommendation]:
        """Build Recommendation object from LLM response."""
        if not datasets or not metrics or not scenarios or not agents:
            return None

        dataset = next(
            (d for d in datasets if d.id == result.get("dataset_id")), datasets[0]
        )
        selected_metrics = [
            m for m in metrics if m.id in result.get("metric_ids", [])
        ] or [metrics[0]]
        scenario = next(
            (s for s in scenarios if s.id == result.get("scenario_id")), scenarios[0]
        )
        agent = next(
            (a for a in agents if a.id == result.get("agent_id")), agents[0]
        )

        return Recommendation(
            dataset=dataset,
            metrics=selected_metrics,
            agent=agent,
            scenario=scenario,
            reason=result.get("reason", "Based on your request, here's a recommended configuration."),
        )

    def _generate_response(
        self, result: dict, recommendation: Optional[Recommendation]
    ) -> str:
        """Generate friendly response message."""
        intent = result.get("intent", "general_chat")

        responses = {
            "rag_safety": "Since you're focused on safety for your RAG system, I've prioritized metrics that detect hallucinations, toxicity, and jailbreak attempts.",
            "rag_accuracy": "For RAG accuracy evaluation, I've selected metrics that measure context adherence and faithfulness to retrieved documents.",
            "code_eval": "For coding evaluation, I've chosen execution-based metrics that verify code correctness.",
            "general_chat": "For general conversation capabilities, I've selected metrics that evaluate relevance, coherence, and tone.",
            "safety": "For safety testing, I've included comprehensive metrics to detect toxic content and adversarial prompt resistance.",
        }

        base_response = responses.get(
            intent, "Based on your request, here's my recommendation."
        )
        reason = recommendation.reason if recommendation else ""
        return f"{base_response}\n\n{reason}" if reason else base_response
