"""Main Streamlit application entry point for BuscaAI."""

from __future__ import annotations

import streamlit as st

from config import (
    APP_NAME,
    CONSULT_PAGE_LABEL,
    PAGE_ICON,
    REGISTER_PAGE_LABEL,
)
from services import OllamaService, RecordService
from styles import apply_app_styles, render_sidebar_brand
from views import render_consult_view, render_register_view


NAVIGATION_KEY = "selected_page"


def set_page(page_label: str) -> None:
    """Change the current application page stored in the session."""
    st.session_state[NAVIGATION_KEY] = page_label


def main() -> None:
    """Run the BuscaAI Streamlit application."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_app_styles()

    record_service = RecordService()
    ollama_service = OllamaService()
    records_count = len(record_service.list_records())

    if NAVIGATION_KEY not in st.session_state:
        st.session_state[NAVIGATION_KEY] = CONSULT_PAGE_LABEL

    selected_page = st.session_state[NAVIGATION_KEY]

    with st.sidebar:
        render_sidebar_brand()

        st.markdown(
            '<div class="buscaai-navigation-title">Navegação</div>',
            unsafe_allow_html=True,
        )

        st.button(
            "Consultar conhecimento",
            key="navigation_consult_button",
            icon=":material/search:",
            type="primary" if selected_page == CONSULT_PAGE_LABEL else "secondary",
            use_container_width=True,
            on_click=set_page,
            args=(CONSULT_PAGE_LABEL,),
        )

        st.button(
            "Registrar conhecimento",
            key="navigation_register_button",
            icon=":material/edit_note:",
            type="primary" if selected_page == REGISTER_PAGE_LABEL else "secondary",
            use_container_width=True,
            on_click=set_page,
            args=(REGISTER_PAGE_LABEL,),
        )

        st.markdown(
            f"""
            <div class="buscaai-sidebar-card">
                <div class="buscaai-sidebar-label">Base local</div>
                <div class="buscaai-sidebar-value">
                    {records_count} lições aprendidas registradas
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if selected_page == CONSULT_PAGE_LABEL:
        render_consult_view(record_service, ollama_service)
    else:
        render_register_view(record_service)


if __name__ == "__main__":
    main()