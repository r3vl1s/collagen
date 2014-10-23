import numpy as np
import os
import os.path
import yaml
from PIL import Image, ImageOps
from random import choice
from skimage.segmentation import felzenszwalb
from skimage.data import lena
from skimage.util import img_as_float

config_file = open('config.yml')
config = yaml.safe_load(config_file)

#constants for felzenszwalb segmentation function
SCALE = config[':felzenszwalb'][':scale']
SIGMA = config[':felzenszwalb'][':sigma'] 
MIN_SIZE = config[':felzenszwalb'][':min_size'] 

def label_size(label,imarray):
    return (imarray == label).sum()

def sorted_label_sizes(labels, imarray):
    label_list = []
    for label in labels:
        label_list.append([label,label_size(label,imarray)])
    label_list.sort(key=lambda l:l[1])
    return label_list

def n_masks(im,n):
    #returns n masks of largest segments
    im = np.array(im, dtype=np.uint8)
    im1 = img_as_float(im[::2, ::2])

    segments_fz = felzenszwalb(im1,SCALE,SIGMA,MIN_SIZE)
    labels = np.unique(segments_fz)
    labelSizes = sorted_label_sizes(labels,segments_fz)

    #print('# segments ' + str(len(labels)))

    largest_n_labels = labelSizes[-n:]

    masks=[]
    for label in largest_n_labels:
        im2 = np.zeros(im.shape,dtype=np.uint8)
        im2[segments_fz == label[0]] = [255,255,255]
        masks.append(Image.fromarray(im2))
    return masks

def segments(source_image_location,n,output_folder):
    #save n largest transparent segments to folder
    im = Image.open(source_image_location)
    masks= n_masks(im,n)
    for i,mask in enumerate(masks):
        mask = mask.convert('L')
        bbox = mask.getbbox()
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output = output.crop(bbox)
        output.convert('RGBA')
        
        segment_name = os.path.splitext(os.path.basename(source_image_location))[0] + '_s' + str(i) + '.png'
        output.save(os.path.join(output_folder,segment_name))

