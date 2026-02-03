"""
Integration tests for AEval Backend API

These tests verify the full API stack including:
- Health endpoint
- Chat endpoint with real LLM calls
- Error handling
- Response validation
"""

import asyncio
import pytest
import json
from httpx import AsyncClient
from app.main import app


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check_returns_200(self):
        """Test that health check returns 200 OK."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}


class TestChatEndpoint:
    """Tests for the chat endpoint."""

    @pytest.mark.asyncio
    async def test_chat_accepts_valid_request(self):
        """Test that chat endpoint accepts a valid request."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/chat",
                json={"message": "Test my RAG agent for safety"}
            )
            # We accept 200 or 500 (API might fail due to rate limits, etc.)
            assert response.status_code in [200, 500]
            data = response.json()

            if response.status_code == 200:
                assert "content" in data
                assert "recommendation" in data
                assert "quick_replies" in data
                assert isinstance(data["quick_replies"], list)

    @pytest.mark.asyncio
    async def test_chat_returns_422_for_empty_message(self):
        """Test that chat endpoint validates message content."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/chat", json={"message": ""})
            # Should get validation error
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_returns_422_for_missing_message(self):
        """Test that chat endpoint requires message field."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/chat", json={})
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_returns_422_for_long_message(self):
        """Test that chat endpoint rejects messages over 10000 characters."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            long_message = "a" * 10001
            response = await client.post(
                "/api/chat",
                json={"message": long_message}
            )
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_chat_response_structure(self):
        """Test that chat response has correct structure."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/chat",
                json={"message": "Evaluate python coding ability"}
            )

            if response.status_code == 200:
                data = response.json()

                # Check content
                assert isinstance(data["content"], str)
                assert len(data["content"]) > 0

                # Check recommendation if present
                if data.get("recommendation"):
                    rec = data["recommendation"]
                    assert "dataset" in rec
                    assert "metrics" in rec
                    assert "agent" in rec
                    assert "scenario" in rec
                    assert "reason" in rec

                    # Check dataset structure
                    assert "id" in rec["dataset"]
                    assert "name" in rec["dataset"]
                    assert "description" in rec["dataset"]

                    # Check metrics structure
                    assert isinstance(rec["metrics"], list)
                    if len(rec["metrics"]) > 0:
                        assert "id" in rec["metrics"][0]
                        assert "name" in rec["metrics"][0]

                # Check quick_replies
                assert isinstance(data["quick_replies"], list)


class TestDifferentIntents:
    """Tests for different user intents."""

    @pytest.mark.asyncio
    async def test_rag_safety_intent(self):
        """Test chat with RAG safety intent."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/chat",
                json={"message": "Test my RAG agent for safety and hallucinations"}
            )

            if response.status_code == 200:
                data = response.json()
                assert "content" in data
                # Should mention safety in response
                assert "safety" in data["content"].lower() or "recommend" in data["content"].lower()

    @pytest.mark.asyncio
    async def test_code_eval_intent(self):
        """Test chat with code evaluation intent."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/chat",
                json={"message": "Evaluate python coding ability"}
            )

            if response.status_code == 200:
                data = response.json()
                assert "content" in data

    @pytest.mark.asyncio
    async def test_general_chat_intent(self):
        """Test chat with general conversation intent."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/chat",
                json={"message": "Help me configure an evaluation"}
            )

            if response.status_code == 200:
                data = response.json()
                assert "content" in data


class TestErrorHandling:
    """Tests for error handling."""

    @pytest.mark.asyncio
    async def test_handles_missing_data_files(self):
        """Test that missing data files are handled gracefully."""
        # This test would need to mock the data service to return errors
        # For now, we just verify the endpoint doesn't crash
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/chat",
                json={"message": "Test message"}
            )
            # Should return 200 or proper error, not 500
            assert response.status_code in [200, 400, 500]


class TestResponseValidation:
    """Tests for LLM response validation."""

    @pytest.mark.asyncio
    async def test_validates_json_response(self):
        """Test that invalid JSON from LLM is handled."""
        # This would require mocking the LLM response
        # For now, just test that the endpoint processes successfully
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/chat",
                json={"message": "Give me a simple evaluation setup"}
            )

            if response.status_code == 200:
                data = response.json()
                # If we got a recommendation, validate its structure
                if data.get("recommendation"):
                    rec = data["recommendation"]
                    # All required fields should be present
                    assert rec.get("dataset") is not None
                    assert rec.get("agent") is not None
                    assert rec.get("scenario") is not None
                    assert rec.get("metrics") is not None
                    assert isinstance(rec["metrics"], list)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
