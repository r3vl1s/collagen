'''
segments.py segments an image using image segmentation algorithms
(currently felzenszwalb or slic) and returns those segments as transparent pngs.

'''

import numpy as np
import os
import os.path
from collagen import utils
from PIL import Image, ImageOps
from random import choice
from skimage.segmentation import felzenszwalb
from skimage.segmentation import slic
from skimage.util import img_as_float

def label_size(label,imarray):
    return (imarray == label).sum()

def sorted_label_sizes(labels, imarray):
    label_list = []

    for label in labels:
        label_list.append([label,label_size(label,imarray)])
    label_list.sort(key=lambda l:l[1])
    return label_list

def mask_felz(image, config):
    #constants for felzenszwalb segmentation function
    scale = config[':felzenszwalb'][':scale']
    sigma = config[':felzenszwalb'][':sigma'] 
    min_size = config[':felzenszwalb'][':min_size'] 

    segments = felzenszwalb(image, scale, sigma, min_size)
    return segments

def mask_slic(image, config):
    #constants for slic
    n_segments = config[':slic'][':n_segments']
    compactness = config[':slic'][':compactness']
    sigma = config[':slic'][':sigma']

    segments = slic(image, n_segments, compactness, sigma)
    return segments

def n_masks(im,n, config):
    #returns n masks of largest segments
    im = np.array(im, dtype=np.uint8)
    im1 = img_as_float(im[::2, ::2])

    segments = mask_felz(im1, config)
    #segments = mask_slic(im1, config)
    labels = np.unique(segments)
    labelSizes = sorted_label_sizes(labels,segments)

    #print('# segments ' + str(len(labels)))

    largest_n_labels = labelSizes[-n-4:-2]

    masks=[]
    for label in largest_n_labels:
        im2 = np.zeros(im.shape,dtype=np.uint8)
        im2[segments == label[0]] = [255,255,255]
        masks.append(Image.fromarray(im2))
    return masks

def segments(source_image_location,n,output_folder, config):
    #save n largest transparent segments to folder
   
    img = Image.open(source_image_location)
    im = img.convert('RGB')
    masks= n_masks(im,n, config)
    for i,mask in enumerate(masks):
        mask = mask.convert('L')
        bbox = mask.getbbox()
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output = output.crop(bbox)
        output.convert('RGBA')
        
        segment_name = os.path.splitext(os.path.basename(source_image_location))[0] + '_s' + str(i) + '.png'
        output.save(os.path.join(output_folder,segment_name))

