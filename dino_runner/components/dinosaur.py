import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING_SHIELD, DUCKING_HAMMER, JUMPING_SHIELD, JUMPING_HAMMER, RUNNING_SHIELD, RUNNING_HAMMER, SHIELD_TYPE, HAMMER_TYPE, RUNNING, JUMPING, DUCKING, HEART

RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER }
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER }
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
class Dinosaur(Sprite):
  X_POS = 80
  Y_POS = 310
  JUMP_SPEED = 8.5
  Y_POS_DUCK = 340

  def __init__(self):
    self.type = DEFAULT_TYPE
    self.image = RUN_IMG[self.type][0]
    self.dino_rect = self.image.get_rect()
    self.dino_rect.x = self.X_POS
    self.dino_rect.y = self.Y_POS
    self.step_index = 0
    self.dino_run = True
    self.dino_jump = False
    self.dino_duck = False
    self.jump_speed = self.JUMP_SPEED
    self.has_power_up = False
    self.power_time_up = 0
    self.lives = 3

  def update(self, user_input):
    if self.dino_run:
      self.run()
    elif self.dino_jump:
      self.jump()
    elif self.dino_duck:
      self.duck()

    if user_input[pygame.K_UP] and not self.dino_jump:
      self.dino_run = False
      self.dino_jump = True
    elif user_input[pygame.K_DOWN] and not self.dino_jump:
      self.dino_jump = False
      self.dino_run = False
      self.dino_duck = True
    elif not self.dino_jump:
      self.dino_duck = False
      self.dino_run = True
    if user_input[pygame.K_SPACE] and self.has_power_up and self.type == HAMMER_TYPE:
      self.dino_jump = False
      self.dino_run = False
      self.dino_duck = False
      self.image = JUMPING_HAMMER
      self.power_time_up = pygame.time.get_ticks() + 5000
      self.has_power_up = False

    if self.step_index >= 9:
      self.step_index = 0

  def run(self):
      self.image = RUN_IMG[self.type][self.step_index // 5]
      self.dino_rect = self.image.get_rect()
      self.dino_rect.x = self.X_POS
      self.dino_rect.y = self.Y_POS
      self.dino_jump = False
      self.step_index += 1
      if self.has_power_up:
        if pygame.time.get_ticks() - self.power_time_up < 5000:
          self.type = HAMMER_TYPE
        else:
          self.type = DEFAULT_TYPE
          self.has_power_up = False
          self.image = RUN_IMG[self.type][self.step_index // 5]
      else:
        self.image = RUN_IMG[self.type][self.step_index // 5]

  def jump(self):
    self.image = JUMP_IMG[self.type]
    self.dino_rect.y -= self.jump_speed * 4
    self.jump_speed -= 0.8

    if self.jump_speed < -self.JUMP_SPEED:
      self.dino_rect.y = self.Y_POS
      self.dino_jump = False
      self.jump_speed = self.JUMP_SPEED

  def duck(self):
    if self.type == HAMMER_TYPE:
      self.image = DUCK_IMG[self.type][0]
      self.dino_rect = self.image.get_rect()
      self.dino_rect.x = self.X_POS
      self.dino_rect.y = self.Y_POS + 20
    else:
      self.image = DUCK_IMG[self.type][0] if self.step_index < 5 else DUCK_IMG[self.type][1]
      self.dino_rect = self.image.get_rect()
      self.dino_rect.x = self.X_POS
      self.dino_rect.y = self.Y_POS + 30
      self.step_index += 1

  def draw(self, screen):
    for i in range(self.lives):
      heart_rect = pygame.Rect(20 + i * 30, 20, 30, 30)
      screen.blit(HEART, heart_rect)
    screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

  def colision(self, obstacles):
    for obstacle in obstacles:
      if self.dino_rect.colliderect(obstacle.rect):
        if self.lives > 0:
          self.lives -= 1 # Resta una vida
        else:
          # Si no hay más vidas, se reinicia el juego
          self.reset_dinosaur()
          return True

    return False

  def reset_dinosaur(self):
    self.image = DUCK_IMG[self.type][self.step_index // 5]
    self.dino_rect = self.image.get_rect()
    self.dino_rect.x = self.X_POS
    self.dino_rect.y = self.Y_POS
    self.step_index = 0
    self.dino_run = True
    self.dino_jump = False
    self.dino_duck = False

    self.jump_speed = self.JUMP_SPEED