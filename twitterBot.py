#!/usr/bin/env python
import os

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


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
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

    def on_error(self, status_code, data):
        print(status_code)


twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.user(track=trigger)
