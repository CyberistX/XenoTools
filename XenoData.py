#!/usr/bin/env python

import struct
import os
import os.path
import io
from PIL import Image
from PIL import ImageFile

fntTileW=16
fntTileH=11

def lzssDecompress(f):
	decompLen = struct.unpack("@I", f.read(4))
	decompLen = decompLen[0]
	#print("Uncompressed file size: ",str(decompLen))
	byteBuffer = bytearray(decompLen)
	ptr = 0	
	
	while(ptr < decompLen):
		
		'''
		Stop on EOF in compressed file
		'''
		try:
			ctrlByte = struct.unpack("b",f.read(1))
			ctrlByte = ctrlByte[0]
		except:
			break
		
		for i in range(0, 8):
			bit = (ctrlByte & (1 << i))	
			if bit:
				ptr = lzssDecodeByte(struct.unpack("@H",f.read(2)),byteBuffer,ptr)
			else:
				k = f.read(1)
				'''
				Stop on EOF in compressed file
				'''
				try:
					byteBuffer[ptr] = k[0]
					ptr += 1
				except:
					ptr = decompLen +1
					break
	
	return byteBuffer
	

def lzssCompress(f):
	rBuffer = f.read()
	wBuffer = bytearray()
	wBuffer.extend(struct.pack("@i", len(rBuffer)))
	
	rPtr = 0
	
	while(rPtr < len(rBuffer)):
		
		chunk = bytearray()
		ctrlByte = bytearray()
		for i in range(0, 8):
			
			if rPtr + i >= len(rBuffer):
				ctrlByte.extend(bytearray( 8 - len(ctrlByte)))
				break
			
			s, o = lzssSearch(rBuffer, rPtr)
			
			if s >= 0:
				ctrlByte.append(1)
				encData = ((s & 0xF) << 12) ^ (o & 0xFFF)
				chunk.extend(struct.pack("@H",encData))
				rPtr += s +3
			else:
				ctrlByte.append(0)
				chunk.append(rBuffer[rPtr])
				rPtr += 1
		
		b = 0
		for i in range(0,8):
			b^= ctrlByte[i] << i
			
		wBuffer.append(b)
		wBuffer.extend(chunk)
	
	return wBuffer
	

def fontToBmp(f):
	f.seek(14)
	lst = fntSymbolList(f)
	ImageFile.LOAD_TRUNCATED_IMAGES = True
	imgList = []
	for i in range(0,len(lst)):
		b = io.BytesIO(fntGetBitmap(lst[i]))
		im = Image.open(b)
		im = im.convert(mode="1")	
		imgList.append(im)
	atlas = fntMakeAtlas(imgList,60, int(len(imgList)/60) +1)	
	atlas = atlas.convert(mode="L")
	temp = io.BytesIO()
	atlas.save(temp, format="bmp")
	temp.seek(0)
	return temp

def bmpToFont(f):
	header = bytearray([0x08, 0x07, 0x0E, 0x00, 0xF8, 0x00, 0xF0, 0x13, 0x3F, 0x00, 0x15, 0x00, 0x10, 0x00, 0x00, 0x00])
	
	symbolHeight = 11
	symbolWidth = 16
	
	im = Image.open(f)	
	width, height = im.size
	
	symPerRow = int((width -1)/symbolWidth +1)
	symPerCol = int((height -1)/symbolHeight +1)
		
	fnt = bytearray()
	
	for j in range(0, symPerCol):
		for i in range(0, symPerRow):
			box = (i*symbolWidth, j*symbolHeight, (i+1)*symbolWidth, (j+1)*symbolHeight)
			
			sym = im.crop(box)
			''' Ensures image is 8bpp bw '''
			sym = sym.convert(mode="L")
			byteArray = io.BytesIO()
			sym.save(byteArray, format="BMP")
			
			fnt.extend(fntPackSymbol(byteArray))	
			
	data = header
	data.extend(fnt)
	return io.BytesIO(data)
	
def xptGetFileList(f):
	listSize = f.read(4)
	listSize = struct.unpack("@I", listSize)[0]
	fileList = []
	for i in range(1, listSize + 1):
		f.seek(i*16)
		tmp = f.read(11)
		num,offs,size,fmt = struct.unpack("=HIIb", tmp)
		fileList.append({"number" : num, "offset" : offs, "size" : size, "format" : fmt })
	return fileList

def xptGetFile(f, fileList, fileNum):
	f.seek(fileList[fileNum]["offset"])
	data = f.read(fileList[fileNum]["size"])
	return io.BytesIO(data)

def archGetFileIndex(f):
	index = []
	f.seek(0x10C)
	sizes = struct.unpack("@iiiiiiii", f.read(32))
	f.seek(0x130)
	addr = struct.unpack("@iiiiiiii", f.read(32))
	for i in range(0,8):
		index.append({"size" : sizes[i], "offset" : addr[i]})
	eof = struct.unpack("@i", f.read(4))
	index.append({"size" : 0, "offset" : eof[0]})
	return index

def archGetFile(f, fileIndex, fileNum):
	entry = index[fileNum]
	f.seek(entry["offset"])
	dataSize = index[fileNum+1]["offset"] - entry["offset"]
	archFile= f.read(dataSize)
	archFile = io.BytesIO(archFile)
	return archFile
	
def archGetFileDecomp(f, fileIndex, fileNum):
	entry = fileIndex[fileNum]
	f.seek(entry["offset"])
	dataSize = fileIndex[fileNum+1]["offset"] - entry["offset"]
	archFile= f.read(dataSize)
	archFile = io.BytesIO(archFile)
	data = lzssDecompress(archFile)
	return io.BytesIO(data[:entry["size"]])
	
	
'''
	LZSS Helper Functions
'''

def lzssDecodeByte(h, byteBuffer,ptr):
	h = h[0]
	#offset is 3 lower nibbles
	offset = h & 0x0FFF
	#length is higher nibble + 3
	size = ((h & 0xF000) >> 12) +3
	#offset = ptr - ((ptr - offset) % 4096)	
	offset = ptr - (offset % 4078 )
	
	for i in range(offset, offset + size):
		#try:
		if offset < 0:
			byteBuffer[ptr] = 0
			ptr+=1
		else:
			byteBuffer[ptr] = byteBuffer[i]
			ptr += 1
	
	return ptr

def lzssSearch(rBuffer, rPtr):

	sBuffer = bytearray(18)
	if len(rBuffer[:rPtr -1]) < 4078:
		sBuffer.extend(rBuffer[:rPtr -1])
	else:
		sBuffer.extend(rBuffer[rPtr-4078:rPtr -1])
	
	i = 0
	s = 0
	bestSize = -1
	bestOffset = 0 
	while((i < len(sBuffer)) and (rPtr + s < len(rBuffer))):
		
		if (sBuffer[i] == rBuffer[rPtr + s]) and (s < 18):
			s+=1
		else:
			if (s >= 3) and (s > bestSize):
				bestSize = s 
				bestOffset = len(sBuffer) -i + s + 1
			s = 0
		
		i+=1
	
	if (s >= 3) and (s> bestSize):
		bestSize = s 
		bestOffset = len(sBuffer) -i + s + 1
		
	bestSize -=3
	return bestSize, bestOffset

'''
	Bmp/Font Converter Helper Functions
'''

def fntSymbolList(f):
	f.seek(14)
	l = []
	while(True):
		s = f.read(2*11)
		if len(s) < 22:
			break
		l.append(fntProcessSymbol(s))
	return l

def fntGetBitmap(data, fntTileHoriz = 1, tileVert = 1):
	dataSize = len(data)
	bmp = bytearray()
	
	bmp.extend(struct.pack('=c', bytes('B','ASCII')))
	bmp.extend(struct.pack('=c', bytes('M','ASCII')))
	bmp.extend(struct.pack('=i', dataSize + 0x3E))
	bmp.extend(struct.pack('=i', 0))
	bmp.extend(struct.pack('=i', 0x3E))	
	bmp.extend(struct.pack('=i', 0x28))	
	bmp.extend(struct.pack('=i', fntTileW*fntTileHoriz))
	bmp.extend(struct.pack('=i', -fntTileH*tileVert))	
	bmp.extend(struct.pack('=h', 1))
	bmp.extend(struct.pack('=h', 1))
	bmp.extend(struct.pack('=i', 0))
	bmp.extend(struct.pack('=i', dataSize + (dataSize%4)))
	bmp.extend(struct.pack('=i', 1))
	bmp.extend(struct.pack('=i', 1))
	bmp.extend(struct.pack('=i', 2))
	bmp.extend(struct.pack('=i', 0))
	bmp.extend(struct.pack('=I', 0xFFFFFF00))
	bmp.extend(data)
	return bmp

def fntMakeAtlas(imgList, cols, rows):
	atlas = Image.new("1",(cols*fntTileW, rows*fntTileH), 1 )
	i= 0
	j=0
	for img in imgList:
		box = (i*fntTileW, j*fntTileH, (i+1)*fntTileW, (j+1)*fntTileH)
		atlas.paste(img, box)
		i+=1
		if i >= cols:
			i=0
			j+=1
	return atlas

def fntProcessSymbol(sym):
	ret = bytearray(2*len(sym))
	for i in range(0,21,2):
		ret[2*i] = sym[i]
		ret[2*i + 1] = sym[i+1]
	
	return ret

def fntPackSymbol(byteArray):

	byteArray.seek(10)
	offset = struct.unpack("@i", byteArray.read(4))
	byteArray.seek(offset[0])
	sym = byteArray.read()
	byteStream = bytearray()
	for i in range(len(sym) -16, -1, -16 ):
		byteStream.extend(sym[i:i+16])
		
	packedSym = bytearray()
	for i in range(0, len(byteStream) , 8):
		byte = 0
		for j in range(0, 8):
			bit =  ~byteStream[i+j] & 0x01
			byte +=  bit << (7 - j )
		
		packedSym.append(byte)
			
	return packedSym

