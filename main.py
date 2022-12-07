from PIL import Image
import math
import argparse
import time

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def main(args):

    # arguments
    inFile = args.source_file.name
    outTxt = args.dest_file.name
    scale = args.scale
    a_width = args.width
    a_height = args.height
    a_scale_width = args.scale_width
    a_scale_height = args.scale_height
    verbose = args.verbose

    # timer start (verbose)
    start_time = time.time()
    
    try:
        im = Image.open(inFile)
    except:
        print("An exception occured while opening the file")
        exit(1)

    # verbose
    if verbose:
        print(f"Opening '{inFile}' ({im.format}, {im.mode})")

    o_width, o_height = im.size

    x_scale = a_width / o_width if a_width else a_scale_width if a_scale_width else scale
    y_scale = a_height / o_height if a_height else a_scale_height if a_scale_height else scale

    im = im.resize((int(o_width * x_scale), int(o_height * y_scale)), Image.Resampling.NEAREST)
    width, height = im.size

    # verbose
    if verbose:
        if scale == 1:
            print(f"{width}x{height} ({width*height} px)")
        else:
            print(f"{o_width}x{o_height} ({o_width*o_height} px) => {width}x{height} ({width*height} px)")

    txt = open(outTxt, "w")
    
    if im.mode not in ["RGB", "RGBA"]:
        im = im.convert(mode="RGBA")

    pixs = im.load()
    for y in range(height):
        for x in range(width):
            
            cols = pixs[x, y]
            r, g, b, *a = cols
            a = a[0] if a else 255
            d = int(r/3 + g/3 + b/3)

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

    if verbose:
        current_time = time.time()
        time_diff = current_time - start_time
        print(f"\33[2K\rOperation complete! ({time_diff:.2f}s)")

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
parser.add_argument('-sw', '--scale-width', type=float, help='Factor at which to scale the width of the output image', required=False)
parser.add_argument('-sh', '--scale-height', type=float, help='Factor at which to scale the height of the output image', required=False)
parser.add_argument('-w', '--width', type=int, help='Set a specific output width (px)', required=False)
parser.add_argument('--height', type=int, help='Set a specific output height (px)', required=False)
parser.add_argument('-v', '--verbose', action=argparse.BooleanOptionalAction, help='Displays useful information about the conversion process')
parser.add_argument('dest_file', type=argparse.FileType('w'), help='Destination text file')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
