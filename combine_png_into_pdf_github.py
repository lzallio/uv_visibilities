#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:43:44 2025

@author: lzallio
"""

from PIL import Image
import os

def png_to_pdf(png_files, output_pdf):
    """
    Combines a list of .png into a single .pdf.
    """
    if not png_files:
        print("png list is empty.")
        return

    images = []

    try:
        # upload images and go RGB
        for file in png_files:
            img = Image.open(file)
            images.append(img.convert('RGB'))

        # Save the first and add the others
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF successfully created: {output_pdf}")
    except Exception as e:
        print(f"Error while creating the pdf: {e}")


if __name__ == "__main__":
    # Your folder path
    folder_path = '/your_folder/'
    
    # pdf output name
    output_pdf = "out.pdf"

    # Find the png (might need editing)
    png_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if '_2D_' in f and f.endswith('.png')]

    # Order your files per name (number)
    sorted_files = sorted(png_files, key=lambda f: int(os.path.basename(f).split('_')[2].split('.')[0]))

    # Combine png into pdf
    png_to_pdf(sorted_files, folder_path+output_pdf)