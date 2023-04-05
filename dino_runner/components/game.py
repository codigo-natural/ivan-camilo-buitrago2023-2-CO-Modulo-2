import pygame

# Importamos constantes personalizadas desde otro archivo
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, GAMEOVER

# Importamos la clase Dinosaurio desde otro archivo
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.message import draw_message

class Game:
  # Definimos la constante GAME_SPEED con un valor de 20 píxeles por segundo
  GAME_SPEED = 20
  # Constructor de la clase Game
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
    # Creamos un objeto ObstacleManager
    self.obstacle_manager = ObstacleManager()
    # Inicializamos variables
    self.running = False
    self.death_count = 0
    self.total_points = 0
    self.score = 0

  # Función para iniciar el juego
  def execute(self):
    # Cambiamos el valor de running a True para iniciar el bucle principal
    self.running = True
    while self.running:
      if not self.playing:
        # Si el juego no ha comenzado, mostramos el menú
        self.show_menu()
    pygame.display.quit()
    # Salimos de Pygame
    pygame.quit()

  def run(self):
    # self.obstacle_manager.reset_obstacles()
    # self.player.reset_dinosaur()
    # self.score = 0
    # self.game_speed = self.GAME_SPEED
    # Game loop: events - update - draw
    # Iniciamos el juego
    self.reset_all()
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

  # Función para dibujar los elementos del juego
  def draw(self):
    # Controlamos el FPS del juego
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
    pygame.display.flip()

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
    self.screen.fill((255, 255, 255))
    half_screen_height = SCREEN_HEIGHT // 2
    half_screen_width = SCREEN_WIDTH // 2

    if self.death_count == 0:
      draw_message('Press any key to restart ...', self.screen)
    else:
      draw_message('Press any key to restart ...', self.screen)
      draw_message(f'Your Score: {self.score}', self.screen, HALF_SCREEN_WIDTH = half_screen_height + 50)
      draw_message(f'Best Score: {self.total_points}', self.screen, HALF_SCREEN_WIDTH = half_screen_height + 100)
      draw_message(f'Total Deaths: {self.death_count}', self.screen, HALF_SCREEN_WIDTH = half_screen_height + 150)
      GAMEOVER_RECT = GAMEOVER.get_rect()
      GAMEOVER_RECT.center = (half_screen_width, half_screen_height), 
      self.screen.blit(GAMEOVER, (GAMEOVER_RECT.x, GAMEOVER_RECT.y - 50))
      self.screen.blit(ICON, (half_screen_width - 50, half_screen_height - 200))

    pygame.display.update()
    self.handle_events_on_menu()

  def handle_events_on_menu(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
        self.playing = False
      elif event.type == pygame.KEYDOWN:
        self.run()

  def update_score(self):
    if self.score % 100 == 0 and self.game_speed < 500:
      # Incrementamos la velocidad del juego
      self.game_speed += 5
    # actualizamos la puntuacion del juego
    self.score += 1
    # Comprobamos si se ha superado la mejor puntuación
    if self.score > self.total_points:
      self.total_points = self.score
    
  def draw_score(self):
    font = pygame.font.Font(FONT_STYLE, 30)
    text = font.render(f'Score: {self.score}', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (1000, 50)
    self.screen.blit(text, text_rect)

  def reset_all(self):
    self.obstacle_manager.reset_obstacles()
    self.playing = True
    self.game_speed = self.GAME_SPEED
    self.score = 0