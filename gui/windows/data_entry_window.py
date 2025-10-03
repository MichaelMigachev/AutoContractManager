# gui/windows/data_entry_window.py
import tkinter as tk
from tkinter import ttk, messagebox

# Импорты из проекта
from core.database import save_client, get_next_client_id
from core.validators import validate_phone, validate_vin
from core.utils import get_current_date, format_phone
from config.settings import WINDOW_WIDTH, ENTRY_WIDTH


def open_data_entry_window(parent):
    """
    Открывает окно для ввода данных нового клиента
    :param parent: родительское окно (Tk или Toplevel)
    """
    window = tk.Toplevel(parent)
    window.title("➕ Новый клиент")
    window.geometry(f"{WINDOW_WIDTH}x600")
    window.resizable(False, False)
    window.transient(parent)
    window.grab_set()

    # Настройка сетки
    window.columnconfigure(1, weight=1)

    # Поля формы
    fields_config = [
        ("Фамилия", "surname"),
        ("Имя", "name"),
        ("Отчество", "patronymic"),
        ("Марка авто", "car_model"),  # ✅ Обязательное
        ("VIN", "vin"),              # ✅ Обязательное
        ("Индекс", "index"),         # ✅ Обязательное
        ("Адрес", "address"),
        ("Паспорт (серия и номер)", "passport"),
        ("Кем выдан", "issued_by"),
        ("Дата выдачи", "issue_date"),
        ("Код подразделения", "dep_code"),
        ("Телефон", "phone"),
        ("Дата рождения", "birth_date"),
    ]

    entries: dict = {}

    for i, (label_text, key) in enumerate(fields_config):
        ttk.Label(window, text=label_text + ":").grid(
            row=i, column=0, sticky="e", padx=(10, 5), pady=5
        )
        entry = ttk.Entry(window, width=ENTRY_WIDTH)
        entry.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="ew")
        entries[key] = entry

    # Поле "Дата создания" — только для чтения
    ttk.Label(window, text="Дата создания:").grid(
        row=len(fields_config), column=0, sticky="e", padx=(10, 5), pady=5
    )
    date_entry = ttk.Entry(window, width=ENTRY_WIDTH)
    date_entry.insert(0, get_current_date())
    date_entry.config(state="readonly")
    date_entry.grid(row=len(fields_config), column=1, padx=(0, 10), pady=5, sticky="ew")

    def submit():
        """Сбор данных и сохранение"""
        # Собираем данные
        data = {}
        for (label, key), entry in zip(fields_config, entries.values()):
            value = entry.get().strip()
            data[key] = value

        # 🔹 Проверяем только обязательные поля
        required_fields = {
            "car_model": "Марка авто",
            "vin": "VIN",
            "index": "Индекс"
        }

        for key, label in required_fields.items():
            if not data[key]:
                messagebox.showwarning("Ошибка", f"Поле '{label}' обязательно для заполнения.")
                return

        # 🔹 Валидация VIN
        if not validate_vin(data["vin"]):
            messagebox.showerror("Ошибка", "Неверный формат VIN. Должно быть 17 символов (A-Z, 0-9).")
            return

        # 🔹 Валидация телефона (если указан)
        phone = data["phone"]
        if phone and not validate_phone(phone):
            if not messagebox.askyesno("Подтвердить", "Некорректный формат телефона.\nВсё равно сохранить?"):
                return

        # 🔹 Валидация даты выдачи (если указана)
        issue_date = data["issue_date"]
        if issue_date:
            from core.validators import validate_date
            if not validate_date(issue_date):
                if not messagebox.askyesno("Подтвердить", "Некорректная дата выдачи.\nВсё равно сохранить?"):
                    return

        # 🔹 Валидация даты рождения (если указана)
        birth_date = data["birth_date"]
        if birth_date:
            from core.validators import validate_date
            if not validate_date(birth_date):
                if not messagebox.askyesno("Подтвердить", "Некорректная дата рождения.\nВсё равно сохранить?"):
                    return

        # 🔹 Форматирование телефона
        formatted_phone = ""
        phone_index_part = ""
        if phone:
            try:
                formatted_phone, phone_index_part = format_phone(phone)
            except Exception:
                formatted_phone = phone  # если ошибка — сохраняем как есть

        # 🔹 Генерация имени папки
        folder_name = f"{data['surname']}_{data['car_model']}_vin {data['vin']}_{data['index']}"

        # 🔹 Подготовка данных для сохранения
        full_data = {
            "№": get_next_client_id(),
            "Фамилия": data["surname"],
            "Имя": data["name"],
            "Отчество": data["patronymic"],
            "Марка авто": data["car_model"],
            "VIN": data["vin"],
            "Индекс": data["index"],
            "Папка": folder_name,
            "Адрес": data["address"],
            "Паспорт (серия и номер)": data["passport"],
            "Кем выдан": data["issued_by"],
            "Дата выдачи": data["issue_date"],
            "Код подразделения": data["dep_code"],
            "Телефон": formatted_phone,
            "Дата рождения": data["birth_date"],
            "Дата создания папки": get_current_date()
        }

        # 🔹 Сохранение
        if save_client(full_data):
            messagebox.showinfo("Успех", f"Клиент добавлен!")
            window.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные.")

    # Кнопки
    button_frame = ttk.Frame(window)
    button_frame.grid(row=len(fields_config) + 1, column=0, columnspan=2, pady=20)

    ttk.Button(button_frame, text="Отмена", command=window.destroy).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Сохранить", command=submit).pack(side="left", padx=5)

    # Фокус на первое поле
    entries["surname"].focus()
