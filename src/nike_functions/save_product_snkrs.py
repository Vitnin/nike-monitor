import csv
import asyncio
from typing import ChainMap
import pandas as pd

# save new products in ds
def save(product_information, db):
    name = product_information[0]
    color = product_information[1]
    price = product_information[2]
    image =product_information[3]
    code = product_information[4]
    sizes =product_information[5]
    link = product_information[6]
    products_list = []
    changed_link = False
    product_was_available = False
    new_size = False
    with open(db, mode ='r')as file:
        csvFile = csv.reader(file)
        for product in csvFile:
            if product:
                if product[5]!=image:
                    products_list.append(product)
                else:
                    # find out if any new sizes have been added
                    for item in sizes:
                        if item not in product[3]:
                            new_size = True
                    if product[3] != '[]':
                        product_was_available = True
                    if link in product[4]:
                        link = product[4]
                        changed_link = True
                    else:
                        link = f'{link},' + product[4]
                        changed_link = True
    advertise = False
    if sizes != []:
        if product_was_available == False or new_size:
            advertise = True

    if changed_link == False:
        link = link+','
    products_list.append(
        [name, color, price, sizes, link, image, code]
    )
    nike_ds = pd.DataFrame(products_list[1:], columns= ['name', 'color', 'price', 'sizes', 'link', 'image', 'code'])
    nike_ds.to_csv(db, index=False)
    if advertise == True:
        return link
    else:
        return ''

# adjust unavailable products in ds
def update_list(founded_products, db):
    list_to_return = []
    with open(db, mode ='r')as file:
        csvFile = csv.reader(file)
        for product in csvFile:
            if product[5] not in founded_products:
                product[3] = []
            list_to_return.append(product)
    
    nike_ds = pd.DataFrame(list_to_return[1:], columns= ['name', 'color', 'price', 'sizes', 'link', 'image', 'code'])
    nike_ds.to_csv(db, index=False)
