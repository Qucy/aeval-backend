#!/usr/bin/env python3
"""Debug script to test zhipuai LLM response"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from zhipuai import ZhipuAI
from app.config import settings


async def test_llm():
    """Test the LLM directly"""
    print("Testing zhipuai LLM...")
    print(f"API Key: {settings.zai_api_key[:20]}...")
    print(f"Model: {settings.zai_model}")

    client = ZhipuAI(api_key=settings.zai_api_key)

    system_prompt = """You are a helpful assistant. You must respond in JSON format.
Return responses in this JSON format:
{
    "intent": "<intent_category>",
    "reason": "<explanation>"
}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Test my RAG agent for safety"},
    ]

    try:
        print("\nCalling LLM...")
        loop = asyncio.get_event_loop()
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.zai_model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
        )

        print(f"\nResponse type: {type(response)}")
        print(f"Response: {response}")

        if hasattr(response, 'choices'):
            print(f"\nNumber of choices: {len(response.choices)}")
            choice = response.choices[0]
            print(f"Choice type: {type(choice)}")

            if hasattr(choice, 'message'):
                msg = choice.message
                print(f"\nMessage type: {type(msg)}")
                print(f"Message: {msg}")

                if hasattr(msg, 'content'):
                    content = msg.content
                    print(f"\nContent type: {type(content)}")
                    print(f"Content: {content}")
                    print(f"Content length: {len(content) if content else 0}")

                    if content:
                        print(f"\nFirst 100 chars: {content[:100]}")
                        print(f"Last 100 chars: {content[-100:]}")

                        # Try to parse as JSON
                        import json
                        try:
                            parsed = json.loads(content)
                            print(f"\nParsed JSON: {parsed}")
                        except json.JSONDecodeError as e:
                            print(f"\nFailed to parse JSON: {e}")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_llm())
