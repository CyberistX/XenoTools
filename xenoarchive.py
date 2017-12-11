#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  xenoarchive.py
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
import struct
import os
import os.path
from io import BytesIO

def main(args):
	print()
	print("Xenogears field archive unpacker/packer by .ghost")
	print()
	if (len(args) !=3) or ((args[0]!="-x") and args[0] != "-c") :
		print("Usage:")
		print()
		print("To unpack an arcive do:")
		print("\txenoarchive -x srcFile destFolder")
		print()
		print("To create an archive do:")
		print("\txenoarchive -c srcFile destFolder")
		return
	
	srcFile = args[1]
	dstPath = args[2]
	
	if args[0]=="-x":
		print("Opening file:", srcFile)
		f = open(srcFile, 'rb')
		print("Decoding archive.")
		fileIndex = XenoData.archGetFileIndex(f)
		if not os.path.exists(dstPath):
			os.makedirs(dstPath)
		for i in range(0,8):
			dstFile = dstPath + "/" + str(i)
			print("Writing file:", i)
			data = XenoData.archGetFileDecomp(f, fileIndex, i)
			w = open(dstFile, 'wb')
			w.write(data.read())
			w.close()
		print("Done!")
		f.close()
	
	elif args[0]=="-c":
		print("Function not implemented!")
	
	return 0


if __name__ == '__main__':
	import sys
	sys.setrecursionlimit(5000)
	sys.exit(main(sys.argv[1:]))
