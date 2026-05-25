"""Application service responsible for creating and retrieving records."""

from __future__ import annotations

import re
from collections.abc import Callable
from datetime import datetime

from config import RECORD_ID_PREFIX
from models import Record
from repositories import RecordRepository


class RecordService:
    """Apply application rules for lessons learned records."""

    def __init__(
        self,
        repository: RecordRepository | None = None,
        now_provider: Callable[[], datetime] = datetime.now,
    ) -> None:
        """Initialize the service with repository and timestamp dependencies."""
        self.repository = repository or RecordRepository()
        self.now_provider = now_provider

    def list_records(self) -> list[Record]:
        """Return all records currently stored in the local base."""
        return self.repository.load_records()

    def register_record(
        self,
        *,
        title: str,
        department: str,
        process: str,
        problem_description: str,
        identified_cause: str,
        implemented_solution: str,
        observed_result: str,
        keywords: str | list[str] = "",
    ) -> Record:
        """Validate, create and persist a new lesson learned record."""
        required_fields = {
            "Título do conhecimento": title,
            "Área / Setor": department,
            "Processo ou atividade": process,
            "Descrição do problema": problem_description,
            "Causa identificada": identified_cause,
            "Solução aplicada": implemented_solution,
            "Resultado observado": observed_result,
        }

        missing_fields = [
            label
            for label, value in required_fields.items()
            if not str(value).strip()
        ]

        if missing_fields:
            fields_text = ", ".join(missing_fields)
            raise ValueError(f"Preencha os campos obrigatórios: {fields_text}.")

        existing_records = self.repository.load_records()

        record = Record(
            id=self._generate_next_id(existing_records),
            title=title.strip(),
            department=department.strip(),
            process=process.strip(),
            problem_description=problem_description.strip(),
            identified_cause=identified_cause.strip(),
            implemented_solution=implemented_solution.strip(),
            observed_result=observed_result.strip(),
            keywords=self._normalize_keywords(keywords),
            created_at=self.now_provider().isoformat(timespec="seconds"),
        )

        return self.repository.add_record(record)

    @staticmethod
    def _normalize_keywords(keywords: str | list[str]) -> list[str]:
        """Normalize keywords received from the registration form."""
        raw_keywords = keywords.split(",") if isinstance(keywords, str) else keywords

        normalized_keywords: list[str] = []
        existing_keywords: set[str] = set()

        for keyword in raw_keywords:
            normalized_keyword = str(keyword).strip()

            if not normalized_keyword:
                continue

            comparison_key = normalized_keyword.casefold()

            if comparison_key in existing_keywords:
                continue

            existing_keywords.add(comparison_key)
            normalized_keywords.append(normalized_keyword)

        return normalized_keywords

    @staticmethod
    def _generate_next_id(records: list[Record]) -> str:
        """Generate the next sequential identifier for a new record."""
        id_pattern = re.compile(rf"^{re.escape(RECORD_ID_PREFIX)}-(\d+)$")

        existing_numbers = []

        for record in records:
            match = id_pattern.match(record.id)

            if match:
                existing_numbers.append(int(match.group(1)))

        next_number = max(existing_numbers, default=0) + 1

        return f"{RECORD_ID_PREFIX}-{next_number:04d}"