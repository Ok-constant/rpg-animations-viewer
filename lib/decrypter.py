import cv2, sys, json, io, os
import concurrent.futures
from PIL import Image
from ast import literal_eval
from operator import xor
import numpy as np

filename = sys.argv[1]#input("file: ")

class RPGFile:
	def __init__(self):
		self.content = ""

	def createBlobUrl(self, i):
		pass

class Decrypter:
	def __init__(self, buffer):
		self.buffer = buffer
		self.headerLen = 16
		self.defaultHeaderLen = 16
		self.defaultSignature = "5250474d56000000"
		self.defaultVersion = "000301"
		self.defaultRemain = "0000000000"
		self.pngHeaderBytes = "89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52"
		self.encryptionCodeArray = []

	def restoreHeader(self, rpgFile):
		self.modifyFile(rpgFile, "restore")

	def decrypt(self, buf):
		newBuf = buf[self.headerLen:]
		return self.xOrBytes(newBuf)

	def getNormalPNGHeader(self, hLen):
		hToRestore = self.pngHeaderBytes.split(' ')
		if hLen > len(hToRestore):
			hLen = len(hToRestore)

		r = bytearray(hLen)
		for i in range(hLen):
			try:
				r[i] = literal_eval('0x' + hToRestore[i])
			except Exception as e:
				r[i] = 16

		return r

	def restorePngHeader(self, buf):
		pngStartHeader = self.getNormalPNGHeader(self.headerLen)
		b = buf[self.headerLen*2:]
		#newB = bytearray(len(buf)+self.headerLen)
		newB = pngStartHeader + b
		return newB

	def modifyFile(self, rpgFile, modType):
		if modType == "decrypt":
			rpgFile.content = self.decrypt(self.buffer)
			#rpgFile.createBlobUrl(true)
		elif modType == "restore":
			rpgFile.content = self.restorePngHeader(self.buffer)

	def tryOr(self, i, o):
		try:
			return int(i)
		except:
			return o

	def xOrBytes(self, buf):
		b = bytearray(buf)
		for i in range(self.headerLen):
			#b[i] = xor(b[i], 16)
			pass
		print(b[0:self.headerLen])
		return b
