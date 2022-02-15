import requests
import csv
from flask import Flask
from itertools import chain
from flask import render_template, request
app = Flask(__name__)


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
temp_list= []
rates = data[0]["rates"]


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
    for dict in rates:
        if dict["code"] == currency_code:
            amount_bid = dict["ask"]
            currency_amount_int = int(currency_amount)
            result = currency_amount_int * amount_bid
            return render_template('amount_form.html', currency_code=currency_code, amount=currency_amount, result=result)

if __name__ == '__main__':
    app.run(debug=True)

    