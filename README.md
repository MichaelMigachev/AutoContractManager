# AutoContractManager


📌 Приложение для автоматизации оформления **договоров** и **счетов** в автосервисе или компании по оформлению СБКТС/ЭПТС.

Написано на Python с использованием:
- `tkinter` — графический интерфейс
- `openpyxl`, `pandas` — работа с Excel
- `python-docx` — генерация Word-документов
- Чистая архитектура с разделением ответственности
---
### 🌟 Основные возможности

- Ввод данных клиента (ФИО, VIN, паспорт, телефон и др.)  
- Автоформатирование телефона и имени папки  
- Поиск по ФИО, VIN или номеру договора  
- Генерация договора в формате `.docx`  
- Выставление счёта (на расчётный счёт или на карту)  
- Редактирование данных клиента  
- Хранение данных в Excel (`database_of_contracts.xlsx`)  
- Реестр договоров (`contracts_registry.xlsx`)  
- Поддержка шаблонов с `{ключами}` 
 
---
## 🗂️ Структура проекта
```
AutoContractManager/
│
├── main.py                        # Точка входа — запуск GUI
├── pyproject.toml                 # Зависимости
├── README.md                      # Документация
│
├── config/
│ ├── paths.py                     # Пути к файлам
│ └── settings.py                  # Настройки приложения
│
├── core/
│ ├── database.py                  # Работа с Excel: поиск, сохранение
│ ├── document_generator.py        # Генерация .docx из шаблонов
│ ├── validators.py                # Валидация: VIN, телефон, дата
│ └── utils.py                     # Вспомогательные функции
│
├── gui/
│ └── windows/                     # GUI-окна
│ ├── data_entry_window.py         # Ввод данных
│ ├── contract_window.py           # Оформление договора
│ ├── invoice_window.py            # Выставление счёта
│ └── edit_window.py               # Редактирование
│
├── data/
│ ├── database_of_contracts.xlsx   # База клиентов
│ └── contracts_registry.xlsx      # Реестр договоров
│
├── templates/
│ ├── contract_template.docx       # Шаблон договора
│ ├── invoice_template.docx        # Счёт на счёт
│ └── invoice_card_template.docx   # Счёт на карту
│
├── documents_ready/               # Готовые документы (авто)
└── logs/
└── app.log                        # Логи приложения
```