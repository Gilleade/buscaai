"""Streamlit view for registering new lessons learned records."""

from __future__ import annotations

import streamlit as st

from config import DEPARTMENT_OPTIONS
from services import RecordService
from styles import render_page_header


def render_register_view(record_service: RecordService) -> None:
    """Render the form responsible for registering a new record."""
    render_page_header(
        eyebrow="Registro de experiência",
        title="Documente uma nova lição aprendida.",
        description=(
            "Registre uma solução efetivamente aplicada para que ela passe "
            "a fazer parte da base consultável do BuscaAI."
        ),
    )

    with st.form("register_record_form", clear_on_submit=True):
        st.markdown(
            '<div class="buscaai-section-title">Identificação</div>',
            unsafe_allow_html=True,
        )

        title = st.text_input(
            "Título do conhecimento",
            placeholder="Ex.: Controle de torque na fixação de mancais",
        )

        department = st.selectbox(
            "Área / Setor",
            options=DEPARTMENT_OPTIONS,
        )

        process = st.text_input(
            "Processo ou atividade",
            placeholder="Ex.: Montagem de conjunto rotativo",
        )

        st.markdown(
            '<div class="buscaai-section-title">Contexto do problema</div>',
            unsafe_allow_html=True,
        )

        problem_description = st.text_area(
            "Descrição do problema",
            placeholder="Descreva a ocorrência e seu impacto no processo.",
            height=115,
        )

        identified_cause = st.text_area(
            "Causa identificada",
            placeholder="Informe a causa observada após a análise da ocorrência.",
            height=105,
        )

        st.markdown(
            '<div class="buscaai-section-title">Conhecimento aplicado</div>',
            unsafe_allow_html=True,
        )

        implemented_solution = st.text_area(
            "Solução aplicada",
            placeholder="Descreva a ação efetivamente utilizada para tratar o problema.",
            height=115,
        )

        observed_result = st.text_area(
            "Resultado observado",
            placeholder="Descreva os resultados verificados após a aplicação.",
            height=105,
        )

        keywords = st.text_input(
            "Palavras-chave (opcional)",
            placeholder="Ex.: mancal, torque, torquímetro, vibração",
            help=(
                "As palavras-chave auxiliam a organização do registro, "
                "mas a consulta também considera o texto completo."
            ),
        )

        submitted = st.form_submit_button(
            "Salvar conhecimento",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    try:
        record = record_service.register_record(
            title=title,
            department=department,
            process=process,
            problem_description=problem_description,
            identified_cause=identified_cause,
            implemented_solution=implemented_solution,
            observed_result=observed_result,
            keywords=keywords,
        )
    except ValueError as error:
        st.error(str(error))
        return

    st.success("Conhecimento registrado com sucesso.")
    st.markdown(
        f"""
        **Identificador gerado:** `{record.id}`  
        Este registro já pode ser localizado pela consulta inteligente.
        """
    )