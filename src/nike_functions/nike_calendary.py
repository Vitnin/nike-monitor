import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

# getting the information of all products in snkrs calendar
def get_events():
    url = 'https://www.nike.com.br/Snkrs/Calendario?p=1&demanda=true'
    response = requests.get(url)
    # create variables to search for information on the page
    content = response.content
    site = BeautifulSoup(content, 'html.parser')

    # collect a list of all products
    all_informations = site.findAll('div', attrs={'produto__imagem'})

    events = []
    for item in all_informations:
        # availability Date
        available_date = item.find('span').text

        # product link
        link = item.find('a')['href']

        # image link
        image = item.find('img')['data-src']

        # product name
        name = item.find('h2').text.replace(available_date, '')
        
        response = requests.get(link)
        content = response.content
        site = BeautifulSoup(content, 'html.parser')

        # price
        price = site.find('span', attrs={'js-preco'}).text

        # code
        code = site.find('div', attrs={'detalhes-produto__indisponivel-descricao'})
        try:
            if code:
                code = code.text
                code = code.replace(' ', '')
                code = code[-10:]
                if code[6]!='-':
                    code = None
        except:
            code = None

        # color
        color = site.find('div', attrs={'nome-preco-produto'})
        color = color.find('a').text.replace(name[0:-1], '')
        events.append([name, color, image, link, available_date, price, code])

    return events

# update the ds
def update_events():
    events = get_events()
    if events == []:
        return
    # save the link of all collected images in a list
    images = []
    for item in events:
        images.append(item[2])

    # check whether the products are still available from the link in each image
    with open('./db/calendary.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        events_products = []
        saved_images = []
        for product in csvFile:
            if product:
                saved_images.append(product[2])
                if product[2] in images:
                    events_products.append(product)

    # products with unsaved images must be advertised
    products_to_advertise = []
    for item in events:
        if item[2] not in saved_images:
            products_to_advertise.append(item)
            events_products.append(item)

    nike_ds = pd.DataFrame(events_products, columns= ['name', 'color', 'image', 'link', 'date', 'price', 'code'])
    nike_ds.to_csv('./db/calendary.csv', index=False)
    return(products_to_advertise)
