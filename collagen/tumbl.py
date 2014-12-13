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
    CONSUMER_KEY = config[':consumer_key'] 
    CONSUMER_SECRET = config[':consumer_secret'] 
    TOKEN = config[':token'] 
    TOKEN_SECRET = config[':token_secret'] 
    DEFAULT_N = config[':default_n']
    t = Tumblpy(CONSUMER_KEY,CONSUMER_SECRET, TOKEN, TOKEN_SECRET)
    blog_url = t.post('user/info')['user']['blogs'][0]['url']
    return t, DEFAULT_N, blog_url

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



if __name__ == "__main__":

    src_folder = 'source_images'
    tags = 'collagen, collectible'
    img_path = 'collages/20141205T193014191221.png'
    blog_url = t.post('user/info')['user']['blogs'][0]['url']
    lpm = 'lauren-p-m.tumblr.com/'

    t = Tumblpy(CONSUMER_KEY,CONSUMER_SECRET, TOKEN, TOKEN_SECRET)

    #download_tagged_images(t, 'cage', src_folder) 
    #download_blog_images(t, lpm, src_folder) 
    #photo_post(img_path, t, blog_url, tags)
