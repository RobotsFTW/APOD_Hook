import datetime
import json
import textwrap

import discord
import requests
from discord import RequestsWebhookAdapter, Webhook

import config

#Webhook to send astronomy picture of the day

#Create webhook
webhook = Webhook.from_url(config.WEBHOOK_URL, adapter=RequestsWebhookAdapter())

#Get todays date and format it for the APOD API URL
now=datetime.datetime.today()
date="{}-{}-{}".format(now.year, now.month, now.day)

#insert date and api key into the NASA APOD API URL
url = "https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(config.NASA_KEY, date)

#Get information from response to embed in message
res = requests.get(url)
data=res.json()

#check to see if there is an error. Send error and Exit.
if "code" in data:
    msg = data["msg"]
    webhook.send(msg)
    exit()

#create the discord embed, add title
title= data['title']
embed = discord.Embed(title="Astronomy Picture of the Day for {}.".format(date), description=title, color=0x0B3D91)

#textwrap it so it fits within discord message length
descr = data['explanation']
content = textwrap.wrap(descr, 1000)
for item in content:
    embed.add_field(name="Description:", value=item, inline=False)

if data["media_type"] == "image":
    #adds the images to teh embed
    hd_img = data['hdurl']
    sd_img = data['url']
    embed.set_image(url=sd_img)
    embed.add_field(name="HD Image Link:", value=hd_img, inline=False)
    embed.add_field(name="SD Image Link:", value=sd_img, inline=False)
elif data["media_type"] == "video":
    #Adds teh video link to the embed
    vid_url = data["url"]
    embed.add_field(name="Video Link:", value=vid_url, inline=False)

#send Webhook
webhook.send(embed=embed)
