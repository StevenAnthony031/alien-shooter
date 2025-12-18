import pygame, random
from utils import import_folder

class Enemies(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.import_enemies_assets()
        self.animation_speed = 0.2
        self.frame_index = 0
        self.enemies_type = type
        
        self.image = self.animations[self.enemies_type][self.frame_index]
        self.rect = self.image.get_rect(center = (random.randint(850, 900), random.randint(100, 400)))
        
    def import_enemies_assets(self):
        enemies_path = 'data/Enemies/'
        self.animations = {'Bat' : [], 'fly-eye' : []}
        
        for animation in self.animations.keys():
            full_path = enemies_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def animate(self):
        animation = self.animations[self.enemies_type]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        
    def destroy(self):
        if self.rect.right <= 0:
            self.kill()