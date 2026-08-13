import pygame
import item
import item_import
import backpack
import shop
import random
import rarity_odds

class character(pygame.sprite.Sprite):
    
    def __init__(self, health=1, lv=1):
        
        #print(Sheet.get_width(), Sheet.get_height())
        super().__init__()
        
        self.imgSprites=self.character_sprites()
        self.image=self.imgSprites[random.randint(0,len(self.imgSprites)-1)]
        self.rect=self.image.get_rect()
        self.base_health=health
        self.health=health
        self.maxhealth=health #health sprite object?? --> Anzeigen der Hp
        self.health_sprite=None
        self.lv=lv
        self.armor=0
        self.armor_sprite=None

    def character_sprites(self):
        imgSprites=[]
        Sheet=pygame.image.load("images/character/oga_preview.png")
        img=pygame.Rect(16,206, 51, 53)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(89,209, 35, 48)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(154,209, 23, 48)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(214,210, 26, 47)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(341,210, 43, 49)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(403,210, 23, 47)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(28,476, 43, 48)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(90,476, 44, 46)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(139,477, 53, 46)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(204,477, 53, 46)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(273,473, 36, 50)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(328,477, 54, 46)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(12,82, 50, 53)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(84,85, 35, 48)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(155,85, 23, 48)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(217,86, 26, 47)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(270,86, 34, 47)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(322,86, 43, 49)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(404,86,23,47)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(8,351, 44, 49)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(70,351, 44, 47)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(140,352, 54, 47)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(200,352, 53, 37)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(277,348, 36, 51)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        img=pygame.Rect(324,352, 54, 47)
        sprite_img=Sheet.subsurface(img)
        sprite_img=pygame.transform.scale_by(sprite_img,8)
        imgSprites.append(sprite_img)
        return imgSprites

    def updateHealthSprite(self):
        width=self.health
        if(width>150):
            width=150
        height=40
        
        surf=pygame.Surface((150,height),pygame.SRCALPHA)
        hpSurf=surf.subsurface((0, height-10, width, 10))
        hpSurf.fill("RED")
        textfont=pygame.font.Font(None,36)
        if(self.armor>0):
            text="Armor:"+str(self.armor)
            col="grey"
        else:
            text="Health"+str(self.health)
            col="white"
        textsurf=textfont.render(text, True, col, "black")
        surf.blit(textsurf,textsurf.get_rect(center=(150//2, 18)))
        if(self.health_sprite is None):
            self.health_sprite=pygame.sprite.Sprite()
        self.health_sprite.image=surf
        self.health_sprite.rect=self.health_sprite.image.get_rect(topleft=(self.rect.x, self.rect.y-50))
    
    def updateArmorSprite(self):
        if(self.armor>0):
            width=self.armor
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
    
    def reset_cooldowns(self):
        for slot in self.backpack.sprites:
            for itemslot in slot:
                if itemslot.item is not None:
                    itemslot.item.cooldown=itemslot.item.atkSpeed

    def update_combat(self, dt, gegner):
        """Zählt den Cooldown jedes Items runter und greift bei null an."""
        dmg_total=0
        for slot in self.backpack.sprites:
            for itemslot in slot:
                item=itemslot.item
                if item is None:
                    continue
                #reine rüstungs und hp items werden ignoriert
                if item.dmgVal<=0:
                    continue
                item.cooldown-=dt
                if item.cooldown>0:
                    continue
                dmg=item.dmgVal
                if(gegner.armor>0):
                    if(dmg>gegner.armor):
                        overflow=dmg-gegner.armor
                        gegner.armor=0
                        gegner.health-=overflow
                    else:
                        gegner.armor-=dmg
                else:
                    gegner.health-=dmg
                dmg_total+=dmg
                
                item.cooldown+=item.atkSpeed
                if gegner.health<=0:
                    return dmg_total
        return dmg_total
    
    def apply_maxhealth(self):
        bonus=0
        for slot in self.backpack.sprites:
            for itemslot in slot:
                if itemslot.item is not None:
                    bonus+=itemslot.item.hpVal
        self.maxhealth=self.base_health+bonus
        self.health=self.maxhealth

    def defense(self):
        self.armor=0
        for slot in self.backpack.sprites:
            for itemslot in slot:
                if itemslot.item is not None:
                    self.armor+=itemslot.item.defVal
        if(self.armor==0):
            return
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
        self.imgSprites=self.character_sprites()
        self.image=self.imgSprites[random.randint(0,13)]
        self.base_health=health
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
        self.imgSprites=self.character_sprites()
        self.image=self.imgSprites[random.randint(14,len(self.imgSprites)-1)]
        self.base_health=health
        self.health=health
        self.maxhealth=health
        self.lv=lv
        self.rect.x=1000
        self.rect.y=500
        self.backpack=backpack.backpack(3,2,1300,420)

        for arr in self.backpack.sprites:
            for slot in arr:
                wahl_rarity = rarity_odds.roll_rarity(self.lv)
                pools=item_import.item_pools()
                pool = pools.get(wahl_rarity, [])
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
                        hpVal=data['hp'],
                        space_x=1,
                        space_y=1,
                        atkSpeed=data['cooldown']
                    )
                    slot.addItem(new_item)
    
