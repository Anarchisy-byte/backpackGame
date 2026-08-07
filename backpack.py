import pygame
import Itemslot

class backpack(pygame.sprite.Sprite):
    #https://www.pygame.org/docs/ref/sprite.html

    def __init__(self, rows, colom, posx, posy):
        super().__init__()
        self.sprites=[[None for i in range(colom)] for i in range(rows)]
        abstand=130
        self.rows=rows
        self.colom=colom
        for row in range(rows):
            for c in range(colom):
                self.sprites[row][c]=Itemslot.Itemslot(posx+abstand*row,posy+abstand*c)
        self.image=pygame.image.load("images/backpack-inventory1.png")
        self.image=pygame.transform.scale_by(self.image,(2,2))
        self.rect=self.image.get_rect()
        self.rect.x=posx
        self.rect.y=posy
        self.layer=2

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        for row in self.sprites:
            for colom in row:
                colom.draw(screen)

    def returnItemslots(self):
        return self.sprites

    def removeItem(self, item):
        for row in range(self.rows):
            for c in range(self.colom):
                if(item==self.sprites[row][c].item):
                    self.sprites[row][c].item=None

    def get_empty_slot(self):
        for row in range(self.rows):
            for c in range(self.colom):
                if(self.sprites[row][c].item is None):
                    return (row,c)
    
    def addItem(self,sprite):
        row,c=self.get_empty_slot()
        self.sprites[row][c].addItem(sprite)