import pygame
import Itemslot
import item
import item_import
#Vielleicht später from player import balance

class shop(pygame.sprite.Sprite):

    def __init__(self, posx, posy, listItemSlots):
        self.listItemSlots=listItemSlots
        abstand=120
        for i,itemSlot in enumerate(self.listItemSlots):
            itemSlot.rect.x=posx +i*abstand
            itemSlot.rect.y=posy
    
    def fillItem(self, indexSlot, item):
        self.listItemSlots[indexSlot].addItem(item)
        #self.listItemSlots[indexSlot].draw(screen)