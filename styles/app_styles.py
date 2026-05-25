"""Visual helpers and custom styles for the BuscaAI interface."""

from __future__ import annotations

import streamlit as st


CUSTOM_CSS = """
<style>
:root {
    --buscaai-bg: #080D13;
    --buscaai-panel: #0F1620;
    --buscaai-panel-soft: #121C28;
    --buscaai-border: #1D2A38;
    --buscaai-border-strong: #263748;
    --buscaai-text: #F1F5F9;
    --buscaai-muted: #95A4B5;
    --buscaai-accent: #2BD4B3;
    --buscaai-accent-soft: rgba(43, 212, 179, 0.10);
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 78% 4%, rgba(43, 212, 179, 0.08), transparent 30%),
        var(--buscaai-bg);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background-color: #090F16;
    border-right: 1px solid var(--buscaai-border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.6rem;
}

.block-container {
    max-width: 960px;
    padding-top: 2.3rem;
    padding-bottom: 7.5rem;
}

.buscaai-brand {
    padding: 0.3rem 0 1.15rem 0;
}

.buscaai-brand-name {
    font-size: 1.48rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--buscaai-text);
    margin-bottom: 0.18rem;
}

.buscaai-brand-name span {
    color: var(--buscaai-accent);
}

.buscaai-brand-subtitle {
    font-size: 0.80rem;
    line-height: 1.38;
    color: var(--buscaai-muted);
}

.buscaai-sidebar-card {
    margin-top: 1.2rem;
    padding: 0.9rem 0.95rem;
    border: 1px solid var(--buscaai-border);
    border-radius: 14px;
    background: var(--buscaai-panel);
}

.buscaai-sidebar-label {
    font-size: 0.67rem;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: var(--buscaai-muted);
    margin-bottom: 0.38rem;
}

.buscaai-sidebar-value {
    font-size: 0.85rem;
    color: var(--buscaai-text);
    margin-bottom: 0.22rem;
}

.buscaai-page-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--buscaai-accent);
    margin-bottom: 0.72rem;
}

.buscaai-page-title {
    font-size: 2.18rem;
    line-height: 1.08;
    font-weight: 680;
    letter-spacing: -0.055em;
    color: var(--buscaai-text);
    margin-bottom: 0.70rem;
}

.buscaai-page-description {
    max-width: 710px;
    color: var(--buscaai-muted);
    font-size: 1rem;
    line-height: 1.62;
    margin-bottom: 1.55rem;
}

.buscaai-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    border: 1px solid rgba(43, 212, 179, 0.25);
    background: var(--buscaai-accent-soft);
    border-radius: 999px;
    padding: 0.38rem 0.72rem;
    font-size: 0.79rem;
    color: #B8F3E8;
}

.buscaai-status-dot {
    height: 7px;
    width: 7px;
    background-color: var(--buscaai-accent);
    border-radius: 999px;
    display: inline-block;
}

.buscaai-section-title {
    color: var(--buscaai-muted);
    text-transform: uppercase;
    font-size: 0.71rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    margin-top: 0.5rem;
    margin-bottom: 0.25rem;
}

div[data-testid="stChatMessage"] {
    background: var(--buscaai-panel);
    border: 1px solid var(--buscaai-border);
    border-radius: 17px;
    padding: 0.35rem 0.2rem;
    margin-bottom: 0.7rem;
}

[data-testid="stChatInput"] {
    border-color: var(--buscaai-border-strong);
}

[data-testid="stForm"] {
    background: var(--buscaai-panel);
    border: 1px solid var(--buscaai-border);
    border-radius: 18px;
    padding: 1.2rem 1.3rem 0.35rem 1.3rem;
}

/* Registration form field contrast */
[data-testid="stForm"] div[data-baseweb="input"] > div,
[data-testid="stForm"] div[data-baseweb="textarea"] > div,
[data-testid="stForm"] div[data-baseweb="select"] > div {
    background-color: #18222D;
    border-color: #2B3948;
    border-radius: 10px;
    transition: border-color 0.18s ease, box-shadow 0.18s ease;
}

[data-testid="stForm"] div[data-baseweb="input"] > div:hover,
[data-testid="stForm"] div[data-baseweb="textarea"] > div:hover,
[data-testid="stForm"] div[data-baseweb="select"] > div:hover {
    border-color: #3A4C5F;
}

[data-testid="stForm"] div[data-baseweb="input"] > div:focus-within,
[data-testid="stForm"] div[data-baseweb="textarea"] > div:focus-within,
[data-testid="stForm"] div[data-baseweb="select"] > div:focus-within {
    border-color: var(--buscaai-accent);
    box-shadow: 0 0 0 1px rgba(43, 212, 179, 0.35);
}

[data-testid="stForm"] input,
[data-testid="stForm"] textarea {
    color: var(--buscaai-text);
    background-color: transparent;
}

[data-testid="stForm"] input::placeholder,
[data-testid="stForm"] textarea::placeholder {
    color: #728294;
    opacity: 1;
}

[data-testid="stForm"] label {
    color: #D5DEE8;
    font-weight: 500;
}

[data-testid="stForm"] [data-baseweb="select"] span {
    color: var(--buscaai-text);
}

div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    border-radius: 11px;
    min-height: 2.55rem;
    font-weight: 550;
}

div[data-testid="stAlert"] {
    border-radius: 13px;
}

hr {
    border-color: var(--buscaai-border);
}
.buscaai-navigation-title {
    margin-top: 1.15rem;
    margin-bottom: 0.65rem;
    color: var(--buscaai-muted);
    text-transform: uppercase;
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.15em;
}

[data-testid="stSidebar"] div[data-testid="stButton"] button {
    justify-content: flex-start;
    border-radius: 11px;
    min-height: 2.8rem;
    margin-bottom: 0.25rem;
}

[data-testid="stSidebar"] div[data-testid="stButton"] button p {
    font-weight: 500;
}

.st-key-chat_composer {
    background: rgba(8, 13, 19, 0.94);
    border-top: 1px solid var(--buscaai-border);
    padding: 0.75rem 0.1rem 0.7rem 0.1rem;
}

.st-key-chat_composer div[data-testid="stButton"] button {
    min-height: 3.05rem;
    border-radius: 13px;
    font-size: 1.02rem;
    padding-left: 0;
    padding-right: 0;
}

.st-key-chat_composer [data-testid="stChatInput"] {
    border-radius: 14px;
}

.st-key-chat_composer [data-testid="stChatInput"] textarea {
    min-height: 3.05rem;
}
</style>
"""


def apply_app_styles() -> None:
    """Inject the custom visual layer used by the application."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_sidebar_brand() -> None:
    """Render the application identity in the sidebar."""
    st.markdown(
        """
        <div class="buscaai-brand">
            <div class="buscaai-brand-name">Busca<span>AI</span></div>
            <div class="buscaai-brand-subtitle">
                Assistente de consulta<br>
                a lições aprendidas
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(
    *,
    eyebrow: str,
    title: str,
    description: str,
) -> None:
    """Render a consistent title block for application pages."""
    st.markdown(
        f"""
        <div class="buscaai-page-eyebrow">{eyebrow}</div>
        <div class="buscaai-page-title">{title}</div>
        <div class="buscaai-page-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )