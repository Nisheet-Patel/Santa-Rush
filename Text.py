import pygame

class TEXT:
    def __init__(self, text, font, color):
        if font == 'snowfont':
            snow_font = pygame.font.Font('assets\\fonts\\SnowtopCaps.otf', 100)
            self.textbox = snow_font.render(text, True, color)
            self.textRect = self.textbox.get_rect()
        elif font == 'yolissa':
            yolissa_font = pygame.font.Font('assets\\fonts\\Yolissa Demo.ttf', 50)
            self.textbox = yolissa_font.render(text, True, color)
            self.textRect = self.textbox.get_rect()

    def update(self,screen):
        screen.blit(self.textbox, self.textRect)
    
    