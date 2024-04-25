import pygame, os, sys
import random
from pygame.locals import *
from pygame import mixer

## Medidas de la pantallita
width = 640
height = 480
##


### Inicializacion 
pygame.init()

### Variables que usaremos 
fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((width,height))
font = pygame.font.Font(None,32)

## Musiquita
mixer.init()
mixer.music.load('Musica.wav')
mixer.music.play()



### POSICION

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y

### Datos del Juego 

class GameData:
    def __init__(self):
         # Cantidad de vidas que tiene el jugador
        self.lives = 3
        # Un booleano para cambiar a verdadero cuando toca su cola o un muro
        self.isDead = False 
        # Estos seran los bloques que conforman la cola de la serpiente
        self.blocks = [] 
        # Lo usaremos para las animaciones en este caso las unidades seran milisegundos
        self.tick = 250 
        #  La velocidad 
        self.speed = 150
        # Los niveles de dificultad (solo para que se vea mejor)
        self.level = 1 
        # Nos dice el numero de comida que ha sido consumido en este nivel
        self.berrycount = 0 
        # Los segmentos que agregamos al consumir comida
        self.segments = 1
        
        self.frame = 0
        
        # Coordenadas aleatorias de la comidita
        bx = random.randint(1,38)
        by = random.randint(1,28)
        
        
        self.berry = Position(bx,by)
        self.blocks.append(Position(20,15))
        self.blocks.append(Position(19,15))
        
        # La direccion a la que se dirige la serpiente 
        # 0 es la derecha
        # 1 es la izquierda 
        # 2 es hacia arriba
        # 3 es hacia bajo
        # Aqui tenemos que tener en cuenta que no puedes ir en reversa 
        # es decir de abajo a arriba o de derecha a izquiera
        self.direction = 0  


# FUNCIONES
        
# Lo que debe hacer cuando pierde una vida
def loseLife(gamedata):
	gamedata.lives -= 1
	gamedata.direction = 0
	gamedata.blocks[:] = []
	gamedata.blocks.append(Position(20,15))
	gamedata.blocks.append(Position(19,15))

# Posicion de la comida
def positionBerry(gamedata):
	bx = random.randint(1, 38)
	by = random.randint(1, 28)
	found = True
	
	while (found):
		found = False
		for b in gamedata.blocks:
			if (b.x == bx and b.y == by):
				found = True
				
		if (found):
			bx = random.randint(1, 38)
			by = random.randint(1, 28)				
			
	gamedata.berry = Position(bx, by)

# Carga el mapa del nivel (esta hecho con ceros y unos)
def loadMapFile(fileName):
	f = open(fileName, 'r')
	content = f.readlines()
	f.close()
	return content
        
# Que pasa si colisionas contigo
	
def headHitBody(gamedata):
	head = gamedata.blocks[0]
	
	for b in gamedata.blocks:
		if (b != head):
			if(b.x == head.x and b.y == head.y):
				return True
				
	return False
# Que pasa si colisionas con los muros	
def headHitWall(map, gamedata):
	row = 0

	for line in map:
		col = 0
		for char in line:
			if ( char == '1'):	
				if (gamedata.blocks[0].x == col and gamedata.blocks[0].y == row):
					return True

			col += 1

		row += 1	
		
	return False
 # Dibujar cosas en pantalla

def drawData(surface, gamedata):
	text = font.render("Vidas = %d, Nivel= %d" % ( gamedata.lives, gamedata.level ), 0, (255, 255, 255))
	textpos = text.get_rect(centerx=surface.get_width()/2, top=32)
	surface.blit(text, textpos)

        # Dibujar la pantalla de Game Over	
def drawGameOver(surface):
	
	text1 = font.render("Game Over", 1, (255, 255, 255))
	text2 = font.render('Presione espacio para continuar', 1, (255, 255, 255))
	# named parameters
	textpos1 = text1.get_rect(centerx=surface.get_width()/2, top=surface.get_height()/2 - 48)
	textpos2 = text2.get_rect(centerx=surface.get_width()/2, top=surface.get_height()/2)
	surface.blit(text1, textpos1)
	surface.blit(text2, textpos2)


    # Dibujar los muros	
def drawWalls(surface, img, map):

	row = 0

	for line in map:
		col = 0
		for char in line:
			if ( char == '1'):
				imgRect = img.get_rect()
				imgRect.left = col * 16
				imgRect.top = row * 16
				surface.blit(img, imgRect)
			col += 1

		row += 1


	  # Dibujar la serpiente		
def drawSnake(surface, img, gamedata):
	first = True

	for b in gamedata.blocks:
		dest = (b.x * 16, b.y * 16, 16, 16)
		if ( first ):
			first = False
			src = (((gamedata.direction * 2) + gamedata.frame) * 16, 0, 16, 16)
		else:
			src = (8 * 16, 0, 16, 16)

		surface.blit(img, dest, src)


# Actualizar el juego
		
def updateGame(gamedata, gameTime):
	gamedata.tick -= gameTime
	
	head = gamedata.blocks[0]
	
	if (gamedata.tick < 0):
		gamedata.tick += gamedata.speed
		gamedata.frame += 1
		gamedata.frame %= 2
		if (gamedata.direction == 0):
			move = (1, 0)
		elif (gamedata.direction == 1):
			move = (-1, 0)
		elif (gamedata.direction == 2):
			move = (0, -1)
		else:
			move = (0, 1)
			
		newpos = Position(head.x + move[0], head.y + move[1])
		
		first = True
		for b in gamedata.blocks:
			temp = Position(b.x, b.y)
			b.x = newpos.x
			b.y = newpos.y
			newpos = Position(temp.x, temp.y)			
	

	# movimiento de la serpiente

	keys = pygame.key.get_pressed()
				
	if (keys[K_RIGHT] and gamedata.direction != 1):
		gamedata.direction = 0
	elif (keys[K_LEFT] and gamedata.direction != 0):
		gamedata.direction = 1
	elif(keys[K_UP] and gamedata.direction != 3):
		gamedata.direction = 2 
	elif(keys[K_DOWN] and gamedata.direction != 2):
		gamedata.direction = 3
		
	# colision con la comida
	
	if (head.x == gamedata.berry.x and head.y == gamedata.berry.y):
		lastIdx = len(gamedata.blocks) - 1
		for i in range(gamedata.segments):
			gamedata.blocks.append(Position(gamedata.blocks[lastIdx].x, gamedata.blocks[lastIdx].y))
	
		bx = random.randint(1, 38)
		by = random.randint(1, 28)
		gamedata.berry = Position(bx, by)
		gamedata.berrycount += 1
		if (gamedata.berrycount == 10):
			gamedata.berrycount = 0
			gamedata.speed -= 25
			gamedata.level += 1
			gamedata.segments *= 2
			if (gamedata.segments > 64):
				gamedata.segments = 64
			
			if (gamedata.speed < 100):
				gamedata.speed = 100
# Cargar imagenes
def loadImages():
	wall = pygame.image.load('wall.png')
	raspberry = pygame.image.load('berry.png')
	snake = pygame.image.load('snake.png')
	
	return {'wall':wall, 'berry':raspberry, 'snake':snake}
	
images = loadImages()

images['berry'].set_colorkey((255, 0, 255))

### Aqui cargamos el mapa del nivel
#nos da un nivel al azar y carga el mapa correspondiente
nivel = random.randint(1,3)
snakemap = loadMapFile('map_{}.txt'.format(nivel))
## Nota el nivel no cambiara hasta que no cerremos y volvamos a ejecutar el programa

data = GameData()


quitGame = False
isPlaying = False

while not quitGame:

	if isPlaying:
		x = random.randint(1, 38)
		y = random.randint(1, 28)
		data.level = nivel 
		rrect = images['berry'].get_rect()
		rrect.left = data.berry.x * 16
		rrect.top = data.berry.y * 16
	
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
	
		# Actualizamos cosillas
		updateGame(data, fpsClock.get_time())
		crashed = headHitWall(snakemap, data) or headHitBody(data)
		if (crashed):
			loseLife(data)
			positionBerry(data)

		isPlaying = (data.lives > 0)
		
		if (isPlaying):	
			surface.fill((0, 0, 0))
		
			# Dibujamos los muros la comida y la viborita 
			drawWalls(surface, images['wall'], snakemap)
			surface.blit(images['berry'], rrect)
			drawSnake(surface, images['snake'], data)
			drawData(surface, data)

	else:
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		if (keys[K_SPACE]):
			isPlaying = True
			data = None
			data = GameData()
			
		drawGameOver(surface)

	pygame.display.update()
	fpsClock.tick(30)