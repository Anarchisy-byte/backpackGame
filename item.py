import pygame
class item(pygame.sprite.Sprite):
    def __init__(self, color, width, height, img, posx, posy):
        super().__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.posx=posx
        self.posy=posy
        self.img=img
    
    def update(self, screen):
        pass