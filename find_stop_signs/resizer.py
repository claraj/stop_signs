from pixel_iterator import block_of_pixels_iterator, convert_line_to_array
import constants

import math 


# TODO NOT COMPLETE 

def resize(header, image_bytes, width, height, row_length):  
    """ 3x3 only right now, would need to re-write iterator  """
    
    out_image = []

    for block, counter in block_of_pixels_iterator(image_bytes, height, width, row_length):
        
        row = math.floor(counter / row_length)
        col = math.floor(counter % row_length)
        
        if (row - 1) % 3 == 0 and (counter - 1) % 3 == 0 :  # 1, 4, 7 ... 
            if block:   # returns None if includes sides of image or padding bytes
                average = block_average(block)
            else:
                average = WHITE_BYTE  # or, not an edge. Padding color is ignored as far as I can tell
            
            out_image.append(average)
        else:
            continue

    out_image_array = convert_line_to_array(pixels_in_one_line, height, row_length)


def block_average(block):
    total = 0
    for row in block:
        for p in row:   
            total += p 

    return total / 9   # depending on 3x3 yuck