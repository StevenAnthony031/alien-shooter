import pygame, sys, random, time
from blackhole import BlackHole
from player import Player
from enemies import Enemies
from platform import Platform
from utils import collision_sprite, game_over, display_score, control_text
from difficulty import DifficultyManager

# Initialize the game
pygame.init()
running = False
start_time = 0
score = 0
high_score = 0

# Initialize DDA System
difficulty_manager = DifficultyManager()

# Windows
windows_width = 800
windows_height = 500
screen = pygame.display.set_mode((windows_width, windows_height))
pygame.display.set_caption('Space Shooter')

# Game fps
clock = pygame.time.Clock()

# Platforms groups
platform = pygame.sprite.Group()
platform.add(Platform(700, 500))

# Player groups
player = Player(platform)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

# Bullet groups
bullet = pygame.sprite.Group()

# Enemies groups
enemies = pygame.sprite.Group()

# Explosions
explode = pygame.sprite.Group()

# Planet
black_hole = pygame.sprite.GroupSingle()
black_hole.add(BlackHole())

# Timers
enemies_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemies_timer,difficulty_manager.enemy_spawn_rate)
platform_timer = pygame.USEREVENT + 2
pygame.time.set_timer(platform_timer, difficulty_manager.platform_spawn_rate)
bullet_cooldown = 0.5 # seconds
last_bullet_time = 0

# DDA check timer
dda_check_interval = 10  # Check difficulty every 10 seconds
last_dda_check = 0

# Font
title_font = pygame.font.Font('data/Font/ethnocentric_rg.otf', 50)
text_font = pygame.font.Font('data/Font/ethnocentric_rg.otf', 20)
small_font = pygame.font.Font('data/Font/ethnocentric_rg.otf', 12)

# Sound
game_music = pygame.mixer.Sound('data/Sound/Never Gonna Give You Up 8 bit.mp3')
game_music.set_volume(0.2)
game_music.play(loops = -1)

# Intro screen
intro_bg = pygame.image.load('data/UI/Space_Background.png').convert_alpha()

game_name = title_font.render('ALIEN SHOOTER', True, '#e1e1df')
game_name_rect = game_name.get_rect(center = (windows_width/2, 150))

control_info_button = pygame.transform.rotozoom(pygame.image.load('data/UI/Info_BTN.png').convert_alpha(), 0, 0.2)
control_info_button_rect = control_info_button.get_rect(center = (40, 40))

start_button = pygame.transform.rotozoom(pygame.image.load('data/UI/Start_BTN.png').convert_alpha(), 0, 0.4)
start_button_rect = start_button.get_rect(center = (windows_width/2, 300))

replay_button = pygame.transform.rotozoom(pygame.image.load('data/UI/Replay_BTN.png').convert_alpha(), 0, 0.4)
replay_button_rect = replay_button.get_rect(center = (windows_width/2, 200))

# Background
space_bg = pygame.image.load('data/Backgrounds/5532919.jpg').convert_alpha()
space_bg = pygame.transform.smoothscale(space_bg, (windows_width, windows_height))

# Difficulty notification
difficulty_notification = ""
notification_time = 0
notification_duration = 1.5  # seconds

# Game loop
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if running:
            if event.type == enemies_timer:
                enemies.add(Enemies(random.choice(['Bat', 'Bat' ,'fly-eye', 'fly-eye', 'fly-eye'])))
            if event.type == platform_timer:
                platform.add(Platform(random.randint(850, 950), random.randint(150, 400)))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k or event.key == pygame.K_SPACE:
                    current_time = time.time()
                    if current_time - last_bullet_time >= bullet_cooldown:
                        bullet.add(player.create_bullet())
                        last_bullet_time = current_time
                        # Track bullet fired for DDA
                        difficulty_manager.update_performance(score, bullet_fired=True)
            
    if running:
        screen.blit(space_bg, (0, 0))
        score = display_score(text_font, screen, start_time, windows_width)

        # Check Collision (Player Died or not)
        running = (
            collision_sprite(player_group, enemies, 40, platform, bullet, explode)
            and game_over(player_group, enemies, platform, bullet, explode)
        )

        # Played Died
        if not running:
            # Count death
            difficulty_manager.update_performance(score, is_death=True)

            # Adjust difficulty
            adjustment = difficulty_manager.adjust_difficulty()

            if adjustment == "EASIER":
                difficulty_notification = "DIFFICULTY DECREASED!"
                notification_time = score

                pygame.time.set_timer(
                    enemies_timer, difficulty_manager.enemy_spawn_rate
                )
                pygame.time.set_timer(
                    platform_timer, difficulty_manager.platform_spawn_rate
                )

        # Periodic adjustment while player still alive
        if running and score - last_dda_check >= dda_check_interval:
            adjustment = difficulty_manager.adjust_difficulty()
            last_dda_check = score

            if adjustment == "EASIER":
                difficulty_notification = "DIFFICULTY DECREASED!"
                notification_time = score

                pygame.time.set_timer(
                    enemies_timer, difficulty_manager.enemy_spawn_rate
                )
                pygame.time.set_timer(
                    platform_timer, difficulty_manager.platform_spawn_rate
                )

            elif adjustment == "HARDER":
                difficulty_notification = "DIFFICULTY INCREASED!"
                notification_time = score

                pygame.time.set_timer(
                    enemies_timer, difficulty_manager.enemy_spawn_rate
                )
                pygame.time.set_timer(
                    platform_timer, difficulty_manager.platform_spawn_rate
                )
        
        # Display difficulty info
        difficulty_text = small_font.render(f'DIFFICULTY: {difficulty_manager.get_difficulty_name()}', True, '#FFD700')
        difficulty_rect = difficulty_text.get_rect(topleft = (10, 10))
        screen.blit(difficulty_text, difficulty_rect)
        
        # Display stats
        stats = difficulty_manager.get_stats()
        kills_text = small_font.render(f'KILLS: {stats["enemies_killed"]}', True, '#e1e1df')
        kills_rect = kills_text.get_rect(topleft = (10, 30))
        screen.blit(kills_text, kills_rect)
        
        accuracy_text = small_font.render(f'ACC: {stats["accuracy"]}', True, '#e1e1df')
        accuracy_rect = accuracy_text.get_rect(topleft = (10, 50))
        screen.blit(accuracy_text, accuracy_rect)
        
        # Display difficulty change notification
        if difficulty_notification and score - notification_time < notification_duration:
            notif_text = text_font.render(difficulty_notification, True, '#FF4444')
            notif_rect = notif_text.get_rect(center = (windows_width/2, 150))
            screen.blit(notif_text, notif_rect)
        
        # Update sprite with dynamic difficulty
        player_group.update(windows_width)
        black_hole.update()
        bullet.update(explode, enemies, difficulty_manager, score)
        
        # Update enemies with dynamic speed
        for enemy in enemies:
            enemy.rect.x -= difficulty_manager.enemy_speed
            enemy.animate()
            enemy.destroy()
        
        # Update platforms with dynamic speed
        for plat in platform:
            plat.speed = difficulty_manager.platform_speed
            plat.rect.x -= plat.speed
            plat.destroy()
            
        explode.update()
        
        # Draw sprite
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
                    difficulty_manager.reset()
                    last_dda_check = 0
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
                    difficulty_manager.reset()
                    last_dda_check = 0
                    
    pygame.display.update()
    clock.tick(60) # limit fps to 60fps