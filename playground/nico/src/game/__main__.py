import pygame as pg
from pygame.locals import *
from typing import List, Dict, Tuple, Union, Callable
import obj
import game.tile
import game.cam
import game.player


WIND_SIZE = 128, 72
FPS = 60




def main():
	pg.display.init()
	pg.display.set_mode(WIND_SIZE, flags=SCALED|RESIZABLE, vsync=True)

	notExit = True
	clock = pg.time.Clock()
	wind = pg.display.get_surface()
	rect = pg.Rect(0,0,128,72)

	assert pg.image.get_extended()

	obj.load('Cam', 0, 0)
	obj.load('TileMap', 0, 0)
	game.player.Test(0)

	while notExit:
		for event in pg.event.get():
			notExit = event.type != pg.QUIT


		wind.fill((128, 128, 128))

		obj.update()

		obj.draw()

		pg.display.flip()
		clock.tick(FPS)
	

	obj.close()
	pg.display.quit()

	return 0


if __name__ == '__main__':
	main()
