'''
Collagen is a commandline utility that creates a collage using image segmentation.
'''

import os
import os.path
from collagen import segments
from collagen import collage
import sys
from collagen import utils
import argparse

COLLAGEN_DIR = os.path.abspath(__file__ + "/../../")

def segment_images(source_image_folder,segment_path, segments_per_image, config):

    print('Segmenting images...')
    
    images = os.listdir(source_image_folder)
    if images:
        for image in images:
            image_path = os.path.join(source_image_folder,image)
            if utils.is_image(image_path):
                segments.segments(image_path, segments_per_image, segment_path, config)
    else: 
        sys.exit('No images to segment in source folder.')

def collagen(source_folder, output_folder):

    config = utils.load_config('config')

    num_collages = config[':collage'][':number_of_collages']
    max_pastes = config[':collage'][':number_of_pastes']
    segments_per_image = config[':segments_per_image'] 
    collage_width = config[':collage'][':width']
    collage_height = config[':collage'][':height']
    segment_path = os.path.join(COLLAGEN_DIR, config[':segments_folder'])
    

    segment_images(source_folder, segment_path, segments_per_image, config)

    name = []
    for i in range(num_collages):
        name.append(collage.collage(segment_path, output_folder, max_pastes, collage_width, collage_height))

    utils.delete_folder_files(segment_path)

    return name


