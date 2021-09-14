from os import name
import time
import csv
import pandas as pd
#from threading import Thread
from multiprocessing import Process

# nike functions
import debug_colors
from nike_functions import standard_scraper
from nike_functions import default_information_collector
from nike_functions import save_product
from nike_functions import snkrs_scrapper
from nike_functions import snkrs_information_collector
from nike_functions import save_product_snkrs
from nike_functions import nike_calendary

class scrapers():
    def __init__(self):
        pass

    def search_nike_snkrs(self):
        global verify_snkrs
        verify_snkrs = False
        start_time = time.time()
        try:
            products = snkrs_scrapper.scrape_site()
            if products == False:
                debug_colors.prRed('Error loading stock')
                return
        except:
            return
        
        # coletar informações do produto de cada link
        product_list = []
        for item in products:
            try:
                product_information = snkrs_information_collector.search_on_web(item)
            except:
                debug_colors.prRed(f'{item} failed')
                return
            if product_information != None:
                product_list.append(product_information)

        # salvar produto no banco de dados
        
        with open('./db/advertise.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            waiting_list_products = []
            for item in csvFile:
                waiting_list_products.append(item)

        products_found = []
        for product in product_list:
            new_link = save_product_snkrs.save(product, f'./db/snkrs.csv')
            # anunciar no discord
            products_found.append(product[3])
            if new_link != '':
                debug_colors.prGreen('add product')
                name = product[0]
                color = product[1]
                price = product[2]
                sizes = product[5]
                links = product[6]
                image = product[3]
                code = product[4]
                replace_product = [name, color, price, sizes, new_link, image, code]
                waiting_list_products.append(replace_product)
                
        nike_ds = pd.DataFrame(waiting_list_products[1:], columns= ['nome', 'cor', 'preço', 'tamanhos', 'link', 'imagem', 'code'])
        nike_ds.to_csv('./db/advertise.csv', index=False)

        save_product_snkrs.update_list(products_found, f'./db/snkrs.csv')
        end_time = time.time()
        debug_colors.prGreen(f'Snkrs scanned [{end_time-start_time} seconds]')

    def search_nike_m_basquete(self):
        start_time = time.time()
        self.search_nike('masculino basquete', 'nike_m_basquete')
        end_time = time.time()
        debug_colors.prGreen(f'Masculino basquete scanned [{end_time - start_time} seconds]')

    # preset para vasculhar cada página
    def search_nike(self, category, destiny):
        # coletar links dos produtos
        try:
            products = standard_scraper.scrape_site(category)
            if products == False:
                debug_colors.prRed('Error loading products')
                return
        except:
            print('Error')
            return
            
        # coletar informações do produto de cada link
        product_list = []
        for item in products:
            try:
                product_information = default_information_collector.search_on_web(item)
            except:
                debug_colors.prRed(f'{item} failed')
                return
            if product_information != None:
                product_list.append(product_information)
        waiting_list_products = []
        # salvar produto no banco de 
        
        with open('./db/advertise.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            waiting_list_products = []
            for item in csvFile:
                waiting_list_products.append(item)

        products_found = []
        for product in product_list:
            new_link = save_product.save(product, f'./db/{destiny}.csv')
            # anunciar no discord
            products_found.append(product[4])
            if new_link != '':
                debug_colors.prGreen('add product')
                name = product[0]
                color = product[1]
                price = product[2]
                sizes = product[5]
                links = product[6]
                image = product[3]
                code = product[4]
                replace_product = [name, color, price, sizes, new_link, image, code]
                waiting_list_products.append(replace_product)
        
        nike_ds = pd.DataFrame(waiting_list_products[1:], columns= ['nome', 'cor', 'preço', 'tamanhos', 'link', 'imagem', 'code'])
        nike_ds.to_csv('./db/advertise.csv', index=False)

        save_product.update_list(products_found, f'./db/{destiny}.csv')

    def calendary(self):
        start_time = time.time()
        try:
            events = nike_calendary.update_events()
            with open('./db/advertise_calendary.csv', mode ='r')as file:
                csvFile = csv.reader(file)
                waiting_list_products = []
                for item in csvFile:
                    waiting_list_products.append(item)
            for item in events:
                waiting_list_products.append(item)
            calendary_ds = pd.DataFrame(waiting_list_products[1:], columns= ['nome', 'cor', 'imagem', 'link', 'data', 'preço', 'code'])
            calendary_ds.to_csv('./db/advertise_calendary.csv', index=False)

            end_time = time.time()
            debug_colors.prGreen(f'Calendary scanned [{end_time-start_time} seconds]')
        except:
            debug_colors.prRed('Error scanning calendar')
            return


scrape = scrapers()
def run_nike_snkrs():
    while True:
        scrape.search_nike_snkrs()

def run_nike_m_basquete():
    while True:
        scrape.search_nike_m_basquete()

def run_nike_m_casual():
    while True:
        scrape.search_nike_m_casual()

def run_calendary():
    while True:
        scrape.calendary()
        time.sleep(50)

t1 = Process(target=run_nike_snkrs)
t2 = Process(target=run_nike_m_basquete)
t3 = Process(target=run_calendary)
#t4 = Process(target=run_nike_m_casual)
t1.start()
t2.start()
t3.start()
#t4.start()
