from PIL import Image, ImageDraw

from time_fn import timer
from thinning import thin
import hough_transform
from find_edges import find_edges
from histogram_equalization import histogram_equalize
import stop_sign 
from file_io import *
from pixel_iterator import block_of_pixels_iterator, convert_line_to_array, image_chunk_iterator
from constants import *


filename = 'bw_images/image-4.bmp'

# pre_thinned = 'out/bw_images/pre_thinned/image-4-stop_thinned.bmp'
# filename = pre_thinned

@timer
def find_stop_signs():

    # used when working with pre-saved thinned images 
    # header, color_table, thinned_array = read_bmp_file(pre_thinned)
    # print('Get dimensions')
    # height, width, row_length = dimensions(header)
    # is_there_a_stop_sign(thinned_array, height, width, row_length, chunk_image=True)
    # exit()

    print('Read bitmap')
    header, color_table, original_file_array = read_bmp_file(filename)

    print('Get dimensions')
    height, width, row_length = dimensions(header)

    print('Histogram equalization')
    histogram_equalized = histogram_equalize(original_file_array, height, width, row_length)
    save_bmp_file(output_filename(filename).replace('.bmp', '_histo.bmp'), header, color_table, histogram_equalized)
    
    print('finding edges')
    edges = find_edges(original_file_array, height, width, row_length)
    # edges = find_edges(histogram_equalized, height, width, row_length)
    save_bmp_file(output_filename(filename).replace('.bmp', '_edges.bmp'), header, color_table, edges)

    print('thinning edges')
    thinned = thin(edges, height, width, row_length)

    print('saving file')
    save_bmp_file(output_filename(filename).replace('.bmp', '_thinned.bmp'), header, color_table, thinned)

    is_there_a_stop_sign(thinned, height, width, row_length, chunk_image=True)
    

def is_there_a_stop_sign(image_bytes, height, width, row_length, chunk_image=False):

    # print('examining entire image')

    # lines, bounding_box = find_stop(image_bytes, height, width, row_length)   # bounding_box needs to be a list with coords [top left x, top left y, bottom right x, bottom right y]
    # if bounding_box:
    #     # im_with_square.rectangle([start_col, start_row, start_col+chunk_width, start_row+chunk_height], outline=128)
    #     return    

    if chunk_image:

        print('Examining blocks')

        # what size chunks? 
        chunk_size = int(min(height, width, MIN_CHUNK_SIZE))
        chunk_overlap = int(chunk_size * CHUNK_OVERLAP)

        im = Image.open(filename)
        im_with_square = ImageDraw.Draw(im)

        for index, chunk in enumerate(image_chunk_iterator(image_bytes, height, width, row_length, chunk_size, chunk_overlap)):

            pixel_chunk, start_row, start_col, chunk_height, chunk_width = chunk    
            lines, bounding_box = find_stop(pixel_chunk, chunk_height, chunk_width, chunk_width)

            im_with_square.rectangle([start_col, start_row, start_col+chunk_width, start_row + chunk_height], outline=0) 

            if bounding_box:                
                break    # if we only expect 1 stop sign. Or could carry on and look for others?
            
        im.show()


def find_stop(image_bytes, height, width, row_length):  

    lines, pixels_for_lines = hough_transform.find_lines(image_bytes, height, width, row_length) 

    max_d = hough_transform.max_d_for_image(height, width) 

    result = stop_sign.find_stop_sign(lines, pixels_for_lines, max_d)

    if result:

        im = Image.open(filename)
        im_with_square = ImageDraw.Draw(im)

        stop_sign_lines, bounding_box = result #= stop_sign.find_stop_sign(lines, pixels_for_lines, max_d)

        im_with_square.rectangle(bounding_box, outline=0) 
        im.show() 
       
    # if stop_sign_lines:
        # print('there seems to be a stop sign in the square at ', start_row, start_col, chunk_height, chunk_width)
        print('there seems to be a stop sign in the square given by lines')
        for l in stop_sign_lines:
            print(l)

        hough_transform.plot_lines(stop_sign_lines, height, width, max_d)

        # stop_sign_pixels, bounding_box = stop_sign.stop_sign_location_for_lines(lines)
        # bounding_box = stop_sign.bounding_box_for_pixels(stop_sign_pixels)
        return stop_sign_lines, bounding_box 

    else:
        print('No stop sign found')
        return None, None 







if __name__ == '__main__':
    find_stop_signs()