# This file was modified by Yue Guo
# -*- coding: utf-8 -*-


import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error
from math import log10
import matplotlib.pyplot as plt
import pandas as pd
import re

def show_img(image1, image2, ssim, rmse):
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(image1)
    axes[0].set_title(f"eval SSIM: {ssim:.4f} RMSE: {rmse:.4f}".format(ssim=ssim))
    axes[0].axis('off')

    axes[1].imshow(image2)
    axes[1].set_title("gt")
    axes[1].axis('off')

    difference = (image1/255. - image2/255.) ** 2
    difference_gray = np.mean(difference, axis=2)

    im = axes[2].imshow(difference_gray, cmap='hot', interpolation='nearest')
    axes[2].set_title('Squared Difference Heatmap')
    axes[2].axis('off')
    fig.colorbar(im, ax=axes[2], label='Squared Difference')

    plt.tight_layout()

    plt.show()


def bgr_to_rgb(image):
    print(image.shape)
    return image[:, :, [2, 1, 0]]


def calculate_metrics(image1, image2):
    height, width, _ = image1.astype(float).shape
    
    normalized_image1 = image1.astype(float) / 255.0
    normalized_image2 = image2.astype(float) / 255.0

    ssim_value = ssim(image1, image2, win_size=11, channel_axis=2)

    reshaped_image1 = normalized_image1.reshape(-1, 3)
    reshaped_image2 = normalized_image2.reshape(-1, 3)

    
    mse = mean_squared_error(reshaped_image1, reshaped_image2)
    rmse = np.sqrt(mse)
    
    
    max_pixel = 1.0
    psnr = 20 * log10(max_pixel / rmse)
    
    return ssim_value, rmse, psnr


def process_images_in_folders(eval_folder, gt_folder):

    eval_image_files = sorted([f for f in os.listdir(eval_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg')) and f.startswith('J')])
    gt_image_files = sorted([f for f in os.listdir(gt_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    num_images = len(eval_image_files)
    
    print(eval_folder)
    print(eval_image_files)
    print(gt_image_files)
    
    total_ssim = 0.0
    total_rmse = 0.0
    total_psnr = 0.0
    
    for i in range(num_images):
        eval_image_path = os.path.join(eval_folder, eval_image_files[i])
        gt_image_path = os.path.join(gt_folder, gt_image_files[i])
        
        eval_image = cv2.imread(eval_image_path)
        gt_image = cv2.imread(gt_image_path)
        
        if eval_image is not None and gt_image is not None:
            eval_image = bgr_to_rgb(eval_image)
            gt_image = bgr_to_rgb(gt_image)
            
            ssim_value, rmse, psnr = calculate_metrics(eval_image, gt_image)
            
            print(ssim_value)
            
            total_ssim += ssim_value
            total_rmse += rmse
            total_psnr += psnr
            
    avg_ssim = total_ssim / num_images
    print(num_images)
    print(total_ssim)
    avg_rmse = total_rmse / num_images
    avg_psnr = total_psnr / num_images
    
    return avg_ssim, avg_rmse, avg_psnr

def process_folders_in_parent_folder(parent_folder, gt_folder_path, excel_path):
    pattern = re.compile(r"^render_step_\d+$")

    subfolders = [
        f for f in os.listdir(parent_folder)
        if os.path.isdir(os.path.join(parent_folder, f))
        and not pattern.match(f)
    ]

    result_df = pd.DataFrame(columns=['Subfolder', 'PSNR', 'SSIM', 'RMSE'])
    
    for subfolder in subfolders:
        eval_folder_path = os.path.join(parent_folder, subfolder)
        
        avg_ssim, avg_rmse, avg_psnr = process_images_in_folders(eval_folder_path, gt_folder_path)
        
        print(f"Subfolder: {subfolder}")
        print(f"Average SSIM: {avg_ssim:.5f}")
        print(f"Average RMSE: {avg_rmse:.5f}")
        print(f"Average PSNR: {avg_psnr:.5f}")
        
        result_df = pd.concat([result_df, pd.DataFrame({'Subfolder': [subfolder], 'PSNR': [avg_psnr], 'SSIM': [avg_ssim], 'RMSE': [avg_rmse]})], ignore_index=True)
        
    result_df.to_excel(excel_path, index=False)

if __name__ == "__main__":

    parent_folder_path = "" # Render images' folder 
    gt_folder_path = "" # In-air GT images' folder
    excel_path = parent_folder_path + "crop-result.xlsx"

    process_folders_in_parent_folder(parent_folder_path, gt_folder_path, excel_path)