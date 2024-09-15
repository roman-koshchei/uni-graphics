from skimage import io, util, transform
from matplotlib import pyplot as plt
import numpy as np

image = io.imread('./images/town.png')

image_uint8 = util.img_as_ubyte(image)
# convert to rgb instead of rgba
image_rgb = image[:, :, :3]

# Get original dimensions
original_height, original_width = image_rgb.shape[:2]

# Calculate new dimensions (1.5 times the original)
new_height = int(original_height * 1.5)
new_width = int(original_width * 10)

resized_image = transform.resize(image_rgb, (new_height, new_width), anti_aliasing=True) * 255
resized_image = resized_image.astype(np.uint8)

# print(resized_image)

old_color = np.array([237, 125, 67])  
new_color = np.array([0, 236, 50])

tolerance = 50

height, width, channels = resized_image.shape

# Iterate through each pixel
for y in range(height):
    for x in range(width):
        # Check if the pixel matches the old color
         if np.all(np.abs(resized_image[y, x] - old_color) <= tolerance):
            # Change the pixel to the new color
            resized_image[y, x] = new_color

red_multiplier = 1.02
green_multiplier = 0.98

for y in range(height):
    for x in range(width):
        new_red = resized_image[y, x][0] * red_multiplier
        if(new_red > 255): new_red = 255
        resized_image[y, x][0] = new_red
        resized_image[y, x][1] = resized_image[y, x][1] * green_multiplier 


io.imsave('./images/res.jpg', resized_image)


