#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lzss.py
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

from XenoHandler import *
import XenoData

def main(args):
	print()
	print("Xenogears lzss compressor/decompressor by .ghost")
	print()
	if (len(args) !=3) or ((args[0]!="-x") and args[0] != "-c") :
		print("Usage:")
		print()
		print("To decompress a file do:")
		print("\tlzss -x srcFile destFile")
		print()
		print("To compress a file do:")
		print("\tlzss -c srcFile destFile")
		return
	
	srcFile = args[1]
	dstFile = args[2]
	
	if args[0]=="-x":
		print("Opening file:", srcFile)
		f = open(srcFile, 'rb')
		print("Decompressing data")
		data = XenoData.lzssDecompress(f)
		print("Writing file:",dstFile)
		w = open(dstFile, 'wb')
		w.write(data)
		f.close()
		w.close()
		print("Done!")
	
	elif args[0]=="-c":
		print("Opening file:", srcFile)
		f = open(srcFile, 'rb')
		print("Compressing data")
		data = XenoData.lzssCompress(f)
		print("Writing file:",dstFile)
		w = open(dstFile, 'wb')
		w.write(data)
		f.close()
		w.close()
		print("Done!")
	
	return 0


if __name__ == '__main__':
	import sys
	sys.setrecursionlimit(5000)
	sys.exit(main(sys.argv[1:]))
