import pygame
class item(pygame.sprite.Sprite):
    def __init__(self, image, name, position:"tuple"):
        super().__init__(self)
        self._image = image
        self.rect = image.get_rect(topleft=position)
        self.render()

    
    def update(self, screen):
        ...

    def render():
        ...