
from constants import * 
import math 
from collections import namedtuple
import numpy as np 
import matplotlib.pyplot as pyplot
from datetime import datetime


Line = namedtuple('line', 'd theta value')
Pixel = namedtuple('pixel', 'x y')

deg_to_rad = { d: math.radians(d) for d in range(0, 180+1, THETA_STEP) }  # save calculating it every time
    
"""
TODO Can also include information from edge detection, how much does an edge pass the threshold? 
"""

def max_d_for_image(height, width):
    return 2 * math.ceil(math.sqrt(height * height + width * width))  # actual d values will range from -max_d to +max_d


def find_lines(image, height, width, row_length):  # Hough transform

    edge_count = 0

    theta_values = int(180 / THETA_STEP)

    max_d = max_d_for_image(height, width)

    total_d = max_d * 2   
    number_of_d_in_histogram = math.ceil(total_d / D_STEP)

    a = [ [ 0 for i in range(theta_values + 1) ] for j in range(number_of_d_in_histogram) ]  # 2d array 

    # empty list for each cell
    locations_of_pixels_for_cell = [ [ [] for i in range(theta_values + 1) ] for j in range(number_of_d_in_histogram) ]

    for y, row in enumerate(image):   
        for x, pixel in enumerate(row):   
            if y <= 0 or x <= 0 or x >= width or y >= height:  
                # skip padding px 
                # skip pixels at the edges because we don't have any information about them 
                # ignore or write 0 or something 
                continue
            else: 
                pixel = image[y][x]
                if pixel == BLACK_BYTE or pixel == 0:  # is edge 
                    edge_count += 1   # may be used to determine interestingness threshold

                    for theta_chunk in range(0, 180+1, THETA_STEP):   
                        theta_rad = deg_to_rad[theta_chunk]
                        theta_quantized =  int(theta_chunk / THETA_STEP)
                        d = (y * math.sin(theta_rad)) + (x * math.cos(theta_rad))
                        d_quantized = quantize_intersect(max_d, d)
                        a[d_quantized][theta_quantized] += 1
                        locations_of_pixels_for_cell[d_quantized][theta_quantized].append( Pixel(x, y) )


    # print('there are', edge_count, 'edge elements.')

    # identify popular lines
    lines = where_in_image_are_lines(a, edge_count, max_d)
    if lines:
        plot_lines(lines, height, width, max_d)
        print('there are ', len(lines), 'lines')
    else:
        print('no lines')

    return lines, locations_of_pixels_for_cell 


def where_in_image_are_lines(a, edge_count, max_d):

    # interesting line threshold - value may be 7 for small image with one line, or 100s or 1000s for big image. 
    # what are the distribution of values in the histogram a? 
    largest_value = max( [ max(row) for row in a ])
    interesting_line_threshold = largest_value * HOUGH_INTERESTING_LINE_THRESHOLD  # a percent, like 0.8 for 80%  
    
    height = len(a)

    interesting_lines = []
    for quantized_d, row in enumerate(a):
        for quantized_theta, value in enumerate(row): 
            if value > interesting_line_threshold:
                d = get_d_from_quantized(max_d, quantized_d)
                theta = quantized_theta * THETA_STEP
                line = Line(d, theta, value)
                interesting_lines.append(line)
               
    return interesting_lines


def quantize_intersect(max_d, calculated_d):
    # total range is -max_d to +max_d 
    # d is the actual intersect, and may be negative. 
    # quantized intersect is the value of d mapped to array indexes, so is a positive integer between 0 and max_d 
    return int((calculated_d + max_d) / D_STEP)


def get_d_from_quantized(max_d, quantized_d):
    # d is the actual intersect, and may be negative. 
    # quantized intersect is the value of d mapped to array indexes, so is a positive integer between 0 and max_d 
    return (quantized_d * D_STEP) - max_d


def plot_lines(lines, height, width, max_d):

    pyplot.style.use('seaborn-whitegrid')
    figure = pyplot.figure()
    axes = pyplot.axes()
    x = np.linspace(0, width, 10000)

    axes.set_ylim([0, height])

    for line in lines:
        d = line.d 
        theta = line.theta

        if theta == 0 or theta == 180:     
            if d >= 0:
                axes.axvline(d)  # this is the actual d value, not quantized. 
            else:
                print('vertical line with negative intercept')
        else:
            axes.plot(x, normal_to_cartesian(x, d, theta))

    ts = int(datetime.now().timestamp())
    figure.savefig(f'out/plot_{ts}.png')
    pyplot.close()



def normal_to_cartesian(x, d, theta):  
    # function called by matplot lib to chart the line
    theta_rad = math.radians(theta)
    return (d - (x * math.cos(theta_rad) )) / math.sin(theta_rad) 







