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

class Gift(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets\\images\\gift-45px.png')
        self.rect = self.image.get_rect()
        self.rect.x = 1024
        self.rect.bottom = 672

        self.speed = 5.5
        self.collect_sound = pygame.mixer.Sound('assets\\sound\\gift_collect .wav')
    def update(self):
        if self.rect.x > -100:
            self.rect.x -= self.speed
        else:
            self.kill()

    @staticmethod
    def collide():
        GAME['score'] += 1
        score_count.txt = f"{GAME['score']}"
        score_count.update()

pygame.init()

GAME = {
    'animation': False,
    'animation_speed': 0,
    'state': 'main_menu',
    'player_select': '',
    'score': 0
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
all_gifts = pygame.sprite.Group()
# custom event for adding a new Hurdle
ADDHURDLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDHURDLE, 5000)
# Color
WHITE = (255,255,255)

# Text For Menus
santa_rush_title = TEXT("Santa Rush", fontloc='snowfont', size=100)
play_title = TEXT("Play")
credits_title = TEXT("Credits")
Exit_title = TEXT("Exit")
Gameover_title = TEXT("Gameover", fontloc='snowfont', size=100)
play_again_title = TEXT("Play Again")
main_menu_title = TEXT("Main Menu")
pause_title = TEXT('Pause', fontloc='snowfont', size=100)
resume_title = TEXT('Resume')
restart_title = TEXT('Restart')
score_count = TEXT(f"{GAME['score']}", fontloc='shepherd')
t1 = TEXT('Created by')
t2 = TEXT('Nisheet Patel',fontloc='snowfont',size=100)
# Defalut Location of Text
santa_rush_title.txt_rect.center = (screen_width/2, 100)
play_title.txt_rect.center = (screen_width/2, 300)
credits_title.txt_rect.center = (screen_width/2, 360)
Exit_title.txt_rect.center = (screen_width/2, 420)
Gameover_title.txt_rect.center = (screen_width/2, -452)
play_again_title.txt_rect.center = (-40,350)
main_menu_title.txt_rect.center = (1064, 420)
pause_title.txt_rect.center = (screen_width/2,-452)
resume_title.txt_rect.center = (1062,350)
restart_title.txt_rect.center = (-40,420)
score_count.txt_rect.x = 50
score_count.txt_rect.y = 13
t1.txt_rect.center = (screen_width/4,-302)
t2.txt_rect.center = (screen_width/2, -202)

def Main_Game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        elif event.type == ADDHURDLE:
            if GAME['state'] == 'main_game':
                # Generate hurdles
                hurdle = Hurdle()
                hurdle.rect.x += random.randint(0,128) 
                all_hurdles.add(hurdle)
                all_sprites.add(hurdle)
                # generate Gifts
                for pos in [[256,384],[384,512],[512,640]]:    
                    if random.random() < 0.3:
                        gift = Gift()
                        gift.rect.x += random.randint(pos[0],pos[1])
                        all_sprites.add(gift)
                        all_gifts.add(gift)

    if pygame.sprite.spritecollide(player, all_hurdles, dokill=True):
        GAME['state'] = 'gameover'
        GAME['player_select'] = 'gameover'
        GAME['animation_speed'] = 0
        GAME['animation'] = True
    if pygame.sprite.spritecollide(player, all_gifts, dokill=True):
        Gift().collect_sound.play()
        Gift.collide()

    # Get user key pressed 
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_p]:    # Pause Game
        GAME['animation_speed'] = 0
        GAME['player_select'] = 'pause'
        GAME['animation'] = True
        GAME['state'] = 'pause'
    player.update(pressed_keys)

    all_hurdles.update()
    all_gifts.update()
    screen.blit(background, (0,0))
    screen.blit(snow_land, (0,672))
    
    # Gift Count Display
    screen.blit(Gift().image, (0,0))
    score_count.draw(screen)
    
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
            if play_title.txt_rect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'play'
            if Exit_title.txt_rect.collidepoint(mpos):
                pygame.quit()
                running = False
            elif credits_title.txt_rect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'credits'
    screen.blit(background, (0,0))

    if GAME['animation']:
        if GAME['player_select'] == "menu":
            GAME['animation_speed'] += -2
            if play_title.txt_rect.centerx >= (screen_width/2):
                GAME['animation'] = False
                GAME['animation_speed'] = 0
        else:
            GAME['animation_speed'] += 2
            if play_title.txt_rect.centerx < -30:
                GAME['animation'] = False
                if GAME['player_select'] == 'play':
                    GAME['state'] = 'main_game'
                elif GAME['player_select'] == 'credits':
                    GAME['state'] = 'credits'
                    GAME['animation'] = True
                    GAME['animation_speed'] = 0
        
        santa_rush_title.txt_rect.centery -= GAME['animation_speed']
        play_title.txt_rect.centerx -= GAME['animation_speed']
        credits_title.txt_rect.centerx += GAME['animation_speed']
        Exit_title.txt_rect.centerx -= GAME['animation_speed']
        # if y > 672: 
        #     y -= 5
        #     screen.blit(snow_land, (0,y))

    santa_rush_title.draw(screen)
    play_title.draw(screen)
    credits_title.draw(screen)
    Exit_title.draw(screen)
    pygame.display.flip()

def Gameover_Menu():
    main_menu_title.txt_rect.centery = 420
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if play_again_title.txt_rect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'play_again'
            elif main_menu_title.txt_rect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'menu'    
    screen.blit(background, (0,0))

    if GAME['animation']:
        if GAME['player_select'] == "gameover":
            GAME['animation_speed'] += -2
            if play_again_title.txt_rect.centerx >= (screen_width/2):
                GAME['animation'] = False
                GAME['animation_speed'] = 0
        else:
            GAME['animation_speed'] += 2
            if play_again_title.txt_rect.centerx < -30:
                GAME['animation'] = False
                if GAME['player_select'] == 'play_again':
                    GAME['state'] = 'main_game'
                elif GAME['player_select'] == 'menu':
                    GAME['state'] = 'main_menu'
                    GAME['animation'] = True
                    GAME['animation_speed'] = 0

    Gameover_title.txt_rect.centery -= GAME['animation_speed']
    play_again_title.txt_rect.centerx -= GAME['animation_speed']
    main_menu_title.txt_rect.centerx += GAME['animation_speed']

    Gameover_title.draw(screen)
    play_again_title.draw(screen)
    main_menu_title.draw(screen)
    pygame.display.flip()

def Pause_Menu():
    main_menu_title.txt_rect.centery = 490
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if resume_title.txt_rect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'resume'
            elif main_menu_title.txt_rect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'menu'
    screen.blit(background, (0,0))

    if GAME['animation']:
        if GAME['player_select'] == "pause":
            GAME['animation_speed'] += -2
            if restart_title.txt_rect.centerx >= (screen_width/2):
                GAME['animation'] = False
                GAME['animation_speed'] = 0
        else:
            GAME['animation_speed'] += 2
            if restart_title.txt_rect.centerx < -30:
                GAME['animation'] = False
                if GAME['player_select'] == 'resume':
                    GAME['state'] = 'main_game'
                elif GAME['player_select'] == 'menu':
                    GAME['state'] = 'main_menu'
                    GAME['animation'] = True
                    GAME['animation_speed'] = 0
    
    pause_title.txt_rect.centery -= GAME['animation_speed']
    resume_title.txt_rect.centerx += GAME['animation_speed']
    restart_title.txt_rect.centerx -= GAME['animation_speed']
    main_menu_title.txt_rect.centerx += GAME['animation_speed']

    pause_title.draw(screen)
    resume_title.draw(screen)
    restart_title.draw(screen)
    main_menu_title.draw(screen)
    pygame.display.flip()

def credits():
    main_menu_title.txt_rect.centery = 730
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            if main_menu_title.txt_rect.collidepoint(mpos):
                GAME['animation'] = True
                GAME['player_select'] = 'menu'
    
    if GAME['animation']:
        if GAME['player_select'] == "credits":
            GAME['animation_speed'] += -2
            if main_menu_title.txt_rect.centerx <= (screen_width/2):
                GAME['animation'] = False
                GAME['animation_speed'] = 0
        else:
            GAME['animation_speed'] += 2
            if main_menu_title.txt_rect.centerx > (screen_width):
                GAME['animation'] = False
                GAME['animation_speed'] = 0
                if GAME['player_select'] == 'menu':
                    GAME['state'] = 'main_menu'
                    GAME['animation'] = True
                    GAME['animation_speed'] = 0
    
    t1.txt_rect.centery -= GAME['animation_speed']
    t2.txt_rect.centery -= GAME['animation_speed']
    main_menu_title.txt_rect.centerx += GAME['animation_speed']
    screen.blit(background, (0,0))
    t1.draw(screen)
    t2.draw(screen)
    main_menu_title.draw(screen)
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
    elif GAME['state'] == 'credits':
        credits()
    clock.tick(60)