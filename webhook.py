import requests
import discord
from discord import Webhook, RequestsWebhookAdapter, File
import textwrap
import datetime
import json
#python config file
import config

#webhook to send astronomy picture of the day

# Create webhook
webhook = Webhook.from_url(config.WEBHOOK_URL, adapter=RequestsWebhookAdapter())

now=datetime.datetime.today()
YYYY=now.year
MM=now.month
DD=now.day

date="{}-{}-{}".format(YYYY, MM, DD)
url = "https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(config.NASA_KEY, date)

res = requests.get(url)
data=res.json()
title= data['title']
date = data['date']
descr = data['explanation']
hd_img = data['hdurl']
sd_img = data['url']

embed = discord.Embed(title="Astronomy Picture of the Day for {}.".format(date), description=title, color=0xfc3d21)
embed.set_image(url=sd_img)

#textwrap it so it fits within discord message length
content = textwrap.wrap(descr, 1000)
for item in content:
    embed.add_field(name="Description:", value=item, inline=False)

embed.add_field(name="HD Image Link:", value=hd_img, inline=False)
embed.add_field(name="SD Image Link:", value=sd_img, inline=False)
# Send embed to server
webhook.send(embed=embed)
