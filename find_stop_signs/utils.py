from constants import *

def print_img(img_bytes, msg=None, i=None, file=None):
    print(f'\n{msg} {i=}')
    if img_bytes is None:
        print('bytes = None')
    else:
        # for row in reversed(img_bytes):   # compare reverse that reverses in place
        for row in img_bytes:   # compare reverse that reverses in place
            out = ''.join([ '0' if b == WHITE_BYTE or b == WHITE else '*' for b in row ])
            print(out)

        if file:
            with open(file, 'w') as f:
                for row in img_bytes:   # compare reverse that reverses in place
                    out = ''.join([ '0' if b == WHITE_BYTE or b == WHITE else '*' for b in row ])
                    f.write(out)
                    f.write('\n')
        