import pygame
class buttonGUI(pygame.sprite.Sprite):

    def b_sprites_create(self):
        imageSheet=pygame.image.load("images/Items/vector-set-colorful-pixel-art-open-play-close-buttons-pixelated-video-game-icons-off.png")
        list_of_sprites=[]
        img_rect=pygame.Rect(583,67,496,163)
        img=imageSheet.subsurface(img_rect)
        list_of_sprites.append(img)
        return list_of_sprites

    def __init__(self, imageindex, posx, posy):
        super().__init__()
        self.button_sprites=self.b_sprites_create()
        self.image=self.button_sprites[imageindex]
        self.rect=self.image.get_rect()
        self.rect.topleft=(posx,posy)

    
    def draw(self, screen):
        screen.blit(self.image,self.rect)