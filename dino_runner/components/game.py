import pygame

# Importamos constantes personalizadas desde otro archivo
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS

# Importamos la clase Dinosaurio desde otro archivo
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

class Game:
  def __init__(self):
# Inicialización de Pygame
    pygame.init()

    # Configuramos el título y el ícono de la ventana del juego
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(ICON)

    # Creamos la ventana con las dimensiones definidas por las constantes SCREEN_WIDTH y SCREEN_HEIGHT
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Creamos un objeto reloj para controlar el FPS del juego
    self.clock = pygame.time.Clock()

    # Inicializamos la variable playing como False, indicando que el juego aún no ha comenzado
    self.playing = False

    # Velocidad del juego en píxeles por segundo
    self.game_speed = 20

    # Coordenadas x e y de la imagen de fondo
    self.x_pos_bg = 0
    self.y_pos_bg = 380
    # Creamos un objeto Dinosaurio
    self.player = Dinosaur()
    self.obstacle_manager = ObstacleManager()

  def run(self):
    # Game loop: events - update - draw
    # Iniciamos el juego
    self.playing = True
    # Bucle principal del juego: eventos - actualización - dibujado
    while self.playing:
      self.events()
      self.update()
      self.draw()

      # Salimos de Pygame
    pygame.quit()

  def events(self):
    # Manejo de eventos del juego
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # Si el usuario cierra la ventana, detenemos el juego
        self.playing = False

  def update(self):
    # Actualización de los elementos del juego
    user_input = pygame.key.get_pressed()
    self.player.update(user_input)
    self.obstacle_manager.update(self)

  def draw(self):
    # Dibujado de los elementos del juego
    self.clock.tick(FPS)
    # Rellenamos la pantalla con el color blanco
    self.screen.fill((255, 255, 255))
    # Dibujamos el fondo
    self.draw_background()
    # Dibujamos el dinosaurio
    self.player.draw(self.screen)
    # Dibujamos el obstaculo (cactus)
    self.obstacle_manager.draw(self.screen)
    # Actualizamos la pantalla
    pygame.display.update()
    # pygame.display.flip()

  def draw_background(self):
    # Dibujado del fondo del juego
    image_width = BG.get_width()

    # Dibujamos la imagen de fondo en su posición inicial
    self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))

    # Dibujamos una segunda imagen de fondo para crear el efecto de movimiento
    self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
    
    # Si la primera imagen se ha movido completamente fuera de la pantalla,
    # la movemos hacia la derecha y la dibujamos de nuevo para crear el efecto de bucle
    if self.x_pos_bg <= -image_width:
      self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
      self.x_pos_bg = 0

    # Movemos la imagen de fondo hacia la izquierda
    self.x_pos_bg -= self.game_speed
