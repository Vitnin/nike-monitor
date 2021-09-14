import requests
from bs4 import BeautifulSoup
from random import choice

from nike_functions import debug_colors

# returning found links
def get_links(url):
    
    response = requests.get(url)

    # create variables to search for information on the page
    content = response.content
    site = BeautifulSoup(content, 'html.parser')
    products_link = []
    description = site.findAll('a', attrs={'aspect-radio-box'})
    for item in description:
        products_link.append(item['href'])
    return products_link

# search for links with keywords
def check_product(products_links):
    keywords = ['dunk-low', 'jordan-1-', 'off-white', 'stussy', 'sacai', 'dunk-high']
    selected_products = []
    for product in products_links:
        for item in keywords:
            if item in product:
                selected_products.append(product)

    return selected_products

def scrape_site():
    list_of_products = []
    # scan all pages by changing the page index
    cont = 1
    while True:
        url = f'https://www.nike.com.br/Snkrs/Feed?p={cont}&demanda=true'
        products_links = get_links(url)
        debug_colors.prYellow(f'scanning page {cont} of category snkrs')

        # if I don't find any links it means I've already found it, I've searched all the pages
        if products_links == []:
            debug_colors.prYellow('[snkrs] verified')
            if cont == 1:
                return False
            break

        # verify that the links obtained contain valid products
        checked_products = check_product(products_links)
        if checked_products:
            for product in checked_products:
                list_of_products.append(product)
        cont+=1
    return list_of_products
