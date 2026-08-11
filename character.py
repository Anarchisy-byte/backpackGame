import pygame
import item
import item_import
import backpack
import shop
import random

class character(pygame.sprite.Sprite):
    
    def __init__(self, health=1, lv=1):
        
        #print(Sheet.get_width(), Sheet.get_height())
        super().__init__()
        
        self.imgSprites=self.character_sprites()
        self.image=self.imgSprites[random.randint(0,len(self.imgSprites)-1)]
        self.rect=self.image.get_rect()
        self.health=health
        self.maxhealth=health #health sprite object?? --> Anzeigen der Hp
        self.health_sprite=None
        self.lv=lv
        self.armor=0
        self.armor_sprite=None

    def character_sprites(self):
        imgSprites=[]
        Sheet=pygame.image.load("images/character/flat-design-pixel-art-character-element-collection.png").convert_alpha()
        img=pygame.Rect(145,213, 391, 982)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,0.3)
        imgSprites.append(sprite_img)
        img=pygame.Rect(585,232, 392, 963)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,0.3)
        imgSprites.append(sprite_img)
        img=pygame.Rect(1007,136, 427, 1059)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,0.3)
        imgSprites.append(sprite_img)
        img=pygame.Rect(1466,213, 390, 982)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,0.3)
        imgSprites.append(sprite_img)
        return imgSprites

    def updateHealthSprite(self):
        width=3*self.health*3
        height=5
        surf=pygame.Surface((width,height))
        surf.fill("RED")
        if(self.health_sprite is None):
            self.health_sprite=pygame.sprite.Sprite()
        self.health_sprite.image=surf
        self.health_sprite.rect=self.health_sprite.image.get_rect(topleft=(self.rect.x, self.rect.y))
    
    def updateArmorSprite(self):
        if(self.armor>0):
            width=3*self.armor*3
            if(width>150):
                width=150
            height=5
            surf=pygame.Surface((width,height))
            surf.fill("GRAY")
            if(self.armor_sprite is None):
                self.armor_sprite=pygame.sprite.Sprite()
            self.armor_sprite.image=surf
            self.armor_sprite.rect=self.armor_sprite.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.backpack.draw(screen)
        self.updateHealthSprite()
        screen.blit(self.health_sprite.image, self.health_sprite.rect)
        if(self.armor!=0):
            self.updateArmorSprite()
            screen.blit(self.armor_sprite.image, self.armor_sprite.rect)
    
    def attack(self, gegner):
        sum=0
        for slot in self.backpack.sprites:
            for itemslot in slot:
                if itemslot.item is not None:
                    if(gegner.armor<=0):
                        gegner.health-=itemslot.item.dmgVal
                        sum+=itemslot.item.dmgVal
                    else:
                        gegner.armor-=itemslot.item.dmgVal
                        sum+=itemslot.item.dmgVal
                else:
                    if(gegner.armor<=0):
                        gegner.health-=1
                        sum+=1
                    else:
                        gegner.armor-=1
                        sum+=1
        return sum
    
    def defense(self):
        self.armor=0
        for slot in self.backpack.sprites:
            for itemslot in slot:
                if itemslot.item is not None:
                    self.armor+=itemslot.item.defVal
        if(self.armor==0):
            return
        self.armor*=int(0.1*self.maxhealth)
        self.armor=int(self.armor)
        width=3*self.armor*3
        height=5
        surf=pygame.Surface((width,height))
        surf.fill("GRAY")
        if(self.armor_sprite is None):
            self.armor_sprite=pygame.sprite.Sprite()
        self.armor_sprite.image=surf
        self.armor_sprite.rect=self.armor_sprite.image.get_rect(topleft=(self.rect.x, self.rect.y))

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
    
