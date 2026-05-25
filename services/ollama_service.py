"""Service responsible for communicating with the local Ollama model."""

from __future__ import annotations

from typing import Any

import requests

from config import (
    OLLAMA_API_URL,
    OLLAMA_KEEP_ALIVE,
    OLLAMA_MODEL,
    OLLAMA_OPTIONS,
    OLLAMA_TIMEOUT_SECONDS,
)
from models import Record
from prompts import build_system_prompt


class OllamaServiceError(RuntimeError):
    """Represent failures while consulting the local Ollama service."""


class OllamaService:
    """Consult the local model using currently registered lessons learned."""

    def consult(
        self,
        *,
        question: str,
        records: list[Record],
        conversation: list[dict[str, str]] | None = None,
    ) -> str:
        """Send a user question and the local records to the Ollama model."""
        normalized_question = question.strip()

        if not normalized_question:
            raise ValueError("A pergunta não pode estar vazia.")

        if not records:
            return (
                "Ainda não há conhecimentos registrados na base local.\n\n"
                "Cadastre uma solução aplicada antes de realizar uma consulta."
            )

        messages = [
            {
                "role": "system",
                "content": build_system_prompt(records),
            }
        ]

        messages.extend(self._normalize_conversation(conversation or []))

        messages.append(
            {
                "role": "user",
                "content": normalized_question,
            }
        )

        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "think": False,
            "keep_alive": OLLAMA_KEEP_ALIVE,
            "options": OLLAMA_OPTIONS,
        }

        try:
            response = requests.post(
                OLLAMA_API_URL,
                json=payload,
                timeout=OLLAMA_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise OllamaServiceError(
                "Não foi possível consultar o modelo local. "
                "Verifique se o Ollama está em execução e se o modelo "
                f"'{OLLAMA_MODEL}' está disponível."
            ) from error

        try:
            response_data: dict[str, Any] = response.json()
        except ValueError as error:
            raise OllamaServiceError(
                "O Ollama retornou uma resposta inválida."
            ) from error

        answer = (
            response_data.get("message", {})
            .get("content", "")
            .strip()
        )

        if not answer:
            raise OllamaServiceError(
                "O modelo local não retornou uma resposta para a consulta."
            )

        return answer

    @staticmethod
    def _normalize_conversation(
        conversation: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        """Keep only valid user and assistant messages from the current session."""
        normalized_messages = []

        for message in conversation:
            role = message.get("role")
            content = message.get("content", "").strip()

            if role not in {"user", "assistant"} or not content:
                continue

            normalized_messages.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        return normalized_messages