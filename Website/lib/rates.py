#import requests
import json
import os
import datetime

currDir = os.getcwd()
countriesDir = currDir + "/lib/textfiles/countries.json"
exchange_ratesDir = currDir + "/lib/textfiles/exchange_rates.json"


class Rates:
    def get_currencies(currency_code, ausPrice):
        if os.path.exists(exchange_ratesDir):
            with open(exchange_ratesDir, "r") as rates_database:
                rates = json.load(rates_database)
            return round(rates.get("rates").get(currency_code) * ausPrice, 2)
        else:
            response = requests.get('https://v3.exchangerate-api.com/bulk/b1fb41cae3647ed2c4330bc7/AUD')
            with open(exchange_ratesDir, "w") as rates_database:
                json.dump(json.loads(response.text), rates_database)
            with open(exchange_ratesDir, "r") as rates_database:
                rates = json.load(rates_database)
            return round(rates.get("rates").get(currency_code) * ausPrice, 2)

    def get_countries(country):
        with open(countriesDir, "r") as countries_database:
            countries = json.load(countries_database)
        currency_code = countries.get(country)
        return currency_code

class Countries:
    def get_countries():
        sorted_countries = []
        with open(countriesDir, "r") as countries_database:
            countries = json.load(countries_database)
        for key in countries.keys():
            sorted_countries.append(key)
        sorted_countries.sort()
        return sorted_countries
         #use in html file for the countries drop down

#for testing,
#print(Countries.get_countries())
#print(Rates.get_currencies(Rates.get_countries("Korea"), 70))

    #need to delete exchange rate file occassionlly to update currencies
    #need to put this file in routes for getting the countries for html
