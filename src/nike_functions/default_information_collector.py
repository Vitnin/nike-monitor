import requests
from bs4 import BeautifulSoup

# here we will collect all information from the product page and extract and return the relevant information

# collect all information about a product from the link
def search_on_web(link):
    returnable_sizes = []
    for c in range(0,6):
        response = requests.get(link)
        content = response.content
        site = BeautifulSoup(content, 'html.parser')

        # NAME
        name = site.findAll('div', attrs={'class': 'nome-produto'})
        name = name[-1]
        name = name.find('h1').text
        name = name.replace('Tênis ', '')

        # PRICE
        price = site.find('span', attrs={'js-preco'})
        price = price.find('span').text

        # COLOR
        color = site.find('ul', attrs={'variacoes-cores-estilo'})
        color = color.find('li').text
        color = color.split(': ')
        color = color[1]

        # SIZES
        try:
            size = site.find('ul', attrs={'variacoes-tamanhos__lista'})
            excluded = size.findAll('li', attrs={'tamanho-desabilitado'})
            excluded_sizes = []
            for item in excluded:
                excluded_sizes.append(item.text)

            size = size.findAll('label')
            sizes = []
            for item in size:
                if item.text not in excluded_sizes:
                    sizes.append(item.text)
        except:
            sizes = []

        # CODE
        code = site.find('ul', attrs={'variacoes-cores-estilo'})
        code = code.find('span').text
        
        # IMAGE
        image = site.find('a', attrs={'produto__foto js-produto__foto'})
        image = image['data-standard']
        for item in sizes:
            if item not in returnable_sizes:
                returnable_sizes.append(item)
    if returnable_sizes != []:
        returnable_sizes = sorted(returnable_sizes)
    return name, color, price, image, code, sizes, link
