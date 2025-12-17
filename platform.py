import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        
        self.image = pygame.transform.rotozoom(pygame.image.load('data/Environment/rock_bar_resize.png'), 0, 1.2)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect(midtop = (pos_x, pos_y))  
        
    def destroy(self):
        if self.rect.right <= 0:
            self.kill()
               
    def update(self):
        self.rect.x -= 2
        self.destroy()