import pygame
from pygame.locals import *
import item
import Itemslot
import backpack
import os

#Einstellungen für Lokales laufen des Programms
print("SDL_VIDEODRIVER =", os.environ.get("SDL_VIDEODRIVER"))
print("DISPLAY =", os.environ.get("DISPLAY"))
print("XAUTHORITY =", os.environ.get("XAUTHORITY"))

pygame.init()
#Mouse Position wird getracked um Objekte an die richtigen Stellen zu platzieren
MousePos=pygame.font.Font(None,36)
screen=pygame.display.set_mode((1280,720))
clock=pygame.time.Clock()


#Testen Anzeigen eines Items
TestBackpack=backpack.backpack(3,2,50,50)



running=True
while running:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False
    
    screen.fill("blue")

    #tuple mouse.get_pos() wird ausgegeben
    x,y=pygame.mouse.get_pos()
    MousePos_surface=MousePos.render(str(x)+" "+str(y),True,"black")
    screen.blit(MousePos_surface, (10,10))

    TestBackpack.draw(screen)
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
