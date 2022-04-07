from pixel_iterator import block_of_pixels_iterator, convert_line_to_array
from constants import *
import kernels


def find_edges(image, height, width, row_length):
    # apply the sobel operators, one at a time
    # if any operator reports an edge, there's an edge. 
    # TODO which operator reported the edge - clues for the Hough transform?
    # todo write something to the edge elements to preserve original image size
     
    pixels_in_one_line = []

    is_edge = BLACK_BYTE    # 0
    not_edge = WHITE_BYTE    # 255

    for pixel_block, counter in block_of_pixels_iterator(image, height, width, row_length):

        this_pixel_is_edge = not_edge

        if counter % row_length >= width:
            pixels_in_one_line.append(PADDING)

        elif pixel_block is None:
            pixels_in_one_line.append(not_edge)
    
        else:    
            
            this_pixel_is_edge = not_edge
            for name, kernel in kernels.sobel_edge_detectors.items():
                if apply_kernel(kernel, pixel_block) > SOBEL_EDGE_THRESHOLD:
                    this_pixel_is_edge = is_edge
                    break  # no need to check the other operators - if one says edge, it's an edge
            pixels_in_one_line.append(this_pixel_is_edge)
    
    assert (height * row_length) == len(pixels_in_one_line) 
    
    # chop pixels_in_one_line into rows and cols 
    out_pixels = convert_line_to_array(pixels_in_one_line, height, row_length)

    return out_pixels



def apply_kernel(square, filter):
    total = 0
    for r1, r2 in zip(square, filter):
        for c1, c2 in zip(r1, r2):
            total += c1 * c2

    total = int(total)

    if total < 0: 
        return 0
    elif total > 255:
        return 255
    else:
        return total
