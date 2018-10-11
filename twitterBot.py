#!/usr/bin/env python
import os
import time
from twython import Twython
from twython import TwythonStreamer
import sys
import botModules

APP_KEY = os.environ['aKey']
APP_SECRET = os.environ['aSecret']
OAUTH_TOKEN = os.environ['oauth']
OAUTH_TOKEN_SECRET = os.environ['oauthSecret']
file = open('trigger.txt', "r+")
trigger = file.read()
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
since = 0
while True:
    while True:
        howmany = twitter.get_lastfunction_header('x-rate-limit-remaining')
        if int(howmany) <= 0:
            break
        timewhen = twitter.get_lastfunction_header('x-rate-limit-rest')
        wait = (int(timewhen) - int(datetime.datetime.now().strftime('%s'))) / howmany
        timeline = twitter.get_home_timeline(since_id=since)
        for tweet in timeline:
            since = tweet['id']
            check(tweet)
        time.sleep(wait)
    timeleft = int(timewhen) - int(datetime.datetime.now().strftime('%s'))
    time.sleep(timeleft)

def check(data):
    bot = botModules.botModules(twitter, data)
    if 'text' in data:
        print(data['text'])
        x = data['text']
        try:
            if not(x[:2] == 'RT'):
                command = x[x.find("!"):].split()[0]
                if 'fuk you' in x:
                    twitter.update_status(status="@" + data['user']['screen_name']
                                                 + " ye fuk u too -bot", in_reply_to_status_id=data['id'])
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
