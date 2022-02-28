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
    'status': 'main_menu',
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

# Text For Menu
santa_rush_title = TEXT("Santa Rush", 'snowfont', (255,255,255))
play_title = TEXT("Play", 'yolissa', (255,255,255))
credits_title = TEXT("Credits", 'yolissa', (255,255,255))
Exit_title = TEXT("Exit", 'yolissa', (255,255,255))
# Defalut Location of Text
santa_rush_title.textRect.center = (screen_width/2, 100)
play_title.textRect.center = (screen_width/2, 300)
credits_title.textRect.center = (screen_width/2, 360)
Exit_title.textRect.center = (screen_width/2, 420)

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
        GAME['status'] = 'main_menu'
    # Get user key pressed 
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_p]:    # Pause Game
        GAME['animation_speed'] = 0
        GAME['player_select'] = 'menu'
        GAME['animation'] = True
        GAME['status'] = 'main_menu'
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
                    GAME['status'] = 'main_game'
        
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

running = True
while running:
    if GAME['status'] == 'main_menu':
        Main_Menu()
    elif GAME['status'] == 'main_game':
        Main_Game()

    clock.tick(60)