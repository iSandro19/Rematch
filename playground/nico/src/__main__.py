import pygame as pg
from pygame.locals import *
from typing import List, Dict, Tuple, Union, Callable
import obj


WIND_SIZE:Tuple[int, int] = 512, 512
FPS:int = 60

from random import randint

class Test(obj.ObjState, pg.sprite.Sprite):
	containers:pg.sprite.Group = None
	screen:pg.Rect = None
	xSpeed:int = None
	ySpeed:int = None

	_nReflex = 0
	_MAX_N_REFLEX = 3

	#Actions
	def __init__(
		self,
		containers:pg.sprite.Group,
		x:int,
		y:int,
		xSpeed:int,
		ySpeed:int,
		screen:pg.Rect
	)->None:
		self.next(Test.__init__)
		pg.sprite.Sprite.__init__(self)
		self.screen = screen
		self.image = pg.image.load("PerfilP.png")
		self.containers = containers
		self.add(containers)
		self.rect = self.image.get_rect().copy()
		self.rect.move_ip(x, y)
		self.xSpeed = xSpeed
		self.ySpeed = ySpeed

	def changeXDirection(self)->None:
		self.next(Test.changeXDirection)

		self.xSpeed *= -1
		self._nReflex += 1

	def changeYDirection(self)->None:
		self.next(Test.changeYDirection)

		self.ySpeed *= -1
		self._nReflex += 1

	def close(self)->None:
		self.next(Test.close)

		self.kill()


	#States
	def moving(self)->None:
		if self.rect[0]+self.xSpeed < 0:
			self.changeXDirection()
			self.rect.move(0, self.rect[1])

		elif self.rect[0]+self.rect[2]+self.xSpeed > self.screen[2]:
			self.changeXDirection()
			self.rect.move(self.screen[2], self.rect[1])

		elif self.rect[1]+self.ySpeed < 0:
			self.changeYDirection()
			self.rect.move(self.rect[0], 0)

		elif self.rect[1]+self.rect[3]+self.ySpeed > self.screen[3]:
			self.changeYDirection()
			self.rect.move(self.rect[0], self.screen[3])
		else:
			self.rect.move_ip(self.xSpeed, self.ySpeed)

		if self._nReflex > self._MAX_N_REFLEX:
			self.close()

Test.setStates([Test.moving])
Test.setArcs([
	[[], [Test.__init__]],
	[[Test.close], [Test.changeXDirection, Test.changeYDirection]],
])


def main() -> int:
	pg.display.init()
	pg.display.set_mode(WIND_SIZE, flags=SCALED|RESIZABLE, vsync=True)

	notExit:bool = True
	clock:pg.time.Clock = pg.time.Clock()
	wind:pg.Surface = pg.display.get_surface()

	assert pg.image.get_extended()

	tests = pg.sprite.Group()
	
	Test(
		tests,
		randint(0, wind.get_rect()[2]-64),
		randint(0, wind.get_rect()[3]-64),
		randint(1, 5),
		randint(1, 5),
		wind.get_rect()
	)

	delay:int = 0

	while notExit and tests:
		for event in pg.event.get():
			notExit = event.type != pg.QUIT

		delay += 1

		if delay == 100:
			Test(
				tests,
				randint(0, wind.get_rect()[2]-64),
				randint(0, wind.get_rect()[3]-64),
				randint(1, 5),
				randint(1, 5),
				wind.get_rect()
			)
			delay = 0

		tests.update()

		wind.fill((128, 128, 128))
		
		tests.draw(wind)

		pg.display.flip()
		clock.tick(FPS)
	

	pg.display.quit()

	return 0


if __name__ == '__main__':
	main()
