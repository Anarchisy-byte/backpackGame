import pygame
from pygame.locals import *
import item
import Itemslot
import backpack
import shop
import character
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

class itemSlotGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def storedItems(self):
        l=[]
        for s in self.sprites():
            l.append(s.item)
        return l


#Testen der Elemente Backpack und Shop
TestBackpack=backpack.backpack(3,2,100,600)

TestShop=shop.shop(950,300)

#Erzeugen von ItemSlotgroup
testitemslotgroup=itemSlotGroup()
testitemslotgroup.add(TestBackpack.returnItemslots())
testitemslotgroup.add(TestShop.returnItemslots())

#Erstellen von Items
item_imges=item.item.createItemSprites()
testitemgroup=itemgroup()
testitemgroup.add([item.item(item_imges[i],"test", 50+i*50, 50) for i in range(20)])
curser=curser()
top_item=None

#Anzeige von Texten
displayed_text=[]
REMOVE_TEXT_EVENT = pygame.USEREVENT + 1

running=True
while running:
    screen.fill("blue")
    TestBackpack.draw(screen)
    TestShop.draw(screen)
    testitemgroup.draw(screen)
    curser.update(screen)
    for text in displayed_text:
        screen.blit(text.image, text.rect)
    for event in pygame.event.get():
        x,y=pygame.mouse.get_pos()
        if event.type== pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEBUTTONDOWN  and event.button==3:
            collided_items=testitemgroup.get_sprites_at((x,y))
            if collided_items:
                top_item=collided_items[-1]
                testitemgroup.move_to_front(top_item)
                print("show stats")

                #Anzeigen der Stats eines Items
                textf=pygame.font.Font(None,20)
                texts=textf.render(top_item.stats(),True, "black", "white")
                text_sprite=pygame.sprite.Sprite()
                text_sprite.image=texts
                text_sprite.rect=texts.get_rect(center=(x,y))
                displayed_text.append(text_sprite)

                pygame.time.set_timer(REMOVE_TEXT_EVENT,300)
                top_item=None

        elif event.type == REMOVE_TEXT_EVENT:
            if(displayed_text==[]):
                pygame.time.set_timer(REMOVE_TEXT_EVENT, 0)
            else:
                del displayed_text[0]
                
            
        elif event.type == pygame.MOUSEBUTTONDOWN  and event.button==1:
            #erstellt List mit überlappenden sprites an mouse, pos; sprite mit highest layer hinten 
            collided_items=testitemgroup.get_sprites_at((x,y))
            collided_items=[item for item in collided_items if item not in testitemslotgroup.storedItems()]
            if collided_items:
                top_item=collided_items[-1]
                testitemgroup.move_to_front(top_item)
                print("clicked")
                top_item.move(x,y)
        elif event.type==pygame.MOUSEMOTION:
            if(top_item is not None):
                x,y=pygame.mouse.get_pos()
                top_item.move(x,y)
        elif event.type==pygame.MOUSEBUTTONUP and event.button==1:
            if(top_item is not None):
                #over an itemslot
                overitemslot=pygame.sprite.spritecollide(top_item, testitemslotgroup,False)
                if(overitemslot!=list()):
                    if(not overitemslot[0].checkItem()):
                        overitemslot[0].addItem(top_item)
                top_item=None
                
                


    pygame.display.update()
    
    clock.tick(60)
    

pygame.quit()


