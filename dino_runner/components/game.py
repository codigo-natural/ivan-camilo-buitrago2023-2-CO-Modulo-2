import pygame

# Importamos constantes personalizadas desde otro archivo
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE

# Importamos la clase Dinosaurio desde otro archivo
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.obstacles.menu import Menu

class Game:
  GAME_SPEED = 20
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
    self.game_speed = self.GAME_SPEED

    # Coordenadas x e y de la imagen de fondo
    self.x_pos_bg = 0
    self.y_pos_bg = 380
    # Creamos un objeto Dinosaurio
    self.player = Dinosaur()
    self.obstacle_manager = ObstacleManager()
    self.menu = Menu('Press any key to start...', self.screen)
    self.running = False
    self.death_count = 0
    self.score = 0

  def execute(self):
    self.running = True
    while self.running:
      if not self.playing:
        self.show_menu()
    pygame.display.quit()
    # Salimos de Pygame
    pygame.quit()

  def run(self):
    self.obstacle_manager.reset_obstacles()
    self.player.reset_dinosaur()
    self.score = 0
    self.game_speed = self.GAME_SPEED
    # Game loop: events - update - draw
    # Iniciamos el juego
    self.playing = True
    # Bucle principal del juego: eventos - actualización - dibujado
    while self.playing:
      self.events()
      self.update()
      self.draw()

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
    self.update_score()

  def draw(self):
    # Dibujado de los elementos del juego
    self.clock.tick(FPS)
    # Rellenamos la pantalla con el color blanco
    self.screen.fill((255, 255, 255))
    # Dibujamos el fondo
    self.draw_background()
    # Dibujamos el dinosaurio
    self.player.draw(self.screen)
    # Dibujamos la puntuacion en pantalla
    self.draw_score()
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

  def show_menu(self):
    half_screen_height = SCREEN_HEIGHT // 2
    half_screen_width = SCREEN_WIDTH // 2
    self.menu.reset_screen_color(self.screen)

    if self.death_count == 0:
      self.menu.draw(self.screen)
    else:
      self.menu.update_message('new Message')
      self.menu.draw(self.screen)

    self.screen.blit(ICON, (half_screen_width - 50, half_screen_height - 140))
    self.menu.update(self)

  def update_score(self):
    self.score += 1

    if self.score % 100 == 0 and self.game_speed < 500:
      self.game_speed += 5

  def draw_score(self):
    font = pygame.font.Font(FONT_STYLE, 30)
    text = font.render(f'Score: {self.score}', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (1000, 50)
    self.screen.blit(text, text_rect)