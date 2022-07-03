from bs4 import BeautifulSoup
import requests
import re
from csv import writer

product = input("What product you want to search?")

# getting the url
url = f"https://www.newegg.com/p/pl?d={product}&N=8000%204131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

# getting the number of pages
page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

# iterating through pages
with open('products.csv', 'w', encoding='utf8', newline='') as f:

    thewriter = writer(f)
    header = ['Price', 'Link']
    thewriter.writerow(header)
    for page in range(1, pages+1):
        url = f"https://www.newegg.com/p/pl?d={product}&N=8000%204131&page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        # searching just the products under the tag
        div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

        # only searching the item input by the user
        items = div.find_all(text=re.compile(product))

        for item in items:
            parent = item.parent
            if parent.name != "a":
                continue

            link = parent['href']
            next_parent = item.find_parent(class_="item-container")
            price = next_parent.find(class_="price-current").strong.string

            items_found[item] = {"price": int(price.replace(",", "")), "link": link}


    thewriter.writerow(items_found)
