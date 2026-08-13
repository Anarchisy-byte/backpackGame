import random
import pygame
from Itemslot import Itemslot
from item import item
import item_import
import rarity_odds

class shop(pygame.sprite.Sprite):

    def __init__(self, listItemSlots=None):
        super().__init__()
        if listItemSlots is None:
            listItemSlots=[Itemslot() for i in range(5)]
        self.listItemSlots=listItemSlots

        #parameter für itemboxen im shop
        top_y=270
        bottom_y=420
        top_x=[1270,1440,1610]
        bottom_x=[1355,1525]
        positions=[(top_x[0],top_y),(top_x[1],top_y),(top_x[2],top_y),
                   (bottom_x[0],bottom_y),(bottom_x[1],bottom_y)]
        for slot,(x,y) in zip(self.listItemSlots,positions):
            slot.rect.centerx=x
            slot.rect.centery=y

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
                        space_y=1,
                        atkSpeed=data['cooldown']
                    )
                    slot.addItem(new_item)

    def refresh(self, player, curRound, pools=None):
        """Leert den Shop und befüllt ihn neu, gesperrte Slots bleiben erhalten"""
        if player.gold >= self.refresh_cost:
            player.gold -= self.refresh_cost
            self.refresh_cost+=1
            for slot in self.listItemSlots:
                if not slot.locked:
                    slot.removeItem() 
            self.fillRandomItem(curRound,pools=pools)
            return True
        return False

    def draw(self,screen):
        for item_Slot in self.listItemSlots:
            item_Slot.draw(screen)