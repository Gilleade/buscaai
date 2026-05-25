"""Streamlit view for consulting lessons learned records through local AI."""

from __future__ import annotations

import streamlit as st

from services import OllamaService, OllamaServiceError, RecordService


CHAT_HISTORY_KEY = "consultation_messages"


def render_consult_view(
    record_service: RecordService,
    ollama_service: OllamaService,
) -> None:
    """Render the consultation chat interface."""
    st.header("Consultar conhecimento")

    st.write(
        "Descreva um problema ou situação para localizar experiências "
        "anteriormente registradas."
    )

    records = record_service.list_records()

    st.caption(f"Registros disponíveis na base local: {len(records)}")

    if CHAT_HISTORY_KEY not in st.session_state:
        st.session_state[CHAT_HISTORY_KEY] = []

    messages: list[dict[str, str]] = st.session_state[CHAT_HISTORY_KEY]

    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Descreva o problema encontrado ou pergunte por uma solução anterior..."
    )

    if not question:
        return

    previous_messages = list(messages)

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consultando conhecimentos registrados..."):
            try:
                answer = ollama_service.consult(
                    question=question,
                    records=records,
                    conversation=previous_messages,
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