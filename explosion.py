import pygame
from utils import import_folder

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.animations = import_folder('data/Fx/Bullet_Hit')
        self.animation_speed = 0.075
        self.frame_index = 0
        
        self.image = pygame.transform.scale2x(self.animations[self.frame_index])
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
                
    def animate(self):
        animation = self.animations
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            self.kill()
            
        self.image = pygame.transform.scale2x(animation[int(self.frame_index)])
            
    def update(self):
        self.animate()