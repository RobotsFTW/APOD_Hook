import requests
import discord
from discord import Webhook, RequestsWebhookAdapter, File
import textwrap
import datetime
import json
#python config file with the API keys in it.
import config

#Webhook to send astronomy picture of the day

#Create webhook
webhook = Webhook.from_url(config.WEBHOOK_URL, adapter=RequestsWebhookAdapter())

#Get todays date and format it for the APOD API URL
now=datetime.datetime.today()
YYYY=now.year
MM=now.month
DD=now.day
date="{}-{}-{}".format(YYYY, MM, DD)

#insert date and api key into the NASA APOD API URL
url = "https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(config.NASA_KEY, date)

#Get information from response to embed in message
res = requests.get(url)
data=res.json()
title= data['title']
date = data['date']
descr = data['explanation']
hd_img = data['hdurl']
sd_img = data['url']

#create the discord embed, and add the SD image
embed = discord.Embed(title="Astronomy Picture of the Day for {}.".format(date), description=title, color=0x0B3D91)
embed.set_image(url=sd_img)

#textwrap it so it fits within discord message length
content = textwrap.wrap(descr, 1000)
for item in content:
    embed.add_field(name="Description:", value=item, inline=False)

#Add image links
embed.add_field(name="HD Image Link:", value=hd_img, inline=False)
embed.add_field(name="SD Image Link:", value=sd_img, inline=False)

# Send embed to server
webhook.send(embed=embed)
