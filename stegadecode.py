from PIL import Image
from bitarray import bitarray
import sys

"""
    Extracts all the bits embedded inside an image file
    produced using LSB Image Steganography techniques in
    order to retrieve the hidden regular file.

    Usage: python3 [scriptname] [/path/to/image]

    The image must use lossless encoding, otherwise
    information might be compromised or lost during 
    compression. The script assumes that the input image
    includes some hidden content, otherwise its behaviour
    is undefined.

"""

# Retrieves the information hidden in the picture
# The byte string retrieved is formatted as follows

#   - first 4 bytes -> extension length
#   - n following bytes -> extension
#   - next 4 bytes -> content length
#   - next m bytes -> content 

def retrieve_file(content):
    print('Saving...') 

    # Reads extension size and then reads the bytes
    # containing the extension
    ext_size = int.from_bytes(
            content[:4], 
            byteorder='big'
    )

    ext = content[4:4+ext_size].decode('utf-8')
    
    # Reads content length and then reads the content
    content_length = int.from_bytes(
            content[ext_size+4:ext_size+8], 
            byteorder='big'
    )

    content = content[ext_size+8:ext_size+8+content_length]
    
    # Saves to a file with the given extensions
    with open(f'out.{ext}', 'wb') as f:
        f.write(content)

    print(f'Output written to out.{ext}')
    print(f'Wrote {content_length} bytes')


# Extracts embedded content inside the image
def decode(image):
    print("Extracting content...")

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

    content = b.tobytes()
    retrieve_file(content)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Provide a valid path to an image file")
        sys.exit(1)

    IMAGE = sys.argv[1]
    image = Image.open(IMAGE)
    decode(image)
