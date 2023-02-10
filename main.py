#!/usr/bin/env python
from dotenv import load_dotenv
from flask import Flask, Response
from datetime import datetime
from datetime import timedelta
from time import mktime
import requests
import os
import sys
import json


load_dotenv()
SECRET = os.getenv('PAGE_ACCESS_TOKEN')
endpoint = '/me/posts'
fields = 'permalink_url,full_picture,story,created_time,message,is_published,parent_id,is_hidden,status_type'
server_url = 'https://graph.facebook.com/v15.0'


def facebook_request(endpoint, fields):
    url = f'{server_url}{endpoint}'
    params = {
            'fields': fields,
            'access_token': SECRET,
            }
    r = requests.get(url, params=params)
    return r.json()


posts = []
updateThreshold = 10 * 1000  # 10s
lastUpdateTimestamp = 0


def update_cache():
    r = facebook_request(endpoint, fields)
    if 'data' not in r:
        print(f'{datetime.now()} Error: couldn\'t fetch data from facebook\'s server', file=sys.stderr)
        return

    raw_data = r['data']

    for raw_post in raw_data:
        post = dict()

        if not raw_post['is_published'] or raw_post['is_hidden']:
            continue

        post['id'] = raw_post['id']
        post['permalink_url'] = raw_post['permalink_url']

        if raw_post['status_type'] == 'mobile_status_update':
            post['type'] = 'normal'
        if raw_post['status_type'] == 'added_photos':
            post['type'] = 'photo'
        if raw_post['status_type'] == 'added_video':
            post['type'] = 'video'
        if raw_post['status_type'] == 'created_event':
            post['type'] = 'event'

        if 'parent_id' in raw_post:
            post['shared'] = True
            post['orignal_url'] = f'https://facebook.com/{raw_post["parent_id"]}'
        else:
            post['shared'] = False

        if 'full_picture' in raw_post:
            post['picture_url'] = raw_post['full_picture']

        # format now : YYYY-MM-DDTHH:MM:SS+ZZZZ
        # should be  : YYYY-MM-DDTHH:MM:SS+ZZ:ZZ
        date_published = raw_post['created_time']
        date_published = list(date_published)
        date_published.insert(-2, ':')
        date_published = ''.join(date_published)
        date_published = datetime.fromisoformat(date_published)
        post['timestamp'] = mktime(date_published.timetuple())

        if 'story' in raw_post:
            post['text'] = raw_post['story']
        if 'message' in raw_post:
            post['text'] = raw_post['message']

        posts.append(post)


update_cache()
last_update = datetime.now()
update_threshold = timedelta(seconds=10)


app = Flask(__name__)


# @app.route("/")
def home() -> str:
    return "<h1>general kenobi</h1>"


# return latest post but not newer than provided timestamp
@app.route('/<int:timestamp>')
def get_post(timestamp: int) -> str:
    global last_update
    if datetime.now() - last_update >= update_threshold:
        update_cache()
        last_update = datetime.now()
        print('udpate done')
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    for post in posts:
        if post['timestamp'] < timestamp:
            resp.data = json.dumps(post)
            return resp
    resp.data = json.dumps({'message': 'post not found'})
    return resp


if __name__ == '__main__':
    app.run()
