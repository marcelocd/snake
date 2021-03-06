import pygame, random
from pygame.locals import *
from pygame import mixer

# FUNCTIONS -----------------------------
def on_grid_random(GRID_LENGTH, GRID_HEIGHT, BASIC_UNIT):
	x = random.randint(0, GRID_LENGTH - BASIC_UNIT)
	y = random.randint(0, GRID_HEIGHT - BASIC_UNIT)
	return (x // BASIC_UNIT * BASIC_UNIT, y // BASIC_UNIT * BASIC_UNIT)

def collision(c1, c2):
	return (c1[0] == c2[0] and c1[1] == c2[1])

# ---------------------------------------

# CONSTANTS -----------------------------
EASY = 10
MEDIUM = 20
HARD = 30
IMPOSSIBLE = 50

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

SCREEN_LENGTH = 500
SCREEN_HEIGHT = 300

SCORE_BOARD_LENGTH = 200
SCORE_BOARD_HEIGHT = 300

GRID_LENGTH = 300
GRID_HEIGHT = 300

BASIC_UNIT = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# ---------------------------------------

pygame.init()
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')

# GAME SOUNDS ---------------------------
eat_sound = mixer.Sound('eat.wav')
game_over_sound = mixer.Sound('game_over.wav')

# ---------------------------------------

# DEFINING WHERE THE SNAKE CAN CRAWL
grid = pygame.Surface((GRID_LENGTH, GRID_HEIGHT))
grid.fill(BLACK)
grid_pos = (0, 0)

# DEFINING THE SNAKE PROPERTIES
snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((BASIC_UNIT, BASIC_UNIT))
snake_skin.fill(WHITE)
snake_direction = LEFT

#DEFINING THE APPLE PROPERTIES
apple_pos = on_grid_random(GRID_LENGTH, GRID_HEIGHT, BASIC_UNIT)
apple = pygame.Surface((BASIC_UNIT, BASIC_UNIT))
apple.fill(RED)

# DEFINING WHERE THE SCORE IS SHOWN
score_board = pygame.Surface((SCORE_BOARD_LENGTH, SCORE_BOARD_HEIGHT))
score_board.fill(BLUE)
score_board_pos = (GRID_LENGTH + 1, 0)

# DEFINING THE SCORE STYLE AND INITIAL VALUE
score_font = pygame.font.Font('freesansbold.ttf', 25)
score_pos = (GRID_LENGTH + 10, 10)
score = 0

clock = pygame.time.Clock()

while True:
	clock.tick(EASY)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()

		if event.type == KEYDOWN:
			if event.key == K_UP:
				if snake_direction != DOWN:
					snake_direction = UP
			if event.key == K_RIGHT:
				if snake_direction != LEFT:
					snake_direction = RIGHT
			if event.key == K_DOWN:
				if snake_direction != UP:
					snake_direction = DOWN
			if event.key == K_LEFT:
				if snake_direction != RIGHT:
					snake_direction = LEFT

	if collision(snake[0], apple_pos):
		eat_sound.play()
		apple_pos = on_grid_random(GRID_LENGTH, GRID_HEIGHT, BASIC_UNIT)
		# It doesn't matter which value for the cell is appended here:
		snake.append((0,0))
		score += 1

	snake_length = len(snake)

	# because of this for, the appended cell will assume the value of the previous one.
	# (This for updates the body)
	for i in range(snake_length - 1, 0, -1):
		snake[i] = (snake[i - 1][0], snake[i - 1][1])

	# (These ifs update the head)
	if snake_direction == UP:
		if snake[0][1] == 0:
			snake[0] = (snake[0][0], GRID_HEIGHT - BASIC_UNIT)
		else:
			snake[0] = (snake[0][0], snake[0][1] - BASIC_UNIT)
	if snake_direction == RIGHT:
		if snake[0][0] == (GRID_LENGTH - BASIC_UNIT):
			snake[0] = (0, snake[0][1])
		else:
			snake[0] = (snake[0][0] + BASIC_UNIT, snake[0][1])
	if snake_direction == DOWN:
		if snake[0][1] == (GRID_HEIGHT - BASIC_UNIT):
			snake[0] = (snake[0][0], 0)
		else:
			snake[0] = (snake[0][0], snake[0][1] + BASIC_UNIT)
	if snake_direction == LEFT:
		if snake[0][0] == 0:
			snake[0] = (GRID_LENGTH - BASIC_UNIT, snake[0][1])
		else:
			snake[0] = (snake[0][0] - BASIC_UNIT, snake[0][1])

	# It's not possible for the snake to collide
	# with itself if its length is shorter than 5.
	if snake_length >= 5:
		for i in range(4, snake_length, 1):
			if collision(snake[0], snake[i]):
				game_over_sound.play()
				clock.tick(1)
				pygame.quit()
				quit()


	screen.blit(grid, grid_pos)
	screen.blit(apple, apple_pos)
	for pos in snake:
		screen.blit(snake_skin, pos)

	screen.blit(score_board, score_board_pos)
	score_text = score_font.render('Score: ' + str(score), True, BLACK)
	screen.blit(score_text, score_pos)

	pygame.display.update()
