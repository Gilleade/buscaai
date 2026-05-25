"""Streamlit view for registering new lessons learned records."""

from __future__ import annotations

import streamlit as st

from config import DEPARTMENT_OPTIONS
from services import RecordService


def render_register_view(record_service: RecordService) -> None:
    """Render the form responsible for registering a new record."""
    st.header("Registrar conhecimento")

    st.write(
        "Registre uma solução já aplicada para que ela possa ser "
        "consultada futuramente pelo BuscaAI."
    )

    with st.form("register_record_form", clear_on_submit=True):
        st.subheader("Identificação")

        title = st.text_input(
            "Título do conhecimento",
            placeholder="Ex.: Checklist para evitar retrabalho na montagem",
        )

        department = st.selectbox(
            "Área / Setor",
            options=DEPARTMENT_OPTIONS,
        )

        custom_department = ""

        if department == "Outro":
            custom_department = st.text_input(
                "Informe a área / setor",
                placeholder="Ex.: Compras",
            )

        process = st.text_input(
            "Processo ou atividade",
            placeholder="Ex.: Montagem de componentes",
        )

        st.subheader("Contexto do problema")

        problem_description = st.text_area(
            "Descrição do problema",
            placeholder=(
                "Descreva a situação que ocorreu e o impacto observado."
            ),
            height=110,
        )

        identified_cause = st.text_area(
            "Causa identificada",
            placeholder="Descreva a causa ou fator que contribuiu para o problema.",
            height=100,
        )

        st.subheader("Conhecimento aplicado")

        implemented_solution = st.text_area(
            "Solução aplicada",
            placeholder="Descreva a ação que foi efetivamente utilizada.",
            height=110,
        )

        observed_result = st.text_area(
            "Resultado observado",
            placeholder="Descreva o resultado obtido após aplicar a solução.",
            height=100,
        )

        keywords = st.text_input(
            "Palavras-chave (opcional)",
            placeholder="Ex.: montagem, retrabalho, checklist",
        )

        submitted = st.form_submit_button(
            "Salvar conhecimento",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    selected_department = (
        custom_department if department == "Outro" else department
    )

    try:
        record = record_service.register_record(
            title=title,
            department=selected_department,
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
    st.write(f"**Identificador:** {record.id}")
    st.info(
        "Este registro já está disponível para consulta no BuscaAI."
    )