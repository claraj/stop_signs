from pixel_iterator import block_of_pixels_iterator
from constants import *

def histogram_equalize(image, height, width, row_length):

    out_image = [ [0] * row_length for row in range(height) ]

    histogram = [0] * 256

    list_of_pixels = []
    for row in image:
        list_of_pixels += row[:-2]

    count_0 = list_of_pixels.count(0)
    histogram[0] = count_0

    for val in range(1, 256):
        count = list_of_pixels.count(val)
        histogram[val] = histogram[val-1] + count

    total_pixels = height * width

    for val in range(256):
        histogram[val] = min(int(histogram[val] * 255 / total_pixels) + 1, 255)

    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            if x >= row_length:
                out_image[y][x] = PADDING    
            else:
                out_image[y][x] = histogram [ image[y][x]  ]
                
                
    out_image = [ bytearray(row) for row in out_image ]

    return out_image


