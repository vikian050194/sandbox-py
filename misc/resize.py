#!/usr/bin/env python3


from contextlib import nullcontext
import os
from PIL import Image

# pip install Pillow

dir = "/home/kirill/Pictures/updated"
expected_input_width = 1864
expected_input_height = 1053

target_width = 1280
target_height = 800

cut_height_at = 860

def check(name):
    return ".png" in name and "Screenshot from" in name

images = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and check(f)]
images.sort()

for i in range(len(images)):
    image_path = images[i]

    if "popup" in image_path:
        cut_width_at = 1050
    else:
        cut_width_at = 1300

    img = Image.open(image_path)

    assert img.height == expected_input_height
    assert img.width == expected_input_width

    dy = (expected_input_height - target_height) // 2
    dx = (expected_input_width - target_width) // 2

    img2 = img.crop((0, 0, cut_width_at - dx, cut_height_at - dy))
    img1 = img.crop((cut_width_at + dx, 0, expected_input_width, cut_height_at - dy))
    img3 = img.crop((0, cut_height_at + dy, cut_width_at - dx, expected_input_height))
    img4 = img.crop((cut_width_at + dx, cut_height_at + dy, expected_input_width, expected_input_height))


    result = Image.new(mode=img.mode, size=(target_width, target_height))

    result.paste(img2, (0, 0))
    result.paste(img1, (cut_width_at - dx, 0))
    result.paste(img3, (0, cut_height_at - dy))
    result.paste(img4, (cut_width_at - dx, cut_height_at - dy))

    # result = result.resize((1280, 800))

    result.save(f'{dir}/Screenshot {i}{i}.png')
