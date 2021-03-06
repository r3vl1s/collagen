'''
collage.py randomly pastes segments generated by segment.py onto a canvas
'''

from PIL import Image
from datetime import datetime
import random
import os
import os.path
import imghdr

WHITE = (255,255,255,255)
TRANSPARENT = (255,255,255,0)

def canvas_create(dim, color):
    #create white/transparent canvas
    canvas = Image.new('RGBA', dim, color)
    return canvas

def paste(canvas,segment):
    width,height = canvas.size
    box = (random.randrange(width),random.randrange(height)) 
    canvas.paste(segment,box,mask=segment)
    return canvas

def unique_name():
    #create unique name
    name = datetime.isoformat(datetime.now())
    name = name.translate({ord(i):None for i in ':.-'})
    name = name + '.png'
    return name

def pick_segment(segment_path):
    segments = [item for item in os.listdir(segment_path) if imghdr.what(os.path.join(segment_path,item))]
    segment_name = os.path.join(segment_path,random.choice(segments))
    segment = Image.open(segment_name)
    return segment

def collage(segment_path, output_folder, min_pastes, max_pastes, dim):

    print('Making collage...')

    number_of_pastes = random.randint(min_pastes, max_pastes)
    image_dim = random.choice([dim, dim[::-1]]) #flip width and height or not
    color = random.choice([WHITE, TRANSPARENT])
    canvas = canvas_create(image_dim, color)

    for i in range(number_of_pastes):
        segment = pick_segment(segment_path)
        canvas = paste(canvas,segment)

    name = unique_name()
    canvas.save(os.path.join(output_folder, name))
    return name

