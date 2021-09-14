import csv

# function scans all databases and
# returns the product with the order code
def searching(code):
    list_to_return = []

    # add all products to a list

    with open('./db/nike_m_basquete.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for product in csvFile:
            list_to_return.append(product)

    with open('./db/snkrs.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for product in csvFile:
            list_to_return.append(product)

    # return product with corresponding code
    for item in list_to_return:
        if item[6] == code:
            return item
