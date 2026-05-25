"""Application configuration constants for BuscaAI."""

from pathlib import Path


# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RECORDS_FILE = DATA_DIR / "records.json"


# Application identity
APP_NAME = "BuscaAI"
APP_SUBTITLE = "Assistente Inteligente de Consulta a Lições Aprendidas"
APP_DESCRIPTION = (
    "Registre conhecimentos obtidos a partir de problemas solucionados "
    "e consulte experiências anteriores utilizando inteligência artificial local."
)
PAGE_ICON = "🔎"


# Navigation labels displayed in the user interface
CONSULT_PAGE_LABEL = "Consultar conhecimento"
REGISTER_PAGE_LABEL = "Registrar conhecimento"


# Record configuration
SCHEMA_VERSION = "1.0"
RECORD_ID_PREFIX = "LL"
DEPARTMENT_OPTIONS = [
    "Produção",
    "Qualidade",
    "Estoque",
    "Manutenção",
    "Logística",
    "Engenharia",
    "Administrativo",
    "Outro",
]


# Ollama configuration
OLLAMA_MODEL = "qwen3:4b-instruct"
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_TIMEOUT_SECONDS = 120
OLLAMA_KEEP_ALIVE = "15m"

OLLAMA_OPTIONS = {
    "temperature": 0.1,
    "num_ctx": 4096,
    "num_predict": 400,
}