
import requests
import pygame

from cardmaker import Card
from io import BytesIO

card = Card("https://en.wikipedia.org/wiki/" + input("Card link: ").replace(" ", "_"))

pygame.init()

pygame.font.init()
my_font = pygame.font.SysFont(None, 25)

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

response = requests.get(card.image_link)
img = pygame.image.load(BytesIO(response.content))


# crop = pygame.Surface((280, 270))
crop = pygame.Surface((290, 270), pygame.SRCALPHA)
#crop.fill((color[0], color[1], color[2], alpha))

while running :
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	ml, mm, mr = pygame.mouse.get_pressed()
	mx, my = pygame.mouse.get_pos()

	screen.fill("black")

	rect(20, 20, 300, 450)

	write(card.name, 30, 30, (0, 0, 0))

	txt = f"Hp {card.health} Def {card.defence}"
	wide = textwidth(txt)
	write(txt, 290 - wide, 30, (0, 0, 0))

	txt = f"Type: {card.type}"
	wide = textwidth(txt)
	write(txt, 290 - wide, 50, (0, 0, 0))

	for n,i in enumerate(card.moves) :
		ypos = 345 + 20 * n

		write(i[0], 30, ypos, (0, 0, 0))

		wide = textwidth(str(i[1]))
		write(str(i[1]), 290 - wide, ypos, (0, 0, 0))

	txt = f"Strong against: {card.strength}"
	wide = textwidth(txt)
	write(txt, 290 - wide, 440, (0, 0, 0))

	#rect(30, 70, 280, 270, (0, 0, 0))

	crop.blit(img, (0, 0))

	x_off, y_off = 0, 0

	if img.get_rect().w < 280 :
		x_off = (280 - img.get_rect().w) / 2

	screen.blit(crop, (30 + int(x_off), 70 + y_off))

	pygame.display.flip()

	clock.tick(60)

	lm = not(ml)
