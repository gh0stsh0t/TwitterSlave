import _thread
import datetime
import json
import os
import random
import re
import time
import urllib.parse
import urllib.request

import requests
from fuzzywuzzy import process


class botModules:
    def __init__(self, keys, tweet):
        self.twitter = keys
        self.data = tweet

    def quit(self, x):
        # elif '!quit' in x:
        self.twitter.update_status(
            status="@" + self.data['user']['screen_name'] + " shutting downmuna ako doi, goodbye kaibigan ko",
            in_reply_to_status_id=self.data['id'])
        raise SystemExit

    def flip(self, x):
        # elif '!flip' in x:
        if random.randint(1, 2) == 1:
            self.twitter.update_status(status="@" + self.data['user']['screen_name'] + " 💀 Heads!",
                                       in_reply_to_status_id=self.data['id'])
        else:
            self.twitter.update_status(status="@" + self.data['user']['screen_name'] + " 🐍 Tails!",
                                       in_reply_to_status_id=self.data['id'])

    def dice(self, x):
        # elif '!dice' in x:
        try:
            result = random.randint(1, int(x[x.find('!dice') + 5:].split()[0]))
            self.twitter.update_status(status="@" + self.data['user']['screen_name'] + " 🎲"
                                              + str(result), in_reply_to_status_id=self.data['id'])
        except (ValueError, IndexError) as e:
            self.twitter.update_status(status="@" + self.data['user']['screen_name'] + " 🎲"
                                              + str(random.randint(1, 6)), in_reply_to_status_id=self.data['id'])

    def countdown(self, x):
        query = x[x.find('!') + 10:]
        api_url_base = "https://www.episodate.com/api/"
        headers = {'Content-Type': 'application/json'}
        api_url = '{0}search?q={1}&page=1'.format(api_url_base, query)
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            response = json.loads(response.content.decode('utf-8'))
            named = {}
            if response['tv_shows']:
                for tv in response['tv_shows']:
                    named[tv['name']] = tv['permalink']
                name = process.extractOne(query, named.keys())[0]
                api_url = '{0}show-details?q={1}'.format(api_url_base, named[name])
                response = requests.get(api_url, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.content.decode('utf-8'))
                    if response['tvShow']['countdown']:
                        then = datetime.datetime.strptime(response['tvShow']['countdown']['air_date'],
                                                          "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()
                        d = divmod(then.total_seconds(), 86400)  # days
                        h = divmod(d[1], 3600)  # hours
                        m = divmod(h[1], 60)  # minutes
                        s = m[1]  # seconds

                        filename = 'temp.jpg'
                        request = requests.get(response['tvShow']['image_path'], stream=True)
                        if request.status_code == 200:
                            with open(filename, 'wb') as image:
                                for chunk in request:
                                    image.write(chunk)
                            with open(filename, 'rb') as photo:
                                response = self.twitter.upload_media(media=photo)
                            self.twitter.update_status(
                                status="@" + self.data['user'][
                                    'screen_name'] + " Next episode of %s in %d days, %d hours, %d minutes, %d seconds" % (
                                    name, d[0], h[0], m[0], s), media_ids=[response['media_id']],
                                in_reply_to_status_id=self.data['id'])
                            os.remove(filename)
                        else:
                            self.twitter.update_status(
                                status="@" + self.data['user'][
                                    'screen_name'] + " Next episode of %s in %d days, %d hours, %d minutes, %d seconds" % (
                                    name, d[0], h[0], m[0], s)
                                , in_reply_to_status_id=self.data['id'])
                    else:
                        self.twitter.update_status(
                            status="@" + self.data['user'][
                                'screen_name'] + " Nothing yet for " + name + " in the near future :( "
                            , in_reply_to_status_id=self.data['id'])
                else:
                    self.twitter.update_status(
                        status="@" + self.data['user']['screen_name'] + " An error occurred, can you try again later?"
                        , in_reply_to_status_id=self.data['id'])
            else:
                self.twitter.update_status(
                    status="@" + self.data['user']['screen_name'] + " No results, please fix typos and try again"
                    , in_reply_to_status_id=self.data['id'])
        else:
            self.twitter.update_status(
                status="@" + self.data['user']['screen_name'] + " An error occurred, can you try again later?"
                , in_reply_to_status_id=self.data['id'])

    def commandList(self, x):
        # elif '!commandList' in x:
        temp = open('README.md', 'r').read().split('\n')
        self.twitter.update_status(status="@" + self.data['user'][
            'screen_name'] + " https://raw.githubusercontent.com/gh0stsh0t/TwitterSlave/master/README.md"
                                   , in_reply_to_status_id=self.data['id'])

    def play(self, x):
        # elif '!play' in x:
        query_string = urllib.parse.urlencode({"q": x[x.find('!') + 5:]})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string + "&sp=CAM%253D")
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        link_result = "http://www.youtube.com/watch?v=" + search_results[0]
        print("playing " + link_result)
        self.twitter.update_status(status="@" + self.data['user']['screen_name'] + " playing "
                                          + link_result, in_reply_to_status_id=self.data['id'])

    def player(self, x):
        # elif '!player' in x:
        query_string = urllib.parse.urlencode({"q": x[x.find('!') + 7:]})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        link_result = "http://www.youtube.com/watch?v=" + search_results[0]
        print("playing " + link_result)
        self.twitter.update_status(status="@" + self.data['user']['screen_name'] + " playing "
                                          + link_result, in_reply_to_status_id=self.data['id'])

    def noteThis(self, x):
        # elif '!noteThis' in x:
        z = 'testruntime'
        self.twitter.update_status(status="@" + self.data['user']['screen_name'] + "  " + z,
                                   in_reply_to_status_id=self.data['id'])

    def remindMe(self, x):
        # if '!remindMe' in x:
        delayer = x[x.find('!remindMe') + 9:].split()
        timer = delayer[1].lower()
        if 'min' in timer:
            delay = int(delayer[0]) * 60
        elif 'hr' in timer or 'hour' in timer:
            delay = int(delayer[0]) * 3600
        else:
            delay = int(delayer[0])
        print(str(delay) + " " + str(self.data['id']) + " " + self.data['user']['screen_name'])
        '''
        try:
            send dm here
        :except tae
        tae
        '''
        _thread.start_new_thread(self.delayWake, (delay, self.data['id'], self.data['user']['screen_name'], delayer))

    def delayWake(self, delay, tweetID, name, message):
        time.sleep(delay)
        print('sending delayed message')
        why = ''
        for words in message[2:]:
            why = why + ' ' + words
        frends = self.twitter.lookup_friendships(screen_name=name)
        kinsa = self.twitter.show_user(screen_name=name)
        if kinsa['protected'] or 'followed_by' in frends:
            self.twitter.send_direct_message(screen_name=name, text=why)
        else:
            self.twitter.update_status(status="@" + name + why, in_reply_to_status_id=tweetID)

    def deleteAllT(self, x):
        # user=self.twitter.show_user(user_id=self.data[id])
        # num=int(user['statuses_count'])
        # for x in range(num,0,-200):
        try:
            result = int(x[x.find('!deleteAll') + 10:].split()[0])
        except (ValueError, IndexError):
            result = 200
        timeline = self.twitter.get_user_timeline(count=result, since_id='103807114965187789', max_id=self.data['id'])
        for tweet in timeline:
            status = int(tweet['id_str'])
            self.twitter.destroy_status(id=status)
            print('Tweet deleted: ' + str(status))
