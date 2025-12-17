import pygame, sys, random, time
from blackhole import BlackHole
from player import Player
from enemies import Enemies
from platform import Platform
from utils import collision_sprite, game_over, display_score, control_text

# initialize the game
pygame.init()
running = False
start_time = 0
score = 0
high_score = 0

# windows
windows_width = 800
windows_height = 500
screen = pygame.display.set_mode((windows_width, windows_height))
pygame.display.set_caption('Space Shooter')

# game fps
clock = pygame.time.Clock()

# platforms groups
platform = pygame.sprite.Group()
platform.add(Platform(700, 400))

# player groups
player = Player(platform)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

# bullet groups
bullet = pygame.sprite.Group()

# enemies groups
enemies = pygame.sprite.Group()

# explosions
explode = pygame.sprite.Group()

# planet
black_hole = pygame.sprite.GroupSingle()
black_hole.add(BlackHole())

# timers
enemies_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemies_timer, 1200)
platform_timer = pygame.USEREVENT + 2
pygame.time.set_timer(platform_timer, 1000)
bullet_cooldown = 0.5 # seconds
last_bullet_time = 0

# font
title_font = pygame.font.Font('data/Font/ethnocentric_rg.otf', 50)
text_font = pygame.font.Font('data/Font/ethnocentric_rg.otf', 20)

# sound
game_music = pygame.mixer.Sound('data/Sound/Never Gonna Give You Up 8 bit.mp3')
game_music.set_volume(0.2)
game_music.play(loops = -1)

# intro screen
intro_bg = pygame.image.load('data/UI/Space_Background.png').convert_alpha()

game_name = title_font.render('ALIEN SHOOTER', True, '#e1e1df')
game_name_rect = game_name.get_rect(center = (windows_width/2, 150))

control_info_button = pygame.transform.rotozoom(pygame.image.load('data/UI/Info_BTN.png').convert_alpha(), 0, 0.2)
control_info_button_rect = control_info_button.get_rect(center = (40, 40))

start_button = pygame.transform.rotozoom(pygame.image.load('data/UI/Start_BTN.png').convert_alpha(), 0, 0.4)
start_button_rect = start_button.get_rect(center = (windows_width/2, 300))

replay_button = pygame.transform.rotozoom(pygame.image.load('data/UI/Replay_BTN.png').convert_alpha(), 0, 0.4)
replay_button_rect = replay_button.get_rect(center = (windows_width/2, 200))

# background
space_bg = pygame.image.load('data/Backgrounds/5532919.jpg').convert_alpha()
space_bg = pygame.transform.smoothscale(space_bg, (windows_width, windows_height))

# game loop
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if running:
            if event.type == enemies_timer:
                enemies.add(Enemies(random.choice(['Bat', 'Bat' ,'fly-eye', 'fly-eye', 'fly-eye'])))
            if event.type == platform_timer:
                platform.add(Platform(random.randint(825, 900), random.randint(180, 380)))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k or event.key == pygame.K_SPACE:
                    current_time = time.time()
                    if current_time - last_bullet_time >= bullet_cooldown: # make bullet cannot be spammed
                        bullet.add(player.create_bullet())
                        last_bullet_time = current_time
            
    if running:
        screen.blit(space_bg, (0, 0))
        score = display_score(text_font, screen, start_time, windows_width)
        
        running = collision_sprite(player_group, enemies, 40, platform, bullet, explode) and game_over(player_group, enemies, platform, bullet, explode)
        
        # update sprite
        player_group.update(windows_width)
        black_hole.update()
        bullet.update(bullet, explode, enemies)
        enemies.update()
        explode.update()
        platform.update()
        
        # draw sprite
        bullet.draw(screen)
        black_hole.draw(screen)
        player_group.draw(screen)
        enemies.draw(screen)
        explode.draw(screen)
        platform.draw(screen)
        
    else:
        screen.blit(intro_bg, (0, 0))
        player_group.sprite.rect.midbottom = (700, 400)
        platform.add(Platform(700, 400))
        
        if score > high_score : high_score = score
        
        score_text = text_font.render(f'SCORE : {score}', True, '#e1e1df')
        score_text_rect = score_text.get_rect(center = (windows_width/2, 300))
        high_score_text = text_font.render(f'RECORD : {high_score}', True, '#e1e1df')
        high_score_rect = high_score_text.get_rect(center = (windows_width/2, 350))
        
        if score == 0 and high_score == 0:
            screen.blit(game_name, game_name_rect)
            screen.blit(start_button, start_button_rect)
            screen.blit(control_info_button, control_info_button_rect)
            mouse_pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed() == (True, False, False):
                    running = True
                    start_time = int(pygame.time.get_ticks()/1000)
            elif control_info_button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed() == (True, False, False):
                    control_text(screen, intro_bg, text_font, windows_width)
        else :
            screen.blit(replay_button, replay_button_rect)
            screen.blit(score_text, score_text_rect)
            screen.blit(high_score_text, high_score_rect)
            mouse_pos_replay = pygame.mouse.get_pos()
            if replay_button_rect.collidepoint(mouse_pos_replay):
                if pygame.mouse.get_pressed() == (True, False, False):
                    running = True
                    start_time = int(pygame.time.get_ticks()/1000)
                    
    pygame.display.update()
    clock.tick(60) # limit fps to 60fps