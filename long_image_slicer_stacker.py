# -*- coding: utf-8 -*-
"""
AI used: Bing - CoPilot aka ChatGPT4

1st Prompt: (main slice and stack function)
    write a python script that divides, by num_divisions, an image's width or height, 
dependent on user direction is horizontal divides height or vertical divides width. 
the split pieces will then be pieced back together into new image either stacking them ontop of 
eachother if split vertically or next to eachother if split horizontally and save 
the file in the same directory as the original with added string indicating it was 
stacked and by number of divisions. the function name and inputs are 
split_image_and_stack(image_path, output_path, direction, num_divisions) and it 
should have a progress bar

2nd Prompt: (gui interface)
    [In the frenzy of troubleshooting, I lost this prompt, but I think it was something as follows]
    write a python function that uses tkinter gui popup window that asks user for file and stores into 
variable image_path. sets output_path to the same directory path as the image_path, asks user for direction
 which is either verticle or horizontal, asks for number of divisions using scrollable number selection and 
returns to variable num_divisions from 2 to 12 integers, and asks the user via check box to save_pieces.
    
Issues:
    the math was incorrect on where to paste the piece of the image, changed to 
    height from piece_size fixed the issue.
    Default options were manipulated to fit what I wanted in the gui code.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PIL import Image
import os
from tqdm import tqdm

def split_image_and_stack(image_path, output_path, direction, num_divisions, save_pieces):
    # Open the image
    with Image.open(image_path) as img:
        # Get the width and height of the image
        width, height = img.size

        # Calculate the size of each piece
        if direction == 'horizontal':
            piece_size = height // num_divisions
        else:
            piece_size = width // num_divisions

        # Split the image into pieces
        pieces = []
        for i in tqdm(range(num_divisions), desc='Splitting image'):
            if direction == 'horizontal':
                box = (0, i * piece_size, width, (i + 1) * piece_size)
            else:
                box = (i * piece_size, 0, (i + 1) * piece_size, height)
            pieces.append(img.crop(box))
            
        if save_pieces:
            for i, piece in enumerate(tqdm(pieces, desc='Showing pieces')):
                # add code here bing
                filename, ext = os.path.splitext(image_path)
                piece_filename = f"{filename}_{direction}_piece_{i+1}_of_{num_divisions}{ext}"
                piece.save(os.path.join(output_path, piece_filename))

        # Create a new image by stacking the pieces
        if direction == 'horizontal':
            print('Horizontal')
            new_image = Image.new('RGB', (width * num_divisions, piece_size))
            for i, piece in enumerate(tqdm(pieces, desc='Stacking pieces on-side')):
                # new_image.paste(piece, (0, i * height))
                new_image.paste(piece, (i * width, 0))
        else:
            new_image = Image.new('RGB', (piece_size, height * num_divisions))
            for i, piece in enumerate(tqdm(pieces, desc='Stacking pieces on-top')):
                # new_image.paste(piece, (i * piece_size, 0))
                new_image.paste(piece, (0, i * height))

        #new_image.show()
        
        # Save the new image
        filename, ext = os.path.splitext(image_path)
        new_filename = f"{filename}_stacked_{num_divisions}_{direction}{ext}"
        while True:
            try:
                new_image.save(os.path.join(output_path, new_filename))
                break
            except FileExistsError:
                # Increment the last string of the filename
                new_filename = new_filename.rsplit('_', 1)[0] + '_' + str(int(new_filename.rsplit('_', 1)[1]) + 1) + ext
               
        new_image.save(os.path.join(output_path, new_filename))

    return "Image has been split and stacked successfully!"
            
def get_input():
    image_path = image_path_entry.get()
    output_path = os.path.dirname(image_path)
    direction = direction_var.get()
    num_divisions = num_divisions_var.get()
    save_pieces = save_pieces_var.get()
    print(f"Image path: {image_path}")
    print(f"Output path: {output_path}")
    print(f"Split Direction: {direction}")
    print(f"Number of divisions: {num_divisions}")
    print(f"Save pieces?: {save_pieces}")
    root.destroy()
    split_image_and_stack(image_path, output_path, direction, num_divisions, save_pieces)
    #stacked_img = Image.open(os.path.join(output_path, stacked_filename))
    #stacked_img.show()

root = tk.Tk()
root.title("Image Processing")
root.geometry("400x150")

# Image path
image_path_label = tk.Label(root, text="Image path:")
image_path_label.grid(row=0, column=0)
image_path_entry = tk.Entry(root, width=30)
image_path_entry.grid(row=0, column=1)
image_path_button = tk.Button(root, text="Browse", command=lambda: image_path_entry.insert(0, filedialog.askopenfilename()))
image_path_button.grid(row=0, column=2)

# Direction
direction_label = tk.Label(root, text="Split Direction:")
direction_label.grid(row=1, column=0)
direction_var = tk.StringVar(value="vertical")
direction_horizontal = tk.Radiobutton(root, text="Horizontal", variable=direction_var, value="horizontal")
direction_horizontal.grid(row=1, column=1)
direction_vertical = tk.Radiobutton(root, text="Vertical", variable=direction_var, value="vertical")
direction_vertical.grid(row=1, column=2)

# Number of divisions
num_divisions_label = tk.Label(root, text="Number of divisions:")
num_divisions_label.grid(row=2, column=0)
num_divisions_var = tk.IntVar(value=2)
num_divisions_combobox = ttk.Combobox(root, textvariable=num_divisions_var, values=list(range(2, 21)))
num_divisions_combobox.grid(row=2, column=1)

# Save each cut piece
save_pieces_var = tk.BooleanVar(value=True)
save_pieces_checkbutton = tk.Checkbutton(root, text="Save pieces?", variable=save_pieces_var)
save_pieces_checkbutton.grid(row=6, column=1)

# Submit button
submit_button = tk.Button(root, text="Submit", command=get_input)
submit_button.grid(row=7, column=1)

root.mainloop()

