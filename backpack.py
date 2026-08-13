import pygame
import Itemslot

class backpack(pygame.sprite.Sprite):
    #https://www.pygame.org/docs/ref/sprite.html


    def __init__(self, rows, colom, posx, posy):
        super().__init__()
        self.image=pygame.image.load("images/backpack.png")
        self.image=pygame.transform.scale_by(self.image,(1.3,2))

        #Manuelle anpassung der itemslots im Rucksack
        abstand=110
        box_size=110
        left_offset=130
        top_offset=140

        self.abstand=abstand
        self.sprites=[[None for i in range(colom)] for i in range(rows)]
        self.rows=rows
        self.colom=colom
        for row in range(rows):
            for c in range(colom):
                self.sprites[row][c]=Itemslot.Itemslot(posx+left_offset+abstand*c,posy+top_offset+abstand*row,size=box_size)
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
        slot=self.sprites[row][c]
        slot.addItem(sprite)
        #Item-Sprite an die (ggf. kleinere) Rucksack-Slot-Größe anpassen --
        #im Shop soll die ursprüngliche Größe erhalten bleiben, daher erst hier skalieren
        target=int(self.abstand*0.85)
        sprite.image=pygame.transform.smoothscale(sprite.image,(target,target))
        sprite.rect=sprite.image.get_rect(center=slot.rect.center)
        return slot