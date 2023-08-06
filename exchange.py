import pandas as pd
import numpy as np

import requests


url = "https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt"

resonse = requests.get(url)
list_of_rates = resonse.text.split("\n")[:-1]

current_date = list_of_rates[0].split(" ")[0]
curr_name = []
exch_rate = []

for element in list_of_rates:
    if "EUR" in element:
        curr_name.append(element.split("|")[-2])
        exch_rate.append(element.split("|")[-1])
    if "USD" in element:
        curr_name.append(element.split("|")[-2])
        exch_rate.append(element.split("|")[-1])
    if "GBP" in element:
        curr_name.append(element.split("|")[-2])
        exch_rate.append(element.split("|")[-1])
    if "CHF" in element:
        curr_name.append(element.split("|")[-2])
        exch_rate.append(element.split("|")[-1])

exchange_rates = pd.DataFrame(
    {"date": current_date, "currency": curr_name, "rate": exch_rate},
    index=[i for i in range(1, len(exch_rate) + 1)],
)
