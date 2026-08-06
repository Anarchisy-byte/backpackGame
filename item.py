import pygame
class item(pygame.sprite.Sprite):
    def createItemSprites():
        itemSheet=pygame.image.load("images/Items/roguelikeitems.png").convert_alpha()
        item_texturesize=16
        item_sprites=[]
        for row in range(itemSheet.get_width()//item_texturesize):
            for col in range(itemSheet.get_height()//item_texturesize):
                x=row*item_texturesize
                y=col*item_texturesize
                img=pygame.Rect(x,y, item_texturesize, item_texturesize)
                sprite_img=itemSheet.subsurface(img)
                sprite_img=pygame.transform.scale_by(sprite_img,5)
                item_sprites.append(sprite_img)
        return item_sprites

    def __init__(self, image, name, posx,posy, cost=0, rarity="", itemtype="", itemID="", dmgVal=0, defVal=0, space_x=1, space_y=1):
        super().__init__()
        self.image = image
        self.rect=self.image.get_rect(center=(posx,posy))

        #Itemspezifische Eigenschaften
        self.cost=int(cost)
        self.rarity=rarity
        self.itemtype=itemtype
        self.itemID=itemID
        self.dmgVal=dmgVal
        self.defVal=defVal
        self.space_x=space_x
        self.space_y=space_y

    
    def move(self, x,y):
        self.rect.centerx=x
        self.rect.centery=y
        

    def draw(self,screen):
        screen.blit(self.image, self.rect)
    
    def stats(self):
        return f"cost: {self.cost} dmgVal: {self.dmgVal} defVal: {self.defVal}"
