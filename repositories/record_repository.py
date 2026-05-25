"""JSON repository responsible for persisting BuscaAI records."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from config import RECORDS_FILE, SCHEMA_VERSION
from models import Record


class RecordRepository:
    """Manage record persistence in a local JSON file."""

    def __init__(self, file_path: Path = RECORDS_FILE) -> None:
        """Initialize the repository with the JSON storage file path."""
        self.file_path = Path(file_path)

    def initialize_file(self) -> None:
        """Create the storage file with an empty structure when it does not exist."""
        if self.file_path.exists():
            return

        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.save_records([])

    def load_records(self) -> list[Record]:
        """Load all records from the local JSON storage file."""
        self.initialize_file()

        try:
            with self.file_path.open("r", encoding="utf-8-sig") as file:
                payload = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Unable to read records file '{self.file_path}'. "
                "The JSON content is invalid."
            ) from error

        if not isinstance(payload, dict):
            raise ValueError("Records file content must be a JSON object.")

        raw_records = payload.get("records")

        if not isinstance(raw_records, list):
            raise ValueError("Records file must contain a 'records' list.")

        return [Record.from_dict(record_data) for record_data in raw_records]

    def save_records(self, records: Iterable[Record]) -> None:
        """Persist all provided records in the local JSON storage file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "schema_version": SCHEMA_VERSION,
            "records": [record.to_dict() for record in records],
        }

        temporary_file = self.file_path.with_suffix(".tmp")

        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
            file.write("\n")

        temporary_file.replace(self.file_path)

    def add_record(self, record: Record) -> Record:
        """Append a new record to the storage file and return the saved record."""
        records = self.load_records()

        if any(existing_record.id == record.id for existing_record in records):
            raise ValueError(f"A record with ID '{record.id}' already exists.")

        records.append(record)
        self.save_records(records)

        return record