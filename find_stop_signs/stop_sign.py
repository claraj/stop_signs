from constants import *
from utils import print_img
from hough_transform import quantize_intersect

def find_stop_sign(initial_lines, pixels_for_lines, max_d):
    # examine lines - at least 6 with angles that match 135deg (45) apart from each other 
    # returns None if stop sign not present, or not enough lines

    # TODO use pixels_for_lines to confirm OR as source for lines to make stop sign 

    if not initial_lines:
        print('no lines')
        return

    lines = initial_lines[:]  # make a copy 

    # TODO maybe throw out any with very similar d and theta? 
    # Remember these are quantized
    lines.sort( key = lambda l: l.theta)

    while len(lines) >= MIN_LINES_FOR_STOP_SIGN: 
        line = lines[0]
        # does this work with all the other lines to make a stop sign?
        angle = line.theta
        angles = other_angles_needed(angle)
        matching_lines = lines_with_angles(lines, angles, VARIATION_FROM_45)
        if len(matching_lines) >= MIN_LINES_FOR_STOP_SIGN:
            pixels = get_pixels_for_selected_lines(matching_lines, pixels_for_lines, max_d)
            bounding_box = get_bounding_box(pixels)
            return matching_lines, bounding_box
        # else, remove this line since it's not part of a stop sign, and test the other lines
        lines.remove(line)


def other_angles_needed(angle):
    if angle == 180:
        angle = 0

    angles = [angle]
    for x in range(7):
        angle = (angle + 45) % 180
        if angle == 180:
            angle = 0
        angles.append(angle)
    return angles 


def lines_with_angles(lines, angles, acceptable_delta):
    matching_lines = []
    for angle in angles:
        for line in lines:
            line_angle = 0 if line.theta == 180 else line.theta
            # TODO 0 = 180 and so 175 is close to 0 
            if abs(line_angle - angle) <= acceptable_delta or abs((line_angle - 180) - angle) <= acceptable_delta:
            # if abs(line.theta - angle) < acceptable_delta:
                # do we already have this one or a very similar line?
                if not matching_d(matching_lines, line):
                    matching_lines.append(line)
                    break  # only add one matching line per angle 
        
    return matching_lines


def matching_d(matching_lines, line):
    for l in matching_lines:
        if abs(l.d - line.d) < INTERCEPT_SEPARATION:
            return True 
    return False


def get_pixels_for_selected_lines(lines, pixels_for_lines, max_d):

    if not lines:
        print('no lines')
        return 

    pixels = []  # list of all the pixel locations. Do we care which pixels came from which lines? 
    for line in lines:

        # def get_d_from_quantized(max_d, step, quantized_d):
        # def quantize_intersect(max_d, step, calculated_d):
        d_index = quantize_intersect(max_d, line.d)
        theta_index = int(line.theta / THETA_STEP)
        pixels += pixels_for_lines[d_index][theta_index]


    min_x = min( [p.x for p in pixels ] )
    min_y = min( [p.y for p in pixels ] )
    max_x = max( [p.x for p in pixels ] )
    max_y = max( [p.y for p in pixels ] )

    range_x = max_x - min_x
    range_y = max_y - min_y

    # this only works if we know the offsets from the origin
    image = [ [ WHITE_BYTE for x in range(range_x + 1) ] for y in range(range_y + 1) ]

    for pixel in pixels:   # list of Pixel named tuples
        x = pixel.x - min_x 
        y = range_y - ( pixel.y - min_y )  # the y axis is "upside down"
        image[y][x] = BLACK_BYTE

    print_img(image, file='out/pixels.txt')  # draw "pixels" to a text file, for debugging

    return pixels 



def get_bounding_box(pixels):
    top_left_x = min( [p.x for p in pixels ] )
    top_left_y = min( [p.y for p in pixels ] )
    bottom_right_x = max( [p.x for p in pixels ] )
    bottom_right_y = max( [p.y for p in pixels ] )

    return [top_left_x, top_left_y, bottom_right_x, bottom_right_y]