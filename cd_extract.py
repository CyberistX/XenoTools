#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cd_extract.py
#
#  Copyright (c) 2017 Andrea Uccheddu (.ghost)
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
#  (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, 
#  publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
#  so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
#  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
#
#

from XenoHandler import XenoHandler
import XenoData
import os
import os.path

def main(args):
	print()
	print("Xenogears CD extractor by .ghost")
	print()
	if (len(args) !=2):
		print("Usage:")
		print()
		print("To extract Xenogears CD image into a folder:")
		print("\tcd_extract /path/to/cd.bin /dest/folder")
		print()
		return
	
	srcFile = args[0]
	dstFolder = args[1]
	
	print("Opening disc image.")
	f = open(srcFile, "rb")
	print("Parsing file index.")
	cdHandler = XenoHandler(f)
	
	tmpPath = dstFolder
	
	for entry in cdHandler.mFileIndex.keys():
		if cdHandler.isFolder(entry):
			print("Creating folder: ", dstFolder + "/" + str(cdHandler.mFileIndex[entry]["folderNum"]))
			tmpPath = dstFolder + "/" + str(cdHandler.mFileIndex[entry]["folderNum"])
			if not os.path.exists(tmpPath):
				os.makedirs(tmpPath)
		else:
			print("Extracting file: ", tmpPath + "/" + str(entry))
			w = open(tmpPath + "/" + str(entry), "wb")
			data = cdHandler.getFile(entry)
			w.write(data.read())
			w.close()
	print("Done!")
			

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv[1:]))
