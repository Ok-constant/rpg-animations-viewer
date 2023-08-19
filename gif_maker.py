from lib.gif_maker import *
options = get_options()
t = options["type"]
if t == "frames":
	get_frames(options)
elif t == "folder_gifs":
	load_folder()
elif t == "folder_imgs":
	load_folder_imgs()
#get_frames(get_options())
#load_folder()
