import kernels
from pixel_iterator import block_of_pixels_iterator, convert_line_to_array
from constants import *
from utils import print_img
from copy import deepcopy


def thin(edges_image, height, width, row_length):

    # make a copy in which the rows are processed from top down, not bottom up
    edges_image = deepcopy(edges_image)
    edges_image.reverse()

    i = 0
    
    # print_img('initial image', edges_image, i)

    final_points = find_final_points(0, edges_image, height, width, row_length)
    # print_img('final points start', final_points, i)

    while not identical_image(edges_image, final_points):
        contour_points = generate_contour_points(i, edges_image, height, width, row_length)
        # print_img('contour points', contour_points, i)
        edges_image = remove_contour_keep_final(edges_image, contour_points, final_points, width)
        # print_img('edges points after remove contour keep final', edges_image, i)
        i = ( i + 1 ) % 4
        final_points = update_final_points_for_index_with_final_points_from_edge_image(i, edges_image, final_points, height, width, row_length)
        # print_img('final points', final_points, i )

        # input('enter to continue')
        
    # return final_points  # or edge image, whatever, they'll be the same
    final_points.reverse()
    return final_points  # or edge image, whatever, they'll be the same


def find_final_points(index, edges_image, height, width, row_length):
    a = kernels.ai[index]
    b, other_b = kernels.final_b_kernels[index]  # two b 

    line_of_pixels = []
    for pixel_block, counter in block_of_pixels_iterator(edges_image, height, width, row_length, mode="UPRIGHT"):

        # Ignore padding
        if counter % row_length >= width:
            line_of_pixels.append(PADDING)
            continue
        
        if pixel_block is None: 
            line_of_pixels.append(WHITE_BYTE)

        # elif is_final_a_or_b(a, b, None, pixel_block):  # test all at once
        elif is_final_a_or_b(a, b, other_b, pixel_block):  # test all at once
            # then it's a final point 
            line_of_pixels.append(BLACK_BYTE)

        else:
            line_of_pixels.append(WHITE_BYTE)

    return convert_line_to_array(line_of_pixels, height, row_length)


def is_final_a_or_b(a_grid, b_grid, other_b_grid, pixel_block):

    # TODO if entire block is white no need to rest, return False 
  
    if is_final_a(pixel_block, a_grid):
        return True

    if is_final_b(pixel_block, b_grid):
        return True 

    if is_final_b(pixel_block, other_b_grid):
        return True 

    return False 


def is_final_a(pixel_block, a_grid):

    # for an a to represent a final point, the 1 (=255) and 0 must match
    # there must be at least one BLACK pixel in the red area ('r')
    # there must be at least one BLACK pixel in the blue area ('b')

    # Example a, this is the right one,

    # [ 
    #     ['b', 'b',  0 ], 
    #     ['b',  1 , 'r'], 
    #     [ 0 , 'r', 'r'], 
    # ],


    pixel_in_red = False 
    pixel_in_blue = False
    zero_one_matches = 0  # needs to be 3
    
    # print(pixel_block, a_grid)
    for pixel_row, a_row in zip(pixel_block, a_grid):
        for pixel, a_pixel in zip(pixel_row, a_row):
            if a_pixel == 'r' and pixel == BLACK_BYTE:
                pixel_in_red = True 
            elif a_pixel == 'b' and pixel == BLACK_BYTE:
                pixel_in_blue = True 
            elif a_pixel == 0 and pixel == WHITE_BYTE:
                zero_one_matches += 1
            elif a_pixel == 1 and pixel == BLACK_BYTE:
                zero_one_matches += 1
    
    if pixel_in_red and pixel_in_blue and zero_one_matches == 3:
        return True 


def is_final_b(pixel_block, b_grid):

    # For a b pixel to be final,
    # to represent a final point, the 1 (=255) and 0 must match
    # There must be one pixel in the blue area 
    # The None points are ignored
    #     
    # [ 
    #     ['b',  'b',  'b' ], 
    #     [None,  1 ,  0   ], 
    #     [ 0 ,   1,   None], 
    # ],

    pixel_in_blue = False 
    zero_one_matches = 0   # needs to be 4

    for pixel_row, b_row in zip(pixel_block, b_grid):
        for pixel, b_pixel in zip(pixel_row, b_row):
            if b_pixel is not None:
                if b_pixel == 'b' and pixel == BLACK_BYTE:
                    pixel_in_blue = True 
                elif b_pixel == 0 and pixel == WHITE_BYTE:
                    zero_one_matches += 1
                elif b_pixel == 1 and pixel == BLACK_BYTE:
                    zero_one_matches += 1 

    return pixel_in_blue and zero_one_matches == 4                


def identical_image(edges_image, final_points):
    for e_row, f_row in zip(edges_image, final_points):
        for e_col, f_col in zip(e_row, f_row):
            if e_col != f_col:
                return False 
    return True


def generate_contour_points(index, edges_image, height, width, row_length):

    # looking for contour points in one specific direction, above, below, left, or right
    contour_point = kernels.contour_points[index]
    line_of_pixels = []
    for pixel_block, counter in block_of_pixels_iterator(edges_image, height, width, row_length, mode="UPRIGHT"):

        # print_img('block', pixel_block, counter)

        # IGNORE PADDING
        if counter % row_length >= width:
            line_of_pixels.append(PADDING)
            continue

        # does this match the contour? 
        if pixel_block is None:
            line_of_pixels.append(WHITE_BYTE)
            continue

        contour_match_count = 0

        for pixel_row, contour_row in zip(pixel_block, contour_point):
            for pixel, contour in zip(pixel_row, contour_row):
                # this should only be true twice, once for the 0 and once for the 1 
                if contour is not None:
                    if pixel == WHITE_BYTE and contour == 0:
                        contour_match_count += 1
                    elif pixel == BLACK_BYTE and contour == 1:
                        contour_match_count += 1

        if contour_match_count == 2: 
            line_of_pixels.append(BLACK_BYTE)
        else:
            line_of_pixels.append(WHITE_BYTE)
        

    out_pixels = convert_line_to_array(line_of_pixels, height, row_length)
    return out_pixels
        

def remove_contour_keep_final(edges_image, contour_points, final_points, width):
    # Modify edges image to remove the contour points, and add/keep final points 
    for edges_row, contour_row, final_row, y in zip(edges_image, contour_points, final_points, range(len(edges_image))):
        for pixel, contour_point, final_point, x in zip(edges_row, contour_row, final_row, range(len(edges_row))):  
            
            # ignore padding bytes
            if x >= width:
                edges_image[y][x] = PADDING
            
            # don't modify any pixels that are not final, or contour
            elif final_point == BLACK_BYTE:
                # keep and continue 
                edges_image[y][x] = BLACK_BYTE

            elif contour_point == BLACK_BYTE:
                # remove, by setting to white 
                edges_image[y][x] = WHITE_BYTE

    return edges_image 


def update_final_points_for_index_with_final_points_from_edge_image(index, edges_image, final_points,  height, width, row_length):

    # compute final points for this index 
    # add those final points to the current final_points image

    new_final_points = find_final_points(index, edges_image, height, width, row_length) 

    # print_img("existing final points", final_points, index)
    # print_img("new final points", new_final_points, index)


    for y, new_final_point_row in enumerate(new_final_points):
        for x, new_final_point in enumerate(new_final_point_row):
            if new_final_point == BLACK_BYTE:
                final_points[y][x] = BLACK_BYTE

    # print_img("updated final points", final_points, index)

    return final_points


