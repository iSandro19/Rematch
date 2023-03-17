import pygame as pg
from pygame.locals import *
from typing import List, Dict, Tuple, Union, Callable
import obj
import sys
import tileditor
import game.image

FPS = 10

def main(argc, argv):
	if argc < 5:
		print("Usage: tileditor ROOM_W ROOM_H SPRITE_SHEET_HASH OUT_FILE [IN_FILE]")
		return

	room_w 		= int(argv[1])
	room_h 		= int(argv[2])
	sprtShtHash = int(argv[3])
	outFile		= argv[4]
	inFile		= None if argc == 5 else argv[5]

	pg.display.init()
	ss = obj.load('SpriteSheet', sprtShtHash, 0)

	wind = pg.display.set_mode((room_w*ss.clip.w, room_h*ss.clip.h), flags=SCALED|RESIZABLE, vsync=True)

	te = tileditor.TileEditor(0, sprtShtHash, room_w, room_h, outFile, inFile)

	clock = pg.time.Clock()

	assert pg.image.get_extended()

	while True:
		wind.fill((128, 128, 128))

		obj.update()

		obj.draw()

		pg.display.flip()
		clock.tick(FPS)
	
	pg.display.quit()
	te.close()

	return 0

main(len(sys.argv), sys.argv)
