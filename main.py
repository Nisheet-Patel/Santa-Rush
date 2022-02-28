import pygame
import random
import debug
from Text import TEXT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.is_jumping = False
        self.is_sliding = False

        self.land = 565
        self.sprite_count = 0
        self.current_santa_sprite = 0
        self.santa_running_sprites = []
        self.santa_jump_sprites = []
        self.santa_slide_sprites = []

        # load santa running images
        for i in range(1,12):
            self.santa_running_sprites.append(
                pygame.image.load(f'assets\\images\\santa\\Run ({i}).png')
            )

        # Load santa jump images
        for i in range(1,17):
            self.santa_jump_sprites.append(
                pygame.image.load(f'assets\\images\\santa\\Jump ({i}).png')
            )

        # Load santa slide images
        for i in range(1,12):
            self.santa_slide_sprites.append(
                pygame.image.load(f'assets\\images\\santa\\Slide ({i}).png')
            )

        self.image = self.santa_running_sprites[self.current_santa_sprite]
        self.rect = self.image.get_rect()
        # player x,y
        self.rect.x = 300
        self.rect.y = self.land

        self.gravity = 0
        self.speed = 0.4

    def update(self,pressed_keys):
        if pressed_keys[pygame.K_UP] and self.rect.y == self.land:
            self.gravity -= 23
            self.is_jumping = True
            self.is_running = False
            self.current_santa_sprite = 0
            self.speed = 0.5
        elif pressed_keys[pygame.K_DOWN] and self.is_running:
            self.is_sliding = True
            self.is_running = False
        else:
            self.is_sliding = False

        self.current_santa_sprite += self.speed

        if self.current_santa_sprite >= self.sprite_count:
            self.current_santa_sprite = 0

        if self.is_running:
            self.land = 565
            self.sprite_count = 10
            self.image = self.santa_running_sprites[int(self.current_santa_sprite)]
            
        elif self.is_jumping:
            self.sprite_count = 15
            self.image = self.santa_jump_sprites[int(self.current_santa_sprite)]
        
        elif self.is_sliding:
            self.sprite_count = 10
            self.image = self.santa_slide_sprites[int(self.current_santa_sprite)]
            self.land = 600
            self.rect.y = self.land
        # Debug
        # print(self.is_running,self.is_jumping,self.is_sliding)
        
        # Gravity
        self.gravity += 1  # Fall speed
        self.rect.y += self.gravity

        if self.rect.y >= self.land:
            self.gravity = 0
            self.rect.y = self.land

            self.is_jumping = False
            self.is_running = True
            self.speed = 0.4

# Load all Hurdel images
hurdel_sprites = [
    pygame.image.load('assets\\images\\Hurdle\\SnowMan.png'),
    pygame.image.load('assets\\images\\Hurdle\\IceBox.png'),
    pygame.image.load('assets\\images\\Hurdle\\Stone.png'),
    pygame.image.load('assets\\images\\Hurdle\\Crystal.png'),
    [
        pygame.image.load('assets\\images\\Hurdle\\snowball\\snowball_01.png'),
        pygame.image.load('assets\\images\\Hurdle\\snowball\\snowball_02.png'),
        pygame.image.load('assets\\images\\Hurdle\\snowball\\snowball_03.png'),
        pygame.image.load('assets\\images\\Hurdle\\snowball\\snowball_04.png'),
        pygame.image.load('assets\\images\\Hurdle\\snowball\\snowball_05.png'),
        pygame.image.load('assets\\images\\Hurdle\\snowball\\snowball_06.png')
    ]
]

class Hurdle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.current_sprite = 0  # For snow ball animation
        self.sc = random.randint(0,4)
        
        if self.sc != 4:
            self.image = hurdel_sprites[self.sc]
        else:
            self.image = hurdel_sprites[self.sc][self.current_sprite]
        
        self.rect = self.image.get_rect()
        if self.sc == 4:
            self.rect.bottom = 590
        else:
            self.rect.bottom = 672
        self.rect.x = 1024

        self.speed = 5.5

    def update(self):
        if self.sc == 4:
            self.current_sprite += 0.2  # animation speed
            if self.current_sprite > 5:
                self.current_sprite = 0
            self.image = hurdel_sprites[self.sc][int(self.current_sprite)]
            # Follow Player
            if player.is_jumping and self.rect.x > player.rect.x:
                self.rect.y = player.rect.y
        
        if self.rect.x > -100:
            self.rect.x -= self.speed
        else:
            self.kill()

pygame.init()

GAME = {
    'animation': False,
    'animation_speed': 0,
    'state': 'main_menu',
    'player_select': ''
}
# Variables
screen_width = 1024
screen_height = 800
# Loaded Images
snow_land = pygame.image.load('assets\\images\\snow_land.png')
background = pygame.image.load('assets\\images\\BG.png')
# Setup
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
# sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
all_hurdles = pygame.sprite.Group()
# custom event for adding a new Hurdle
ADDHURDLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDHURDLE, 2000)
# Color
WHITE = (255,255,255)


# Text For Menus
santa_rush_title = TEXT("Santa Rush", 'snowfont', WHITE)
play_title = TEXT("Play", 'yolissa', WHITE)
credits_title = TEXT("Credits", 'yolissa', WHITE)
Exit_title = TEXT("Exit", 'yolissa', WHITE)
Gameover_title = TEXT("Gameover", 'snowfont', WHITE)
play_again_title = TEXT("Play Again", 'yolissa', WHITE)
main_menu_title = TEXT("Main Menu", 'yolissa', WHITE)
pause_title = TEXT('Pause', 'snowfont', WHITE)
resume_title = TEXT('Resume', 'yolissa', WHITE)
restart_title = TEXT('Restart', 'yolissa', WHITE)
# Defalut Location of Text
santa_rush_title.textRect.center = (screen_width/2, 100)
play_title.textRect.center = (screen_width/2, 300)
credits_title.textRect.center = (screen_width/2, 360)
Exit_title.textRect.center = (screen_width/2, 420)
Gameover_title.textRect.center = (screen_width/2, -452)
play_again_title.textRect.center = (-40,350)
main_menu_title.textRect.center = (1064, 420)
pause_title.textRect.center = (screen_width/2,-452)
resume_title.textRect.center = (1062,350)
restart_title.textRect.center = (-40,420)

def Main_Game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        elif event.type == ADDHURDLE:
            if len(all_sprites)-1 < 2:  # max 2 hurdle on screen
                new_hurdle = Hurdle()
                new_hurdle.rect.x += random.randint(20, 500) 
                all_sprites.add(new_hurdle)
                all_hurdles.add(new_hurdle)
            
    if pygame.sprite.spritecollide(player, all_hurdles, dokill=True):
        GAME['state'] = 'gameover'
        GAME['player_select'] = 'gameover'
        GAME['animation_speed'] = 0
        GAME['animation'] = True
    # Get user key pressed 
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_p]:    # Pause Game
        GAME['animation_speed'] = 0
        GAME['player_select'] = 'pause'
        GAME['animation'] = True
        GAME['state'] = 'pause'
    player.update(pressed_keys)
    all_hurdles.update()

    screen.blit(background, (0,0))
    screen.blit(snow_land, (0,672))
    
    all_sprites.draw(screen)
    # debug.draw_mid_points(screen, player)
    pygame.display.flip()

def Main_Menu():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if play_title.textRect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'play'
            if Exit_title.textRect.collidepoint(mpos):
                pygame.quit()
                running = False
    screen.blit(background, (0,0))

    if GAME['animation']:
        if GAME['player_select'] == "menu":
            GAME['animation_speed'] += -2
            if play_title.textRect.centerx >= (screen_width/2):
                GAME['animation'] = False
                GAME['animation_speed'] = 0
        else:
            GAME['animation_speed'] += 2
            if play_title.textRect.centerx < -30:
                GAME['animation'] = False
                if GAME['player_select'] == 'play':
                    GAME['state'] = 'main_game'
        
        santa_rush_title.textRect.centery -= GAME['animation_speed']
        play_title.textRect.centerx -= GAME['animation_speed']
        credits_title.textRect.centerx += GAME['animation_speed']
        Exit_title.textRect.centerx -= GAME['animation_speed']
        # if y > 672: 
        #     y -= 5
        #     screen.blit(snow_land, (0,y))

    santa_rush_title.update(screen)
    play_title.update(screen)
    credits_title.update(screen)
    Exit_title.update(screen)
    pygame.display.flip()

def Gameover_Menu():
    main_menu_title.textRect.centery = 420
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if play_again_title.textRect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'play_again'
            elif main_menu_title.textRect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'menu'    
    screen.blit(background, (0,0))

    if GAME['animation']:
        if GAME['player_select'] == "gameover":
            GAME['animation_speed'] += -2
            if play_again_title.textRect.centerx >= (screen_width/2):
                GAME['animation'] = False
                GAME['animation_speed'] = 0
        else:
            GAME['animation_speed'] += 2
            if play_again_title.textRect.centerx < -30:
                GAME['animation'] = False
                if GAME['player_select'] == 'play_again':
                    GAME['state'] = 'main_game'
                elif GAME['player_select'] == 'menu':
                    GAME['state'] = 'main_menu'
                    GAME['animation'] = True
                    GAME['animation_speed'] = 0

    Gameover_title.textRect.centery -= GAME['animation_speed']
    play_again_title.textRect.centerx -= GAME['animation_speed']
    main_menu_title.textRect.centerx += GAME['animation_speed']

    Gameover_title.update(screen)
    play_again_title.update(screen)
    main_menu_title.update(screen)
    pygame.display.flip()

def Pause_Menu():
    main_menu_title.textRect.centery = 490
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if resume_title.textRect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'resume'
            elif main_menu_title.textRect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'menu'
    screen.blit(background, (0,0))

    if GAME['animation']:
        if GAME['player_select'] == "pause":
            GAME['animation_speed'] += -2
            if restart_title.textRect.centerx >= (screen_width/2):
                GAME['animation'] = False
                GAME['animation_speed'] = 0
        else:
            GAME['animation_speed'] += 2
            if restart_title.textRect.centerx < -30:
                GAME['animation'] = False
                if GAME['player_select'] == 'resume':
                    GAME['state'] = 'main_game'
                elif GAME['player_select'] == 'menu':
                    GAME['state'] = 'main_menu'
                    GAME['animation'] = True
                    GAME['animation_speed'] = 0
    
    pause_title.textRect.centery -= GAME['animation_speed']
    resume_title.textRect.centerx += GAME['animation_speed']
    restart_title.textRect.centerx -= GAME['animation_speed']
    main_menu_title.textRect.centerx += GAME['animation_speed']

    pause_title.update(screen)
    resume_title.update(screen)
    restart_title.update(screen)
    main_menu_title.update(screen)
    pygame.display.flip()

running = True
while running:
    if GAME['state'] == 'main_menu':
        Main_Menu()
    elif GAME['state'] == 'main_game':
        Main_Game()
    elif GAME['state'] == 'gameover':
        Gameover_Menu()
    elif GAME['state'] == 'pause':
        Pause_Menu()
    clock.tick(60)