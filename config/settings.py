# config/settings.py

# Общие настройки
APP_NAME = "AutoContractManager"
APP_VERSION = "1.0"
COMPANY_NAME = "ИП Петров П.П."
COMPANY_INN = "123456789012"
COMPANY_ADDRESS = "г. Москва, ул. Ленина, д. 1"
COMPANY_PHONE = "+7 999 123-45-67"

# Префиксы и форматы
CONTRACT_PREFIX = "-ИП"          # Добавляется к номеру договора: 101-ИП
DEFAULT_CURRENCY = "RUB"
CURRENCY_SYMBOL = "₽"

# Лимиты
MAX_SEARCH_RESULTS = 10
AUTOCOMPLETE_DELAY_MS = 300       # Задержка при поиске в мс

# Параметры документов
DEFAULT_SERVICE_SBKTS = "выпуску СБКТС + ЭПТС"
DEFAULT_SERVICE_SCRAP = "списанию утильсбора"
DEFAULT_PAYMENT_METHOD = " "
PAYMENT_METHOD_CARD = "НА КАРТУ"

# Налоги и стоимость (можно вынести в базу позже)
TAX_RATE = 0.20  # НДС 20%
DEFAULT_PRICE_SBKTS = 32000
DEFAULT_PRICE_SCRAP = 1500

# Форматы дат
DATE_FORMAT = "%d.%m.%Y"
DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"

# Настройки интерфейса
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 500
BUTTON_FONT = ("Arial", 12)
ENTRY_WIDTH = 30

# Режим разработки
DEBUG = False
