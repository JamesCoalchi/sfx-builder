import os
import sys
import base64
import subprocess
import PyInstaller.__main__
import packer

filesToPack = []

def get_files():
	files = []
	while 1:
		file = input("Input file path (Blank if finished): \n>>> ").strip('"')
		if file:
			if os.path.isfile(file):
				print("Added file: " + file)
				files.append(file)
			else:
				print("Provided file path (" + file + ") is not valid. Provide a different file path.")
				continue
		elif len(files) != 0:
			print("Files: " + str(files))
			return files
		else:
			print("Please provided at least 1 file.")

def main():
	filesToPack = get_files()
	output_name = str(input("Input output name. (Not including file extensions):\n>>> ")).split('.')[0]
	run_after_unpack = [name.strip() for name in str(input("Input file names to run after unpacking (separated by commas, including extensions):\n>>> ")).split(",")]
	print(run_after_unpack)
	packer.pack(filesToPack, run_after_unpack, output_name)

if __name__ == '__main__':
	main()
