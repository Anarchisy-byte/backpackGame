import pygame
class item(pygame.sprite.Sprite):
    def __init__(self, image, name, posx,posy, cost, rarity, itemtype, itemID, dmgVal, defVal, space_x, space_y):
        super().__init__(self)
        self._image = image
        self.rect = image.get_rect()
        self.rect.x=posx
        self.rect.y=posy

        #Itemspezifische Eigenschaften
        self.cost=cost
        self.rarity=ratity
        self.itemtype=itemtype
        self.itemID=itemID
        self.dmgVal=dmgVal
        self.defVal=defVal
        self.space_x=space_x
        self.space_y=space_y

    
    def update(self, screen):
        ...

    def draw(self,screen):
        screen.blit(self.image, self.rect)