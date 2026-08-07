import random
import pygame
from Itemslot import Itemslot
from item import item
import item_import
#Vielleicht später from player import balance

class shop(pygame.sprite.Sprite):

    def __init__(self, posx, posy, listItemSlots=None):
        super().__init__()

        if self.listItemSlots==None:
            self.listItemSlots=[Itemslot() for i in range(5)]
        else:
            self.listItemSlots=listItemSlots

        self.listItemSlots=listItemSlots
        self.image=pygame.image.load("images/shop.jpg")
        self.image=pygame.transform.smoothscale_by(self.image,(0.1,0.1))
        self.rect=self.image.get_rect()
        self.rect.x=posx
        self.rect.y=posy

        #Positionierung der Itemslots
        abstand=120
        for i,itemSlot in enumerate(self.listItemSlots):
            itemSlot.rect.x=posx +i*abstand
            itemSlot.rect.y=posy

        self.item_sprites = item.createItemSprites()

    
    def fillRandomItem(self,pools):
        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        for slot in self.listItemSlots:
            if slot.is_empty():
                wahl_rarity = random.choices(rarities) #später mit weigths wahrscheinlichkeiten für einzelne rarities festlegen
                pool = pools.get(wahl_rarity, [])
                if pool:
                    data = random.choice(pool)
                    #Erstellt ein Item-Objekt basierend auf den Daten aus dem Pool
                    sprite_idx = int(data["sprite_index"])
                    img = self.item_sprites[sprite_idx]
                    

                    new_item = item(
                        image=img,
                        name = data["name"],
                        name=data['name'],
                        posx=slot.rect.centerx,
                        posy=slot.rect.centery,
                        cost=data['cost'],
                        rarity=data['rarity'],
                        itemtype=data['itemtype'],
                        itemID=data['itemID'],
                        dmgVal=data['dmgVal'],
                        defVal=data['defVal'],
                        space_x=data['space_x'],
                        space_y=data['space_y']
                    )
                    slot.addItem(new_item)

    def refresh(self, player, pools):
        """Leert den Shop und befüllt ihn neu"""
        if player.gold >= self.refresh_cost:
            player.gold -= self.refresh_cost
            for slot in self.listItemSlots:
                slot.removeItem() # Slot leeren
            self.fillRandomItem(pools)
            return True
        return False
    """
    def fillItem(self, indexSlot, item):
        self.listItemSlots[indexSlot].addItem(item)

        maybe später um items zu locken
        """
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        for item_Slot in self.listItemSlots:
            item_Slot.draw(screen)