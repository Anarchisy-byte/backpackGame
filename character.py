import pygame
import item
import item_import
import backpack
import shop
import random

class character(pygame.sprite.Sprite):
    
    def __init__(self, health=1, lv=1):
        Sheet=pygame.image.load("images/character/7965103.jpg").convert_alpha()
        print(Sheet.get_width(), Sheet.get_height())
        super().__init__()
        
        Sprites=[]
        S_width=500
        s_height=Sheet.get_height()
        row=0
        for row in range(Sheet.get_width()//S_width):
            x=row*S_width
            y=0
            img=pygame.Rect(x,y, S_width, s_height)
            sprite_img=Sheet.subsurface(img)
            sprite_img=pygame.transform.scale_by(sprite_img,0.3)
            Sprites.append(sprite_img)

        self.image=Sprites[2]
        self.rect=self.image.get_rect()
        self.health=health
        self.maxhealth=health #health sprite object?? --> Anzeigen der Hp
        self.health_sprite=None
        self.lv=lv

    def updateHealthSprite(self):
        width=3*self.health*3
        height=5
        surf=pygame.Surface((width,height))
        surf.fill("RED")
        if(self.health_sprite is None):
            self.health_sprite=pygame.sprite.Sprite()
        self.health_sprite.image=surf
        self.health_sprite.rect=self.health_sprite.image.get_rect(topleft=(self.rect.x, self.rect.y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.backpack.draw(screen)
        self.updateHealthSprite()
        screen.blit(self.health_sprite.image, self.health_sprite.rect)
    
    def attack(self, gegner):
        for slot in self.backpack.sprites:
            for itemslot in slot:
                if itemslot.item is not None:
                    gegner.health-=itemslot.item.dmgVal
        gegner.health-=1

class player(character):

    def __init__(self, health, lv, gold, backpack):
        super().__init__()
        self.health=health
        self.maxhealth=health
        self.lv=lv
        self.gold=gold
        self.backpack=backpack
        self.rect.x=600
        self.rect.y=500

class enemy(character):
    def __init__(self, health, lv):
        super().__init__()
        self.health=health
        self.maxhealth=health
        self.lv=lv
        self.rect.x=1050
        self.rect.y=500
        self.backpack=backpack.backpack(3,2,1300,600)

        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        for arr in self.backpack.sprites:
            for slot in arr:
                wahl_rarity = random.choices(rarities) #später mit weigths wahrscheinlichkeiten für einzelne rarities festlegen
                pools=item_import.itempools.item_pools()
                pool = pools.get(wahl_rarity[0], [])
                if pool:
                    data = random.choice(pool)
                    #Erstellt ein Item-Objekt basierend auf den Daten aus dem Pool
                    sprite_idx = int(data["sprite_id"])
                    item_sprites=item.item.createItemSprites()
                    img = item_sprites[sprite_idx]
                        
                    new_item = item.item(
                        image=img,
                        name = data["name"],
                        posx=slot.rect.centerx,
                        posy=slot.rect.centery,
                        cost=data['cost'],
                        rarity=data['rarity'],
                        itemtype=data['type'],
                        itemID=data['item_id'],
                        dmgVal=data['attack'],
                        defVal=data['armor'],
                        space_x=1,
                        space_y=1
                    )
                    slot.addItem(new_item)
    
