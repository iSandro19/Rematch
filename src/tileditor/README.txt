Editor de niveles para el módulo 'obj':

EJECUCIÓN:

	Desde el directorio hacer:

	python -m tileditor ROOM_W ROOM_H SPRITE_SHEET_HASH OUT_FILE [IN_FILE]

	Siendo:

	· ROOM_W: el número de columnas de tiles de la sala.
	· ROOM_H: el número de filas de tiles de la sala.
	· SPRITE_SHEET_HASH: identificador o hash del objeto 'game.image.SpriteSheet' a usar en el editor para dibujar. Estos objetos se encuentran en 'playground/nico/src/game/data/sprite_sheets.json'.
	· OUT_FILE: prefijo del fichero donde se guardará la colisión (fichero con sufijo '_tl_col.json') y el de aspecto de la sala (fichero con sufijo '_tl_map.json').
	· IN_FILE: prefijo del fichero de colision y el de aspecto para editarlos. Optativo en el caso de querer crear una nueva sala y necesario para modificar una sala ya creada previamente.

MANUEJO:
	Una vez especificado los argumentos del programa debidamente, se creará una ventana vacia si no se especifico el 'IN_FILE', o con la habitación guardada en los archivos con prefijo 'IN_FILE' en el caso de hacerlo.

	A mayores, aparecerá sobre el cursor la porción del SpriteSheet de la esquina superior izquierda dentro de la cuadricula de la habitación.

	Para pintar sobre la habitación usando esa porción del SpriteSheet, se hace click izquierdo en la coordenada escogida. Si se desea borrar lo pintado, se hace click derecho sobre ello.

	Para cambiar la porción del SpriteSheet a pintar, se puede desplazar a las porciones proximas con las teclas: 'W' para la de arriba, 'S' para la de abajo, 'A' para la de la izquieda, y 'D' para la de la derecha. Tenga en cuenta que el SpriteSheet tiene un tamaño limitado y no podrá desplazar más allá la porción.

	También puede reflejar la porción escogida con la tecla 'H' para hacerlo en horizontal, y 'V' para vertical.

	Una vez dibujado el aspecto de la sala, puede añadir la colisión entrando en su modo con la tecla 'C', donde pasará a ver un rectángulo rojo sobre el cursor y que de la misma manera que con las porciones del SpriteSheet, podrá hacer que esa celda sea colisionable con el click izquierdo y desacerlo con el derecho.
	Cabe añadir que en este modo, no podrá modificar el aspecto de la sala a no ser que vuelva a pulsar la tecla 'C' pero dejará de ver la colisión y poder editarla.

	Finalmente para guardar la colisión y el aspecto de la sala en los dos ficheros con el prefijo escogido, se pulsará la tecla 'G', y si no quiere guardarlo, simplemente cierre el programa son hacerlo.
