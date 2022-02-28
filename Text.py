import pygame

font_location = {
    'snowfont': 'assets\\fonts\\SnowtopCaps.otf',
    'yolissa': 'assets\\fonts\\Yolissa Demo.ttf',
    'shepherd': 'assets\\fonts\\ShepherdFreehand-Regular.ttf'
}

class TEXT:
    def __init__(self, txt, fontloc='yolissa', fg=(255,255,255), size=50):
        self.txt = txt
        self.fontloc = font_location[fontloc]
        self.fg = fg
        self.size = size
        
        self.font = pygame.font.Font(self.fontloc, self.size)
        self.txt_surf = self.font.render(self.txt, True, self.fg)
        self.txt_rect = self.txt_surf.get_rect()

    def update(self):
        self.txt_surf = self.font.render(self.txt, True, self.fg)

    def draw(self,screen):
        screen.blit(self.txt_surf, self.txt_rect)
    