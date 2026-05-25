"""Streamlit view for consulting lessons learned records."""

from __future__ import annotations

import streamlit as st

from services import RecordService


def render_consult_view(record_service: RecordService) -> None:
    """Render the initial consultation page before AI integration."""
    st.header("Consultar conhecimento")

    st.write(
        "Descreva um problema ou situação para localizar experiências "
        "anteriormente registradas."
    )

    records = record_service.list_records()

    st.info(
        "A consulta por inteligência artificial será conectada na próxima etapa."
    )

    st.caption(f"Registros disponíveis na base local: {len(records)}")