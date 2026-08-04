import pygame
import Itemslot

class backpack(pygame.sprite.Sprite):
    #https://www.pygame.org/docs/ref/sprite.html
    """Einfügen von Items in backpack über add
    entfernen über remove
    Anzeigen über pygame.sprite.RenderUpdates.draw()"""

    def __init__(self, rows, colom, posx, posy):
        super().__init__()
        self.sprites=[[None for i in range(colom)] for i in range(rows)]
        abstand=130
        for row in range(rows):
            for c in range(colom):
                self.sprites[row][c]=Itemslot.Itemslot(posx+abstand*row,posy+abstand*c)
        self.image=pygame.image.load("images/backpack-inventory1.png")
        self.rect=self.image.get_rect()
        self.rect.x=posx
        self.rect.y=posy
        self.layer=2

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        for row in self.sprites:
            for colom in row:
                colom.draw(screen)

