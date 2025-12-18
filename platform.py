import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.image = pygame.transform.rotozoom(
            pygame.image.load('data/Environment/rock_bar_resize.png').convert_alpha(),
            0,
            1.2
        )
        self.rect = self.image.get_rect(midtop=(pos_x, pos_y))
        self.speed = 0
        
    def destroy(self):
        if self.rect.right <= 0:
            self.kill()

    def update(self):
        self.destroy()
