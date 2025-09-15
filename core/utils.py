# core/utils.py
import os
import re
import logging
from datetime import datetime
from pathlib import Path

# Путь к логам
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOGS_DIR / "app.log"

# Создаём папку для логов
os.makedirs(LOGS_DIR, exist_ok=True)


def setup_logging():
    """Настраивает логирование в файл и консоль"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Формат
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для файла
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Добавляем обработчики, если их ещё нет
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logging.info("Логирование запущено")


def get_current_date(fmt="%d.%m.%Y") -> str:
    """Текущая дата в нужном формате"""
    return datetime.now().strftime(fmt)


def get_current_date_verbose() -> str:
    """Дата в словесном формате: '5 ноября 2024 г.'"""
    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]
    now = datetime.now()
    return f"{now.day} {months[now.month - 1]} {now.year} г."


def sanitize_filename(filename: str) -> str:
    """
    Убирает недопустимые символы из имени файла
    """
    # Заменяем недопустимые символы на подчёркивание
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Убираем множественные пробелы и подчистить начало/конец
    filename = re.sub(r'\s+', ' ', filename).strip()
    return filename


def format_phone(phone: str) -> tuple[str, str]:
    """
    Форматирует телефон и возвращает (форматированный, последние_4_цифры)
    Пример: +7 999 123-45-67, 45 67
    """
    digits = ''.join(filter(str.isdigit, phone))[-11:]
    digits = digits.zfill(11)

    formatted = f"+{digits[0]} {digits[1:4]} {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    index_part = f"{digits[-4:-2]} {digits[-2:]}"

    return formatted, index_part


def number_to_words(num: int) -> str:
    """Преобразует число от 10 до 99 в текст (частичная реализация)"""
    if num < 10 or num > 99:
        return "число вне диапазона"

    ones = ['', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    teens = ['десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать',
             'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать']
    tens = ['', '', 'двадцать', 'тридцать', 'сорок', 'пятьдесят',
            'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']

    if 10 <= num < 20:
        return teens[num - 10]
    else:
        t = tens[num // 10]
        o = ones[num % 10]
        return t + ('' if o == '' else ' ' + o)
