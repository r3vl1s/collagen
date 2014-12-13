import sys
import os
from collagen import collagen

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

    collagen.collagen(source_image_folder, output_folder)

