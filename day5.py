import requests
from bs4 import BeautifulSoup


def get_countries_currency():
    tr = BeautifulSoup(requests.get("https://www.iban.com/currency-codes").text, 'html.parser').\
        find("table", class_="table table-bordered downloads tablesorter").find_all("tr")
    country_dict = {}
    for idx, element in enumerate(tr):
        row = []
        for i in element:
            line = i.string
            if line != '\n':
                row.append(i.string)
        country_dict.update({idx: tuple(row)})
    return country_dict


def get_input_and_print_code(country_dict):

    for i in range(1, len(country_dict)):
        print(f"# {i} {country_dict[i][0]}")

    flag = True

    while flag:
        try:
            number = int(input("#: "))
            if not 0 < number < 269:
                print("Choose a number from the list.")
                continue
            flag = False
        except ValueError:
            print("That wasn't a number.")
    print(f"You choose {country_dict[number][0]}")
    print(f"The currency code is {country_dict[number][2]}")


countries_dict = get_countries_currency()
get_input_and_print_code(countries_dict)