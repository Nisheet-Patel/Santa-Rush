import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.is_jumping = False
        self.is_sliding = False

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
        self.rect.x = 200
        self.rect.y = 560

        self.gravity = 0
        self.speed = 0.4

    def update(self,pressed_keys):

        if pressed_keys[pygame.K_UP] and self.rect.y == 560:
            self.gravity -= 20
            self.is_jumping = True
            self.is_running = False
            self.current_santa_sprite = 0
            self.speed = 0.9
        if pressed_keys[pygame.K_DOWN]:
            self.is_sliding = True
            self.is_running = False
        else:
            self.is_sliding = False
            self.is_running = True

        self.current_santa_sprite += self.speed

        if self.current_santa_sprite >= self.sprite_count:
            self.current_santa_sprite = 0

        if self.is_running:
            self.sprite_count = 10
            self.image = self.santa_running_sprites[int(self.current_santa_sprite)]
            
        elif self.is_jumping:
            self.sprite_count = 15
            self.image = self.santa_jump_sprites[int(self.current_santa_sprite)]
        
        elif self.is_sliding:
            self.sprite_count = 10
            self.image = self.santa_slide_sprites[int(self.current_santa_sprite)]

        # Gravity
        self.gravity += 1  # Fall speed
        self.rect.y += self.gravity

        if self.rect.y >= 560:
            self.gravity = 0
            self.rect.y = 560

            self.is_jumping = False
            self.is_running = True
            self.speed = 0.4

# Load all Hurdel images
hurdel_sprites = [
    pygame.image.load('assets\\images\\Hurdle\\SnowMan.png'),
    pygame.image.load('assets\\images\\Hurdle\\IceBox.png'),
    pygame.image.load('assets\\images\\Hurdle\\Stone.png'),
    pygame.image.load('assets\\images\\Hurdle\\Crystal.png')
]

class Hurdle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = hurdel_sprites[random.randint(0,3)]
        self.rect = self.image.get_rect()
        self.rect.bottom = 672
        self.rect.x = 1024

        self.speed = 5.5

    def update(self):
        if self.rect.x > -100:
            self.rect.x -= self.speed
        else:
            self.kill()

pygame.init()

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


running = True
while running:
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

    # Get user key pressed 
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    all_hurdles.update()

    screen.blit(background, (0,0))
    screen.blit(snow_land, (0,672))
    
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)