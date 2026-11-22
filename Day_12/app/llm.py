from typing import Protocol


class LLMClient(Protocol):
    def generate(self, question: str, context: str) -> str: ...


class MockLLM:
    """Deterministic local model adapter used for development and tests."""

    def generate(self, question: str, context: str) -> str:
        if not context.strip():
            return (
                "I couldn't find relevant EPFO information in the available "
                "knowledge records. Please consult the official EPFO portal "
                "or a qualified EPFO helpdesk for confirmation."
            )
        return (
            "Based on the available EPFOSathi records: "
            f"{context[:1800]} "
            "Please verify account-specific details on the official EPFO portal."
        )


class OpenAICompatibleLLM:
    """Optional adapter. Uses the OpenAI Python SDK only when configured."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, question: str, context: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": (
                    "You are EPFOSathi, an informational assistant. "
                    "Use only supplied context, do not invent policy details, "
                    "and advise users to verify account-specific matters with EPFO."
                )},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or "No answer was generated."


def get_llm():
    from app.config import settings
    if settings.llm_provider.lower() == "openai" and settings.openai_api_key:
        return OpenAICompatibleLLM(settings.openai_api_key)
    return MockLLM()
