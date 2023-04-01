# Importamos el módulo pygame y la clase Sprite
import pygame
from pygame.sprite import Sprite

# Importamos la constante RUNNING, JUMPING y DUCKING del archivo constants.py
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING

# Definimos la clase Dinosaur que hereda de Sprite
class Dinosaur(Sprite):
  # Establecemos algunas constantes para la posición y velocidad del dinosaurio
  """
    Clase que representa al dinosaurio del juego.

    Hereda de la clase Sprite de Pygame para ser dibujado en la pantalla.

    Atributos:
        X_POS (int): posición horizontal del dinosaurio en la pantalla.
        Y_POS (int): posición vertical del dinosaurio en la pantalla.
        JUMP_SPEED (float): velocidad de salto del dinosaurio.

        image (Surface): imagen actual del dinosaurio.
        dino_rect (Rect): rectángulo de colisión del dinosaurio.
        step_index (int): índice de paso actual del dinosaurio.
        dino_run (bool): indica si el dinosaurio está corriendo.
        dino_jump (bool): indica si el dinosaurio está saltando.
        jump_speed (float): velocidad de salto actual del dinosaurio.
        dino_duck (bool): indica si el dinosaurio está agachado.
    """
  X_POS = 80
  Y_POS = 310
  JUMP_SPEED = 8.5

  def __init__(self):
    # Inicializamos los atributos del dinosaurio, incluyendo la imagen, rectángulo, índice de paso, etc.
    self.image = RUNNING[0]
    self.dino_rect = self.image.get_rect()
    self.dino_rect.x = self.X_POS
    self.dino_rect.y = self.Y_POS
    self.step_index = 0
    self.dino_run = True
    self.dino_jump = False
    self.jump_speed = self.JUMP_SPEED
    self.dino_duck = False

  def update(self, user_input):
    # Actualizamos el estado del dinosaurio según la entrada del usuario y la acción actual
    if self.dino_run:
      self.run()
    elif self.dino_jump:
      self.jump()
    elif self.dino_duck:
      self.duck()

    # Cambiamos al estado de salto si el usuario presiona la tecla de arriba y no estamos saltando actualmente
    if user_input[pygame.K_UP] and not self.dino_jump:
      self.dino_run = False
      self.dino_jump = True
    # Cambiamos al estado de correr si el usuario no está presionando la tecla de arriba y no estamos saltando
    elif not self.dino_jump:
      self.dino_run = True

    # Reiniciamos el índice de paso cada 10 ciclos de actualización
    if self.step_index >= 10:
      self.step_index = 0

    # Cambiamos al estado de agacharse si el usuario presiona la tecla de abajo y no estamos saltando actualmente
    if user_input[pygame.K_DOWN] and not self.dino_jump:
      self.dino_duck = True
    else:
      self.dino_duck = False

  def run(self):
    # Actualizamos la imagen del dinosaurio en el estado de correr
    if self.dino_duck:
      # Cambiamos entre dos imágenes para crear la animación de agacharse
      self.image = DUCKING[0] if self.step_index < 5 else DUCKING[1]
      self.dino_rect = self.image.get_rect()
      self.dino_rect.x = self.X_POS
      self.dino_rect.y = self.Y_POS + 25
      self.step_index += 1
    else:
      # Cambiamos entre dos imágenes para crear la animación de correr
      self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
      self.dino_rect = self.image.get_rect()
      self.dino_rect.x = self.X_POS
      self.dino_rect.y = self.Y_POS
      self.step_index += 1

  def jump(self):
    # Actualizamos la imagen y la posición del dinosaurio en el estado de saltar
    self.image = JUMPING
    self.dino_rect.y -= self.jump_speed * 4
    self.jump_speed -= 0.8

    if self.jump_speed < -self.JUMP_SPEED:
      self.dino_rect.y = self.Y_POS
      self.dino_jump = False
      self.jump_speed = self.JUMP_SPEED

  def duck(self):
    # Actualizamos la imagen y la posición del dinosaurio en el estado de agacharse
    self.image = DUCKING
    self.dino_rect.y = self.Y_POS + 25

  def draw(self, screen):
    # Dibujamos el dinosaurio en la pantalla
    screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))