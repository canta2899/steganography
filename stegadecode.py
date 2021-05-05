from PIL import Image
from bitarray import bitarray
import sys

"""
    Extracts all the bits embedded inside an image file
    produced using LSB Image Steganography techniques in
    order to retrieve the hidden regular file.

    Usage: python3 [scriptname] [/path/to/image]

    The image must have lossless encoding, otherwise
    information might be compromised or lost during 
    compression.

"""

def decode(image):

    # Pixel Matrix
    width, height = image.size
    pxmatrix = image.load()

    # Will store all the LSB 
    b = bitarray() 

    # Retrieving LSB for every RGB pixel tuple
    for py in range(0, height):
        for px in range(0, width):
            red, green, blue = pxmatrix[px, py]
            b.append(red & 1)
            b.append(green & 1)
            b.append(blue & 1)

    content = b.tobytes().split(b'split')

    # raw bytes content and file extension
    data = content[0]
    ext = content[1].decode('utf-8')

    # Saving as bytes to a file 
    with open(f'out{ext}', 'wb') as a:
        a.write(content[0])


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Provide a valid path to an image file")
        sys.exit(1)

    IMAGE = sys.argv[1]
    image = Image.open(IMAGE)
    decode(image)
