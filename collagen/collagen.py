'''
Collagen is a commandline utility that creates a collage using image segmentation.
'''

import os
import os.path
import segments
import collage
import sys
import utils


def segment_images(source_image_folder,segment_path, segments_per_image):
    
    #TODO add information about how many images segmented
    images = os.listdir(source_image_folder)
    for image in images:
        image_path = os.path.join(source_image_folder,image)
        if utils.is_image(image_path):
            segments.segments(image_path, segments_per_image, segment_path)

def collagen(source_folder, output_folder):

    config = utils.load_config()

    num_collages = config[':collage'][':number_of_collages']
    max_pastes = config[':collage'][':number_of_pastes']
    segments_per_image = config[':segments_per_image'] 
    collage_width = config[':collage'][':width']
    collage_height = config[':collage'][':height']
    segment_path = os.path.join(os.path.realpath('..'), config[':segments_folder'])
    

    segment_images(source_folder, segment_path, segments_per_image)

    for i in range(num_collages):
        name = collage.collage(segment_path, output_folder, max_pastes, collage_width, collage_height)

    utils.delete_folder_files(segment_path)

if __name__ == "__main__":

    #parse arguments
    try:
        source_image_folder = sys.argv[1]
    except IndexError:
        print("usage: python3 collagen.py [source folder] [output folder]")
        sys.exit(1)
        
    if not os.path.isdir(source_image_folder):
        print("Error: Not a folder. Please specify a source folder.")
        sys.exit(1)

    try:
        output_folder = sys.argv[2]
    except IndexError:
        print("No output folder specified.")
        sys.exit(1)

    if not os.path.isdir(output_folder):
        print("Error: Not a folder. Please specify an output folder.")
        sys.exit(1)

    #load config and call collagen

    collagen(source_image_folder, output_folder)

