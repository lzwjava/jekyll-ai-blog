import os
import shutil

source_directory = "/home/lzw/Projects/imagenet/images/train"

files = os.listdir(source_directory)

for filename in files:
    prefix = filename.split("_")[0]

    destination_directory = os.path.join(source_directory, prefix)

    if not os.path.exists(destination_directory):
        os.mkdir(destination_directory)

    source_file = os.path.join(source_directory, filename)
    destination_file = os.path.join(destination_directory, filename)

    shutil.move(source_file, destination_file)

print("Images have been moved to subdirectories based on filename prefixes.")
