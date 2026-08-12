import random
import pygame
from Itemslot import Itemslot
from item import item
import item_import
import rarity_odds

class shop(pygame.sprite.Sprite):

    def __init__(self, posx, posy, listItemSlots=[Itemslot() for i in range(5)]):
        super().__init__()
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
        self.refresh_cost=0

    def returnItemslots(self):
        return self.listItemSlots

    def fillRandomItem(self,curRound,pools=None):
        for slot in self.listItemSlots:
            if slot.is_empty():
                wahl_rarity = rarity_odds.roll_rarity(curRound)
                if pools is None:
                    pools=item_import.item_pools()
                pool = pools.get(wahl_rarity, [])
                if pool:
                    data = random.choice(pool)
                    #Erstellt ein Item-Objekt basierend auf den Daten aus dem Pool
                    sprite_idx = int(data["sprite_id"])
                    img = self.item_sprites[sprite_idx]
                    

                    new_item = item(
                        image=img,
                        name = data["name"],
                        #name=data['name'],
                        posx=slot.rect.centerx,
                        posy=slot.rect.centery,
                        cost=data['cost'],
                        rarity=data['rarity'],
                        itemtype=data['type'],
                        itemID=data['item_id'],
                        dmgVal=data['attack'],
                        defVal=data['armor'],
                        hpVal=data['hp'],
                        space_x=1,
                        space_y=1
                    )
                    slot.addItem(new_item)

    def refresh(self, player, curRound, pools=None):
        """Leert den Shop und befüllt ihn neu"""
        if player.gold >= self.refresh_cost:
            player.gold -= self.refresh_cost
            self.refresh_cost+=1
            for slot in self.listItemSlots:
                slot.removeItem() # Slot leeren
            self.fillRandomItem(curRound,pools=pools)
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