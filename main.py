import pygame
from pygame.locals import *
import item
import Itemslot
import backpack
import shop
import os

#Einstellungen für Lokales laufen des Programms
#xhost + local:
print("SDL_VIDEODRIVER =", os.environ.get("SDL_VIDEODRIVER"))
print("DISPLAY =", os.environ.get("DISPLAY"))
print("XAUTHORITY =", os.environ.get("XAUTHORITY"))

pygame.init()
#Mouse Position wird getracked um Objekte an die richtigen Stellen zu platzieren
MousePos=pygame.font.Font(None,36)
screen=pygame.display.set_mode((1920,1280))
clock=pygame.time.Clock()


class curser(pygame.sprite.Sprite):
    def __init__(self, color="white", width=10, height=10):
        self.image=pygame.Surface([width, height])
        self.image.fill(color)
        self.rect=self.image.get_rect()

    
    def update(self, screen):
        x,y=pygame.mouse.get_pos()
        self.rect.x=x
        self.rect.y=y
        screen.blit(self.image, self.rect)
        MousePos_surface=MousePos.render(str(x)+" "+str(y),True,"black")
        screen.blit(MousePos_surface, (10,10))

class itemgroup(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()
        


#Testen Anzeigen eines Items
TestBackpack=backpack.backpack(3,2,100,600)
TestShop=shop.shop(950,300)
item_imges=item.item.createItemSprites()
testitemgroup=itemgroup()
testitemgroup.add([item.item(item_imges[i],"test", 50+i*50, 50) for i in range(20)])
curser=curser()
top_item=None


running=True
while running:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False
    
    screen.fill("blue")

    #tuple mouse.get_pos() wird ausgegeben
    

    TestBackpack.draw(screen)
    TestShop.draw(screen)
    testitemgroup.draw(screen)
    curser.update(screen)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN  and event.button==1: 
            collided_items=pygame.sprite.spritecollide(curser, testitemgroup,False)
            if collided_items:
                top_item=max(collided_items)
                print("clicked")
                x,y=pygame.mouse.get_pos()
                top_item.move(screen,x,y)
        elif event.type==pygame.MOUSEMOTION:
            if(top_item is not None):
                x,y=pygame.mouse.get_pos()
                top_item.move(screen,x,y)
        elif event.type==pygame.MOUSEBUTTONUP and event.button==1:
            if(top_item is not None):
                top_item=None
                


    pygame.display.update()
    
    clock.tick(60)
    

pygame.quit()


