import requests
from requests.exceptions import RequestException as RE
import re


def check_url(url):
    checking = re.sub(" ", "", url)
    http_rex = re.compile(r'(^http:\/\/)|(^https:\/\/)')
    full_rex = re.compile(r'(^[a-z]{4,5}:\/\/).+[.].+')
    if not http_rex.match(checking):
        checking = 'http://' + checking
    if not full_rex.match(checking):
        return False
    return checking


def get_urls():
    raw_url_list = input("Please write a URL or URLs you want to check. (separated by comma) \n").strip().split(",")
    pretty_url_list = []

    for url in raw_url_list:
        pretty_url = check_url(url)
        if pretty_url is not False:
            pretty_url_list.append(pretty_url)
        else:
            print('{url} is invalid url'.format(url=url))
    return pretty_url_list


def check_url_legit(urls):
    for url in urls:
        try:
            response = requests.get(url)
            if response is not None:
                print("{url} is up!".format(url=url))
        except RE:
            print("{url} is down!".format(url=url))


def ask_to_restart():
    yes_or_yes = input("Do you want start over? [y/n] :")
    if yes_or_yes == 'y':
        return True
    elif yes_or_yes == 'n':
        return False
    else:
        print("That is invalid answer.")
        return False


def main():
    restart = True
    while restart:
        url_input = get_urls()
        check_url_legit(url_input)
        restart = ask_to_restart()

main()