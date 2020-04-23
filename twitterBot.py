#!/usr/bin/env python
import os
import time
from datetime import datetime
from twython import Twython
from twython import TwythonStreamer
import sys
import botModules

APP_KEY = os.environ['aKey']
APP_SECRET = os.environ['aSecret']
OAUTH_TOKEN = os.environ['oauth']
OAUTH_TOKEN_SECRET = os.environ['oauthSecret']
file = open('trigger.txt', "r+")
def check(data):
    bot = botModules.botModules(twitter, data)
    if 'text' in data:
        print(data['text'])
        x = data['text']
        try:
            if not(x[:2] == 'RT'):
                command = x[x.find("!"):].split()[0]
                moduleCalls = {"!remindMe": bot.remindMe,
                               "!deleteAll": bot.deleteAllT,
                               "!noteThis": bot.noteThis,
                               "!player": bot.player,
                               "!play": bot.play,
                               "!commandList": bot.commandList,
                               "!dice": bot.dice,
                               "!flip": bot.flip,
                               "!countdown": bot.countdown,
                               "!quit": bot.quit}
                moduleCalls[command](x)
        except Exception as ex:
            pass #
trigger = file.read()
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
since = "1050347525364830208"
while True:
    while True:
        limits = twitter.get_application_rate_limit_status()
        howmany = limits["resources"]["statuses"]["/statuses/home_timeline"]["remaining"]
        if int(howmany) <= 0:
            break
        timewhen = limits["resources"]["statuses"]["/statuses/home_timeline"]["reset"]
        wait = (int(timewhen) - int(datetime.now().strftime('%s'))) / howmany
        timeline = twitter.get_home_timeline(since_id=since)
        print("get_home_timeline calls remaining {} reset in {}".format(howmany,wait*howmany))
        for tweet in reversed(timeline):
            since = tweet['id']
            check(tweet)
        time.sleep(wait)
    timeleft = int(timewhen) - int(datetime.now().strftime('%s'))
    time.sleep(timeleft)

