#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  XenoHandler.py
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

import struct
import io

class XenoHandler:	
	
	'''
		Constructor
	'''
	
	def __init__(self, tFile):
		
		self.rawSectS = 2352
		self.isoSectS = 2048
		self.isoHedrS = 24
		self.crcS = 280
		self.realTocI = 24
		
		self.mFile = tFile
		self.mFile.seek(0, 2)
		self.mSize = self.mFile.tell()
		self.mFile.seek(0)
		self.mFileIndex = self.getHiddenToc()		
		
	
	'''
		Raw Data Access
	'''
	
		
	def getRawSec(self, tSecN):
		
		self.pFile.seek(tSecN*gRawSectS)
		tRet = self.pFile.read(gRawSectS)
		self.pFile.seek(0)
		return  tRet	
	
	
	def getIsoSec(self, tSecN):
		
		self.mFile.seek(tSecN*self.rawSectS + self.isoHedrS)
		tRet = self.mFile.read(self.isoSectS)		
		self.mFile.seek(0)
		return tRet
	
	
	'''
		Init Helper Functions
	'''
	
			
	def getHiddenToc(self):
		
		eot = bytearray([ 0xFF, 0xFF, 0xFF, 0,  0, 0, 0, 0])			
		i = self.realTocI
		toc = dict()
		data = bytearray()
		run = True
		buf = bytearray()
		folderCount = 0
		
		while(run):			
			data = self.getIsoSec(i)
			j = 0			
			nrun = True
			while(nrun):				
				if j > len(data):
					nrun = False
					break				
				#check for leftover bytes before end of sector
				if j >= len(data)-7:
					buf = bytearray()
					for k in range(j,len(data)):
						buf.append(data[k])
						nrun = False
					break				
				#check from leftover bytes from previous sector
				if len(buf) > 0:
					buf.extend(bytearray(data))
					data=buf					
					buf = bytearray()
					
				#default case, read the 7 byte entry
				byteSeq = bytearray([ data[j],data[j+1],data[j+2], 0,data[j+3],data[j+4],data[j+5],data[j+6]])				
				#break loop on find end of table
				if byteSeq == eot:
					run = False
					break;				
				
				entry = dict()
				offset, size = struct.unpack("<Ii",byteSeq)
				entry["offset"] = offset
				entry["size"] = size
				if size < 0:
					entry["label"] = "FOLDER"
					entry["folderNum"] = folderCount
					folderCount += 1
				else:
					entry["label"] = "FILE"
				entry["fileNum"] = len(toc)
				toc[entry["fileNum"]] = entry
				
				j +=7
			i+=1
		return toc
	
	
	'''
		File Utilities
	'''
	
	
	def getFile(self, fileNum):
		startSector = self.mFileIndex[fileNum]["offset"]
		endSector = startSector + int( (self.mFileIndex[fileNum]["size"] -1) / 2048 + 1)
		data = bytearray()
		for i in range(startSector, endSector):
			data.extend(self.getIsoSec(i))
		data = data[:self.mFileIndex[fileNum]["size"]]
		data = io.BytesIO(data)
		data.seek(0)
		
		return data
	
	def isFolder(self, fileNum):
		return self.mFileIndex[fileNum]["label"] == "FOLDER"
	
	def isFile(self, fileNum):
		return self.mFileIndex[fileNum]["label"] == "FILE"

		
	
	
		
