from tkinter import *
from PIL import Image
import os, sys
root = Tk()

params = ''.join(sys.argv[1:])
pair = params.split('=')
global files
if pair[0] == "folder":
	p = pair[1].split('/')
	rng = None
	if p[-1] != "":
		r = p[-1].split('-')
		if len(r) == 1:
			rng = int(r[0])
		else:
			rng = (int(r[0]), int(r[1]))

	folder = ''.join(p[0:-1])+"/"
	#print(folder)
	if rng is None:
		files = [f"{folder}{f.name}" for f in os.scandir(folder)]
	else:
		f = os.scandir(folder)
		
		files = []
		global b
		if type(rng) == tuple:
			b = rng
		else:
			b = (0, rng)
		#print(b)
		for x, file in enumerate(f):
			if x < b[0]:
				continue
			files.append(f"{folder}{file.name}")
			if x == (b[1]-1):
				break
elif pair[0] == "files":
	files = pair[1].split(',')
else:
	print("choose an option (folder or files)")
	exit(0)
	
gifs = []
for f in files:
	frameCnt = Image.open(f).n_frames
	#print(f)
	frames = [PhotoImage(file=f, format="gif -index " +str(i)) for i in range(frameCnt)]
	gifs.append({
		"count":frameCnt,
		"frames": frames,
		"name":f
	})

img = 0
ind = 0

def press(key):
	global img, ind
	name = key.keysym
	if name == "Right":
		img += 1
	elif name == "Left":
		img -= 1
	if img < 0:
		img = len(gifs)-1
	elif img >= len(gifs):
		img = 0
	ind = 0
	root.title(f"{gifs[img]['name']} - {img+1}/{len(gifs)}")
	#print(img, gifs)

root.title(f"{gifs[img]['name']} - {img+1}/{len(gifs)}")

def update(*args):
	global ind
	frames = gifs[img]
	if len(frames["frames"]) <= ind:
		ind = 0
	frame = frames["frames"][ind]
	ind += 1
	if ind >= frames["count"]:
		ind = 0
	label.configure(image=frame)
	root.after(100, update, ind)
label = Label(root)
label.pack()
root.bind("<KeyPress>", press)
root.after(0, update)
root.mainloop()
