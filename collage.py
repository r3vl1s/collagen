from PIL import Image
import random
import os
import os.path
import imghdr

def canvas_create(width,height):
    #create white/transparent canvas
    canvas = Image.new('RGBA',(width,height),"white")
    return canvas

def paste(canvas,segment):
    width,height = canvas.size
    box = (random.randrange(width),random.randrange(height)) 
    canvas.paste(segment,box,mask=segment)
    return canvas

def unique_name():
    #create unique name
    from datetime import datetime
    name = datetime.isoformat(datetime.now())
    name = name.translate({ord(i):None for i in ':.-'})
    name = name + '.png'
    return name

def pick_segment(segment_path):
    segments = [item for item in os.listdir(segment_path) if imghdr.what(os.path.join(segment_path,item))]
    segment_name = os.path.join(segment_path,random.choice(segments))
    segment = Image.open(segment_name)
    return segment

def collage(segment_path,output_folder,max_pastes,width,height):

    N = max_pastes
    canvas = canvas_create(width,height)

    for i in range(N):
        segment = pick_segment(segment_path)
        canvas = paste(canvas,segment)

    name = unique_name()
    canvas.save(os.path.join(output_folder,name))

