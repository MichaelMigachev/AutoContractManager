# core/document_generator.py
from docx import Document
from pathlib import Path
import logging
from typing import Dict, Any

# Импорты из проекта
from config.paths import OUTPUT_DIR, CONTRACT_TEMPLATE, INVOICE_TEMPLATE, INVOICE_CARD_TEMPLATE
from config.settings import (
    APP_NAME,
    COMPANY_NAME,
    DEFAULT_CURRENCY,
    CURRENCY_SYMBOL
)
from core.utils import sanitize_filename, get_current_date


def replace_placeholders_in_paragraph(paragraph, data: Dict[str, Any]):
    """Заменяет {ключ} на значение в параграфе"""
    for key, value in data.items():
        placeholder = f"{{{key}}}"
        if placeholder in paragraph.text:
            # Сохраняем форматирование каждого run
            for run in paragraph.runs:
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, str(value))


def replace_placeholders_in_table(table, data: Dict[str, Any]):
    """Заменяет {ключ} на значение в таблицах"""
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                replace_placeholders_in_paragraph(paragraph, data)


def fill_template(template_path: Path, output_path: Path, data: Dict[str, Any]) -> bool:
    """
    Заполняет шаблон Word и сохраняет результат

    :param template_path: путь к .docx шаблону
    :param output_path: куда сохранить заполненный документ
    :param data: словарь с данными для подстановки
    :return: True при успехе
    """
    try:
        if not template_path.exists():
            logging.error(f"Шаблон не найден: {template_path}")
            return False

        doc = Document(template_path)

        # Замена в обычных параграфах
        for paragraph in doc.paragraphs:
            replace_placeholders_in_paragraph(paragraph, data)

        # Замена в таблицах
        for table in doc.tables:
            replace_placeholders_in_table(table, data)

        # Сохранение
        doc.save(output_path)
        logging.info(f"Документ создан: {output_path}")
        return True

    except Exception as e:
        logging.error(f"Ошибка при генерации документа: {e}")
        return False


def generate_contract(client_data: Dict[str, Any]) -> bool:
    """
    Создаёт договор на основе данных клиента

    :param client_data: данные клиента из Excel
    :return: True при успехе
    """
    from core.database import get_next_contract_number

    # Данные для шаблона
    contract_num = get_next_contract_number()
    full_name = f"{client_data['Фамилия']} {client_data['Имя']} {client_data['Отчество']}"
    car_info = f"{client_data['Марка авто']} (VIN {client_data['VIN']})"
    phone, _ = client_data.get("Телефон_формат", ("", ""))  # может быть предварительно обработан
    if not phone:
        phone, _ = format_phone(client_data['Телефон'])

    context = {
        "NUM": contract_num.replace("-ИП", ""),
        "FULL_NUM": contract_num,
        "DATE": get_current_date(),
        "FIO": full_name,
        "FULL_FIO": full_name,
        "SHORT_FIO": f"{client_data['Фамилия']} {client_data['Имя'][0]}. {client_data['Отчество'][0]}.",
        "CAR": client_data['Марка авто'],
        "VIN": client_data['VIN'],
        "CAR_INFO": car_info,
        "ADDRESS": client_data['Адрес'],
        "INDEX": client_data['Индекс'],
        "PASSPORT": client_data['Паспорт (серия и номер)'],
        "ISSUED_BY": client_data['Кем выдан'],
        "ISSUE_DATE": client_data['Дата выдачи'],
        "DEP_CODE": client_data['Код подразделения'],
        "BIRTH_DATE": client_data['Дата рождения'],
        "PHONE": phone,
        "COMPANY": COMPANY_NAME,
        "APP_NAME": APP_NAME
    }

    # Имя файла
    safe_fio = sanitize_filename(full_name)
    safe_index = client_data['Индекс'] if '*' not in client_data['Индекс'] else "ИНДЕКС"
    filename = f"Договор №{contract_num} ({safe_fio})_{safe_index}.docx"
    output_path = OUTPUT_DIR / filename

    # Генерация
    success = fill_template(CONTRACT_TEMPLATE, output_path, context)
    return success


def generate_invoice(
    client_data: Dict[str, Any],
    contract_num: str,
    service_type: str,
    amount: int,
    payment_method: str = "account"  # 'account' или 'card'
) -> bool:
    """
    Выставляет счёт

    :param client_data: данные клиента
    :param contract_num: номер договора
    :param service_type: услуга ("sbkts" или "scrap")
    :param amount: сумма в рублях
    :param payment_method: способ оплаты
    :return: True при успехе
    """
    from core.utils import number_to_words

    full_name = f"{client_data['Фамилия']} {client_data['Имя']} {client_data['Отчество']}"
    thousands = amount // 1000
    amount_text = number_to_words(thousands).capitalize() + " тысяч"

    service_desc = {
        "sbkts": "выпуску СБКТС + ЭПТС",
        "scrap": "списанию утильсбора"
    }.get(service_type, "услуге")

    # Выбор шаблона
    if payment_method == "card":
        template_path = INVOICE_CARD_TEMPLATE
        method_label = " НА КАРТУ "
    else:
        template_path = INVOICE_TEMPLATE
        method_label = ""

    context = {
        "NUM": contract_num.replace("-ИП", ""),
        "FULL_NUM": f"{contract_num}-001",
        "DATE": get_current_date(),
        "VERBOSE_DATE": get_current_date("%d %B %Y").replace(' ', ' ').replace('0', 'о'),  # можно улучшить
        "FIO": full_name,
        "ADDRESS": client_data['Адрес'],
        "AMOUNT": str(amount),
        "AMOUNT_RUB": f"{amount} {CURRENCY_SYMBOL}",
        "AMOUNT_TEXT": amount_text,
        "SERVICE": service_desc,
        "CAR_INFO": f"{client_data['Марка авто']}_vin {client_data['VIN']}",
        "INDEX": client_data['Индекс'],
        "CONTRACT_REF": f"{contract_num} от {client_data.get('Дата создания папки', '__.__.____')}",
        "METHOD_LABEL": method_label.strip(),
        "COMPANY": COMPANY_NAME,
        "INN": "123456789012",
        "BANK_ACCOUNT": "40817810123456789012",
        "BANK_NAME": "Сбербанк",
        "BANK_BIC": "044525225",
        "CORR_ACCOUNT": "30101810400000000225"
    }

    # Имя файла
    safe_fio = sanitize_filename(full_name)
    filename = f"Счёт{method_label}№ {context['FULL_NUM']} от {context['DATE']} для {safe_fio}_{context['INDEX']}.docx"
    filename = sanitize_filename(filename)
    output_path = OUTPUT_DIR / filename

    # Генерация
    success = fill_template(template_path, output_path, context)
    return success


# --- Удобные функции ---

def format_phone(phone: str) -> tuple[str, str]:
    """Дублируем из utils, если нужно (или импортировать)"""
    from core.utils import format_phone as util_format
    return util_format(phone)
