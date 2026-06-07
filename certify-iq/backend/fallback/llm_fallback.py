from __future__ import annotations
import os
import time
import json
from typing import Optional


class LLMFallbackChain:
    def __init__(self):
        self._mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"

    def call(self, prompt: str, system: str = "", context: str = "") -> dict:
        if self._mock_mode:
            return self._tier4_mock(prompt)

        # Tier 1: Azure OpenAI GPT-4o
        result = self._tier1_azure(prompt, system, context)
        if result:
            return {**result, "tier_used": 1}

        # Tier 2: OpenAI direct
        result = self._tier2_openai(prompt, system, context)
        if result:
            return {**result, "tier_used": 2}

        # Tier 3: Anthropic Claude
        result = self._tier3_anthropic(prompt, system, context)
        if result:
            return {**result, "tier_used": 3}

        # Tier 4: Mock
        return self._tier4_mock(prompt)

    def _tier1_azure(self, prompt: str, system: str, context: str) -> Optional[dict]:
        try:
            from openai import AzureOpenAI
            client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT", ""),
                api_key=os.getenv("AZURE_SEARCH_KEY", ""),
                api_version=os.getenv("OPENAI_API_VERSION", "2024-02-01"),
            )
            t0 = time.monotonic()
            resp = client.chat.completions.create(
                model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4o"),
                messages=[
                    {"role": "system", "content": system or "You are a helpful AI assistant."},
                    {"role": "user", "content": f"{context}\n\n{prompt}" if context else prompt},
                ],
                temperature=0.3,
                max_tokens=800,
                timeout=10,
            )
            latency_ms = int((time.monotonic() - t0) * 1000)
            return {"response": resp.choices[0].message.content or "", "latency_ms": latency_ms}
        except Exception as e:
            print(f"Tier 1 failed: {e}")
            return None

    def _tier2_openai(self, prompt: str, system: str, context: str) -> Optional[dict]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
            t0 = time.monotonic()
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system or "You are a helpful AI assistant."},
                    {"role": "user", "content": f"{context}\n\n{prompt}" if context else prompt},
                ],
                temperature=0.3,
                max_tokens=800,
                timeout=8,
            )
            latency_ms = int((time.monotonic() - t0) * 1000)
            return {"response": resp.choices[0].message.content or "", "latency_ms": latency_ms}
        except Exception:
            return None

    def _tier3_anthropic(self, prompt: str, system: str, context: str) -> Optional[dict]:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
            t0 = time.monotonic()
            resp = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                system=system or "You are a helpful AI assistant.",
                messages=[{"role": "user", "content": f"{context}\n\n{prompt}" if context else prompt}],
                timeout=8,
            )
            latency_ms = int((time.monotonic() - t0) * 1000)
            return {"response": resp.content[0].text, "latency_ms": latency_ms}
        except Exception:
            return None

    def _tier4_mock(self, prompt: str) -> dict:
        return {
            "response": "Mock response: structured recommendation based on employee profile and knowledge base. [Source: Engineering Certification Guide]",
            "latency_ms": 50,
            "tier_used": 4,
        }


fallback_chain = LLMFallbackChain()