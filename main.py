# main.py
import tkinter as tk
from tkinter import messagebox
import os

# Пути к корню проекта и добавление в sys.path (чтобы импорты работали)
import sys
from pathlib import Path

# Определяем путь к проекту
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))

# Импортируем GUI-окна из модулей
from gui.windows.data_entry_window import open_data_entry_window
from gui.windows.contract_window import open_contract_window
from gui.windows.invoice_window import open_invoice_window
from gui.windows.edit_window import open_edit_window

# Импортируем утилиты
from core.utils import setup_logging
from config.paths import OUTPUT_DIR, CLIENTS_DB_PATH, CONTRACTS_DB_PATH


def create_directories():
    """Создаёт необходимые папки, если их нет"""
    dirs = [OUTPUT_DIR, "logs"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def check_files():
    """Проверяет наличие необходимых файлов"""
    missing = []
    if not os.path.exists(CLIENTS_DB_PATH):
        missing.append("data/database_of_contracts.xlsx")
    if not os.path.exists(CONTRACTS_DB_PATH):
        missing.append("data/contracts_registry.xlsx")
    return missing


def on_closing():
    """Действие при закрытии окна"""
    if messagebox.askokcancel("Выход", "Закрыть программу?"):
        root.destroy()


def create_main_window():
    global root
    root = tk.Tk()
    root.title("AutoContractManager — Оформление договоров")
    root.geometry("450x500")
    root.resizable(False, False)

    # Настройка фона и шрифтов
    root.configure(bg="#f0f0f0")
    button_font = ("Arial", 12)

    # Заголовок
    tk.Label(
        root,
        text="Выберите действие",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0",
        fg="#333"
    ).pack(pady=20)

    # Кнопки
    tk.Button(
        root,
        text="➕ Внесение данных клиента",
        font=button_font,
        width=30,
        height=2,
        command=lambda: open_data_entry_window(root)
    ).pack(pady=10)

    tk.Button(
        root,
        text="📄 Составление договора",
        font=button_font,
        width=30,
        height=2,
        command=lambda: open_contract_window(root)
    ).pack(pady=10)

    tk.Button(
        root,
        text="💰 Выставить счёт",
        font=button_font,
        width=30,
        height=2,
        command=lambda: open_invoice_window(root)
    ).pack(pady=10)

    tk.Button(
        root,
        text="✏️ Редактирование данных",
        font=button_font,
        width=30,
        height=2,
        command=lambda: open_edit_window(root)
    ).pack(pady=10)

    # Обработчик закрытия окна
    root.protocol("WM_DELETE_WINDOW", on_closing)

    return root


def main():
    """Главная функция запуска приложения"""
    # Создаём папки
    # create_directories()

    # Логирование
    # setup_logging()

    # Проверяем файлы
    missing_files = check_files()
    if missing_files:
        messagebox.showwarning(
            "Внимание",
            f"Не хватает файлов:\n" + "\n".join(missing_files) +
            "\n\nСоздайте их вручную или скопируйте шаблоны."
        )

    # Создаём главное окно
    global root
    root = create_main_window()

    # Запускаем цикл
    root.mainloop()


if __name__ == "__main__":
    main()
