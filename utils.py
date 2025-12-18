import pygame, math
from os import walk

def import_folder(path):
    surface_list = []
    
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.transform.rotozoom(pygame.image.load(full_path).convert_alpha(), 0, 1.5)
            surface_list.append(image_surf)
    
    return surface_list

def collision_sprite(player_group, enemies, max_distance, platform, bullet, explode):
    for player in player_group.sprites():
        for enemy in enemies.sprites():
            distance = math.sqrt((player.rect.centerx - enemy.rect.centerx)**2 + (player.rect.centery - enemy.rect.centery)**2)
            if distance <= max_distance and player.rect.colliderect(enemy.rect):
                enemy.kill()
                enemies.empty()
                platform.empty()
                bullet.empty()
                explode.empty()
                return False
    return True

def enemies_collision(sprite, enemies):
    hits = pygame.sprite.spritecollide(sprite, enemies, True)
    return hits
        
def game_over(players, enemies, platform, bullet, explode):
    for player in players:
        if player.rect.y >= 500: 
            enemies.empty()
            platform.empty()
            bullet.empty()
            explode.empty()
            return False
    return True

def display_score(text_font, screen, start_time, windows_width):
    current_time = int(pygame.time.get_ticks()/1000) - start_time # in seconds
    score_text = text_font.render(f'score : {current_time}', True, '#e1e1df')
    score_rect = score_text.get_rect(center = (windows_width/2, 50))
    screen.blit(score_text, score_rect)
    return current_time

def control_text(screen, intro_bg, text_font, windows_width):
    screen.blit(intro_bg, (0, 0))
    jump_text = text_font.render('W : Jump', True, '#e1e1df')
    jump_text_rect = jump_text.get_rect(center = (windows_width/2, 200))
    move_text = text_font.render('A or D : Run', True, '#e1e1df')
    move_text_rect = move_text.get_rect(center = (windows_width/2, 250))
    shoot_text = text_font.render('K or SPACE : shoot', True, '#e1e1df')
    shoot_text_rect = shoot_text.get_rect(center = (windows_width/2, 300))
    screen.blit(jump_text, jump_text_rect)
    screen.blit(move_text, move_text_rect)
    screen.blit(shoot_text, shoot_text_rect)

