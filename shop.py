import pygame
import Itemslot
import item
import item_import
#Vielleicht später from player import balance

class shop(pygame.sprite.Sprite):

    def __init__(self, posx, posy, listItemSlots=[Itemslot.Itemslot() for i in range(5)]):
        self.listItemSlots=listItemSlots
        self.image=pygame.image.load("images/shop.jpg")
        self.image=pygame.transform.smoothscale_by(self.image,(0.1,0.1))
        self.rect=self.image.get_rect()
        self.rect.x=posx
        self.rect.y=posy
        abstand=120
        for i,itemSlot in enumerate(self.listItemSlots):
            itemSlot.rect.x=posx +i*abstand
            itemSlot.rect.y=posy
    """
    def fillRandomItem(self):
        for item_slot in self.listItemSlots:
            item_slot.addItem()
    """

    def fillItem(self, indexSlot, item):
        self.listItemSlots[indexSlot].addItem(item)

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        for item_Slot in self.listItemSlots:
            item_Slot.draw(screen)
    
    def returnItemslots(self):
        return self.listItemSlots