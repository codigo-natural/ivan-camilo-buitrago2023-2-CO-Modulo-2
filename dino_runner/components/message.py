import pygame
from dino_runner.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FONT_STYLE

FONT_COLOR = (0, 0, 0)
FONT_SIZE = 30

# Definimos la función draw_message, que recibe un mensaje, una pantalla, un color de fuente, 
# un tamaño de fuente y las posiciones de la pantalla donde se ubicará el texto
def draw_message(
  message,
  screen,
  font_color = FONT_COLOR,
  font_size = FONT_SIZE,
  HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2, # pos_x
  HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2 # pos_y
):
  font = pygame.font.Font(FONT_STYLE, font_size)
  text = font.render(message, True, font_color)
  text_rect = text.get_rect()
  text_rect.center = (HALF_SCREEN_HEIGHT, HALF_SCREEN_WIDTH)
  screen.blit(text, text_rect)
