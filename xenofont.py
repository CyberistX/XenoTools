#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  xenofont.py
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

def main(args):
	print()
	print("Xenogears font encoder/decoder by .ghost")
	print()
	if (len(args) !=3) or ((args[0]!="-d") and args[0] != "-e") :
		print("Usage:")
		print()
		print("To decode a font do:")
		print("\txenofont -d fntFile bmpFile")
		print()
		print("To encode a font do:")
		print("\txenofont -e bmpFile fntFile")
		return
	
	srcFile = args[1]
	dstFile = args[2]
	
	if args[0]=="-d":
		print("Opening file:", srcFile)
		f = open(srcFile, 'rb')
		print("Decoding font")
		data = XenoData.fontToBmp(f)
		print("Writing file:",dstFile)
		w = open(dstFile, 'wb')
		w.write(data.read())
		f.close()
		w.close()
		print("Done!")
	
	elif args[0]=="-e":
		print("Opening file:", srcFile)
		f = open(srcFile, 'rb')
		print("Encoding font")
		data = XenoData.bmpToFont(f)
		print("Writing file:",dstFile)
		w = open(dstFile, 'wb')
		w.write(data.read())
		f.close()
		w.close()
		print("Done!")
	
	return 0


if __name__ == '__main__':
	import sys
	sys.setrecursionlimit(5000)
	sys.exit(main(sys.argv[1:]))

