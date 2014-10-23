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

#image = os.path.join(os.environ['HOME'],'collagen/2.jpg')
#output_folder = os.path.join(os.environ['HOME'],'collagen/segments/')
source_image_folder = sys.argv[1]
output_folder = sys.argv[2]

def segment_images(source_image_folder,segment_path):
    #TODO add information about how many images segmented
    images = os.listdir(source_image_folder)
    for image in images:
        image_path = os.path.join(source_image_folder,image)
        image_type = imghdr.what(image_path)
        if image_type:
            segments.segments(image_path, SEGMENTS_PER_IMAGE ,SEGMENT_PATH)

def delete_folder_files(folder):
    for f in os.listdir(folder):
        file_path = os.path.join(folder, f)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

segment_images(source_image_folder, SEGMENT_PATH)

for i in range(NUMBER_OF_COLLAGES):
    collage.collage(SEGMENT_PATH,output_folder,MAX_COLLAGE_PASTES,COLLAGE_W,COLLAGE_H)

delete_folder_files(SEGMENT_PATH)

