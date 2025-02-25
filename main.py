import pygame

pygame.init()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

pygame.display.set_caption("Template Script")

lm = False

def textwidth(text: str, font = my_font) :
	return font.render(text, False, (0,0,0)).get_width()
def textheight(text: str, font = my_font) :
	return font.render(text, False, (0,0,0)).get_height()

def write(text: str, x: float = 0.0, y: float = 0.0, col: tuple[int, int, int] = (255,255,255), font = my_font) :
	text_surface = font.render(text, False, col)
	screen.blit(text_surface, (x,y))

	return text_surface.get_width()

def rect(x: float, y: float, w: float, h: float, col: tuple[int, int, int] = (255, 255, 255)) :
	pygame.draw.rect(
		screen,
		col,
		pygame.Rect(
			x, y,
			w, h
		)
	)

def line(sx: float, sy: float, ex: float, ey: float, col: tuple[int, int, int] = (255, 255, 255), w: int = 1) :
	pygame.draw.line(screen, col, (sx, sy), (ex, ey), w)

def circ(x: float, y: float, r: float, col: tuple[int, int, int] = (255, 255, 255)) :
	pygame.draw.circle(screen, col, (x, y), r)


while running :
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	ml, mm, mr = pygame.mouse.get_pressed()
	mx, my = pygame.mouse.get_pos()

	screen.fill("black")

	pygame.display.flip()

	clock.tick(60)

	lm = not(ml)
