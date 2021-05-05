from PIL import Image
from bitarray import bitarray
import sys

IMAGE = sys.argv[1]
SPLIT = '%%%'
if len(sys.argv) > 2:
    SPLIT = sys.argv[2]
    print('Changed split to %s' % SPLIT)


image = Image.open(IMAGE)
width, height = image.size
pxmatrix = image.load()

def extract_lsb(pixel):
    return pixel & 1

def decode():
    b = bitarray()
    for py in range(0, height):
        for px in range(0, width):
            red, green, blue = pxmatrix[px, py]
            b.append(extract_lsb(red))
            b.append(extract_lsb(green))
            b.append(extract_lsb(blue))

    content = b.tobytes().split(b'split')
    data = content[0]
    ext = content[1].decode('utf-8')
    with open(f'out{ext}', 'wb') as a:
        a.write(content[0])

decode()
