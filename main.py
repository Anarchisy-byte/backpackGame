import pygame
from pygame.locals import *
import item
import item_import
import Itemslot
import backpack
import shop
import character
import os
import sys
import buttonGUI

#bildschirm scaling
if sys.platform=="win32":
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

#Bildschirmzustände
STATE_MENU = "menu"
STATE_SHOP = "shop"
STATE_BATTLE = "battle"

#Einstellungen für Lokales laufen des Programms
#xhost + local:
print("SDL_VIDEODRIVER =", os.environ.get("SDL_VIDEODRIVER"))
print("DISPLAY =", os.environ.get("DISPLAY"))
print("XAUTHORITY =", os.environ.get("XAUTHORITY"))

os.environ['SDL_VIDEO_WINDOW_POS']='0,0'
pygame.init()
#Mouse Position wird getracked um Objekte an die richtigen Stellen zu platzieren
MousePos=pygame.font.Font(None,36)
screen=pygame.display.set_mode((1920,1280), pygame.SCALED)
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

#Kampf und Shop-Phasen:
BUY_PHASE_EVENT = pygame.USEREVENT +2
ENTER_BATTLE_PHASE_EVENT = pygame.USEREVENT +3

#Geld des Spielers
tMoney=pygame.font.Font(None,36)

#BackgroundMusik
pygame.mixer.music.load("sounds/short_adventure.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)
purchaseSound=pygame.mixer.Sound("sounds/snd_purchase.wav")
accept=pygame.mixer.Sound("sounds/Accept.mp3")

#Platzhalter bis start_new_game() das erste Mal läuft
TestBackpack=None
BackPackSlots=None
ShopSlots=None
TestShop=None
startbutton=None
refreshButton=None
buttons=None
enemy=None
player=None
curRound=1
newRound=True

state=STATE_MENU

#Menü-Buttons (unabhängig vom Spielstand, nur einmal erzeugt)
menu_start_button=buttonGUI.buttonGUI(0, 700, 500)
menu_quit_button=buttonGUI.buttonGUI(4, 700, 700)
menu_font=pygame.font.Font(None, 40)

def load_shop(item_pools=None):
    TestShop=shop.shop(950,300)
    TestShop.refresh(player,curRound,item_pools)
    return TestShop

def start_new_game():
    global TestBackpack, BackPackSlots, ShopSlots, TestShop, startbutton, buttons, enemy, player, curRound, newRound, state

    TestBackpack=backpack.backpack(3,2,200,600)
    BackPackSlots=itemgroup()
    BackPackSlots.add(TestBackpack.returnItemslots())
    ShopSlots=None
    TestShop=None
    startbutton=buttonGUI.buttonGUI(0, 1000, 950)
    buttons=itemgroup()
    buttons.add(startbutton)
    enemy=None
    player=character.player(50,1,10, TestBackpack)
    curRound=1
    newRound=True

    state=STATE_SHOP
    pygame.event.post(pygame.event.Event(BUY_PHASE_EVENT))

itemStatsFont=pygame.font.Font(None,20)

def draw_item_tooltip(screen):
    x,y=pygame.mouse.get_pos()
    hovered_slots=[]
    if state==STATE_SHOP and ShopSlots is not None:
        hovered_slots+=ShopSlots.get_sprites_at((x,y))
    hovered_slots+=BackPackSlots.get_sprites_at((x,y))

    if not hovered_slots:
        return

    slot=hovered_slots[-1]
    if slot.item is None:
        return

    texts=itemStatsFont.render(slot.item.stats(),True, "black", "white")
    screen.blit(texts, (x-60,y-15))

def create_damage_sprite(screen, dmg, enemy):
    dmgFont=pygame.font.Font(None,36)
    screen.blit(dmgFont.render(str(dmg),True, "white", None),(enemy.rect.x, enemy.rect.y-15))

running=True
while running:
    screen.fill("blue")
    curser.update(screen)

    if state==STATE_MENU:
        menu_start_button.draw(screen)
        screen.blit(menu_font.render("Start", True, "black"), menu_start_button.rect.topleft)
        menu_quit_button.draw(screen)
        screen.blit(menu_font.render("Beenden", True, "black"), menu_quit_button.rect.topleft)

    else:
        BackPackSlots.draw(screen)
        screen.blit(tMoney.render("Gold:"+str(player.gold),True, "black", "white"),(10,45))
        player.draw(screen)

        if state==STATE_SHOP and TestShop is not None:
            TestShop.draw(screen)
            startbutton.draw(screen)
            refreshButton.draw(screen)

        elif state==STATE_BATTLE and enemy is not None:
            enemy.draw(screen)

        draw_item_tooltip(screen)

    #Gameloop
    """Jede Runde werden alle Attacken alle 5 Sek ausgeführt --> endet sobald einer Tot ist """
    
    if state==STATE_BATTLE:
        print("attack")
        print(player.armor, player.health, enemy.armor, enemy.health)
        if newRound:
            player.apply_maxhealth()
            enemy.apply_maxhealth()
            player.defense()
            enemy.defense()
            newRound=False
        dmg_dealt=player.attack(enemy)
        print("Dmg_dealt:"+str(dmg_dealt))
        dmg_sprite=create_damage_sprite(screen,dmg_dealt,enemy) 
        pygame.time.wait(400)
        if(enemy.health>0):
            dmg_dealt=enemy.attack(player)
            print("Dmg_dealt:"+str(dmg_dealt))
            dmg_sprite=create_damage_sprite(screen,dmg_dealt,player) 
            pygame.time.wait(400)       

        if(enemy.health<=0 or player.health<=0):
            print("defeated")
            if(player.health<=0):
                state=STATE_MENU
            else:
                state=STATE_SHOP
                player.gold+=10
                curRound+=1
                newRound=True
                pygame.event.post(pygame.event.Event(BUY_PHASE_EVENT))
    


    for event in pygame.event.get():
        x,y=pygame.mouse.get_pos()
        if event.type== pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            #Temporär --> wird geändert zum Gameplayloop
            if state==STATE_MENU:
                pass
            elif event.key == pygame.K_PLUS:
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.1)
            elif event.key == pygame.K_MINUS:
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.1)
            elif event.key == pygame.K_r:
                if state==STATE_SHOP:
                    TestShop.refresh(player,curRound)
                    print(player.gold)


        #Kaufphase starten
        elif event.type==BUY_PHASE_EVENT:
            if state!=STATE_BATTLE:
                del enemy
                startbutton=buttonGUI.buttonGUI(0, 950, 950)
                refreshButton=buttonGUI.buttonGUI(2, 1500, 950)
                buttons.add(startbutton)
                buttons.add(refreshButton)
                enemy=None
                TestShop=load_shop()#übergabe itempool
                TestShop.draw(screen)
                ShopSlots=itemgroup()
                ShopSlots.add(TestShop.returnItemslots())
            else:
                print("in battle")

        elif event.type==ENTER_BATTLE_PHASE_EVENT:
            del TestShop
            del startbutton
            del refreshButton
            TestShop=None
            enemy=character.enemy(50,curRound)
            state=STATE_BATTLE
            ...

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and state==STATE_MENU:
            if menu_start_button.rect.collidepoint(x,y):
                start_new_game()
                accept.play()
            elif menu_quit_button.rect.collidepoint(x,y):
                running=False

        #Kaufen mit Linksclick
        elif event.type == pygame.MOUSEBUTTONDOWN  and event.button==1:
            #Wenn battle --> nicht kaufen/verkaufen
            if state==STATE_BATTLE:
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
                if collided_slots[-1] is refreshButton:
                    TestShop.refresh(player,curRound)
                    accept.play()
                    continue
                pygame.event.post(pygame.event.Event(ENTER_BATTLE_PHASE_EVENT))
                accept.play()
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
                    purchaseSound.play()


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
                player.gold += item_to_sell.cost//2
                TestBackpack.removeItem(item_to_sell) 
                del item_to_sell
                purchaseSound.play()
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