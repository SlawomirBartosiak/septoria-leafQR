#! python3
# lab_gener.py
"""
@author: Slawomir Bartosiak
requirements:
pip	19.2.3
pypng 0.0.20
Pillow 7.1.2
pyqrcode 1.2.1
"""

import pyqrcode
import os
from PIL import Image, ImageFont, ImageDraw, ImageOps


yes = {'yes', 'y', 'ye', 'tak', '[y]'}
no = {'no', 'n', 'nie', '[n]'}

choice = input('Please enter [y] - yes, to add titles to output files  or '
               '[n] - no, to save files without title.\n').lower()
while choice not in yes and choice not in no:
    choice = input('Please enter [y] - yes, to add titles to output files  or '
                   '[n] - no, to save files without title.\n').lower()

# Check directory
os.makedirs('labels_output', exist_ok=True)
dir_old = os.getcwd()
output_path = dir_old + '\\labels_output\\'

# Remove the old files from the labels_output directory
old_files = [f for f in os.listdir(output_path) if f.endswith('.png')]
for file in old_files:
    os.remove(output_path + file)

# Create an object list form a txt file
with open('object_list.txt') as f:
    object_list = f.readlines()
    object_list = [x.strip() for x in object_list]  # Append lines to list
    object_list = [string for string in object_list if string != ""]  # Remove empty strings from list

# Create QR codes and save images
for obj in object_list:
    print('QR code saved as: ', obj, '.png', sep='')
    qr = pyqrcode.create(obj)
    qr.png(output_path + obj + '.png', scale=8)

# Add a title to images
if choice in yes:
    qr_to_add_text = [f for f in os.listdir(output_path) if f.endswith('.png')]
    for qr_obj in qr_to_add_text:
        qr_im = Image.open(output_path+qr_obj)
        qr_im = ImageOps.expand(qr_im, border=20, fill=255)
        font = ImageFont.truetype('arial.ttf', 25)
        draw = ImageDraw.Draw(qr_im)
        draw.text((5, 5), qr_obj.strip('.png'), font=font)
        qr_im.save(output_path + qr_obj)
elif choice in no:
    pass
print('Finished')
