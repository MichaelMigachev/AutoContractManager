# окно ввода данных клиента
import tkinter as tk
from tkinter import ttk, messagebox

# Импорты из проекта
from core.database import find_client, save_contract_record, get_next_registry_id, is_contract_exists_for_fio
from core.document_generator import generate_contract
from config.settings import WINDOW_WIDTH, ENTRY_WIDTH
from core.utils import get_current_date


def open_contract_window(parent):
    """
    Окно для поиска клиента и оформления договора
    :param parent: родительское окно
    """
    window = tk.Toplevel(parent)
    window.title("📄 Оформление договора")
    window.geometry(f"{WINDOW_WIDTH}x200")
    window.resizable(False, False)
    window.transient(parent)
    window.grab_set()

    # Центрирование элементов
    window.columnconfigure(1, weight=1)

    # Поле ввода
    ttk.Label(window, text="Введите VIN или ФИО:").grid(
        row=0, column=0, padx=(10, 5), pady=30, sticky="e"
    )
    search_entry = ttk.Entry(window, width=ENTRY_WIDTH)
    search_entry.grid(row=0, column=1, padx=(0, 10), pady=30, sticky="ew")
    search_entry.focus()

    def create_contract():
        search_term = search_entry.get().strip()
        if not search_term:
            messagebox.showwarning("Внимание", "Введите данные для поиска.")
            return

        # Поиск клиента
        client_data = find_client(search_term)
        if client_data is None:
            messagebox.showerror("Ошибка", "Клиент не найден. Проверьте ФИО или VIN.")
            return

        # Формируем полное ФИО
        full_name = f"{client_data['Фамилия']} {client_data['Имя']} {client_data['Отчество']}"

        # 🔍 Проверка на существующий договор
        if is_contract_exists_for_fio(full_name):
            answer = messagebox.askyesno(
                "Дубликат договора",
                f"Договор для клиента:\n{full_name}\nуже существует.\n\n"
                "Вы уверены, что хотите создать ещё один?"
            )
            if not answer:
                return  # Отмена операции
        # Подтверждение
        full_name = f"{client_data['Фамилия']} {client_data['Имя']} {client_data['Отчество']}"
        if not messagebox.askyesno("Подтверждение", f"Оформить договор для:\n{full_name}?"):
            return

        # Генерация договора
        success = generate_contract(client_data.to_dict())
        if success:
            # Сохранение в реестр договоров
            from core.database import get_next_contract_number

            contract_data = {
                "Номер": get_next_registry_id(),
                "ФИО": full_name,
                "Номер договора": get_next_contract_number(),
                "Телефон": client_data["Телефон"],
                "Индекс": client_data["Индекс"],
                "Дата": get_current_date()
            }
            save_contract_record(contract_data)

            messagebox.showinfo("Успех", f"Договор успешно создан и сохранён! \n\n"
                                         f"Номер договора: {contract_data['Номер договора']}\n"
                                         f"Клиент: {full_name}\n"
                                         f"Дата: {get_current_date()}")
            window.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось создать договор.\nПроверьте шаблон 'contract_template.docx'.")

    # Кнопки
    button_frame = ttk.Frame(window)
    button_frame.grid(row=1, column=0, columnspan=2, pady=10)

    ttk.Button(button_frame, text="Отмена", command=window.destroy).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Оформить", command=create_contract).pack(side="left", padx=5)

    # Обработка Enter
    search_entry.bind("<Return>", lambda event: create_contract())
