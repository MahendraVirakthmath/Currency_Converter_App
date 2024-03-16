import json
import requests
from decouple import config
from tkinter import *
from tkinter import Tk, ttk
from PIL import Image, ImageTk

API_KEY = config('API_KEY', default = 'default_api_key')
API_ENDPOINT = 'https://api.currencyapi.com/v3/latest'


def get_currencies() -> list:
    currency_codes = []
    with open('currency.json') as f:
        currency_data = json.load(f)
        for currency in currency_data:
            code, _ = list(currency.items())[0]
            currency_codes.append(code)
    return sorted(currency_codes)


def convert_currency(from_currency: str, to_currency: str, amount: float) -> float:
    query_params = {
        'apikey': API_KEY,
        'base_currency': from_currency,
        'currencies': to_currency
    }
    response = requests.get(API_ENDPOINT, params=query_params)
    currency_data = response.json()
    exchange_rate = currency_data['data'][to_currency]['value']
    exchanged_value = exchange_rate * amount
    return exchanged_value


# Colors
WHITE_COLOR = "#FFFFFF"
BLACK_COLOR = "#333333"
GREENY_COLOR = "#3dc4a0"


def convert():
    amount = float(amount_entry.get())
    from_currency = from_combo.get()
    to_currency = to_combo.get()
    converted_amount = convert_currency(from_currency, to_currency, amount)

    result_label['text'] = f'{to_currency} {converted_amount:.2f}'


# Window Configuration
window = Tk()
window.geometry("380x320")
window.title("Currency Converter")
window.configure(bg=WHITE_COLOR)
window.resizable(height=FALSE, width=FALSE)


# Frames
top_frame = Frame(window, width=380, height=60, bg=GREENY_COLOR)
top_frame.grid(row=0, column=0)

main_frame = Frame(window, width=380, height=260, bg=WHITE_COLOR)
main_frame.grid(row=1, column=0)


# Top Frame Widgets
icon_image = Image.open('exchange.png')
icon_image = icon_image.resize((40, 40))
icon_image = ImageTk.PhotoImage(icon_image)
app_name_label = Label(top_frame, compound=LEFT, text="Currency Converter", height=3, padx=13, pady=30,
                 anchor=CENTER, font=('Arial 16 bold'), bg=GREENY_COLOR, fg=WHITE_COLOR)
app_name_label.place(relx=0.5, rely=0.5, anchor=CENTER)

# Main Frame Widgets
result_label = Label(main_frame, text=" ", width=15, height=2, pady=7, padx=0, anchor=CENTER,
               font=('Ivy 16 bold'), bg=WHITE_COLOR, fg=BLACK_COLOR, relief=SOLID)
result_label.place(x=92, y=10)

from_label = Label(main_frame, text="From", width=8, height=1, pady=0, padx=0, anchor=NW,
                   font=('Ivy 10 bold'), bg=WHITE_COLOR, fg=BLACK_COLOR, relief=FLAT)
from_label.place(x=90, y=90)
from_combo = ttk.Combobox(main_frame, width=8, justify=CENTER, font=('Ivy 12 bold'),)
from_combo['values'] = (get_currencies())
from_combo.current(0)
from_combo.place(x=92, y=115)

to_label = Label(main_frame, text="To", width=8, height=1, pady=0, padx=0, anchor=NW,
                 font=('Ivy 10 bold'), bg=WHITE_COLOR, fg=BLACK_COLOR, relief=FLAT)
to_label.place(x=200, y=90)
to_combo = ttk.Combobox(main_frame, width=8, justify=CENTER, font=('Ivy 12 bold'),)
to_combo['values'] = (get_currencies())
to_combo.current(1)
to_combo.place(x=202, y=115)

amount_entry = Entry(main_frame, width=22, justify=CENTER,font=('Ivy 12 bold'), relief=SOLID)
amount_entry.place(x=92, y=155)

convert_button = Button(main_frame, text="Convert", width=19, padx=5,
                        height=1, bg=GREENY_COLOR, fg=WHITE_COLOR, font=('Ivy 12 bold'), command=convert)
convert_button.place(x=92, y=210)

window.iconphoto(True, icon_image)

# Mainloop
window.mainloop()