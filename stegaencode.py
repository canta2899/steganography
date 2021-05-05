from PIL import Image
from bitarray import bitarray
import sys
import os

def build_message(msg_file):
    with open(msg_file, "rb") as file:
        msg = file.read()
    ext = os.path.splitext(msg_file)[-1].lower()
    msg = msg + b'split' + bytes(ext, 'utf-8') + b'split'
    bits = bitarray()
    bits.frombytes(msg)
    bits = [int(bit) for bit in bits]
    return bits

def new_value(pixel, bit):
    return (pixel & ~1) | bit

def update_color(pixel):
    global index, bound
    if index < bound:
        newpixel = new_value(pixel, bits_msg[index])
        index += 1
        return newpixel
    return pixel

def embed():
    for py in range(0, height):
        for px in range(0, width):
            if index >= bound:
                break

            red, green, blue = pxmatrix[px, py]

            red = update_color(red)
            green = update_color(green)
            blue = update_color(blue)

            pxmatrix[px, py] = (red, green, blue)

    print('Done. Saving...')
    image.save(f'embedded.png')


IMAGE = sys.argv[1]
MESSAGE_FILE = sys.argv[2]

image = Image.open(IMAGE)
width, height = image.size
pxmatrix = image.load()

bits_msg = build_message(MESSAGE_FILE)
bound = len(bits_msg)
index = 0

if bound > width*height*3:
    print("This picture can't cointain the given content")
    exit(1)

embed()
