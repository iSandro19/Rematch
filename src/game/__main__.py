import pygame as pg
from pygame.locals import *
from typing import List, Dict, Tuple, Union, Callable
import obj
import game.tile
import game.cam
import game.player
import game.control
import game.bckgnd


WIND_SIZE = 256,144
FPS = 60
WAIT_TIME = 200		# Tiempo a partir del cual se detecta Pulsado Largo en una tecla


# Función para determinar si una tecla es pulsada de forma larga o corta
def tiempoPulsacion(key):
	key_pressed = pg.key.get_pressed()
	start_time = pg.time.get_ticks()
	while key_pressed[key]:
		# Detecta el tiempo que se mantiene pulsada la tecla
		elapsed_time = pg.time.get_ticks() - start_time

		# Actualiza la tecla pulsada
		key_pressed = pg.key.get_pressed()
	
	# Pulsación larga
	if elapsed_time >= WAIT_TIME: return True
	
	# Pulsación corta
	return False


def main():
	pg.display.init()
	pg.display.set_mode(WIND_SIZE, flags=SCALED|RESIZABLE, vsync=True)

	# Variables para control
	notExit = True	# Bucle de eventos
	gameScreen = 0 	# Si estamos en el menú (0), en gameplay (1) o pausados (2)


	clock = pg.time.Clock()
	wind = pg.display.get_surface()
	rect = pg.Rect(0,0,128,72)

	assert pg.image.get_extended()

	obj.load('Cam', 0, 0)
	obj.load('TileMap', 0, 0)
	obj.load('TileCollision', 0, 0)
	obj.load('TileMap', 1, 0)
	obj.load('TileCollision', 1, 0)
	obj.load('Bckgnd', 0, 0)
	obj.load('Bckgnd', 1, 0)
	obj.load('BckgndParallax', 0, 0)
	obj.load('Control', 0, 0)
	player = obj.load('Player', 0, 0)

	# Instanciar player para poder llamar las funciones

	while notExit:

		# Faltan los inputs que dependen de objetos en la pantalla (menú y pantalla de pausa)
		# Los a=1 son solo para evitar que de error el if, al tener las funciones hechas quitarlo
		for event in pg.event.get():
			if event.type == pg.QUIT:
				notExit = False
			
			if gameScreen == 0:
				gameScreen = 1
				#Etc
			elif gameScreen == 1:
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						#jump and double jump
						player.jump()
						
					elif event.key == K_LSHIFT:
						# dash
						player.dash()

					elif event.key == K_e:
						
						if tiempoPulsacion(event.key):
							a = 1
							#ataque1

						else: #ataque2
							a = 1
					
					elif event.key == K_q:

						if tiempoPulsacion(event.key):
							a = 1
							#ataque3
						else: #ataque4
							a = 1

					elif event.key == K_ESCAPE:
						player.active = False
						gameScreen = 2
				
				elif event.type == KEYUP:
					if event.key == K_SPACE:
						player.fall()

			elif gameScreen == 2:
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						player.active = True
						gameScreen = 1
	
		if gameScreen == 0:

			a = 1

		elif gameScreen == 1:

			wind.fill((128, 128, 128))

			keys = pg.key.get_pressed()

			if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
				player.stopMove()

			elif keys[pg.K_RIGHT]:
				player.moveRight()
				
			elif keys[pg.K_LEFT]:
				player.moveLeft()

			else: player.stopMove()


			obj.update()

			obj.draw()

		pg.display.flip()
		clock.tick(FPS)
	
	pg.display.quit()

	return 0


if __name__ == '__main__':
	main()



