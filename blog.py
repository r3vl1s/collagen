'''
script to manage posting to tumblr
'''

from collagen import collagen
from collagen import tumbl
from collagen import utils
import os
import os.path
import random

COLLAGEN_DIR = os.path.abspath(__file__ + "/../")

tumbl_object, n, blog_url = tumbl.load_config()

config = utils.load_config('config')
source_folder = os.path.join(COLLAGEN_DIR, config[':source_image_folder'])
output_folder = os.path.join(COLLAGEN_DIR, config[':output_image_folder'])

#load tags and blogs
tags_file = os.path.join(COLLAGEN_DIR, config[':tags_file'])
blogs_file = os.path.join(COLLAGEN_DIR, config[':blogs_file'])
tag_list = utils.file_to_list(tags_file)
blog_list = utils.file_to_list(blogs_file)
post_tags = ['collagen', 'collage']

random_tags = [random.choice(tag_list) for i in range(random.randint(1,3))]
random_blogs = [random.choice(blog_list) for i in range(random.randint(1,3))]


#load blogs

for tag in random_tags:
    post_tags.append(tag)
    tumbl.get_tagged_images(tumbl_object, tag, source_folder, n)
for blog in random_blogs:
    tumbl.get_blog_images(tumbl_object, blog, source_folder, n)

tags = (',').join(post_tags)

#create collages
image_names = collagen.collagen(source_folder, output_folder)

#post collages
for image_name in image_names:
    image_path = os.path.join(output_folder, image_name)
    tumbl.post_photo(image_path, tumbl_object, blog_url, tags)

#cleanup source_folder
utils.delete_folder_files(source_folder)

