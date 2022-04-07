# Constants to represent black, and white pixels. Edge images are black lines on white background.
BLACK = 0
BLACK_BYTE = bytearray(BLACK.to_bytes(1, 'big'))  # if there's only one byte endianess doesn't matter. BMP is big-endian, I think

WHITE = 255
WHITE_BYTE = bytearray(WHITE.to_bytes(1, 'big'))

# the image file array rows may have padding to make them a multiple of 4 bytes long 
PADDING = bytearray(BLACK.to_bytes(1, 'big'))


# Dividing image into chunks
MIN_CHUNK_SIZE = 500  # chunks are squares, smallest square used if image is larger than this size in height or width 
CHUNK_OVERLAP = 0.3  # how much chunks overlap as a percentage 0-1.  0.90 is 10% overlap, 0.5 is 50% overlap, 0.3 is 70% overlap

SOBEL_EDGE_THRESHOLD = 120  # larger value, to get sharp edges for stop signs, still finds edges with lower number but more noise

# Hough transform options 
HOUGH_INTERESTING_LINE_THRESHOLD = 0.70  # as a percent of all the lines
THETA_STEP = 1
D_STEP = 1

# Finding lines 
VARIATION_FROM_45 = 5   # how far away from 135 do lines need to be to be considered an octagon?  
MIN_LINES_FOR_STOP_SIGN = 7  # in case an edge is obscured
INTERCEPT_SEPARATION = 30  # how far apart should lines be? This is not very flexible TODO revisit