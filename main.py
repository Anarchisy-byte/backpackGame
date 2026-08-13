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
import random

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
pygame.display.set_caption("Backpackgame")


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
pygame.mixer.music.play(-1)
vol=0.3
pygame.mixer.music.set_volume(vol)
purchaseSound=pygame.mixer.Sound("sounds/snd_purchase.wav")
accept=pygame.mixer.Sound("sounds/Accept.mp3")
gameOverSound=pygame.mixer.Sound("sounds/game_over_bad_chest.wav")
meleeSounds=[]
meleeSounds.append(pygame.mixer.Sound("sounds/melee sounds/animal melee sound.wav"))
meleeSounds.append(pygame.mixer.Sound("sounds/melee sounds/melee sound.wav"))
meleeSounds.append(pygame.mixer.Sound("sounds/melee sounds/sword sound.wav"))

#Background_images
Background_images=[]
img=pygame.image.load("images/background/parallax_forest_pack/parallax_forest_pack/layers/parallax-forest-lights.png")
img=pygame.transform.smoothscale(img, (1920, 1280))
Background_images.append(img)
img=pygame.image.load("images/background/parallax_forest_pack/parallax_forest_pack/layers/parallax-forest-back-trees.png")
img=pygame.transform.smoothscale(img, (1920, 1280))
Background_images.append(img)
img=pygame.image.load("images/background/parallax_forest_pack/parallax_forest_pack/layers/parallax-forest-middle-trees.png")
img=pygame.transform.smoothscale(img, (1920, 1280))
Background_images.append(img)
img=pygame.image.load("images/background/parallax_forest_pack/parallax_forest_pack/layers/parallax-forest-front-trees.png")
img=pygame.transform.smoothscale(img, (1920, 1280))
Background_images.append(img)
background_last_update=0
background_update_delay=200

#Shop-Hintergrund (einmalig laden statt jeden Frame)
shop_background_img=pygame.image.load("images/background/shop_Background.jpeg")
shop_background_img=pygame.transform.scale_by(shop_background_img,3)

#Attack-Animation Frames (einmalig laden statt bei jedem Angriff)
attack_frameSheet=pygame.image.load("images/character/pixel_art_sword_slash_sprites.png")
attack_frames_right=[]
_w=attack_frameSheet.get_width()
_h=attack_frameSheet.get_height()
for _row in range(3):
    for _colom in range(3):
        _f=attack_frameSheet.subsurface((_w/3*_row,_h/3*_colom,_w/3,_h/3))
        attack_frames_right.append(pygame.transform.scale_by(_f,5))
attack_frames_left=[pygame.transform.flip(_f,True,False) for _f in attack_frames_right]


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
dt=1/60 #sekunden seit letztem frame, für die Item-Cooldowns im Kampf

#Zeitlimit: verhindert Softlock, spieler verliert automatisch wenn timer abläuft
battle_elapsed=0
BATTLE_TIMEOUT=25

#Rundenziel
WIN_ROUND=15

#Leben: bei Rundenverlust wird eins abgezogen, erst bei 0 ist es Game Over
MAX_LIVES=3
player_lives=MAX_LIVES

#Herz-Icons für die Lebensanzeige: lifebar_16x16.png ist ein 2x2-Sheet
HEART_SIZE=32
_lifebar_sheet=pygame.image.load("images/HUD/lifebar_16x16.png").convert_alpha()
heart_full=pygame.transform.scale(_lifebar_sheet.subsurface((0,0,16,16)),(HEART_SIZE,HEART_SIZE))
heart_empty=pygame.transform.scale(_lifebar_sheet.subsurface((16,16,16,16)),(HEART_SIZE,HEART_SIZE))

#Menü-Buttons (unabhängig vom Spielstand, nur einmal erzeugt)
menu_start_button=buttonGUI.buttonGUI(0, 700, 500)
menu_quit_button=buttonGUI.buttonGUI(4, 700, 700)
menu_font=pygame.font.Font(None, 100)

#Refresh-Button: statt Sprite-Bild ein selbst gezeichneter Button mit Text + aktuellen Kosten
refreshButtonFont=pygame.font.Font(None,28)

def make_refresh_button_image(cost):
    label=refreshButtonFont.render("Refresh",True,"black")
    cost_label=refreshButtonFont.render(str(cost)+" Gold",True,"black")
    padding=14
    width=max(label.get_width(),cost_label.get_width())+padding*2
    height=label.get_height()+cost_label.get_height()+padding*2+4
    surf=pygame.Surface((width,height))
    surf.fill((100,190,150))
    pygame.draw.rect(surf,(35,95,75),surf.get_rect(),width=3,border_radius=8)
    surf.blit(label,(width//2-label.get_width()//2,padding))
    surf.blit(cost_label,(width//2-cost_label.get_width()//2,padding+label.get_height()+4))
    return surf

class TextButton(pygame.sprite.Sprite):
    def __init__(self, image, posx, posy):
        super().__init__()
        self.image=image
        self.rect=self.image.get_rect(topleft=(posx,posy))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_image(self, image):
        topleft=self.rect.topleft
        self.image=image
        self.rect=self.image.get_rect(topleft=topleft)

battleTimerFont=pygame.font.Font(None,50)

def load_shop(item_pools=None):
    TestShop=shop.shop(950,300)
    TestShop.refresh(player,curRound,item_pools)
    return TestShop

def start_new_game():
    global TestBackpack, BackPackSlots, ShopSlots, TestShop, startbutton, buttons, enemy, player, curRound, newRound, state, player_lives

    TestBackpack=backpack.backpack(3,2,60,420)
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
    player_lives=MAX_LIVES

    state=STATE_SHOP
    pygame.event.post(pygame.event.Event(BUY_PHASE_EVENT))

itemNameFont=pygame.font.Font(None,26)
itemStatsFont=pygame.font.Font(None,20)

def draw_item_tooltip(screen):
    x,y=pygame.mouse.get_pos()
    hovered_slots=[]
    if state==STATE_SHOP and ShopSlots is not None:
        hovered_slots+=ShopSlots.get_sprites_at((x,y))
    if state==STATE_BATTLE and enemy is not None:
        #Gegner-Rucksack ist keine itemgroup, daher direkt über die Zellen prüfen
        for row in enemy.backpack.sprites:
            for slot in row:
                if slot.rect.collidepoint(x,y):
                    hovered_slots.append(slot)
    hovered_slots+=BackPackSlots.get_sprites_at((x,y))

    if not hovered_slots:
        return

    slot=hovered_slots[-1]
    if slot.item is None:
        return

    it=slot.item
    color=it.rarity_color()
    name_surf=itemNameFont.render(it.name,True,color)
    stat_surfs=[itemStatsFont.render(line,True,"white") for line in it.stats_lines()]

    padding=8
    line_gap=3
    width=max([name_surf.get_width()]+[s.get_width() for s in stat_surfs])+padding*2
    height=name_surf.get_height()+line_gap+sum(s.get_height()+line_gap for s in stat_surfs)+padding*2

    box=pygame.Surface((width,height),pygame.SRCALPHA)
    box.fill((20,20,20,225))
    pygame.draw.rect(box,color,box.get_rect(),width=2)

    cursor_y=padding
    box.blit(name_surf,(padding,cursor_y))
    cursor_y+=name_surf.get_height()+line_gap
    for s in stat_surfs:
        box.blit(s,(padding,cursor_y))
        cursor_y+=s.get_height()+line_gap

    pos_x=min(max(x-60,0),1920-width)
    pos_y=min(max(y-height-15,0),1280-height)
    screen.blit(box,(pos_x,pos_y))

def create_damage_sprite(screen, dmg, enemy):
    dmgFont=pygame.font.Font(None,36+random.randint(0,10))
    screen.blit(dmgFont.render(str(dmg),True, "white", None),(enemy.rect.x+random.randint(-5,5), enemy.rect.y-15+random.randint(-15,1)))

def create_attack_animation(screen, cords, mirrored, dmg_dealt, enemy):
    global meleeSounds
    create_damage_sprite(screen,dmg_dealt,enemy)
    meleeSounds[random.randint(0,2)].play()
    frames=attack_frames_left if mirrored else attack_frames_right
    attack_sprite=pygame.sprite.Sprite()
    attack_sprite.frames=frames
    x=-250
    if mirrored:
        x*=-1
    attack_sprite.rect=frames[0].get_rect(center=cords)
    for frame in range(9):
        pygame.time.wait(20)
        screen.blit(attack_sprite.frames[frame],attack_sprite.rect)
        pygame.display.update()
    attack_sprite.kill()
    pygame.display.update()

running=True
while running:
    

    if state==STATE_MENU:
        background_new_update=pygame.time.get_ticks()
        if(background_new_update-background_last_update>=background_update_delay):
            background_last_update=pygame.time.get_ticks()
            for layer in Background_images[:-1]:
                screen.blit(layer,(random.randint(-2,2), random.randint(-2,2)))
            screen.blit(Background_images[-1],(0,0))
        menu_start_button.draw(screen)
        screen.blit(menu_font.render("Backpackgame", True, "black",None),(1920/2-250,300))
        menu_quit_button.draw(screen)
        #screen.blit(menu_font.render("Beenden", True, "black"), menu_quit_button.rect.topleft)

    else:
        if state==STATE_SHOP and TestShop is not None:
            screen.blit(shop_background_img,(0,0))
            TestShop.draw(screen)
            startbutton.draw(screen)
            refreshButton.draw(screen)

        elif state==STATE_BATTLE and enemy is not None:
            background_new_update=pygame.time.get_ticks()
            if(background_new_update-background_last_update>=background_update_delay):
                background_last_update=pygame.time.get_ticks()
                for layer in Background_images[:-1]:
                    screen.blit(layer,(random.randint(-2,2), random.randint(-2,2)))
                screen.blit(Background_images[-1],(0,0))
            enemy.draw(screen)
            timer_left=max(0,BATTLE_TIMEOUT-battle_elapsed)
            timer_surf=battleTimerFont.render(str(int(timer_left)+1),True,"white","black")
            screen.blit(timer_surf,(1920//2-timer_surf.get_width()//2,20))
        curser.update(screen)
        BackPackSlots.draw(screen)
        screen.blit(tMoney.render("Gold:"+str(player.gold),True, "black", "white"),(10,45))
        for i in range(MAX_LIVES):
            heart_img=heart_full if i<player_lives else heart_empty
            screen.blit(heart_img,(10+i*(HEART_SIZE+6),78))
        player.draw(screen)

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
            player.reset_cooldowns()
            enemy.reset_cooldowns()
            newRound=False
            battle_elapsed=0
            pygame.display.update()
            #verhindert nicht laden der sprites bei Instakill
            continue
        dmg_dealt=player.update_combat(dt,enemy)
        if dmg_dealt>0:
            print("Dmg_dealt:"+str(dmg_dealt))
            create_attack_animation(screen,(800,660),False,dmg_dealt,enemy)

        if(enemy.health>0):
            dmg_dealt=enemy.update_combat(dt,player)
            if dmg_dealt>0:
                print("Dmg_dealt:"+str(dmg_dealt))
                create_attack_animation(screen,(1000,660),True,dmg_dealt,player)

        #Zeitlimit gegen Softlock, wenn timer auf 0 und keiner tot verliert der spieler
        battle_elapsed+=dt
        if battle_elapsed>=BATTLE_TIMEOUT and enemy.health>0 and player.health>0:
            print("Zeitlimit erreicht, Spieler verliert")
            player.health=0

        if(enemy.health<=0 or player.health<=0):
            print("defeated")
            if(player.health<=0):
                player_lives-=1
                if player_lives<=0:
                    screen.fill("black")
                    gameOverSound.play()
                    screen.blit(menu_font.render("Game Over", True, "white",None),(1920/2-250,300))
                    pygame.display.update()
                    while(pygame.mixer.get_busy() and running):
                        for event in pygame.event.get():
                            if event.type== pygame.QUIT:
                                running=False
                    state=STATE_MENU
                else:
                    #Leben verloren, aber noch nicht Game Over -> zurück in den Shop, gleiche Runde
                    player.health=player.maxhealth
                    state=STATE_SHOP
                    player.gold+=10+curRound
                    newRound=True
                    pygame.event.post(pygame.event.Event(BUY_PHASE_EVENT))
            elif curRound>=WIN_ROUND:
                screen.fill("black")
                accept.play()
                screen.blit(menu_font.render("Sieg!", True, "white",None),(1920/2-150,300))
                pygame.display.update()
                while(pygame.mixer.get_busy() and running):
                    for event in pygame.event.get():
                        if event.type== pygame.QUIT:
                            running=False
                state=STATE_MENU
            else:
                state=STATE_SHOP
                player.gold+=10+curRound
                curRound+=1
                newRound=True
                pygame.event.post(pygame.event.Event(BUY_PHASE_EVENT))
    


    for event in pygame.event.get():
        x,y=pygame.mouse.get_pos()
        if event.type== pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            #Temporär --> wird geändert zum Gameplayloop
            if event.key == pygame.K_m:
                if pygame.mixer.music.get_volume()==0:
                    pygame.mixer.music.set_volume(vol)
                else:
                    pygame.mixer.music.set_volume(0)
            elif event.key == pygame.K_PLUS:
                vol+=0.1
                if(vol>1):
                    vol=1
                pygame.mixer.music.set_volume(vol)
            elif event.key == pygame.K_MINUS:
                vol-=0.1
                if(vol<0):
                    vol=0
                pygame.mixer.music.set_volume(vol)
            elif event.key == pygame.K_r:
                if state==STATE_SHOP:
                    TestShop.refresh(player,curRound)
                    refreshButton.set_image(make_refresh_button_image(TestShop.refresh_cost))
                    print(player.gold)


        #Kaufphase starten
        elif event.type==BUY_PHASE_EVENT:
            if state!=STATE_BATTLE:
                del enemy
                enemy=None
                TestShop=load_shop()#übergabe itempool
                startbutton=buttonGUI.buttonGUI(0, 950, 950)
                refreshButton=TextButton(make_refresh_button_image(TestShop.refresh_cost), 1500, 950)
                buttons.add(startbutton)
                buttons.add(refreshButton)
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
            enemy=character.enemy(50+curRound*8,curRound)
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
                    refreshButton.set_image(make_refresh_button_image(TestShop.refresh_cost))
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

#umrechnung von frames in sekunden für item-cooldowns
    dt=clock.tick(60)/1000


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