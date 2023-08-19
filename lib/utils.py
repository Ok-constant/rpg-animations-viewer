import sys, json
from file import RPGFile
from decrypter import Decrypter

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