# core/validators.py
import re
# from typing import Match


def validate_phone(phone: str) -> bool:
    """
    Проверяет, соответствует ли строка формату телефона.
    Принимает: +7 999 123-45-67, 89991234567, +7 (999) 123-45-67 и т.п.
    """
    if not phone or not isinstance(phone, str):
        return False

    # Удаляем всё, кроме цифр
    digits = re.sub(r'\D', '', phone)

    # Должно быть 10 или 11 цифр (с 8 или без)
    if len(digits) == 11:
        return digits[0] in ['7', '8']  # +7 или 8
    elif len(digits) == 10:
        return True  # например, 9991234567
    else:
        return False


def validate_vin(vin: str) -> bool:
    """
    Проверяет, является ли строка корректным VIN (17 символов, латинские буквы и цифры)
    """
    if not vin or not isinstance(vin, str):
        return False

    vin = vin.strip().upper()
    # Убираем возможные разделители
    vin = re.sub(r'[\s\-_]+', '', vin)

    # Ровно 17 символов, только A-Z, 0-9, кроме I, O, Q
    pattern = r'^[A-HJ-NPR-Z0-9]{17}$'
    return bool(re.match(pattern, vin))


def validate_date(date_str: str) -> bool:
    """
    Проверяет, соответствует ли строка формату ДД.ММ.ГГГГ
    """
    if not date_str or not isinstance(date_str, str):
        return False

    import re
    match = re.match(r'^(\d{2})\.(\d{2})\.(\d{4})$', date_str.strip())
    if not match:
        return False

    try:
        day, month, year = map(int, match.groups())
        # Проверка диапазонов
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        if year < 1900 or year > 2100:
            return False

        # Проверка корректности даты (например, 30 февраля)
        from datetime import datetime
        datetime(year, month, day)
        return True
    except:
        return False


# --- Для тестирования ---
if __name__ == "__main__":
    print("Телефон:")
    print(validate_phone("+7 999 123-45-67"))  # True
    print(validate_phone("89991234567"))       # True
    print(validate_phone("123"))               # False

    print("\nVIN:")
    print(validate_vin("VF1KZ1G0643044404"))   # True
    print(validate_vin("VF1-KZ1G0-64304-4404")) # True (с дефисами)
    print(validate_vin("VF1KZ1G064304440"))    # False (16 символов)

    print("\nДата:")
    print(validate_date("05.11.2024"))         # True
    print(validate_date("30.02.2024"))         # False
    print(validate_date("1.1.2024"))           # False (не ДД.ММ.ГГГГ)
