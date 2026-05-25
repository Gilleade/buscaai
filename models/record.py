"""Domain model for a lesson learned record stored by BuscaAI."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class Record:
    """Represent a documented lesson learned available in the local knowledge base."""

    id: str
    title: str
    department: str
    process: str
    problem_description: str
    identified_cause: str
    implemented_solution: str
    observed_result: str
    keywords: list[str]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        """Convert the record object into a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Record":
        """Create a Record instance from a dictionary loaded from JSON."""
        required_fields = [
            "id",
            "title",
            "department",
            "process",
            "problem_description",
            "identified_cause",
            "implemented_solution",
            "observed_result",
            "created_at",
        ]

        missing_fields = [
            field_name for field_name in required_fields if field_name not in data
        ]

        if missing_fields:
            missing_fields_text = ", ".join(missing_fields)
            raise ValueError(
                f"Record data is missing required fields: {missing_fields_text}."
            )

        raw_keywords = data.get("keywords", [])

        if not isinstance(raw_keywords, list):
            raise ValueError("Record field 'keywords' must be a list.")

        normalized_keywords = [
            str(keyword).strip()
            for keyword in raw_keywords
            if str(keyword).strip()
        ]

        return cls(
            id=str(data["id"]).strip(),
            title=str(data["title"]).strip(),
            department=str(data["department"]).strip(),
            process=str(data["process"]).strip(),
            problem_description=str(data["problem_description"]).strip(),
            identified_cause=str(data["identified_cause"]).strip(),
            implemented_solution=str(data["implemented_solution"]).strip(),
            observed_result=str(data["observed_result"]).strip(),
            keywords=normalized_keywords,
            created_at=str(data["created_at"]).strip(),
        )