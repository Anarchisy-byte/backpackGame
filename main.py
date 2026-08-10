import pygame
from pygame.locals import *
import item
import item_import
import Itemslot
import backpack
import shop
import character
import os
import buttonGUI

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
    def storedItems(self):
        l=[]
        for s in self.sprites():
            if s.item is not None:
                l.append(s.item)
        return l
    
    def containerOfstoredItem(self,sprite):
        for s in self.sprites():
            if(s.item==sprite):
                return s
    
    def draw(self, scren):
        l=self.sprites()
        for slot in l:
            slot.draw(screen)
    

curser=curser()
top_item=None

#Testen der Elemente Backpack und Shop
TestBackpack=backpack.backpack(3,2,100,600)

#Erzeugen von ItemSlotgroup
BackPackSlots=itemgroup()
BackPackSlots.add(TestBackpack.returnItemslots())
ShopSlots=None

#Anzeige von Texten
displayed_text=[]
REMOVE_TEXT_EVENT = pygame.USEREVENT + 1
a=None


#Kampf und Shop-Phasen:
inbattle=False
BUY_PHASE_EVENT = pygame.USEREVENT +2
ENTER_BATTLE_PHASE_EVENT = pygame.USEREVENT +3

#starte Shop
TestShop=None
pygame.event.post(pygame.event.Event(BUY_PHASE_EVENT))

startbutton=buttonGUI.buttonGUI(0, 1000, 950)
buttons=itemgroup()
buttons.add(startbutton)

enemy=None

player=character.player(10,1,100, TestBackpack)


#Geld des Spielers
tMoney=pygame.font.Font(None,36)

#Derzeitige Runde
curRound=1

def load_shop(item_pools=None):
    TestShop=shop.shop(950,300)
    TestShop.refresh(player,item_pools)                
    return TestShop

running=True
while running:
    screen.fill("blue")
    BackPackSlots.draw(screen)
    curser.update(screen)
    screen.blit(tMoney.render("Gold:"+str(player.gold),True, "black", "white"),(10,45))
    player.draw(screen)
    
    if not inbattle and TestShop is not None:
        TestShop.draw(screen)
        startbutton.draw(screen)
    
    if inbattle and enemy is not None:
        enemy.draw(screen)

    for text in displayed_text:
        screen.blit(text.image, text.rect)
    
    #Gameloop
    """Jede Runde werden alle Attacken alle 5 Sek ausgeführt --> endet sobald einer Tot ist """
    
    if inbattle and enemy is not None:
        print("attack")
        player.attack(enemy)
        pygame.time.wait(100)
        enemy.attack(player)
        pygame.time.wait(100)
        print(enemy.health)
        print(player.health)
        if(enemy.health<=0 or player.health<=0):
            inbattle=False
            print("defeated")
            if(player.health<=0):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            player.gold+=curRound
            curRound+=1
            pygame.event.post(pygame.event.Event(BUY_PHASE_EVENT))
    


    for event in pygame.event.get():
        x,y=pygame.mouse.get_pos()
        if event.type== pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            #Temporär --> wird geändert zum Gameplayloop
            if event.key == pygame.K_a:                
                print("a")
                if inbattle:
                    pygame.event.post(pygame.event.Event(BUY_PHASE_EVENT))
                    inbattle=False
                else:
                    pygame.event.post(pygame.event.Event(ENTER_BATTLE_PHASE_EVENT))
                    inbattle=True
            elif event.key == pygame.K_r:
                if not inbattle:
                    TestShop.refresh(player)
                    print(player.gold)


        elif event.type == pygame.MOUSEBUTTONDOWN  and event.button==3:
            collided_items=[]
            if ShopSlots is not None:
                collided_items=ShopSlots.get_sprites_at((x,y))
            collided_items+=BackPackSlots.get_sprites_at((x,y))

            #wenn keine Items --> abbrechen
            if not collided_items:
                continue

            if collided_items:
                top_item=collided_items[-1]
                if (BackPackSlots.has(top_item)):
                    BackPackSlots.move_to_front(top_item)
                if (ShopSlots.has(top_item)):
                    ShopSlots.move_to_front(top_item)
                print("show stats")

                #Anzeigen der Stats eines Items
                textf=pygame.font.Font(None,20)
                texts=textf.render(top_item.item.stats(),True, "black", "white")
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
        
        #Kaufphase starten
        elif event.type==BUY_PHASE_EVENT:
            if not inbattle:
                del enemy
                startbutton=buttonGUI.buttonGUI(0, 1000, 950)
                buttons.add(startbutton)
                enemy=None
                player.maxhealth+=1
                player.health=player.maxhealth
                TestShop=load_shop()#übergabe itempool
                TestShop.draw(screen)
                ShopSlots=itemgroup()
                ShopSlots.add(TestShop.returnItemslots())
            else:
                print("in battle")

        elif event.type==ENTER_BATTLE_PHASE_EVENT:
            del TestShop
            del startbutton
            TestShop=None
            enemy=character.enemy(10*(1.1)**curRound,curRound)
            inbattle=True
            ...

        #Kaufen mit Linksclick
        elif event.type == pygame.MOUSEBUTTONDOWN  and event.button==1:
            #Wenn battle --> nicht kaufen/verkaufen
            if inbattle:
                continue
            collided_slots = []
            if ShopSlots is not None:
                collided_slots.extend(ShopSlots.get_sprites_at((x, y)))
            if BackPackSlots is not None:
                collided_slots.extend(BackPackSlots.get_sprites_at((x, y)))
            if buttons is not None:
                collided_slots.extend(buttons.get_sprites_at((x,y)))

            if not collided_slots:
                continue
            
            if (buttons.has(collided_slots[-1])):
                pygame.event.post(pygame.event.Event(ENTER_BATTLE_PHASE_EVENT))
                continue

            #vorderster Slot mit Item
            slot = collided_slots[-1]   
            if slot.item is None:
                continue
            
            

            #Unterscheiden Shop und Backpack:
            print(ShopSlots.storedItems())
            if ShopSlots.has(slot):
                ShopSlots.move_to_front(slot)
                #zwischenspeichern des Items
                theItem = slot.item

                if slot.canbuyItem(player.gold) and TestBackpack.get_empty_slot() is not None:
                    player.gold -= theItem.cost
                    #Shop löscht Item
                    slot.buyItem()                       

                    # Zum Backpack hinzufügen
                    BackPack_slot = TestBackpack.addItem(theItem)
                    if BackPack_slot:
                        theItem.rect.center = BackPack_slot.rect.center
                        BackPackSlots.move_to_front(BackPack_slot)
                        print("gekauft", theItem.name)
                else:
                    print("Kein Platz oder kein Geld")

            elif (BackPackSlots.has(slot)):
                print("sell")
                print(player.gold)
                BackPackSlots.move_to_front(slot)
                item_to_sell = slot.item
                player.gold += item_to_sell.cost
                TestBackpack.removeItem(item_to_sell) 
                del item_to_sell
                TestBackpack.update()

    pygame.display.update()
    
    clock.tick(60)
    

pygame.quit()


"""
DRAG AND DROP CODE MIT FEHLER --> Shop Itemslot wird mitbewegt
elif event.type == pygame.MOUSEBUTTONDOWN  and event.button==1:
            #erstellt List mit überlappenden sprites an mouse, pos; sprite mit highest layer hinten 
            collided_items=testitemgroup.get_sprites_at((x,y))
            collided_items=[item for item in collided_items if item not in BackPackSlots.storedItems() and item not in ShopSlots.sprites()]
            l=[item for item in collided_items if item in ShopSlots.storedItems()]
            if (l):
                top_item=l[-1]
                a=ShopSlots.containerOfstoredItem(top_item)
                print("Before:", a.rect.x, a.rect.y)
                a.buyItem(money)
                print("After:", a.rect.x, a.rect.y)
                testitemgroup.move_to_front(top_item)
                print("buy")
                top_item=None

            elif collided_items:
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
                overitemslot=pygame.sprite.spritecollide(top_item, BackPackSlots,False)
                if(overitemslot!=list()):
                    if(not overitemslot[0].checkItem()):
                        overitemslot[0].addItem(top_item)
                top_item=None
                """