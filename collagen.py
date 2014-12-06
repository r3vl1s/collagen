import os
import os.path
import segments
import collage
import sys
import imghdr
import yaml

config_file = open('config.yml')
config = yaml.safe_load(config_file)

SEGMENT_PATH = config[':segments_folder'] 
SEGMENTS_PER_IMAGE = config[':segments_per_image']
NUMBER_OF_COLLAGES = config[':collage'][':number_of_collages']
MAX_COLLAGE_PASTES = config[':collage'][':number_of_pastes']
COLLAGE_W = config[':collage'][':width']
COLLAGE_H = config[':collage'][':height']

def isImage(input_path):
    return imghdr.what(input_path)

def segment_images(source_image_folder,segment_path):
    #TODO add information about how many images segmented
    images = os.listdir(source_image_folder)
    for image in images:
        image_path = os.path.join(source_image_folder,image)
        if isImage(image_path):
            segments.segments(image_path, SEGMENTS_PER_IMAGE ,SEGMENT_PATH)

def delete_folder_files(folder):
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        try:
            if imghdr.what(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


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
        output_folder = sys.argv[1]
    except IndexError:
        print("No output folder specified.")
        sys.exit(1)

    if not os.path.isdir(output_folder):
        print("Error: Not a folder. Please specify an output folder.")
        sys.exit(1)

    segment_images(source_image_folder, SEGMENT_PATH)

    for i in range(NUMBER_OF_COLLAGES):
        collage.collage(SEGMENT_PATH,output_folder,MAX_COLLAGE_PASTES,COLLAGE_W,COLLAGE_H)

    delete_folder_files(SEGMENT_PATH)

