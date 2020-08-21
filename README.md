# APOD_Hook
This is a discord web hook to send the NASA Astronomy picture of the day.

The bot will need a **config.py** file.
It should look like this:
```
NASA_KEY='NASA Api key goes here...'
WEBHOOK_URL='https://discordapp.com/api/webhooks/...the rest of your URL...'
```

I have the webhook run off a crontab every day at 8 am.  
First, make the file executable.  
```
chmod +x webhook.sh  
```
Then add it to the crontab  
```
crontab -e
```
 Then add the following line:  
```
0 8 * * * ~/APOD_Hook/webhook.sh
```
