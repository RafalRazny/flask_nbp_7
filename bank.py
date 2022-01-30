import requests
import csv
from flask import Flask
from itertools import chain
from flask import render_template, request
app = Flask(__name__)


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
temp_list= []

for i in data:
    temp_list.append(i["rates"])

rates_list = list(chain.from_iterable(temp_list))

header = ["currency", "code", "bid", "ask"]

with open('rates.csv', 'w', newline='') as f:
  writer = csv.DictWriter(f, fieldnames=header, delimiter=";")
  writer.writeheader()
  writer.writerows(rates_list)


@app.route('/', methods=['GET', 'POST'])
def currency():
    return render_template("currency_form.html")

@app.route('/calculation_pln/', methods=['GET', 'POST'])
def calculation_pln():
    currency_code = request.form['code']
    currency_amount = request.form['amount']
    amount = float(currency_amount)
    if currency_code == 'USD':
        result = amount * 4.1212
    elif currency_code == 'AUD':
        result = amount * 2.9191
    elif currency_code == 'CAD':
        result = amount * 3.2515
    elif currency_code == 'EUR':
        result = amount * 4.5994
    elif currency_code == 'HUF':
        result = amount * 0.012901
    elif currency_code == 'CHF':
        result = amount * 4.4297
    elif currency_code == 'GPB':
        result = amount * 5.4135
    elif currency_code == 'JPY':
        result = amount * 0.035742
    elif currency_code == 'CZK':
        result = amount * 0.1885
    elif currency_code == 'DKK':
        result = amount * 0.6179
    elif currency_code == 'NOK':
        result = amount * 0.4613
    elif currency_code == 'SEK':
        result = amount * 0.4415
    else:
        currency_code == 'XDR'
        result = amount * 5.7989
    return render_template('amount_form.html', currency_code=currency_code, amount=amount, result=result)

if __name__ == '__main__':
    app.run(debug=True)

    