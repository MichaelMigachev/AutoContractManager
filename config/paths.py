# config/paths.py
from pathlib import Path

# Корень проекта (папка, где лежит main.py)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Папки
DATA_DIR = PROJECT_ROOT / "data"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
OUTPUT_DIR = PROJECT_ROOT / "documents_ready"
LOGS_DIR = PROJECT_ROOT / "logs"

# Файлы данных
CLIENTS_DB_PATH = DATA_DIR / "database_of_contracts.xlsx"
CONTRACTS_DB_PATH = DATA_DIR / "contracts_registry.xlsx"

# Шаблоны документов
CONTRACT_TEMPLATE = TEMPLATES_DIR / "contract_template.docx"
INVOICE_TEMPLATE = TEMPLATES_DIR / "invoice_template.docx"
INVOICE_CARD_TEMPLATE = TEMPLATES_DIR / "invoice_card_template.docx"


# Убедимся, что папки существуют
def setup_directories():
    """Создаёт необходимые директории при импорте"""
    for directory in [DATA_DIR, TEMPLATES_DIR, OUTPUT_DIR, LOGS_DIR]:
        directory.mkdir(exist_ok=True)


setup_directories()
