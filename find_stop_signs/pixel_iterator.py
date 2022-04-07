
def image_chunk_iterator(image, height, width, row_length, chunk_size, chunk_overlap):

    # divide into rough squares since stop signs fit into a square box
    # how big are squares? Want a good chance of stop sign fitting into a square
    #   could return big squares then smaller squares? 
    # how much overlap?

    big_square = chunk_size
    big_square_overlap = chunk_overlap


    smaller_dimen = min(height, width)
    # if smaller_dimen > big_square:
    
    row_counter = 0
    col_counter = 0

    for row_counter in range(0, height, big_square_overlap):
        for col_counter in range(0, width, big_square_overlap):
            print(f'{height=} {width=} {row_counter=} {col_counter=}')
            chunk = get_chunk(image, row_counter, col_counter, big_square, big_square, row_length)
            yield (chunk, row_counter, col_counter, big_square, big_square)
        

def get_chunk(image, start_chunk_row, start_chunk_col, chunk_height, chunk_width, row_length):
    #  do this with slices to make new lists, rather than parts of original 
    rows_in_chunk = image[start_chunk_row: start_chunk_row + chunk_height]
    return [ row[start_chunk_col: min(start_chunk_col+chunk_width, row_length)] for row in rows_in_chunk ] 
    

def block_of_pixels_iterator(image, height, width, row_length, mode=None):
    """ outputs 3x3 blocks of pixels for applying operators such as Sobel """

    counter = 0

    print('.', end='', flush=True)  # progress monitor

    # if mode is None:
    for y, row in enumerate(image):   
        for x, pixel in enumerate(row):    # todo skip the padding pixels
            
            if counter % 10000 == 0:
                print('.', end='', flush=True)

            try: 
                if y-1 < 0 or x-1 < 0 or x + 1 >= width or y + 1 >= height:  # skip padding px and pixels at the edges
                    yield None, counter

                else:
                    pixel_block = [
                        [ image[y-1][x-1] , image[y][x-1], image[y+1][x-1] ],
                        [ image[y-1][x]   ,   pixel,         image[y+1][x] ],
                        [ image[y-1][x+1] , image[y][x+1], image[y+1][x+1] ],
                    ]

                    yield pixel_block, counter

            except IndexError as e:
                yield None, counter   # going to ignore the edge 2 pixels

            counter += 1

    print()  # print a new line after all the dots (if any)


def convert_line_to_array(pixels_in_one_line, height, row_length):
    out_pixels = [] 
    col_counter = 0 

    for row in range(height): 
        new_row = pixels_in_one_line[col_counter: col_counter + row_length]
        out_pixels.append(new_row)
        col_counter += row_length

    return out_pixels


