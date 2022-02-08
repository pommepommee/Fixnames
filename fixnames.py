#!/usr/bin/env python3
import os
import sys
import argparse
import glob
import time
import shutil

parser = argparse.ArgumentParser(description="Fix the first number of a YOLO annotation file according to ancient / new names. For example: if 0 is 'gun' in new names, and 0 is 'handgun' in old, nothing change. But, if 0 is 'gun' in new names and 'gun' is 5 in the old names, 5 -> 0 in all text YOLO annotations files.",usage='use "%(prog)s --old-names path/to/old_classes.txt --new-names path/to/new_classes.txt --input path/to/folder/train/"', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-o", "--old", help="File with 'old' names", type=str, required=True)
parser.add_argument("-n","--new", help="File with 'new' names", type=str, required=True)
parser.add_argument("-i", "--input", help="Path to text files to fix", type=str, required=True)
parser.add_argument("-O", "--Output", help="Fixed txt files", type=str, required=True)
args = parser.parse_args()

old_names = []
new_names = []
d_old = {}
d_new = {}
changes = {}

if 'nt' in os.name:
	sep = '\\'
else:
	print("UNIX")
	sep = '/'
	
def fix(file):
	global old_names, new_names, sep

	with open(file, 'r') as f:
		lines = f.readlines()
		filename = file.split(sep)[-1]
		output = args.Output + sep + filename
		#print(filename)
		with open(output, "w+") as o:
			for line in lines:
				splitted = line.split()
				splitted[0] = changes[int(splitted[0])]
				line = ' '.join(splitted)
				o.write(line + "\n")


def log_infos():
	print("Old names found : ")
	print(old_names)
	print("New names found : ")
	print(new_names)
	print("Old: ")
	print(d_old)
	print("New: ")
	print(d_new)


def main():
	global old_names, new_names
	if not os.path.isfile(args.old):
		print("Argument -o not a file or does not exist.")
		sys.exit(2)
	if not os.path.isfile(args.new):
		print("Argument -n not a file or does not exist.")
		sys.exit(2)
	if not os.path.isdir(args.input):
		print("Argument -i not a folder or does not exist.")
		sys.exit(2)
	
	with open(args.old,'r') as o:
		for line in o.readlines():
			old_names.append(line.strip('\n'))
	with open(args.new,'r') as n:
		for line in n.readlines():
			new_names.append(line.strip('\n'))
	
	cpt = 0
	for el in old_names:
		d_old[el] = cpt
		cpt += 1
	cpt = 0
	for el in new_names:
		d_new[el] = cpt
		cpt += 1

	st = [f"[{d_new[label]}]{label}" for label in d_new]
	st = ' '.join(st)

	for el in d_old:
		ans = -1
		while ans == '' or not int(ans) in list(d_new.values()):
			ask = f"Change \'{el}\' to which ID ?"
			ans = input(f"{ask}\n{st} : ")
		changes[d_old[el]] = ans

	for file in glob.glob(args.input+"/*.txt"):
		if "classes.txt" in file:
			continue
		fix(file)

if __name__ == '__main__':
	main()
