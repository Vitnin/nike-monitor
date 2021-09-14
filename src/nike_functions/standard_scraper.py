from logging import debug
import requests
from bs4 import BeautifulSoup

from nike_functions import debug_colors

# returning found links
def get_links(url, category):
    response = requests.get(url)

    # create variables to search for information on the page
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    products_link = []
    description = site.find_all('div', attrs={'produto__info nao-redireciona'})
    for item in description:
        received_category = item.find('a', attrs={'produto__descricaocurta'})

        # return only items from the selected category
        if received_category.text == category:
            products_link.append(received_category['href'])
        
    return products_link

# looking for product colors
def check_colors(url):
    try:
        response = requests.get(url)
        # create variables to search for information on the page
        content = response.content
        site = BeautifulSoup(content, 'html.parser')

        # color variation
        color_table = site.find('div', attrs={'variacoes-cores'})
        product_colors = color_table.findAll('li')
        colors_list = []
        for item in product_colors:
            colors_list.append(item['url'])
        return colors_list
    except:
        return 'defective link'

# search for links with keywords
def check_product(products_links):
    keywords = ['dunk-low', 'jordan-1-', 'off-white', 'stussy', 'sacai', 'dunk-high']
    selected_products = []
    for product in products_links:
        for item in keywords:
            if item in product:
                # search all colors
                color_list = check_colors(product)
                if color_list != 'defective link':
                    for color in color_list:
                        selected_products.append(color)
    return selected_products

def scrape_site(destination):
    list_of_products = []
    # scan all pages by changing the page index
    cont = 1
    while True:
        # This part of the program works only for tennis in the men's basketball category, 
        # but new categories can be added here.
        if destination == 'masculino basquete':
            url = f'https://www.nike.com.br/masculino/calcados/basquete?p={cont}&loja=&ofertas=&Fabricante=&ordemFiltro=&limit=24&ordenacao=0&Filtros=&precoate=&precode=&tamanho=&cor=&demanda=true'
            category = 'Basquete'

        products_links = get_links(url, category)
        debug_colors.prYellow(f'scanning page {cont} of category {destination}')

        # if I don't find any links it means I've already searched all the pages
        if products_links == []:
            debug_colors.prYellow(f'[{destination}] verified')
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
