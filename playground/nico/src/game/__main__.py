import pygame as pg
from pygame.locals import *
from typing import List, Dict, Tuple, Union, Callable
import obj
import obj.draw


WIND_SIZE:Tuple[int, int] = 128, 128
FPS:int = 60




def main() -> int:
	pg.display.init()
	pg.display.set_mode(WIND_SIZE, flags=SCALED|RESIZABLE, vsync=True)

	notExit:bool = True
	clock:pg.time.Clock = pg.time.Clock()
	wind:pg.Surface = pg.display.get_surface()

	assert pg.image.get_extended()


	while notExit:
		for event in pg.event.get():
			notExit = event.type != pg.QUIT


		wind.fill((128, 128, 128))

		pg.display.flip()
		clock.tick(FPS)
	

	pg.display.quit()

	return 0


if __name__ == '__main__':
	main()
