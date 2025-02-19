#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 12:05:46 2025

@author: lzallio
"""

import os
from PIL import Image
import imageio

# Folder containing the .png images
folder_path = '/your_folder/'

# Get all .png files from the folder, sorted by name (adjust as necessary)
png_files = [f for f in os.listdir(folder_path) if '_2D_' in f and f.endswith('.png')]
sorted_files = sorted(png_files, key=lambda f: int(os.path.basename(f).split('_')[2].split('.')[0]))

# Create an empty list to store the images
images = []

# Open each .png file and append the image to the images list
for file in sorted_files:
    file_path = os.path.join(folder_path, file)
    img = Image.open(file_path)
    images.append(img)

# Path to save the resulting GIF
gif_path = folder_path+'out_name.gif'

# Save images as a GIF
images[0].save(gif_path, save_all=True, append_images=images[1:], loop=0, duration=100)
