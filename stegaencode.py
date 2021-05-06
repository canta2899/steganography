from PIL import Image
from bitarray import bitarray
import sys
import os

"""
    Given an image file and a path to a regular file, produces a 
    new image file which embeds the raw content of the reg file
    by using LSB Image Steganography techniques.

    Usage: python3 [scriptname] [/path/to/image] [/path/to/file]

    The image produced as output will be saved as PNG so that the
    content won't be compromised because of lossy compression.
"""

# Builds a bit array containing both raw content and ext
# given a path to a regular file
def build_message(msg_file):
    
    # Reads file
    with open(msg_file, "rb") as file:
        msg = file.read()

    # Size of the message in bytes
    size_msg = sys.getsizeof(msg)
    size_msg = size_msg.to_bytes(4, byteorder='big')

    # Reads file extension and extension's size
    ext = os.path.splitext(msg_file)[-1][1:].lower()
    size_ext = len(ext).to_bytes(4, byteorder='big')
    
    # Builds the whole message
    msg = size_ext + bytes(ext, 'utf-8') + size_msg + msg

    # Conversion to bit array
    bits = bitarray()
    bits.frombytes(msg)
    bits = [int(bit) for bit in bits]

    return bits


# Modifies the LSB for every color of every pixel
def new_value(pixelcolor, bit):
    return (pixelcolor & ~1) | bit


# Updates pixel LSB if conditions are verified
def update_color(pixel, index, bound, bits_msg):
    if index < bound:
        return (pixel & ~1) | bits_msg[index]
    return pixel


# Checks if the picture will be able to contain the whole file
def check_dimension(bound, width, height):
    if bound > width*height*3:
        print("This picture can't cointain the given content")
        sys.exit(1)


# Builds a new image that embeds the file content
def embed(image, msg_file):
    width, height = image.size
    pxmatrix = image.load()

    # Checks if the file can be stored
    bit_size = (os.stat(msg_file)).st_size * 8
    check_dimension(bit_size, width, height)

    # If so, builds the bit array
    bits_msg = build_message(msg_file)
    bound = len(bits_msg)
        
    # The index will keep track of the next bit to be stored
    index = 0
    
    # For color or every pixel, update the LSB accordingly
    for py in range(0, height):
        for px in range(0, width):
            if index >= bound:
                break

            rgb = pxmatrix[px, py]
            newcolors = []

            for color in rgb:
                newcolors.append(update_color(color, index, bound, bits_msg))
                index += 1

            pxmatrix[px, py] = tuple(newcolors)

    print('Done. Saving...')
    image.save(f'embedded.png') # might take some seconds with big images


if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print("Not enough arugments. Usage:")
        print("python3 [name] [path/to/picture] [path/to/file]")
        sys.exit(1)

    IMAGE = sys.argv[1]
    MESSAGE_FILE = sys.argv[2]

    image = Image.open(IMAGE)

    embed(image, MESSAGE_FILE)


