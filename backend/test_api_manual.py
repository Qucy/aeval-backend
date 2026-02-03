#!/usr/bin/env python3
"""
Manual API testing script for AEval Backend

This script tests the backend API endpoints manually to verify
everything is working before launching.
"""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from httpx import AsyncClient, ASGITransport
from app.main import app


async def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return response.status_code == 200


async def test_chat(message: str):
    """Test chat endpoint"""
    print(f"\nTesting chat endpoint with: '{message}'")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        try:
            response = await client.post(
                "/api/chat",
                json={"message": message},
                timeout=30.0  # 30 second timeout
            )
            print(f"  Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"  Content: {data.get('content', 'No content')[:100]}...")

                if data.get('recommendation'):
                    rec = data['recommendation']
                    print(f"  Dataset: {rec.get('dataset', {}).get('name', 'N/A')}")
                    print(f"  Metrics: {len(rec.get('metrics', []))} metrics")
                    print(f"  Agent: {rec.get('agent', {}).get('name', 'N/A')}")
                    print(f"  Scenario: {rec.get('scenario', {}).get('name', 'N/A')}")

                print(f"  Quick replies: {data.get('quick_replies', [])}")
                return True
            else:
                print(f"  Error: {response.text}")
                return False

        except Exception as e:
            print(f"  Exception: {e}")
            import traceback
            traceback.print_exc()
            return False


async def test_validation():
    """Test input validation"""
    print("\nTesting input validation...")

    test_cases = [
        ("Empty message", {"message": ""}, 422),
        ("Missing message", {}, 422),
        ("Long message", {"message": "a" * 10001}, 422),
    ]

    results = []
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for name, payload, expected_status in test_cases:
            response = await client.post("/api/chat", json=payload)
            status_ok = response.status_code == expected_status
            results.append(status_ok)
            print(f"  {name}: {'✓' if status_ok else '✗'} (got {response.status_code}, expected {expected_status})")

    return all(results)


async def main():
    """Run all tests"""
    print("=" * 60)
    print("AEval Backend Manual API Testing")
    print("=" * 60)

    results = []

    # Test health
    results.append(await test_health())

    # Test various chat messages
    test_messages = [
        "Test my RAG agent for safety",
        "Evaluate python coding ability",
        "I need to test general conversation capabilities",
    ]

    for msg in test_messages:
        results.append(await test_chat(msg))

    # Test validation
    results.append(await test_validation())

    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if all(results):
        print("✓ All tests passed! API is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
