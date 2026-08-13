import pygame
class Itemslot(pygame.sprite.Sprite):
    def __init__(self,posx=0, posy=0, size=None):
        super().__init__()

        #itemSlot soll ein Item halten können
        self.item=None

        #Attribute zum anzeigen lassen
        self.image=pygame.image.load("images/box/boxNormal.png")
        if size is not None:
            #nur der Rucksack übergibt eine Zielgröße, damit seine Slots ins
            #(unveränderte) Rucksack-Sprite passen -- der Shop bleibt unangetastet
            self.image=pygame.transform.smoothscale(self.image,(size,size))
        self.rect=self.image.get_rect()
        self.rect.x=posx
        self.rect.y=posy
        self._layer=1

    def addItem(self,sprite):
        self.item=sprite
        self.item.rect=self.item.image.get_rect(center=self.rect.center)

    def removeItem(self):
        self.item=None

#zwei Mal selbe Methode --> korregiere später
    def checkItem(self):
        if(self.item==None):
            return False
        return True

    def is_empty(self):
        return (self.item==None)

    def move(self):
        pass

    def canbuyItem(self, money):
        if(self.checkItem() and self.item.cost<=money):
            return True
        return False

    def buyItem(self):
        item=self.item
        self.item=None

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        if (self.checkItem()):
            screen.blit(self.item.image, self.item.rect)
