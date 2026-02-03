#!/usr/bin/env python3
"""Test script to verify z.ai backend setup"""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))


async def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from app.config import settings
        print(f"  ✓ Settings loaded (model: {settings.zai_model})")

        from app.models import Dataset, Metric, Scenario, AgentModel, Recommendation
        print("  ✓ All models imported")

        from app.services import DataService, ChatService
        print("  ✓ All services imported")

        from app.agents import EvaluationAgent
        print("  ✓ Agent imported")

        from app.main import app
        print("  ✓ FastAPI app imported")

        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


async def test_data_loading():
    """Test that data files can be loaded"""
    print("\nTesting data loading...")
    try:
        from app.services import DataService

        service = DataService()
        datasets = await service.load_datasets()
        print(f"  ✓ Loaded {len(datasets)} datasets")

        metrics = await service.load_metrics()
        print(f"  ✓ Loaded {len(metrics)} metrics")

        scenarios = await service.load_scenarios()
        print(f"  ✓ Loaded {len(scenarios)} scenarios")

        agents = await service.load_agents()
        print(f"  ✓ Loaded {len(agents)} agents")

        return True
    except Exception as e:
        print(f"  ✗ Data loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_agent_init():
    """Test that agent can be initialized"""
    print("\nTesting agent initialization...")
    try:
        from app.agents import EvaluationAgent
        from app.config import settings

        agent = EvaluationAgent()
        await agent.initialize()
        print(f"  ✓ Agent initialized with API key: {settings.zai_api_key[:10]}...")

        return True
    except Exception as e:
        print(f"  ✗ Agent init failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("=" * 50)
    print("AEval Backend Setup Verification")
    print("=" * 50)

    results = []

    results.append(await test_imports())
    results.append(await test_data_loading())
    results.append(await test_agent_init())

    print("\n" + "=" * 50)
    if all(results):
        print("✓ All tests passed! Backend is ready to use.")
        print("\nStart the server with:")
        print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
