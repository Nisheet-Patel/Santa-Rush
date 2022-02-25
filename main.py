import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.current_santa_sprite = 0
        self.santa_sprites = []
        # load santa images
        for i in range(1,11):
            self.santa_sprites.append(
                pygame.image.load(f'assets\\images\\santa\\Run ({i}).png')
            )

        self.image = self.santa_sprites[self.current_santa_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 560

        self.gravity = 0

    def update(self,pressed_keys):
        self.current_santa_sprite += 0.3

        if self.current_santa_sprite >= 10:
            self.current_santa_sprite = 0

        self.image = self.santa_sprites[int(self.current_santa_sprite)]

        if pressed_keys[pygame.K_UP] and self.rect.y == 560:
            self.gravity -= 20
            
        # Gravity
        self.gravity += 2  # Fall speed
        self.rect.y += self.gravity

        print("gravity: ",self.gravity)
        if self.rect.y >= 560:
            self.gravity = 0
            self.rect.y = 560

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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    
    # Get user key pressed 
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    screen.blit(background, (0,0))
    screen.blit(snow_land, (0,672))
    
    all_sprites.draw(screen)
    

    pygame.display.flip()
    clock.tick(60)