import re
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

CURRENCY_CODE_URL = "https://www.iban.com/currency-codes"


class CurrencyConverter:
    """Currency Converter Definition"""
    def __init__(self, currency_code_url):
        self.currency_code_url = currency_code_url
        self.country_dict = self.get_countries_currency()
        self.NUMBER_OF_COUNTRY = len(self.country_dict)
        self.transfer_url = None
        self.from_country_code = None
        self.to_country_code = None
        self.amount = None

    def get_countries_currency(self):
        tr = BeautifulSoup(requests.get(self.currency_code_url).text, 'html.parser'). \
            find("table", class_="table table-bordered downloads tablesorter").find_all("tr")
        country_dict = {}
        none_counter = 0
        for idx, element in enumerate(tr):
            row = []
            for idx2, i in enumerate(element):
                line = i.string
                if line != '\n':
                    if idx2 == 1:
                        row.append(re.sub('[ ]{2,}', ' ', str(line).lower().capitalize()))
                    else:
                        row.append(line)
            if row[2] is None:
                none_counter += 1
                continue
            country_dict.update({idx - none_counter: tuple(row)})
        return country_dict

    def print_all_countries(self):
        for i in range(1, self.NUMBER_OF_COUNTRY):
            print(f"# {i} {self.country_dict[i][0]}")

    @staticmethod
    def get_number(message="#: "):
        while True:
            try:
                return int(input(message))
            except ValueError:
                print("That wasn't a number.")

    def get_code(self):

        """when user input number, print country name and return currency code of the country"""

        while True:
            number = self.get_number()
            if 0 < number < self.NUMBER_OF_COUNTRY:
                print(self.country_dict[number][0])
                return self.country_dict[number][2]
            else:
                print("Choose a number from the list.")

    def set_countries_code(self):
        print("Where are you from? Choose a country by number")
        self.from_country_code = self.get_code()
        print("Now choose another country.")
        self.to_country_code = self.get_code()

    def set_amount(self):
        message = f"How many {self.from_country_code} do you want to convert to {self.to_country_code}?\n"
        self.amount = self.get_number(message=message)

    def set_url(self):
        self.transfer_url = f"https://transferwise.com/gb/currency-converter/{self.from_country_code}-to-{self.to_country_code}-rate?amount={self.amount}"

    def get_page(self):
        html = requests.get(self.transfer_url)
        return html

    def set_(self):
        self.set_countries_code()
        self.set_amount()
        self.set_url()

    def convert_amount(self):
        """Must call this method after call properly both set_countries_code and set_amount method"""
        html = self.get_page()
        while html.status_code != 200:
            print("Country code is unavailable. Choose another countries")
            self.set_()
            html = self.get_page()
        converted_amount = BeautifulSoup(html.text, 'html.parser').find("input", class_="js-TargetAmount form-control cc-calculator__input")['value']
        return converted_amount

    def print_result(self, amount=None):
        default_str = f"{self.from_country_code} {self.amount} is {self.to_country_code} "
        if amount is None:
            amount = float(self.convert_amount().strip("0"))
        if amount % 1 == 0:
            amount = int(amount)
            print(default_str + f"{amount:,d}")
        else:
            amount = str(amount).strip("0")
            print(default_str + amount)


if __name__ == '__main__':
    converter = CurrencyConverter(CURRENCY_CODE_URL)
    converter.print_all_countries()
    converter.set_()
    converter.print_result()
