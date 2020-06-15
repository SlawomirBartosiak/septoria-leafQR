#! python3
# septoria-leaves.py

"""
@author: Slawomir Bartosiak
requirements:
pip	19.2.3
opencv-python 4.2.0.32
numpy 1.18.1
pandas 1.0.3
pyzbar 0.1.8
"""

import cv2
import numpy as np
import os
import concurrent.futures
import pandas as pd
from pyzbar.pyzbar import decode
import time

t1 = time.perf_counter()

# Parameters
c_size_threshold = 10000  # Leaf area threshold (remove small objects), default 5000
leaf_hue_min = 0  # Min leaf HUE, default 0
leaf_hue_max = 90  # Max leaf HUE, default 90

diseased_hue_min = 0  # Min diseased HUE, default 0
diseased_hue_max = 45  # Max diseased HUE, default 45

save_leaf_im = True  # True/False save an extracted leaf image
save_diseased_im = True  # True/False save an diseased image

# Global variables
list_obj = []  # Object list
area_leaf = []  # List of leaf area
area_diseased = []  # List of diseased leaf area
percent_dh = []  # List of diseased percentage of leaf

# Directories
dir_old = os.getcwd()
os.makedirs('input_images', exist_ok=True)
os.makedirs('output_analysis', exist_ok=True)
input_path = dir_old + '\\input_images\\'
output_path = dir_old + '\\output_analysis\\'

# Remove old files from output
if save_leaf_im is True or save_diseased_im is True:
    output_files = [f for f in os.listdir(output_path)
                    if f.endswith('.jpg')
                    or f.endswith('.JPG')
                    or f.endswith('.PNG')
                    or f.endswith('.JPEG')]
    for file in output_files:
        os.remove(output_path + file)


# Show an image
def img_show(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Slice an image to mask
def slice_func(mask, image):
    im_mask = mask > 0
    im = np.zeros_like(image, np.uint8)
    im[im_mask] = image[im_mask]
    return im


# Count image area in pixels
def area_pixel(image):
    out_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    pixel_count = cv2.countNonZero(out_grey)
    return pixel_count


# Color threshold
def color_threshold(image, hue_min, hue_max):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (hue_min, 0, 0), (hue_max, 255, 255))
    return mask


# Main function
def main(im_name):
    list_append = []  # returned list of [leaf_area, leaf_disease, imName]

    # Load an image
    im_read = cv2.imread(input_path + im_name)

    # Decode a QR code
    decoded_qr = decode(im_read)

    # Check if QR code is on image
    if not decoded_qr:
        decoded = os.path.splitext(im_name)[0]
    else:
        # print(decoded_qr[0].data.decode('ascii'))
        decoded = decoded_qr[0].data.decode('ascii')

    # Color threshold
    mask = color_threshold(im_read, leaf_hue_min, leaf_hue_max)

    # Slice a leaf
    im = slice_func(mask, im_read)

    # Find leaves contours
    img_grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(img_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    counter = 0  # im write leaf counter

    for contour_no in range(len(contours)):
        area = cv2.contourArea(contours[contour_no])  # Contour area in pixels

        if area > c_size_threshold:  # Remove small contours
            counter = counter + 1  # Increment a counter

            mask = np.zeros_like(img_grey)  # Create mask where white is what we want, black otherwise
            cv2.drawContours(mask, contours, contour_no, 255, -1)  # Draw filled contour in mask
            out = slice_func(mask, im)  # Extract out leaf and place into output image

            # Save a sliced leaf image
            if save_leaf_im is True:
                cv2.imwrite(output_path
                            + '%s_leafNO_%s.jpg' % (decoded, str(counter)), out)

            # Slice to leaf contour
            xmin, ymin, w, h = cv2.boundingRect(contours[contour_no])
            xmax = xmin + w
            ymax = ymin + h
            out = out[ymin:ymax, xmin:xmax]

            # Total leaf area
            leaf_area = area_pixel(out)

            # Threshold diseased leaf area
            mask = color_threshold(out, diseased_hue_min, diseased_hue_max)

            # Slice the diseased
            im_disease = slice_func(mask, out)

            # Save a diseased leaf image
            if save_diseased_im is True:
                cv2.imwrite(output_path
                            + 'diseased_%s_leafNO_%s.jpg' % (decoded, str(counter)), im_disease)

            # Count leaf diseased area in pixels
            leaf_disease = area_pixel(im_disease)

            # Append results to list
            list_append.append([leaf_area, leaf_disease, decoded])  # Append output to global variable
    return list_append


# Append [leaf_area, leaf_disease, im_name] to list
def append_to_list(list_append):
    for n in list_append:
        list_obj.append(os.path.splitext(n[2])[0])
        area_leaf.append(n[0])
        area_diseased.append(n[1])
        percent_dh.append((n[1] / n[0])*100)
        print('diseased area', (n[1] / n[0])*100)


# Multiprocessing function
def start_processing():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        files_jpg = [f for f in os.listdir(input_path)
                     if f.endswith('.jpg')
                     or f.endswith('.JPG')
                     or f.endswith('.PNG')
                     or f.endswith('.JPEG')]
        future_proc = {executor.submit(main, f): f for f in files_jpg}
        for future in concurrent.futures.as_completed(future_proc):
            append_to_list(future.result())


# Start multiprocessing:
if __name__ == '__main__':
    start_processing()

    try:
        # Results data frame
        df = pd.DataFrame(list(zip(list_obj, area_leaf, area_diseased, percent_dh)),
                          columns=['sample_name', 'leaf_area', 'diseased_area', 'diseased_percent'])
        df.to_csv('results.csv')
        print(df)

        # Pivot table of leaf_area, diseased_area sum and average of diseased_percent
        df_hd = df.drop(['diseased_percent'], axis=1)
        df_percent = df.drop(['leaf_area', 'diseased_area'], axis=1)

        pt_hd = pd.pivot_table(df_hd, index='sample_name', aggfunc=np.sum)
        pt_percent = pd.pivot_table(df_percent, index='sample_name', aggfunc=np.mean)
        pt = pd.merge(pt_hd, pt_percent, on=['sample_name'])
        pt.to_csv('pivot_table.csv')

    except pd.core.base.DataError:
        print('No images to analyse in the input_images directory')

    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')
