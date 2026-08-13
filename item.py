import pygame

item_sprites=[]
class item(pygame.sprite.Sprite):
    
    def load_item_sprites():
        global item_sprites
        itemSheet=pygame.image.load("images/Items/roguelikeitems.png").convert_alpha()
        item_texturesize=16
        for row in range(13):
            for col in range(14):
                x=row*item_texturesize
                y=col*item_texturesize
                img=pygame.Rect(x,y, item_texturesize, item_texturesize)
                sprite_img=itemSheet.subsurface(img)
                sprite_img=pygame.transform.scale_by(sprite_img,5)
                item_sprites.append(sprite_img)
    
    def createItemSprites():
        global item_sprites
        if (item_sprites==[]):
            item.load_item_sprites()
        return item_sprites

    def __init__(self, image, name, posx,posy, atkSpeed, cost=0, rarity="", itemtype="", itemID="", dmgVal=0, defVal=0, hpVal=0, space_x=1, space_y=1):
        super().__init__()
        self.image = image
        self.rect=self.image.get_rect(center=(posx,posy))

        #Itemspezifische Eigenschaften
        self.name=name
        self.cost=int(cost)
        self.rarity=rarity
        self.itemtype=itemtype
        self.itemID=itemID
        self.dmgVal=dmgVal
        self.defVal=defVal
        self.hpVal=hpVal
        self.space_x=space_x
        self.space_y=space_y
        self.layer=1

        #Angriffs-Cooldown: zählt im Kampf von atkSpeed auf 0 runter, danach greift das Item an
        self.atkSpeed=atkSpeed
        self.cooldown=atkSpeed

    
    def move(self, x,y):
        self.rect.centerx=x
        self.rect.centery=y

    def draw(self,screen):
        screen.blit(self.image, self.rect)
    
    RARITY_COLORS={
        "common": (200,200,200),
        "uncommon": (40,180,70),
        "rare": (50,120,230),
        "epic": (160,60,220),
        "legendary": (230,150,30),
        "mythic": (220,40,40),
    }

    def rarity_color(self):
        return item.RARITY_COLORS.get(self.rarity, (255,255,255))

    def stats_lines(self):
        """item stats als einzelne zeilen"""
        lines=[f"{self.rarity.capitalize()} - {self.cost} Gold"]
        if self.dmgVal>0:
            lines.append(f"Schaden: {self.dmgVal}  (alle {self.atkSpeed}s)")
        if self.defVal>0:
            lines.append(f"Rüstung: {self.defVal}")
        if self.hpVal>0:
            lines.append(f"HP: {self.hpVal}")
        return lines
