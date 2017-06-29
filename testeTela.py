import pygame, sys, os, random
from pygame.locals import *

LARGURA = 900
ALTURA = 500

class Fundo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image("imagem_fundo2.jpg")
        self.rect.centerx = LARGURA/2
        self.rect.centery = ALTURA/2

class Audio():
    def __init__(self):
        pygame.mixer.music.load("Darkling.mp3")
        
    def play(self):
        pygame.mixer.music.play(-1)
    
class Bloco(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.directionx = 0
        self.directiony = 0
        self.velocidade = 30
        self.image, self.rect = load_image("player.png")
        self.rect.centerx = LARGURA/2
        self.rect.centery = ALTURA/2

    def movimenta(self):
        self.rect.move_ip((self.directionx * self.velocidade), (self.directiony * self.velocidade))

    def limite(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= LARGURA:
            self.rect.right = LARGURA
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= ALTURA:
            self.rect.bottom = ALTURA

    def para(self):
        self.directionx = 0
        self.directiony = 0


def load_image(nome):
    fullname = os.path.join("images", nome)
    try:
        image = pygame.image.load(fullname)
    except pygame.error.message:
        print('Impossível carregar imagem : ', fullname)
       # raise SystemExit, message
    return image, image.get_rect()


def main():

    pygame.init()
    audio = Audio()
    jogador = Bloco()
    fundo = Fundo()
    tela = pygame.display.set_mode([LARGURA, ALTURA])
    pygame.display.set_caption('Testando')
    relogio = pygame.time.Clock()
    cor_branca = (255, 255, 255)

    audio.play()
    pygame.key.set_repeat(1, 100)
    
    while True:

        relogio.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    jogador.directionx = -1
                if event.key == pygame.K_RIGHT:
                    jogador.directionx = 1
                if event.key == pygame.K_UP:
                    jogador.directiony = -1
                if event.key == pygame.K_DOWN:
                    jogador.directiony = 1

        jogador.movimenta()
        jogador.limite()
        jogador.para()

        tela.blit(fundo.image,fundo.rect)
        tela.blit(jogador.image, jogador.rect)
        pygame.display.flip()


main()
