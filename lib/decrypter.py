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

def isInt(s):
	try:
		int(s)
		return True
	except:
		return False

def get_options():
	global options
	with open(sys.argv[1], "r") as f:
		options = json.loads(f.read())
	return options

def get_frame(path, ext):
	global text
	with open(path, "rb") as f:
		text = f.read()
	rpgFile = RPGFile()
	if ext == "rpgmvp":
		d = Decrypter(bytes(text))
		d.restoreHeader(rpgFile)
	else:
		rpgFile.content = text
	return rpgFile

def get_frames(options):
	frames = []
	#options = get_options()
	print(options)
	rng = options["range"].split('-')
	s = int(rng[0])
	e = int(rng[1])
	for i in range(s,e+1):
		t = options["templ"]
		if i >= 10:
			t = t[0:-2]
		frames.append(get_frame(f"{options['path']}{t}{i}.{options['ext']}", options["ext"]))
		#show(frames[i].content)
	#print(frames)
	gif = [Image.open(io.BytesIO(f.content)) for f in frames]
	gif[0].save(
		f"{options['out_path']}{options['out']}.gif",
		save_all = True,
		append_images=gif[1:],
		duration = 100,
		loop = 0
	)

def load_and_save_img(path, ext, out, out_path):
	#print("starting")
	frame = get_frame(path, ext).content
	img = Image.open(io.BytesIO(frame))
	i = [img]
	i[0].save(
		f"{out_path}{out}.gif",
		save_all = True,
		append_images=i[0:],
		duration=100,
		loop= 0
	)
	print("saved " + out)

def sort(l):
	#print(l)
	toInt = [int(i) for i in l]
	toInt.sort()
	#print(toInt)
	new = []
	for i in toInt:
		if i >= 10:
			new.append(str(i))
		else:
			new.append("0"+str(i))
	return new


MAX_THREADS = 5
def load_folder():
	options = get_options()
	files = {}
	for file in os.scandir(options["path"]):
		t = file.name
		t = t.replace(f".{options['ext']}", "")
		split = t.split('_')
		if len(split) != 3:
			continue
		name = split[1][0:-2]
		animNum = split[1][-2:]
		if not isInt(animNum):
			continue
		if isInt(split[1]):
			continue
		ind = f"{split[0]}_{name}"
		if not ind in files:
			files[ind] = {}
		if not animNum in files[ind]:
			files[ind][animNum] = []
		files[ind][animNum].append(split[2])
		#print(name, animNum)
	with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
		futures = []
		for file in files:
			#print(file)
			for anim in files[file]:
				if anim == "num":
					continue
				#print(anim)
				#print(files[file])
				s = sort(files[file][anim])
				#print(s)
				o = {
					"path":options["path"],
					"ext": options["ext"],
					"out": f"{file}{anim}",
					"out_path": options["out_path"],
					"templ": f"{file}{anim}_0",
					"range": f"{s[0]}-{s[-1]}"
				}
				futures.append(executor.submit(get_frames, o))
				#t = threading.Thread(target=get_frames, args=(o,))
				#t.start()
		concurrent.futures.wait(futures)
	print("Done!")

def load_folder_imgs():
	options = get_options()
	with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
		futures = []
		for f in os.scandir(options["path"]):
			print(f.name)
			futures.append(executor.submit(load_and_save_img, options["path"]+f.name, options["ext"], f.name, options['out_path']))
		concurrent.futures.wait(futures)
	print("done!")

#d = Decrypter(bytes(text))
#rpgFile = RPGFile()
#d.restoreHeader(rpgFile)
#a = np.frombuffer(rpgFile.content, dtype=np.uint8)
#with open ("test.png", "wb") as f:
#	f.write(rpgFile.content)

#get_frames()

def show(c):
	arr = np.asarray(c, dtype=np.uint8)
	img = cv2.imdecode(arr,-1)
	cv2.imshow("image", img)
	cv2.waitKey(0)
	#cv2.destroyAllWindows()

#show()
#get_frames(get_options())
#load_folder()
load_folder_imgs()
