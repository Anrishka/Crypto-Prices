# Импорт необходимых библиотек
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import requests
import datetime
import ctypes
import sv_ttk
import API

# Обеспечение корректной работы с DPI для операционных систем Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass

# Создание основного окна
root = Tk()
root.geometry('700x570')
root.title("Crypto prices")
root.iconbitmap(r'C:\Users\user\Desktop\курс питон записи\GPT_tasks\crypto\bit.ico')
root.resizable(False, False)

# Определение базового URL для API поставщика данных о криптовалютах
base_url = 'https://api.coingecko.com/api/v3'
# Определение конечной точки для получения данных о ценах криптовалют
endpoint = '/simple/price'
# Определение вашего API-ключа
api_key = API.API
# Определение списка идентификаторов криптовалют
ids_param_list = ['bitcoin', 'ethereum', 'binancecoin', 'tether', 'solana', 'cardano', 'polkadot', 'dogecoin']
# Конкатенация идентификаторов криптовалют для запроса API
ids_param = 'Bitcoin,Ethereum,BinanceCoin,Tether,Solana,Cardano,XRP,Polkadot,USDCoin,Dogecoin'

# Определение параметров для запроса API
params = {
    'ids': ids_param.lower(),
    'vs_currencies': 'usd',
    'include_last_updated_at': 'true',  # Флаг для включения времени последнего обновления
    'include_24hr_change': 'true',  # Флаг для включения изменения за 24 часа
    'x_cg_demo_api_key': api_key  # Добавление вашего API-ключа в качестве параметра запроса
}

# Выполнение запроса к API
response = requests.get(f'{base_url}{endpoint}', params=params)

# Фрейм для отображения информации о криптовалютах
currency_frame = ttk.Frame(root)
currency_frame.pack()

# Словари для хранения полей ввода цен, изменений за 24 часа и времени последнего обновления
price_entries = {}
t24_hour_change_entries = {}
last_updated_entries = {}

# Переменные для управления столбцами и строками
column = 0
row = 0

# Создание виджетов для каждой криптовалюты
for i in ids_param_list:
    if row == 4:
        row = 0
        column += 1

    # Создание отдельного фрейма для каждой криптовалюты
    current_currency_frame = ttk.Frame(currency_frame)
    current_currency_frame.grid(row=row, column=column, padx=10, pady=10)

    # Добавление меток и полей ввода в каждый фрейм
    currency_label = ttk.Label(current_currency_frame, text=i.capitalize(), font='Arial 10 bold')
    currency_label.grid(row=0, column=0, sticky=W)
    price_label = ttk.Label(current_currency_frame, text='Price in USD: ')
    price_label.grid(row=1, column=0, sticky=W)
    t24_hour_change_label = ttk.Label(current_currency_frame, text='24 hour change: ')
    t24_hour_change_label.grid(row=2, column=0, sticky=W)
    last_updated_label = ttk.Label(current_currency_frame, text='Last updated: ')
    last_updated_label.grid(row=3, column=0, sticky=W)

    price_entries[i] = ttk.Entry(current_currency_frame)
    price_entries[i].grid(row=1, column=1, sticky=E)
    t24_hour_change_entries[i] = ttk.Entry(current_currency_frame)
    t24_hour_change_entries[i].grid(row=2, column=1, sticky=E)
    last_updated_entries[i] = ttk.Entry(current_currency_frame)
    last_updated_entries[i].grid(row=3, column=1, sticky=E)

    row += 1

# Функция для обновления информации о криптовалютах
def check_info():
    global response
    # Выполнение запроса к API
    response = requests.get(f'{base_url}{endpoint}', params=params)
    if response.status_code == 200:
        data = response.json()
        # Извлечение необходимой информации о криптовалютах
        for i in ids_param_list:
            price = data[i]['usd']
            last_updated_at = data[i]['last_updated_at']
            last_updated_at_time = datetime.datetime.fromtimestamp(last_updated_at).strftime('%Y-%m-%d, %H:%M')
            change_24hr = data[i]['usd_24h_change']
            formated_change_24ht = round(change_24hr, 2)
            if not formated_change_24ht < 0:
                formated_change_24ht = f'+{formated_change_24ht}'

            # Очистка и обновление полей ввода
            price_entries[i].delete(0, END)
            price_entries[i].insert(0, price)
            t24_hour_change_entries[i].delete(0, END)
            t24_hour_change_entries[i].insert(0, f'{formated_change_24ht}%')
            last_updated_entries[i].delete(0, END)
            last_updated_entries[i].insert(0, last_updated_at_time)
    else:
        error = messagebox.showerror('Что-то пошло не так', 'Не удалось получить данные о криптовалютах')


check_info()

# Кнопка для обновления информации
refresh_button = ttk.Button(root, text='Обновить', command=check_info)
refresh_button.pack(padx=10, pady=10)

sv_ttk.set_theme("dark")

root.mainloop()

