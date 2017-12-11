#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  extract_patch.py
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

import XenoData
import os
import os.path

def main(args):
	print()
	print("Xenogears .xpt patch extractor by .ghost")
	print()
	if (len(args) !=2):
		print("Usage:")
		print()
		print("To extract patch files into a folder:")
		print("\textract_patch /path/to/patch.xpt /dest/folder")
		print()
		return
	
	srcFile = args[0]
	dstFolder = args[1]
	
	print("Opening patch file.")
	f = open(srcFile, "rb")
	print("Parsing file index.")
	fileList = XenoData.xptGetFileList(f)
	
	tmpPath = dstFolder
	
	for i in range(0, len(fileList)):
		tmpPath = dstFolder + "/" + str(fileList[i]["format"])
		if not os.path.exists(tmpPath):
			os.makedirs(tmpPath)
		data = XenoData.xptGetFile(f, fileList, i)
		w = open(tmpPath + "/" + str(fileList[i]["number"]), "wb")
		w.write(data.read())
		w.close()
	print("Done!")
			

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv[1:]))
