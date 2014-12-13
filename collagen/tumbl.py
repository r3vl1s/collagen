'''
tumbl.py does the following:
1. post photo to blog 
2. download n (current limit: 20) images from blog or tag 

'''

from tumblpy import Tumblpy
import yaml
import os
import os.path
from collagen import utils
import argparse

def load_config():
    config = utils.load_config('tumbl_config')
    consumer_KEY = config[':consumer_key'] 
    consumer_secret = config[':consumer_secret'] 
    token = config[':token'] 
    token_secret = config[':token_secret'] 
    default_n = config[':default_n']
    t = Tumblpy(consumer_KEY,consumer_secret, token, token_secret)
    blog_url = t.post('user/info')['user']['blogs'][0]['url']
    return t, default_n, blog_url

#post photo to tumblr
def post_photo(image_path, tumbl_object, url, tags):
    image = open(image_path, 'rb')
    post = tumbl_object.post('post', blog_url=url, params = {'type':'photo', 'tags': tags, 'data' : image})
    print('Uploading ' + image_path + ' to tumblr...')
    print(post)

def get_tagged_images(tumbl_object, tag, folder, n):
    photo_count = 0
    timestamp = ''
    print('Downloading ' + tag + ' tag')
    while photo_count < n:
        posts = tumbl_object.get('tagged', params = {'tag':tag, 'limit':str(n), 'before':timestamp})
        for post in posts:
            if post['type'] == 'photo':
                img_url = post['photos'][0]['original_size']['url']
                if utils.get_ext(img_url) in ['.jpg','.png']:
                    photo_count += 1
                    utils.download_url(img_url, folder)
            timestamp = post['timestamp']
            if photo_count == n:
                break

def get_blog_images(tumbl_object, blog, folder, n):
    photo_count = 0
    offset = 0
    print('Downloading ' + str(n) + ' images from ' + blog)
    while photo_count < n:
        posts = tumbl_object.get('posts', blog_url=blog, params = {'type':'photo', 'limit':str(n), 'offset': str(offset)})['posts']
        for post in posts:
            img_url = post['photos'][0]['original_size']['url']
            if utils.get_ext(img_url) in ['.jpg', '.png']:
                photo_count += 1
                utils.download_url(img_url, folder)
            if photo_count == n:
                break
        offset += n



