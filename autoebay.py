"""
Created by shafi-1 - Shafiullah Rahman

at 19:43 on 22 December 2019
"""

import config.settings as config
import os
import requests
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_keywords():
    if os.stat("keywords.txt").st_size:
        with open("keywords.txt", "r") as keyword_file:
            return keyword_file.readlines()
    else:
        error()


def read_item_ids():
    with open("itemID.txt", "r") as item_id_file:
        return item_id_file.read().splitlines()


def retrieve(search_words):
    try:
        search = search_words.split(',')[0]
        max_price = search_words.split(',')[1]

        if not search.strip() or not max_price.strip():
            error()
    except Exception:
        error()

    url = ('https://svcs.ebay.com/services/search/FindingService/v1'
           '?OPERATION-NAME=findItemsByKeywords'
           '&sortOrder=PricePlusShippingLowest'
           '&buyerPostalCode=' + config.postcode +
           '&SERVICE-VERSION=1.0.0'
           '&GLOBAL-ID=EBAY-GB'
           '&SECURITY-APPNAME=' + config.key +
           '&RESPONSE-DATA-FORMAT=JSON'
           '&REST-PAYLOAD'
           '&itemFilter(0).name=Condition'
           '&itemFilter(0).value=New'
           '&itemFilter(1).name=MaxPrice'
           '&itemFilter(1).value=' + max_price +
           '&itemFilter(1).paramName=Currency'
           '&itemFilter(1).paramValue=GBP'
           '&keywords=' + search)
    url = url.replace(" ", "%20")
    response = requests.get(url)
    return response.json()


def process(item_ids, json):
    if int(json["findItemsByKeywordsResponse"][0]["searchResult"][0]["@count"]) == 0:
        print("No items found :(")
        return None

    for item in (json["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]):
        item_id = item['itemId'][0]
        url = item['viewItemURL'][0]
        title = item["title"][0]
        if 'condition' in item:
            condition = item['condition'][0]['conditionDisplayName'][0]
        else:
            condition = "Unspecified"
        price = item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']
        if item_id in item_ids:
            continue
        else:
            with open("itemID.txt", "a") as item_id_file:
                item_id_file.write(item_id + "\n")
                send_email(url, title, condition, price)


def send_email(url, title, condition, price):
    msg = MIMEMultipart()
    msg['From'] = config.email_from
    msg['To'] = config.email_to
    msg['Subject'] = title

    body = "<a href=\"" + url + "\">" + title + "</a>" + "<br><p>Condition: " + \
           condition + "</p><p>Price: " + price + "</p>"
    msg.attach(MIMEText(body, 'html'))
    print(msg)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(msg['From'], config.password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def error():
    print("Error: Incorrect format!\nFormat: keywords, max_price")
    sys.exit()


def main():
    try:
        searches = read_keywords()
        item_ids = read_item_ids()

        for search in searches:
            json = retrieve(search)
            process(item_ids, json)
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit()


if __name__ == "__main__":
    main()
