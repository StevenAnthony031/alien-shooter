import pygame
from utils import import_folder, enemies_collision
from explosion import Explosion

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, facing_right):
        super().__init__()
        self.animations = import_folder('data/Fx/Bullet')
        self.animation_speed = 0.075
        self.frame_index = 0
        self.facing_right = facing_right
        self.explosion_sound = pygame.mixer.Sound('data/Sound/explosion.wav')
        
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
                
    def animate(self):
        animation = self.animations
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = len(animation)-1
            
        image = self.image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image 
            
    def update(self, explode, enemies, difficulty_manager, score):
        self.explosion_sound.set_volume(0.5)

        if self.facing_right:
            self.rect.x += 5
            hit_enemies = enemies_collision(self, enemies)
            if hit_enemies:
                for _ in hit_enemies:
                    difficulty_manager.update_performance(score, bullet_hit=True)

                self.kill()
                self.explosion_sound.play()
                explosion = Explosion(self.rect.right, self.rect.y)
                explode.add(explosion)

        else:
            self.rect.x -= 5
            hit_enemies = enemies_collision(self, enemies)
            if hit_enemies:
                for _ in hit_enemies:
                    difficulty_manager.update_performance(score, bullet_hit=True)

                self.kill()
                self.explosion_sound.play()
                explosion = Explosion(self.rect.left, self.rect.y)
                explode.add(explosion)

        self.animate()
