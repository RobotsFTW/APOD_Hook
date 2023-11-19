import datetime
import textwrap
import logging
import time
import traceback

import discord
import requests

# user settings
import config

# Webhook to send astronomy picture of the day

# logging
log_file_name = config.log_file
logging.basicConfig(filename=log_file_name, level=logging.INFO)

# put it all in a try except statement to log any errors. i.e. no internet connection
retries = 1
APOD_sent = False

# Tries to send the APOD 5 times.
while not APOD_sent and retries < 5:
    try:
        # Create webhook
        webhook = discord.SyncWebhook.from_url(config.WEBHOOK_URL)

        # Get today's date and format it for the APOD API URL
        now = datetime.datetime.today()
        date = "{}-{}-{}".format(now.year, now.month, now.day)

        # insert date and api key into the NASA APOD API URL
        url = "https://api.nasa.gov/planetary/apod?api_key={}&date={}".format(config.NASA_KEY, date)

        # Get information from response to embed in message
        data = requests.get(url).json()

        # check to see if there is an error. Send error and Exit.
        if "code" in data:
            msg = data["msg"]
            webhook.send(msg)
            exit()

        # create the discord embed, add title
        title = data['title']
        embed = discord.Embed(title="Astronomy Picture of the Day for {}.".format(date), description=title,
                              color=0x0B3D91)

        # textwrap it so it fits within discord message length
        descr = data['explanation']
        for item in textwrap.wrap(descr, 1000):
            embed.add_field(name="Description:", value=item, inline=False)

        if data["media_type"] == "image":
            # adds the images to the embed
            hd_img = data['hdurl']
            sd_img = data['url']
            embed.set_image(url=sd_img)
            embed.add_field(name="HD Image Link:", value=hd_img, inline=False)
            embed.add_field(name="SD Image Link:", value=sd_img, inline=False)
        elif data["media_type"] == "video":
            # Adds the video link to the embed
            vid_url = data["url"]
            embed.add_field(name="Video Link:", value=vid_url, inline=False)

        # send Webhook
        webhook.send(embed=embed)

        # log successfully sent APOD
        logging.info(f'APOD Successfully sent: {now}')

        # create success
        APOD_sent = True
    # logs error and tries to resend it up to five times. Waiting 1 minute longer each time.
    except Exception as e:
        logging.error(f'{datetime.datetime.now()}: {traceback.format_exc()}')
        print(e)
        wait = retries * 60
        time.sleep(wait)
        retries += 1
