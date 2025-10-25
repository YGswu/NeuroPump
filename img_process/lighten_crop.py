# This file was modified by Yue Guo
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
import os

def calculate_t(input_folder):
    color_sum = np.array([0.0, 0.0, 0.0])
    color_count = 0
    
    J_sum = np.array([0.0, 0.0, 0.0])
    J_count = 0
    
    image_files = os.listdir(input_folder)
    
    for filename in image_files:
        if filename.lower().startswith('color') and filename.endswith(('.png', '.jpg', '.jpeg')):
    
            input_path = os.path.join(input_folder, filename)
            img = Image.open(input_path)
            img_array = np.array(img) / 255.0
            
            limit1 = 0.04045 #srgb2linear
            img_array = np.where(img_array > limit1, ((img_array + 0.055) / 1.055) ** 2.4, img_array / 12.92)
    
            color_sum += np.sum(img_array, axis=(0, 1))
            color_count += 1
        
        if filename.endswith(('.png', '.jpg', '.jpeg')) and filename.lower().startswith('j'):
            # print("j")
            input_path = os.path.join(input_folder, filename)
            img = Image.open(input_path)
            img_array = np.array(img) / 255.0
            
            limit1 = 0.04045 #srgb2linear
            img_array = np.where(img_array > limit1, ((img_array + 0.055) / 1.055) ** 2.4, img_array / 12.92)
            
            J_sum += np.sum(img_array, axis=(0, 1))
            J_count += 1
    
    if color_count == 0 or J_count == 0:
        print(input_folder)
        print("error ratio")
        print(f"[ERROR] no images are found in {input_folder}")
        print(k)
        return 1.0 
        
    color_mean = color_sum / (color_count * img_array.shape[0] * img_array.shape[1])
    J_mean = J_sum / (J_count * img_array.shape[0] * img_array.shape[1])
    
    t = np.mean(color_mean) / np.mean(J_mean)
    
    print("t value: ", t)
        
    return t
    
def srgb_to_linear(value):
    limit1 = 0.04045
    value = value / 255
    if value <= limit1:
        return value / 12.92
    else:
        return ((value + 0.055) / 1.055) ** 2.4
        
def linear_to_srgb(value):
    limit2 = 0.0031308
    if value <= limit2:
        return 12.92 * value * 255
    else:
        return 255 * (1.055 * (value ** (1.0 / 2.4)) - 0.)


def process_images(input_folder, output_folder, output_folder_crop, t, x1, y1, x2, y2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    image_files = os.listdir(input_folder)
    
    for filename in image_files:
       
        if filename.endswith(('.png', '.jpg', '.jpeg')):
        # and filename.lower().startswith('j'):
            input_path = os.path.join(input_folder, filename)
            
            img = Image.open(input_path)
            
            # cropping
            img = img.crop((x1, y1, x2, y2))
            
            img_array = np.array(img, dtype=np.float32)
            img_array /= 255.0  # Normalize the values to the range [0, 1]

            # Apply sRGB to linear conversion
            img_array = np.where(img_array > 0.04045, ((img_array + 0.055) / 1.055) ** 2.4, img_array / 12.92)

            # Apply the factor 't' to each channel
            
            img_array *= t

            # Apply linear to sRGB conversion
            img_array = np.where(img_array > 0.0031308, 1.055 * np.power(img_array + 0.00001, 1.0 / 2.4) - 0.055, 12.92 * img_array)

            # Convert the NumPy array back to an Image
            result_img = Image.fromarray((img_array * 255).clip(0, 255).astype(np.uint8))


            # output_subfolder_path = os.path.join(output_folder, output_subfolder)
            output_subfolder_path = output_folder
            output_subfolder_path_crop = output_folder_crop
            
            if not os.path.exists(output_subfolder_path):
                os.makedirs(output_subfolder_path)
            if not os.path.exists(output_subfolder_path_crop):
                os.makedirs(output_subfolder_path_crop)
            
            output_path = os.path.join(output_subfolder_path, filename)
            output_path_crop = os.path.join(output_subfolder_path_crop, filename)
            
            result_img.save(output_path)
            img.save(output_path_crop)
        
        if filename.endswith(('.png', '.jpg', '.jpeg')) and filename.lower().startswith('co'):
            input_path = os.path.join(input_folder, filename)
            
            img = Image.open(input_path)
            # cropping
            img = img.crop((x1, y1, x2, y2))
            
            output_subfolder_path_crop = output_folder_crop
            
            if not os.path.exists(output_subfolder_path_crop):
                os.makedirs(output_subfolder_path_crop)

            output_path_crop = os.path.join(output_subfolder_path_crop, filename)
            img.save(output_path_crop)
            

def process_folders_in_parent_folder(parent_folder, scene):
    subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
    
    for nn in [0]:
        input_folder_path = parent_folder
        output_folder_path = parent_folder + '_fully_rectified_results'
        output_folder_path_crop = parent_folder + '_results_before_lighten'
        
        t = calculate_t(input_folder_path)
        if t > 1:
          t = t
        else:
          t = 1.
        
        if scene == "pre_totoro910":
            x1, y1, x2, y2 = 5, 10, 960, 540
            # x1, y1, x2, y2 = 0, 0, 955, 530  # for gt crop
        
        elif scene == "pre_pg_hero910":
            x1, y1, x2, y2 = 0, 20, 955, 540
            # x1, y1, x2, y2 = 5, 0, 960, 520  # for gt crop

        elif scene == "pre_pg_flower910":
            x1, y1, x2, y2 = 5, 20, 960, 540  
            # x1, y1, x2, y2 = 0, 0, 955, 520   # for gt crop

        elif scene == "pre_lying_cow910":
            x1, y1, x2, y2 = 15, 15, 960, 540
            # x1, y1, x2, y2 = 0, 0, 945, 525   # for gt crop

        elif scene == "pre_master910":
            x1, y1, x2, y2 = 0, 6, 960, 540 
            # x1, y1, x2, y2 = 0, 0, 960, 534  # for gt crop
        
        else: 
            print("[WARNING!] render_scene not in crop-list. Set crop-free! \n Crop is only for evaluation. If this scene really needs crop, please check it in crop_liten.py.")
            x1, y1, x2, y2 = 0, 0, 0, 0
        
        process_images(input_folder_path, output_folder_path, output_folder_path_crop, t, x1, y1, x2, y2)
