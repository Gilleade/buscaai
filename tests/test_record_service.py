"""Tests for the record application service."""

from datetime import datetime

import pytest

from repositories import RecordRepository
from services import RecordService


def build_service(tmp_path) -> RecordService:
    """Create a service connected to temporary test storage."""
    repository = RecordRepository(file_path=tmp_path / "records.json")

    return RecordService(
        repository=repository,
        now_provider=lambda: datetime(2026, 5, 25, 15, 30, 0),
    )


def build_record_data() -> dict[str, str]:
    """Return valid form data for registering a lesson learned."""
    return {
        "title": "Checklist para evitar retrabalho na montagem",
        "department": "Produção",
        "process": "Montagem de componentes",
        "problem_description": (
            "Componentes foram instalados fora da sequência correta, "
            "gerando desmontagem e retrabalho."
        ),
        "identified_cause": "Ausência de orientação visual padronizada.",
        "implemented_solution": "Foi criado um checklist visual.",
        "observed_result": "As montagens seguintes apresentaram menos erros.",
        "keywords": "montagem, retrabalho, checklist",
    }


def test_register_record_generates_identifier_and_persists_record(tmp_path):
    """Service must create the first identifier and save the new record."""
    service = build_service(tmp_path)

    record = service.register_record(**build_record_data())
    stored_records = service.list_records()

    assert record.id == "LL-0001"
    assert record.created_at == "2026-05-25T15:30:00"
    assert stored_records == [record]


def test_register_record_generates_sequential_identifiers(tmp_path):
    """Service must increment identifiers for subsequent records."""
    service = build_service(tmp_path)

    first_record = service.register_record(**build_record_data())
    second_record = service.register_record(**build_record_data())

    assert first_record.id == "LL-0001"
    assert second_record.id == "LL-0002"


def test_register_record_normalizes_keywords(tmp_path):
    """Service must remove empty and repeated keywords before saving."""
    service = build_service(tmp_path)
    data = build_record_data()
    data["keywords"] = " montagem, retrabalho, Montagem, checklist, "

    record = service.register_record(**data)

    assert record.keywords == ["montagem", "retrabalho", "checklist"]


def test_register_record_allows_empty_keywords(tmp_path):
    """Keywords are optional in the registration flow."""
    service = build_service(tmp_path)
    data = build_record_data()
    data["keywords"] = ""

    record = service.register_record(**data)

    assert record.keywords == []


def test_register_record_rejects_missing_required_fields(tmp_path):
    """Service must reject registration when required content is missing."""
    service = build_service(tmp_path)
    data = build_record_data()
    data["problem_description"] = "   "
    data["implemented_solution"] = ""

    with pytest.raises(ValueError, match="Preencha os campos obrigatórios"):
        service.register_record(**data)