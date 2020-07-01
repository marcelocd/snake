import pygame, random
from pygame.locals import *
from pygame import mixer

def on_grid_random(GRID_LENGTH, GRID_HEIGHT, BASIC_UNIT):
	x = random.randint(0, GRID_LENGTH - BASIC_UNIT)
	y = random.randint(0, GRID_HEIGHT - BASIC_UNIT)
	return (x // BASIC_UNIT * BASIC_UNIT, y // BASIC_UNIT * BASIC_UNIT)

def collision(c1, c2):
	return (c1[0] == c2[0] and c1[1] == c2[1])

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

GRID_LENGTH = 300
GRID_HEIGHT = 300

BASIC_UNIT = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((GRID_LENGTH, GRID_HEIGHT))
pygame.display.set_caption('Snake')

snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((BASIC_UNIT, BASIC_UNIT))
snake_skin.fill(WHITE)

apple_pos = on_grid_random(GRID_LENGTH, GRID_HEIGHT, BASIC_UNIT)
apple = pygame.Surface((BASIC_UNIT, BASIC_UNIT))
apple.fill(RED)

my_direction = LEFT

clock = pygame.time.Clock()

mixer.music.load('eat.wav')

while True:
	clock.tick(20)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()

		if event.type == KEYDOWN:
			if event.key == K_UP:
				if my_direction != DOWN:
					my_direction = UP
			if event.key == K_RIGHT:
				if my_direction != LEFT:
					my_direction = RIGHT
			if event.key == K_DOWN:
				if my_direction != UP:
					my_direction = DOWN
			if event.key == K_LEFT:
				if my_direction != RIGHT:
					my_direction = LEFT

	if collision(snake[0], apple_pos):
		mixer.music.play()
		apple_pos = on_grid_random(GRID_LENGTH, GRID_HEIGHT, BASIC_UNIT)
		# It doesn't matter which value for the cell is appended here:
		snake.append((0,0))

	snake_length = len(snake)

	# because of this for, the appended cell will assume the value of the previous one.
	# (This for updates the body)
	for i in range(snake_length - 1, 0, -1):
		snake[i] = (snake[i - 1][0], snake[i - 1][1])

	# (These ifs update the head)
	if my_direction == UP:
		if snake[0][1] == 0:
			snake[0] = (snake[0][0], GRID_HEIGHT - BASIC_UNIT)
		else:
			snake[0] = (snake[0][0], snake[0][1] - BASIC_UNIT)
	if my_direction == RIGHT:
		if snake[0][0] == (GRID_LENGTH - BASIC_UNIT):
			snake[0] = (0, snake[0][1])
		else:
			snake[0] = (snake[0][0] + BASIC_UNIT, snake[0][1])
	if my_direction == DOWN:
		if snake[0][1] == (GRID_HEIGHT - BASIC_UNIT):
			snake[0] = (snake[0][0], 0)
		else:
			snake[0] = (snake[0][0], snake[0][1] + BASIC_UNIT)
	if my_direction == LEFT:
		if snake[0][0] == 0:
			snake[0] = (GRID_LENGTH - BASIC_UNIT, snake[0][1])
		else:
			snake[0] = (snake[0][0] - BASIC_UNIT, snake[0][1])

	# It's not possible for the snake to collide
	# with itself if its length is shorter than 5.
	if snake_length >= 5:
		for i in range(4, snake_length, 1):
			if collision(snake[0], snake[i]):
				pygame.quit()

	screen.fill(BLACK)
	screen.blit(apple, apple_pos)
	for pos in snake:
		screen.blit(snake_skin, pos)

	pygame.display.update()
