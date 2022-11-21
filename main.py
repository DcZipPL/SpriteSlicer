import random
import sys
import time

from PIL import Image
import numpy
import io

debug: bool = False
ignore: bool = False
verbose: bool = False
sleep: bool = False
pre_def_mapping_loc: str = ""
pre_def_output_loc: str = ""

from colorama import Fore
from colorama import Style


def print_debug():
	print(f"   [{Fore.LIGHTBLACK_EX}Debug{Style.RESET_ALL}]", end=" ")


def print_ok():
	print(f"      [{Fore.GREEN}OK{Style.RESET_ALL}]", end=" ")


def print_info():
	print(f"    [{Fore.BLUE}Info{Style.RESET_ALL}]", end=" ")


def print_ignore():
	print(f"[{Fore.YELLOW}Ignoring{Style.RESET_ALL}]", end=" ")


def slice_spritesheet(input_spritesheet: str, size: int):
	print_info()
	print(f"Spritesheet Slicer")
	spritesheet = Image.open(input_spritesheet, "r")
	img_size: (int, int) = spritesheet.size

	slices: Image = []

	for y in range(0, numpy.floor(img_size[0] / size).astype(int)):
		for x in range(0, numpy.floor(img_size[1] / size).astype(int)):
			if verbose:
				print((x * size, y * size, x * size + size, y * size + size))

			slice: Image = spritesheet.copy().crop((x * size, y * size, x * size + size, y * size + size))

			slices.append(slice)

	spritesheet.close()

	# Mappings
	mappings_file_input: str
	if pre_def_mapping_loc != "":
		print_info()
		print(f"Mappings: {pre_def_mapping_loc}")
		mappings_file_input = pre_def_mapping_loc
	else:
		print_info()
		print(f"Mappings file if any:")
		mappings_file_input = input()

	mappings_file = open(mappings_file_input, "r")
	mappings: list[str] = mappings_file.read().split("\n")
	mappings_file.close()

	# Output Directory
	if pre_def_output_loc != "":
		print_info()
		print(f"Output: {pre_def_output_loc}")
		output_dir: str = pre_def_output_loc
	else:
		print_info()
		print(f"Enter output directory:")
		output_dir: str = input()

	# Slicer
	i: int = 0
	for _slice in slices:
		fname: str
		if len(mappings) > 0 and i < len(mappings) and mappings[i] != "":
			fname = mappings[i]
		else:
			if ignore:
				return
			print_info()
			print(f"No mapping found! Enter name:", end="\n         > ")
			fname: str = input()

		if debug and sleep:
			print("--- Press to continue ---")
			mappings[i] = f"i{i}_{fname}"
			input()

		if sleep and not debug:
			time.sleep(random.randint(1, 2000) / 10000)

		empty_pixels: int = 0
		for pixelx in range(16):
			for pixely in range(16):
				pixel = _slice.getpixel((pixelx, pixely))
				if verbose:
					print(pixel)
				if pixel[3] == 0:
					empty_pixels += 1

		if empty_pixels < 16 * 16:
			_slice.save(f"{output_dir}/{fname}.png")
			print_ok()
		else:
			print_ignore()

		print(f"Slice {i}/{len(slices)}: {fname}")

		if debug:
			print_debug()
			print(f"Empty pixels: {empty_pixels}/{16 * 16}.")

		i += 1


if __name__ == "__main__":
	input_img: str = ""

	for arg in sys.argv:
		if arg == "-d":
			debug = True
		if arg == "-i":
			ignore = True
		if arg == "-v":
			verbose = True
		if arg == "-s":
			sleep = True
		if arg == "-h":
			print("------\n"
				  "Arguments:\n"
				  " -d | Debug\n"
				  " -i | Ignore out of mapping slices\n"
				  " -v | Verbose\n"
				  " -s | Sleep for 0.05 every slice"
				  " -h | Help (Every other argument will be ignored)\n"
				  " mappings=PATH | Path to mappings file\n"
				  " output=PATH   | Path to output directory\n"
				  " input=PATH    | Path to input file\n"
				  "------")
			exit(0)
		if "mappings=" in arg:
			pre_def_mapping_loc = arg.replace("mappings=", "")
		if "output=" in arg:
			pre_def_output_loc = arg.replace("output=", "")
		if "input=" in arg:
			input_img = arg.replace("input=", "")
			print_info()
			print(f"Input image: {input_img}")

	if input_img == "":
		print_info()
		print(f"Enter input image:")
		input_img = input()
	slice_spritesheet(input_img, 16)
