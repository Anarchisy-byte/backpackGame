import pygame
import item
import backpack
import shop

class character(pygame.sprite.Sprite):
    
    def __init__(self, health=1, lv=1):
        super().__init__()
        self.image=pygame.image.load("images/character/7965103.png")
        self.rect=self.image.get_rect()
        self.health=health
        self.lv=lv
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class player(character):

    def __init__(self, health, lv, currency, backpack):
        super().__init__()
        self.health=health
        self.lv=lv
        self.currency=currency
        self.backpack=backpack

class enemy(character):
    def __init__(self, health, lv):
        super().__init_()
        self.health=health
        self.lv=lv
    
