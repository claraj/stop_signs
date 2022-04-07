from datetime import datetime
import os

def read_bmp_file(filename):

    image_array = []

    with open(filename, 'rb') as f:
        header = f.read(54)
        height, width, row_length = dimensions(header)
        print(f'{height=} {width=}')

        assert height < 5000  # catch and crash on really large heights - in images resized in Preview 

        color_table = f.read(256 * 4)  # ignore 

        # read row_length bytes into each line 
        for row in range(height):
            row = bytearray(f.read(row_length))  # bytearray is mutable, bytes are not
            image_array.append(row)

    return header, color_table, image_array

        
def dimensions(bmp_header):
    # print(bmp_header)
    height_bytes = bytearray(bmp_header[22:26])
    height_bytes.reverse()   # little endian
    # print(height_bytes)
    height_dec = int(str(height_bytes.hex()), base=16)
   
    width_bytes = bytearray(bmp_header[18:22])
    width_bytes.reverse()   # little endian
    width_dec = int(str(width_bytes.hex()), base=16)
   
    row_length = width_dec   
    while row_length % 4 != 0:  # there must be a simpler way
        row_length += 1

    return height_dec, width_dec, row_length


def output_filename(in_file):
    ts = int(datetime.now().timestamp())
    in_file = in_file.replace('.bmp', '')
    out_file = f'{in_file}_{ts}.bmp'
    return os.path.join('out', out_file)


def save_bmp_file(filename, header, color_table, lines):
    with open(filename, 'wb') as out_file:
        out_file.write(header)
        out_file.write(color_table)
        for line in lines:
            for b in line:
                if isinstance(b, bytearray):
                    out_file.write(b)   
                
                elif isinstance(b, int):
                    out_file.write(b.to_bytes(1, 'big'))

                else:
                    assert False  # not expected, todo, deal with other types??
