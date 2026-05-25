"""Main Streamlit application entry point for BuscaAI."""

from __future__ import annotations

import streamlit as st

from config import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_SUBTITLE,
    CONSULT_PAGE_LABEL,
    PAGE_ICON,
    REGISTER_PAGE_LABEL,
)
from services import OllamaService, RecordService
from views import render_consult_view, render_register_view


def main() -> None:
    """Run the BuscaAI Streamlit application."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=PAGE_ICON,
        layout="centered",
    )

    record_service = RecordService()
    ollama_service = OllamaService()

    st.sidebar.title(APP_NAME)
    st.sidebar.caption("Consulta a Lições Aprendidas")

    selected_page = st.sidebar.radio(
        "Navegação",
        options=[CONSULT_PAGE_LABEL, REGISTER_PAGE_LABEL],
    )

    st.title(APP_NAME)
    st.caption(APP_SUBTITLE)

    if selected_page == CONSULT_PAGE_LABEL:
        st.write(APP_DESCRIPTION)
        st.divider()
        render_consult_view(record_service, ollama_service)
    else:
        render_register_view(record_service)


if __name__ == "__main__":
    main()