import pygame as pg
from pygame.locals import *
from typing import List, Dict, Tuple, Union, Callable
from objstate import *


WIND_SIZE:Tuple[int, int] = 128, 128
FPS:int = 60


class Test(ObjState, pg.sprite.Sprite):
	containers:pg.sprite.Group = None
	screen:pg.Rect = None
	speed:int = None

	_nReflex = 0
	_MAX_N_REFLEX = 5

	#Actions
	def __init__(self, containers:pg.sprite.Group, speed:int, screen:pg.Rect)->None:
		self.next(Test.__init__)
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.image = pg.image.load("game/PerfilP.png")
		self.containers = containers
		self.add(containers)
		self.rect = self.image.get_rect()
		self.speed = speed

	def changeDirection(self)->None:
		self.next(Test.changeDirection)

		self.speed *= -1
		self._nReflex += 1

	def close(self)->None:
		self.next(Test.close)

		self.kill()


	#States
	def moving(self)->None:
		if self.rect[0]+self.speed < 0:
			self.changeDirection()
			self.rect.move(0, self.rect[1])

		elif self.rect[0]+self.rect[2]+self.speed > self.screen[2]:
			self.changeDirection()
			self.rect.move(self.screen[2], self.rect[1])
		else:
			self.rect.move_ip(self.speed, 0)

		if self._nReflex > self._MAX_N_REFLEX:
			self.close()

Test.states = [Test.moving]
Test.arcs = [
	[[], [Test.__init__]],
	[[Test.close], [Test.changeDirection]],
]


def main() -> int:
	pg.display.init()
	pg.display.set_mode(WIND_SIZE, flags=SCALED|RESIZABLE, vsync=True)

	notExit:bool = True
	clock:pg.time.Clock = pg.time.Clock()
	wind:pg.Surface = pg.display.get_surface()

	assert pg.image.get_extended()

	tests = pg.sprite.Group()
	test = Test(tests, 2, wind.get_rect())

	while notExit and tests:
		for event in pg.event.get():
			notExit = event.type != pg.QUIT

		tests.update()

		wind.fill((128, 128, 128))
		
		tests.draw(wind)

		pg.display.flip()
		clock.tick(FPS)
	

	pg.display.quit()

	return 0


if __name__ == '__main__':
	main()
