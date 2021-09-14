import discord
from discord.ext import tasks
from discord.ext import commands
import csv
import pandas as pd

import debug_colors
import cmd_search

bot = commands.Bot(command_prefix='>')
@bot.event
async def on_ready():
    debug_colors.prGreen(f"Bot [{bot.user.name}] is connected to server.")
    check_new_products.start()
    check_calendary.start()

# return message with corresponding received code
@bot.event
async def on_message(message):
    # set channel
    channel = bot.get_channel('Your id here')
    if message.channel == channel and message.author.id != 'Your id here':
        product_info = cmd_search.searching(message.content)
        debug_colors.prCyan('command called')
        if product_info:
            name = product_info[0]
            color = product_info[1]
            price = product_info[2]
            sizes = product_info[3]
            if sizes == '[]':
                sizes = 'no sizes available'
            links = product_info[4]
            image = product_info[5]
            code = product_info[6]

            to_advertise = (name, color, price, sizes, links, image, code)
            await advertise_nike_products(to_advertise, links, True)
        else: 
            await channel.send(f"{message.author}, I didn't find the product!")

def check_excluded_products(received_product):
    with open('./db/produtos_excluidos.csv', mode ='r')as file:   
        csvFile = csv.reader(file)
        products = []
        for item in csvFile:
            if received_product[0].replace(' ', '') == item[0].replace(' ', ''):
                if received_product[1].replace(' ', '') == item[1].replace(' ', ''):
                    return True
        return False

# advertise products
async def advertise_nike_products(product, links, command = False):
    product_excluded = check_excluded_products(product)
    if product_excluded == True:
        return

    # define the channel in which the products will be advertised
    channel = bot.get_channel('Your id here')
    if command == True:
        channel = bot.get_channel('Your id here')
    
    embed = discord.Embed(
        title = 'Model',
        description = product[0],
        colour = 15083355
    )
    embed.set_author(name = 'Nike',
    icon_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwebiconspng.com%2Fwp-content%2Fuploads%2F2017%2F09%2FNike-PNG-Image-55784.png&f=1&nofb=1')
    embed.set_thumbnail(
        url = product[5]
    )
    embed.add_field(name = 'Color', value = product[1], inline=False)
    embed.add_field(name = 'Price', value = product[2], inline=False)
    sizes = str(product[3]).replace("['", '').replace("']", '')
    sizes = sizes.replace(" ',", ' |').replace("',", ' |').replace("'", '').replace('.', ',')
    embed.add_field(name = 'Available sizes', value = sizes, inline=False)
    if product[6] != None and product[6] != '':
        embed.add_field(name = 'Code', value = product[6], inline=False)
    cont = 0
    links = links.split(',')
    for item in links:
        if item != '':
            if cont == 0:
                embed.add_field(name = f'Link to purchase:', value=f'[link]({item})', inline=False)
            elif cont == 1:
                embed.add_field(name = f'Alternative links:', value='(if the main link doesnt work)',inline=False)
            if cont > 0:
                embed.add_field(name = f'Link {cont}', value=f'[link]({item})', inline=False)
            cont+=1
    await channel.send(embed = embed)

# check if new products have been added
@tasks.loop(minutes=1)
async def check_new_products():
    with open('./db/advertise.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        header = True
        for item in csvFile:
            if header:
                header = False
            else:
                try:
                    await advertise_nike_products(item, item[4])
                except:
                    debug_colors.prRed(item)
        nike_ds = pd.DataFrame(columns= ['name', 'color', 'price', 'sizes', 'link', 'image', 'code'])
        nike_ds.to_csv('./db/advertise.csv', index=False)

@tasks.loop(minutes=1)
async def check_calendary():
    with open('./db/advertise_calendary.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        header = True
        for item in csvFile:
            if header:
                header = False
            else:
                try:
                    await advertise_calendary(item)
                except:
                    debug_colors.prRed(item)
                
        calendary_ds = pd.DataFrame(columns= ['name', 'color', 'image', 'link', 'date', 'price', 'code'])
        calendary_ds.to_csv('./db/advertise_calendary.csv', index=False)

async def advertise_calendary(product):
    channel = bot.get_channel('Your id here')
    
    embed = discord.Embed(
        title = 'Model',
        description = product[0],
        colour = 15083355
    )
    embed.set_author(name = 'Nike',
    icon_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwebiconspng.com%2Fwp-content%2Fuploads%2F2017%2F09%2FNike-PNG-Image-55784.png&f=1&nofb=1')
    embed.set_thumbnail(
        url = product[2]
    )
    embed.add_field(name = 'Color', value = product[1], inline=False)
    embed.add_field(name = 'Available in:', value = product[4], inline=False)
    embed.add_field(name = 'Price', value = product[5], inline=False)
    if product[6]:
        embed.add_field(name = 'Code', value = product[6], inline=False)
    embed.add_field(name = f'Link', value=f'[link]({product[3]})', inline=False)
    await channel.send(embed = embed)

bot.run("Your id here")
