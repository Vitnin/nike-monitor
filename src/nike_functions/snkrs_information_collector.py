import requests
from bs4 import BeautifulSoup

from nike_functions import debug_colors

# collect information for a particular product from your link
def search_on_web(link):
    returnable_sizes = []
    for c in range(0,6):
        try:
            response = requests.get(link)

            content = response.content
            site = BeautifulSoup(content, 'html.parser')

            # finding url of first product image
            image = site.find('a', attrs={'class': 'js-produto__foto'})
            image = image['data-standard']

            # model and color information is linked
            # the model name can be found separately, 
            # so just delete the model from the pegged information and I have the color
            name_and_color = site.find('div', attrs={'class': 'nome-preco-produto'})
            name = name_and_color.find('span').text
            color = name_and_color.find('a').text
            color = color.replace(name, '')

            # price
            price = site.find('span', attrs={'class': 'js-valor-por'}).text

            # finding the code separating it from the product description
            code = site.find('div', attrs={'class': 'detalhes-produto__indisponivel-descricao'})
            code = code.find('br')
            if code:
                code = code.text
                code = code.replace(' ', '')
                code = code[-10:]
                if code[6]!='-':
                    code = None

            # finding available sizes
            all_sizes = site.find('main', attrs={'class': 'container-fluid'})
            extracting_script = all_sizes.find('script')
            extracting_script = str(extracting_script).split(':')
            cont = 0
            sizes = []
            for item in extracting_script:
                if item[-11:-1] == 'TemEstoque':
                    verify_stock = extracting_script[cont + 1]
                    if verify_stock[1] == '1':
                        size = extracting_script[cont - 9].split('"')[1]
                        sizes.append(size)
                cont += 1
            
            # if the product has not yet been released, the site returns all sizes. 
            # correct this by setting the sizes if the product has not been released
            not_available = site.find('h3', attrs={'class': 'detalhes-produto__disponibilidade'})
            if not_available != None:
                sizes = []
            for item in sizes:
                if item not in returnable_sizes:
                    returnable_sizes.append(item)
        except:
            debug_colors.prRed(f'error on page {link}')
    # Adjusting the sequence of sizes
    if returnable_sizes != []:
        returnable_sizes = sorted(returnable_sizes)
    try:
        return name, color, price, image, code, returnable_sizes, link
    except:
        debug_colors.prRed('error on page...')
