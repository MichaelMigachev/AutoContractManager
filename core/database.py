# core/database.py
import logging
import pandas as pd
from openpyxl import load_workbook
from typing import Optional, Dict, Any


# Импортируем пути
from config.paths import CLIENTS_DB_PATH, CONTRACTS_DB_PATH


def get_next_client_id(sheet_name="Folder") -> int:
    """Возвращает следующий номер клиента (№)"""
    try:
        df = pd.read_excel(CLIENTS_DB_PATH, sheet_name=sheet_name)
        return int(df["№"].max()) + 1 if not df.empty else 1
    except Exception as e:
        print(f"Ошибка чтения ID: {e}")
        return 1


def find_client(search_term: str) -> Optional[pd.Series]:
    """
    Ищет клиента по VIN, ФИО
    Возвращает строку DataFrame или None
    """
    try:
        df = pd.read_excel(CLIENTS_DB_PATH, sheet_name="Folder")
        df = df.fillna("")  # Заменяем NaN

        mask = (
            df["VIN"].astype(str).str.contains(search_term, case=False, na=False) |
            df["Фамилия"].str.contains(search_term, case=False, na=False) |
            df["Имя"].str.contains(search_term, case=False, na=False) |
            df["Отчество"].str.contains(search_term, case=False, na=False)
        )
        if mask.any():
            return df[mask].iloc[0]
    except Exception as e:
        print(f"Ошибка поиска клиента: {e}")
    return None


def save_client(data: Dict[str, Any]) -> bool:
    """Сохраняет нового клиента в Excel"""
    try:
        wb = load_workbook(CLIENTS_DB_PATH)
        ws = wb["Folder"]
        ws.append(list(data.values()))
        wb.save(CLIENTS_DB_PATH)
        logging.info(f"Клиент сохранён: {data['Фамилия']} {data['Имя']}")
        return True
    except Exception as e:
        logging.error(f"Ошибка сохранения клиента: {e}")
        return False


def get_next_contract_number() -> str:
    """Генерирует следующий номер договора: 101-ИП, 102-ИП и т.д."""
    try:
        df = pd.read_excel(CONTRACTS_DB_PATH, sheet_name="Registry")
        last_num = 0
        for num_str in df["Номер договора"]:
            if isinstance(num_str, str) and "-ИП" in num_str:
                try:
                    n = int(num_str.replace("-ИП", ""))
                    last_num = max(last_num, n)
                except:
                    continue
        return f"{last_num + 1}-ИП"
    except Exception as e:
        print(f"Ошибка получения номера договора: {e}")
        return "101-ИП"


def save_contract_record(contract_data: Dict[str, Any]) -> bool:
    """Сохраняет запись о договоре в реестр"""
    try:
        wb = load_workbook(CONTRACTS_DB_PATH)
        ws = wb["Registry"]
        row = [
            contract_data["Номер"],
            contract_data["ФИО"],
            contract_data["Номер договора"],
            contract_data["Телефон"],
            contract_data["Индекс"],
            contract_data["Дата"]
        ]
        ws.append(row)
        wb.save(CONTRACTS_DB_PATH)
        logging.info(f"Договор сохранён: {contract_data['Номер договора']}")
        return True
    except Exception as e:
        logging.error(f"Ошибка сохранения договора: {e}")
        return False


def get_next_registry_id() -> int:
    """
    Возвращает следующий порядковый номер для реестра договоров
    """
    try:
        df = pd.read_excel(CONTRACTS_DB_PATH, sheet_name="Registry")
        if df.empty:
            return 1
        last_id = df["Номер"].max()
        return int(last_id) + 1
    except Exception as e:
        logging.warning(f"⚠️ Не удалось прочитать Номер из реестра: {e}")
        return 1
