from utils import *
from PIL import Image
import io, os
import concurrent.futures

def get_frames(options):
	frames = []
	rng = options["range"].split('-')
	s = int(rng[0])
	e = int(rng[1])
	for i in range(s,e+1):
		t = options["templ"]
		if i >= 10:
			t = t[0:-2]
		frames.append(get_frame(f"{options['path']}{t}{i}.{options['ext']}", options["ext"]))
	
	gif = [Image.open(io.BytesIO(f.content)) for f in frames]
	gif[0].save(
		f"{options['out_path']}{options['out']}.gif",
		save_all = True,
		append_images=gif[1:],
		duration = 100,
		loop = 0
	)
	print(f"saved {options['out']}.gif")

def load_and_save_img(path, ext, out, out_path):
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
	print(f"saved {out}.gif")


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
		
	with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
		futures = []
		for file in files:
			for anim in files[file]:
				if anim == "num":
					continue
				
				s = sort(files[file][anim])
				
				o = {
					"path":options["path"],
					"ext": options["ext"],
					"out": f"{file}{anim}",
					"out_path": options["out_path"],
					"templ": f"{file}{anim}_0",
					"range": f"{s[0]}-{s[-1]}"
				}
				futures.append(executor.submit(get_frames, o))
				
		concurrent.futures.wait(futures)
	print("Done!")

def load_folder_imgs():
	options = get_options()
	with concurrent.futures.ThreadPoolExecutor(MAX_THREADS) as executor:
		futures = []
		for f in os.scandir(options["path"]):
			futures.append(executor.submit(load_and_save_img, options["path"]+f.name, options["ext"], f.name, options['out_path']))
		concurrent.futures.wait(futures)
	print("done!")