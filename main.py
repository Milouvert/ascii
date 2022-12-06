from PIL import Image
import math
import argparse
import time

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
charsList = list(chars)

inFile = "Image.png"
outTxt = "Output.txt"
scale = 1 
verbose = False

def main(args):

    inFile = args.source_file.name
    outTxt = args.dest_file.name
    scale = args.scale
    verbose = args.verbose

    start_time = time.time()

    im = Image.open(inFile)
    o_width, o_height = im.size
    im = im.resize((int(o_width * scale), int(o_height * scale)), Image.Resampling.NEAREST)
    width, height = im.size

    # verbose
    if verbose:
        print(f"Opening '{inFile}' ({im.format}, {im.mode})")
        if scale == 1:
            print(f"{width}x{height} ({width*height} px)")
        else:
            print(f"{o_width}x{o_height} ({o_width*o_height} px) => {width}x{height} ({width*height} px)")

    txt = open(outTxt, "w")

    pixs = im.load()
    for y in range(height):
        for x in range(width):
            cols = pixs[x, y]
            r, g, b, *a = cols
            a = a[0] if a else 255
            d = int(r/3 + g/3 + b/3)

            pixs[x, y] = (d, d, d, a)

            if a == 0:
                d = 255

            txt.write(getChar(d))

            if verbose:
                current = x + width * y + 1
                total = width*height
                percent = current / total * 100
                loading_char = getLoadingChar(percent)
                current_time = time.time()
                time_diff = current_time - start_time
                print(f"\rProgress: {current}/{total} {loading_char} {percent:.2f}% ({time_diff:.2f}s)", end="")

        txt.write("\n")

def getLoadingChar(n):
    n = int(n)
    if n % 4 == 0:
        return '|'
    if n % 4 == 1:
        return '/'
    if n % 4 == 2:
        return '-'
    if n % 4 == 3:
        return '\\'
    
def getChar(d):
    return chars[math.floor(d / 256 * len(chars))]

parser = argparse.ArgumentParser(
        prog = 'ASCII Art',
        description = 'Turns an image into an ASCII art text file')

parser.add_argument('source_file', type=open, help='Source image file')
parser.add_argument('-s', '--scale', type=float, help='Factor at which to scale the output image', default=1)
parser.add_argument('-v', '--verbose', action=argparse.BooleanOptionalAction, help='Displays useful information about the conversion process')
parser.add_argument('dest_file', type=argparse.FileType('w'), help='Destination text file')


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
