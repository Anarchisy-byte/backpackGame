import pygame
class item(pygame.sprite.Sprite):
    def __init__(self, image, name, posx,posy):
        super().__init__(self)
        self._image = image
        self.rect = image.get_rect()
        self.rect.x=posx
        self.rect.y=posy

    
    def update(self, screen):
        ...

    def draw(self,screen):
        screen.blit(self.image, self.rect)