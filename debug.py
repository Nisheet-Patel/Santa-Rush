import pygame


def draw_mid_points(screen, obj):
    pygame.draw.circle(screen, (255,255,255), obj.rect.midtop, 5)
    pygame.draw.circle(screen, (255,255,255), obj.rect.midleft, 5)
    pygame.draw.circle(screen, (255,255,255), obj.rect.midbottom, 5)
    pygame.draw.circle(screen, (255,255,255), obj.rect.midright, 5)
    pygame.draw.circle(screen, (255,255,255), obj.rect.topleft, 5)
    pygame.draw.circle(screen, (255,255,255), obj.rect.bottomleft, 5)
    pygame.draw.circle(screen, (255,255,255), obj.rect.topright, 5)
    pygame.draw.circle(screen, (255,255,255), obj.rect.bottomright, 5)
    pygame.draw.circle(screen, (255,255,255), obj.rect.center, 5)