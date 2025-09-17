# Окно для выставления счёта
import tkinter as tk
from tkinter import ttk, messagebox

# Импорты из проекта
from core.database import find_client
from core.document_generator import generate_invoice
from config.settings import WINDOW_WIDTH, ENTRY_WIDTH


def open_invoice_window(parent):
    """
    Окно для выставления счёта клиенту
    :param parent: родительское окно
    """
    window = tk.Toplevel(parent)
    window.title("💰 Выставить счёт")
    window.geometry(f"{WINDOW_WIDTH}x400")
    window.resizable(False, False)
    window.transient(parent)
    window.grab_set()

    # Настройка сетки
    window.columnconfigure(1, weight=1)

    row_idx = 0

    # --- 1. Поиск клиента ---
    ttk.Label(window, text="Номер договора или ФИО/VIN:").grid(
        row=row_idx, column=0, padx=(10, 5), pady=15, sticky="e"
    )
    search_entry = ttk.Entry(window, width=ENTRY_WIDTH)
    search_entry.grid(row=row_idx, column=1, padx=(0, 10), pady=15, sticky="ew")
    search_entry.focus()
    row_idx += 1

    # --- 2. Услуга ---
    ttk.Label(window, text="Услуга:").grid(
        row=row_idx, column=0, padx=(10, 5), pady=10, sticky="e"
    )
    service_var = tk.StringVar(value="sbkts")
    ttk.Radiobutton(window, text="Выпуск СБКТС + ЭПТС", variable=service_var, value="sbkts").grid(
        row=row_idx, column=1, sticky="w", padx=(0, 10))
    row_idx += 1
    ttk.Radiobutton(window, text="Списание утильсбора", variable=service_var, value="scrap").grid(
        row=row_idx, column=1, sticky="w", padx=(0, 10))
    row_idx += 1

    # --- 3. Стоимость ---
    ttk.Label(window, text="Стоимость (руб):").grid(
        row=row_idx, column=0, padx=(10, 5), pady=10, sticky="e"
    )
    amount_entry = ttk.Entry(window, width=ENTRY_WIDTH)
    amount_entry.insert(0, "32000")  # значение по умолчанию
    amount_entry.grid(row=row_idx, column=1, padx=(0, 10), pady=10, sticky="ew")
    row_idx += 1

    # --- 4. Способ оплаты ---
    ttk.Label(window, text="Способ оплаты:").grid(
        row=row_idx, column=0, padx=(10, 5), pady=10, sticky="e"
    )
    payment_var = tk.StringVar(value="account")
    ttk.Radiobutton(window, text="На расчётный счёт", variable=payment_var, value="account").grid(
        row=row_idx, column=1, sticky="w", padx=(0, 10))
    row_idx += 1
    ttk.Radiobutton(window, text="На карту", variable=payment_var, value="card").grid(
        row=row_idx, column=1, sticky="w", padx=(0, 10))
    row_idx += 1

    def issue_invoice():
        search_term = search_entry.get().strip()
        service = service_var.get()
        try:
            amount = int(amount_entry.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму (целое положительное число).")
            return

        if not search_term:
            messagebox.showwarning("Внимание", "Введите номер договора, ФИО или VIN.")
            return

        # Поддержка формата "101-ИП"
        if "-ИП" not in search_term:
            search_term_for_search = search_term + "-ИП"
        else:
            search_term_for_search = search_term

        # Поиск в реестре договоров (по номеру) или по ФИО/VIN
        from core.database import pd
        try:
            contracts_df = pd.read_excel("data/contracts_registry.xlsx", sheet_name="Registry")
            contract_match = contracts_df[
                contracts_df["Номер договора"].astype(str) == search_term_for_search
                ]
            if not contract_match.empty:
                # Нашли по номеру договора → ищем клиента по ФИО
                client_fio = contract_match.iloc[0]["ФИО"]
                client_parts = client_fio.split()
                if len(client_parts) >= 1:
                    client_data = find_client(client_parts[0])  # по фамилии
                else:
                    client_data = None
            else:
                # Ищем напрямую по ФИО или VIN
                client_data = find_client(search_term)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать реестр договоров:\n{e}")
            return

        if client_data is None:
            messagebox.showerror("Ошибка", "Клиент не найден.")
            return

        # Подтверждение
        full_name = f"{client_data['Фамилия']} {client_data['Имя']} {client_data['Отчество']}"
        msg = f"Выставить счёт на {amount} ₽\nуслуга: {service}\nклиенту: {full_name}?"
        if not messagebox.askyesno("Подтверждение", msg):
            return

        # Генерация счёта
        success = generate_invoice(
            client_data=client_data.to_dict(),
            contract_num=search_term_for_search,
            service_type=service,
            amount=amount,
            payment_method=payment_var.get()
        )

        if success:
            messagebox.showinfo("Успех", "Счёт успешно создан!")
            window.destroy()
        else:
            messagebox.showerror("Ошибка", "Не удалось создать счёт.\nПроверьте шаблоны в папке 'templates/'.")

    # --- Кнопки ---
    button_frame = ttk.Frame(window)
    button_frame.grid(row=row_idx + 1, column=0, columnspan=2, pady=20)

    ttk.Button(button_frame, text="Отмена", command=window.destroy).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Выставить счёт", command=issue_invoice).pack(side="left", padx=5)

    # Обработка Enter
    search_entry.bind("<Return>", lambda event: amount_entry.focus())
    amount_entry.bind("<Return>", lambda event: issue_invoice())
