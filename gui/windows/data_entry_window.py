# gui/windows/data_entry_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any

# Импорты из проекта
from core.database import save_client, get_next_client_id
from core.validators import validate_phone, validate_vin, validate_date
from core.utils import get_current_date, format_phone
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, ENTRY_WIDTH


def open_data_entry_window(parent):
    """
    Открывает окно для ввода данных нового клиента
    :param parent: родительское окно (Tk или Toplevel)
    """
    window = tk.Toplevel(parent)
    window.title("➕ Новый клиент")
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    window.resizable(False, False)
    window.transient(parent)  # Окно поверх главного
    window.grab_set()  # Блокировка главного окна

    # Настройка сетки
    window.columnconfigure(1, weight=1)

    # Поля формы
    fields = [
        ("Фамилия", "surname"),
        ("Имя", "name"),
        ("Отчество", "patronymic"),
        ("Марка авто", "car_model"),
        ("VIN", "vin"),
        ("Индекс", "index"),
        ("Адрес", "address"),
        ("Паспорт (серия и номер)", "passport"),
        ("Кем выдан", "issued_by"),
        ("Дата выдачи", "issue_date"),
        ("Код подразделения", "dep_code"),
        ("Телефон", "phone"),
        ("Дата рождения", "birth_date"),
    ]

    entries: Dict[str, ttk.Entry] = {}

    for i, (label_text, key) in enumerate(fields):
        ttk.Label(window, text=label_text + ":").grid(
            row=i, column=0, sticky="e", padx=(10, 5), pady=5
        )
        entry = ttk.Entry(window, width=ENTRY_WIDTH)
        entry.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="ew")
        entries[key] = entry

    # Поле "Дата создания" — только для чтения
    ttk.Label(window, text="Дата создания:").grid(
        row=len(fields), column=0, sticky="e", padx=(10, 5), pady=5
    )
    date_entry = ttk.Entry(window, width=ENTRY_WIDTH)
    date_entry.insert(0, get_current_date())
    date_entry.config(state="readonly")
    date_entry.grid(row=len(fields), column=1, padx=(0, 10), pady=5, sticky="ew")

    def submit():
        """Сбор данных и сохранение"""
        data = {}
        for (label, key), entry in zip(fields, entries.values()):
            value = entry.get().strip()
            if not value and key not in ["patronymic"]:  # Отчество — опционально
                messagebox.showwarning("Ошибка", f"Поле '{label}' обязательно для заполнения.")
                return
            data[key] = value

        # Валидация
        if not validate_phone(data["phone"]):
            messagebox.showerror("Ошибка", "Неверный формат телефона. Пример: +7 999 123-45-67")
            return

        if not validate_vin(data["vin"]):
            messagebox.showerror("Ошибка", "Неверный формат VIN. Должно быть 17 символов (буквы и цифры).")
            return

        if not validate_date(data["issue_date"]):
            messagebox.showerror("Ошибка", "Неверный формат даты выдачи. Используйте ДД.ММ.ГГГГ")
            return

        if not validate_date(data["birth_date"]):
            messagebox.showerror("Ошибка", "Неверный формат даты рождения. Используйте ДД.ММ.ГГГГ")
            return

        # Форматирование телефона
        formatted_phone, _ = format_phone(data["phone"])

        # Генерация имени папки
        folder_name = f"{data['surname']}_{data['car_model']}_vin {data['vin']}_{data['index']}"

        # Полные данные для сохранения
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

        # Сохранение
        if save_client(full_data):
            messagebox.showinfo("Успех", f"Клиент {data['surname']} {data['name']} добавлен!")
            window.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные. Проверьте файл Excel.")

    # Кнопки
    button_frame = ttk.Frame(window)
    button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

    ttk.Button(button_frame, text="Отмена", command=window.destroy).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Сохранить", command=submit).pack(side="left", padx=5)

    # Фокус на первое поле
    entries["surname"].focus()
