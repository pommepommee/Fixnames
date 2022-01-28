#!/usr/bin/env python3
import os
import sys
import argparse
import logging
import glob
import time
import shutil
from termcolor import colored
from lxml import etree

logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)
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

	
def fix(file):
	global old_names, new_names
	
	
	#logger.info("Fixing file: "+file)
	with open(file, 'r') as f:
		lines = f.readlines()
		filename = file.split('/')[-1]
		output = args.Output+'/'+filename
		with open(output, "w+") as o:
			for line in lines:
				splitted = line.split(" ")
				#print(splitted)
				if (
					splitted[0] == str(d_old["Grinder"]) or 
					splitted[0] == str(d_old["Screwdriver"]) or 
					splitted[0] == str(d_old["Wrench"]) or 
					splitted[0] == str(d_old["Grinder"]) or 
					splitted[0] == str(d_old["Drill (Tool)"]) or 
					splitted[0] == str(d_old["Bow and arrow"]) or 
					splitted[0] == str(d_old["Ratchet (Device)"])
				):
					print(splitted[0] +" changed to "+str(d_new["other"]))
					splitted[0] = str(d_new["other"])
					line = " ".join(splitted)
					
				elif splitted[0] == str(d_old["Hammer"]):
					print(splitted[0] +" changed to "+str(d_new["axe"]))
					splitted[0] = str(d_new["axe"])
					line = " ".join(splitted)
					
				elif splitted[0] == str(d_old["Kitchen knife"]):
					print(splitted[0] +" changed to "+str(d_new["knife"]))
					splitted[0] = str(d_new["knife"])
					line = " ".join(splitted)
					
				elif splitted[0] == str(d_old["Shotgun"]):
					print(splitted[0] +" changed to "+str(d_new["rifle"]))
					splitted[0] = str(d_new["rifle"])
					line = " ".join(splitted)
				else:
					print("Not changed")
				o.write(line)

def main():
	global old_names, new_names
	if not os.path.isfile(args.old):
		logger.error("Argument -o not a file or does not exist.")
		sys.exit(2)
	if not os.path.isfile(args.new):
		logger.error("Argument -n not a file or does not exist.")
		sys.exit(2)
	if not os.path.isdir(args.input):
		logger.error("Argument -i not a folder or does not exist.")
		sys.exit(2)
	
	with open(args.old,'r') as o:
		lines = o.readlines()
		for line in lines:
			old_names.append(line.strip('\n'))
	with open(args.new,'r') as n:
		lines = n.readlines()
		for line in lines:
			new_names.append(line.strip('\n'))
			
	logger.info("Old names foud : ")
	logger.info(old_names)
	logger.info("New names foud : ")
	logger.info(new_names)
	
	cpt = 0
	for el in old_names:
		d_old[el] = cpt
		cpt += 1
	cpt = 0
	for el in new_names:
		d_new[el] = cpt
		cpt += 1
	print(d_old)
	print(d_new)
	
	for file in glob.glob(args.input+"/*.txt"):
		fix(file)

if __name__ == '__main__':
	main()

