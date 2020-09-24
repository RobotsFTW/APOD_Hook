import datetime
import textwrap
import os
import discord
import requests
from discord import RequestsWebhookAdapter, Webhook
from PIL import Image, ImageFont, ImageDraw

import config

#Webhook to send astronomy picture of the day

#Create webhook
webhook = Webhook.from_url(config.WEBHOOK_URL, adapter=RequestsWebhookAdapter())

#Get todays date and format it for the APOD API URL
now = datetime.datetime.today()
date="{}-{}-{}".format(now.year, now.month, now.day)

#insert date and api key into the NASA APOD API URL
url = "https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(config.NASA_KEY, date)

#Get information from response to embed in message
data = requests.get(url).json()

#check to see if there is an error. Send error and Exit.
if "code" in data:
    msg = data["msg"]
    webhook.send(msg)
    exit()

#create the discord embed, add title
title = data['title']
embed = discord.Embed(title="Astronomy Picture of the Day for {}.".format(date), description=title, color=0x0B3D91)

#textwrap it so it fits within discord message length
descr = data['explanation']
for item in textwrap.wrap(descr, 1000):
    embed.add_field(name="Description:", value=item, inline=False)

if data["media_type"] == "image":
    #adds the images to the embed
    hd_img = data['hdurl']
    sd_img = data['url']
    embed.set_image(url=sd_img)
    embed.add_field(name="HD Image Link:", value=hd_img, inline=False)
    embed.add_field(name="SD Image Link:", value=sd_img, inline=False)
elif data["media_type"] == "video":
    #Adds the video link to the embed
    vid_url = data["url"]
    embed.add_field(name="Video Link:", value=vid_url, inline=False)


#InSight weather

#InSight backround picture file path
path = "insight.png"
new_path = "new_insight.png"
img = Image.open(path)
img2 = ImageDraw.Draw(img)
sansFont= ImageFont.truetype(os.path.join("fonts/", 'LiberationSans-Bold.ttf'), 18)

#insert NASA API key into the url
url = 'https://api.nasa.gov/insight_weather/?api_key={}&feedtype=json&ver=1.0'.format(config.NASA_KEY)

#get json info from url
data = requests.get(url).json()

days = []

#gets the keys for the days and deltes anything older than 7 days
keys = data['sol_keys']
count = len(keys)
count = count - 7
del keys[:count]

x = 46
y = 290
#adds all the info into a list called days
for sol in keys:
    date = data[sol]["First_UTC"]
    temp_high = round(data[sol]["AT"]["mx"], 2)
    temp_low = round(data[sol]["AT"]["mn"], 2)
    wind_high = round(data[sol]["HWS"]["mx"], 2)
    wind_low = round(data[sol]["HWS"]["mn"], 2)
    pressure_high = round(data[sol]["PRE"]["mx"], 2)
    pressure_low = round(data[sol]["PRE"]["mn"], 2)
    season = data[sol]["Season"]
    #day_info = (sol, date, temp_high, temp_low, wind_high, wind_low, pressure_high, pressure_low, season)
    #days.append(day_info)
    season = "Season: " + season
    img2.text((x, y), season, fill='white', font=sansFont)

#save image to new path
img.save(new_path)

embed2 = discord.Embed(title='InSight Mars Weather', description='NASAs InSight Mars lander takes continuous weather measurements \
                       (temperature, wind, pressure) on the surface of Mars at Elysium Planitia, a flat, smooth plain near Mars equator.', color=0x0B3D91)

#creates a file object and attaches it to embed2
file = discord.File(new_path, filename=new_path)
embed2.set_image(url="attachment://new_insight.png")

#send Webhook
webhook.send(embeds=(embed, embed2), file=file)

