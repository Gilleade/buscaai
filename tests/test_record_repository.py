"""Tests for the JSON record repository."""

import pytest

from models import Record
from repositories import RecordRepository


def build_record(record_id: str = "LL-0001") -> Record:
    """Create a record instance for repository tests."""
    return Record(
        id=record_id,
        title="Checklist para evitar retrabalho na montagem",
        department="Produção",
        process="Montagem de componentes",
        problem_description=(
            "Componentes foram instalados fora da sequência correta, "
            "gerando desmontagem e retrabalho."
        ),
        identified_cause="Ausência de orientação visual padronizada.",
        implemented_solution="Foi criado um checklist visual.",
        observed_result="As montagens seguintes apresentaram menos erros.",
        keywords=["montagem", "retrabalho", "checklist"],
        created_at="2026-05-25T14:35:00",
    )


def test_load_records_creates_empty_file_when_storage_does_not_exist(tmp_path):
    """Repository must create an empty JSON storage file when needed."""
    file_path = tmp_path / "records.json"
    repository = RecordRepository(file_path=file_path)

    records = repository.load_records()

    assert records == []
    assert file_path.exists()


def test_save_and_load_records_preserves_record_content(tmp_path):
    """Repository must persist and restore saved records."""
    file_path = tmp_path / "records.json"
    repository = RecordRepository(file_path=file_path)
    record = build_record()

    repository.save_records([record])
    loaded_records = repository.load_records()

    assert len(loaded_records) == 1
    assert loaded_records[0] == record


def test_add_record_appends_record_to_storage(tmp_path):
    """Repository must append a new record to the existing local base."""
    file_path = tmp_path / "records.json"
    repository = RecordRepository(file_path=file_path)

    repository.add_record(build_record("LL-0001"))
    repository.add_record(build_record("LL-0002"))

    loaded_records = repository.load_records()

    assert len(loaded_records) == 2
    assert loaded_records[0].id == "LL-0001"
    assert loaded_records[1].id == "LL-0002"


def test_add_record_rejects_duplicate_identifier(tmp_path):
    """Repository must not accept two records with the same identifier."""
    file_path = tmp_path / "records.json"
    repository = RecordRepository(file_path=file_path)
    record = build_record("LL-0001")

    repository.add_record(record)

    with pytest.raises(ValueError, match="already exists"):
        repository.add_record(record)