import pygame
from utils import import_folder
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, platform):
        super().__init__()
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.2
        
        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.5
        self.jump_height = -15.5
        self.current_x = 0
        self.jump_sound = pygame.mixer.Sound('data/Sound/SFX_Jump_02.wav')
        self.can_jump = True

        # Player status
        self.status = 'idle'
        self.facing_right = True
        self.on_platform = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.platform = platform
        self.was_on_platform = False

        # Player first position
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(midbottom = (700, 500))
        
    def import_player_assets(self):
        player_path = 'data/Player/'
        self.animations = {'idle' : [], 'run' : [], 'jump' : [], 'fall' : [], 'shoot' : []}
        
        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def wall (self, windows_width):
        if self.rect.left <= 0 :
            self.rect.left = 0
        elif self.rect.right >= windows_width:
            self.rect.right = windows_width
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y = 0
    
    def animate(self):
        animation = self.animations[self.status]
        
        if self.status == 'shoot' :
            self.frame_index += 0.15
            if self.frame_index >= len(animation):
                self.frame_index = 0
                self.status = 'idle'
        else :
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
        
        # Change the player direction
        image = self.image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image 
            
        # Set the rect position if there is collision to avoid overlapping surfaces
        if self.on_platform and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_platform and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_platform:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
            
    def input(self):
        keys = pygame.key.get_pressed()

        # Horizontal Movement
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        # Jump
        if (keys[pygame.K_w] and self.can_jump and self.on_platform):
            self.direction.y = self.jump_height
            self.jump_sound.play()
            self.can_jump = False   

        # Shoot
        if keys[pygame.K_SPACE] or keys[pygame.K_k]:
            self.status = 'shoot'

            
    def get_status(self):
        if self.direction.y < 0 and self.status != 'shoot':
            self.status = 'jump'
        elif self.direction.y > 1 and self.status != 'shoot':
            self.status = 'fall'
        else:
            for sprite in self.platform.sprites():
                if self.direction.x != 0 :
                    self.status = 'run'
                elif self.status != 'shoot' and (self.on_platform or self.rect.bottom == 400):
                    self.status = 'idle'
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def horizontal_movement_collision(self):
        self.rect.x += self.direction.x * 4
        for sprite in self.platform.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    self.on_left = True
                    self.current_x = self.rect.left
                elif self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                    self.on_right = True
                    self.current_x = self.rect.right
        if self.on_left and (self.rect.left < self.current_x or self.direction.x >= 0):
            self.on_left = False
        if self.on_right and (self.rect.right > self.current_x or self.direction.x <= 0):
            self.on_right = False
    
    def vertical_movement_collision(self):
        self.apply_gravity()

        self.on_platform = False
        self.on_ceiling = False

        for sprite in self.platform.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top

                    # Dynamic Speed
                    if hasattr(sprite, "speed"):
                        self.rect.x -= sprite.speed

                    self.direction.y = 0
                    self.on_platform = True

                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                    self.on_ceiling = True

        # Reset Jump Condition
        if self.on_platform and not self.was_on_platform:
            self.can_jump = True

        self.was_on_platform = self.on_platform
    
    def update(self, windows_width):
        self.jump_sound.set_volume(0.02)
        self.get_status()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.input()
        self.wall(windows_width)
        self.animate()

    def create_bullet(self):
        return Bullet(self.rect.center[0], self.rect.center[1], self.facing_right)