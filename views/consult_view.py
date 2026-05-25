"""Streamlit view for consulting lessons learned records through local AI."""

from __future__ import annotations

import streamlit as st

from services import OllamaService, OllamaServiceError, RecordService
from styles import render_page_header


CHAT_HISTORY_KEY = "consultation_messages"


def clear_conversation() -> None:
    """Clear the visible consultation history stored in the current session."""
    st.session_state[CHAT_HISTORY_KEY] = []


def render_chat_composer(messages: list[dict[str, str]]) -> str | None:
    """Render the fixed bottom composer with a clear button and chat input."""
    with st.bottom:
        with st.container(key="chat_composer"):
            clear_column, prompt_column = st.columns(
                [0.65, 9.35],
                vertical_alignment="bottom",
                gap="small",
            )

            with clear_column:
                st.button(
                    "🗑️",
                    key="clear_conversation_button",
                    help="Limpar conversa",
                    use_container_width=True,
                    disabled=not messages,
                    on_click=clear_conversation,
                )

            with prompt_column:
                return st.chat_input(
                    "Descreva o problema encontrado ou consulte uma solução anterior...",
                    key="consultation_prompt",
                )


def render_consult_view(
    record_service: RecordService,
    ollama_service: OllamaService,
) -> None:
    """Render the consultation chat interface."""
    records = record_service.list_records()

    if CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[CHAT_HISTORY_KEY] = []

    messages: list[dict[str, str]] = st.session_state[CHAT_HISTORY_KEY]

    render_page_header(
        eyebrow="Consulta assistida",
        title="Encontre experiências já documentadas.",
        description=(
            "Descreva a situação encontrada e o BuscaAI consultará somente "
            "as lições aprendidas registradas na base local."
        ),
    )

    st.markdown(
        f"""
        <div class="buscaai-status-pill">
            <span class="buscaai-status-dot"></span>
            {len(records)} registros disponíveis para consulta
        </div>
        """,
        unsafe_allow_html=True,
    )


    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = render_chat_composer(messages)

    if not question:
        return

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultando a base de lições aprendidas..."):
            try:
                answer = ollama_service.consult(
                    question=question,
                    records=records,
                )
            except (OllamaServiceError, ValueError) as error:
                answer = str(error)
                st.error(answer)
            else:
                st.markdown(answer)

    messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )