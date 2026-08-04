import pygame
class backpack(pygame.sprite.Group):
    #https://www.pygame.org/docs/ref/sprite.html
    """Einfügen von Items in backpack über add
    entfernen über remove
    Anzeigen über pygame.sprite.RenderUpdates.draw()"""

    def __init__(self, sprites:"Verschiedene Items vom Typ Sprite"):
        super().__init__(self)
        self.sprites=sprites

