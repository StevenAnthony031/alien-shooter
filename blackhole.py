import pygame
from utils import import_folder

class BlackHole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = import_folder('data/Environment/BlackHole')
        self.animation_speed = 0.15
        self.frame_index = 0
        
        self.image = pygame.transform.rotozoom(self.animations[self.frame_index], 0, 2)
        self.rect = self.image.get_rect(center = (700, 90))
    
    def animate(self):
        animation = self.animations
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = pygame.transform.rotozoom(animation[int(self.frame_index)], 0, 2)
    
    def update(self):
        self.animate()