import pygame, sys, os, random
from pygame.locals import *

LARGURA = 900
ALTURA = 500
CHAO = ALTURA - 20
white = (255,255,255)
black = (0,0,0)
bright_black = (89, 89, 89)
red = (255,0,0)
dark_red = (139, 0, 0)
green = (0, 255, 0)
dark_green = (0, 100, 0)
tela = pygame.display.set_mode([LARGURA, ALTURA])
relogio = pygame.time.Clock()

class Fundo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("mapa.png")
        self.rect.centerx = LARGURA / 2
        self.rect.centery = ALTURA / 2

class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("menu.png")
        self.rect.centerx = LARGURA/2
        self.rect.centery = ALTURA/2


class Audio():
    def __init__(self):
        pygame.mixer.music.load("Darkling.mp3")

    def play(self):
        pygame.mixer.music.play(-1)


class Obstaculo():
    def __init__(self):
        self.list_obj = []

    def dispara(self):
        object = Bloco()
        self.list_obj.append(object)


class Bloco(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("obstaculo5.png")
        self.rect.height -= 10
        self.rect.width -= 10
        self.rect.left = LARGURA + 1
        self.rect.centery = random.randrange(CHAO - (self.rect.height * 3 / 2), CHAO)
        self.velocidade = -4

    def colocar(self, superficie):
        superficie.blit(self.image, self.rect)

    def trajetoria(self):
        self.rect.move_ip(self.velocidade, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.impulso = 0
        self.gravidade = 4
        self.queda = 0
        self.image, self.rect = load_image("player.png")
        self.rect.left = 10
        self.rect.bottom = CHAO
        self.chao = self.rect.bottom

    def movimento(self):
        self.rect.move_ip(0, (self.gravidade + self.impulso + self.queda))

    def abaixa(self):
        if (self.rect.bottom == CHAO):
            self.rect.move_ip(0, CHAO + 20)

    def salto(self):
        if (self.rect.bottom == CHAO):
            self.impulso = -14

    def limite(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= CHAO:
            self.rect.bottom = CHAO
            self.queda = 0

    def para(self):
        if (self.rect.top <= CHAO - 4.5 * self.rect.height):
            self.impulso = 0


def load_image(nome):
    fullname = os.path.join("images", nome)
    try:
        image = pygame.image.load(fullname)
    except pygame.error.message:
        print('Impossível carregar imagem : ', fullname)
        # raise SystemExit, message
    return image, image.get_rect()


def colide(player, list):
    for retangulo in list.list_obj:
        if player.rect.colliderect(retangulo):
            print("COLIDIU")
            return True
        else:
            return False


class Pontuacao():
    def __init__(self):
        self.num = 0


class Text():
    def __init__(self, descricao, cor):
        self.tamanho = 30
        self.font_text = pygame.font.SysFont(pygame.font.get_default_font(), self.tamanho)
        self.text = self.font_text.render(descricao, 1, cor)
        self.rect = self.text.get_rect()
        self.rect.right = LARGURA
        self.rect.top = 0

def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def botao(msg,x,y,w,h,ic,ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
            
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(tela, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "novo jogo":
                main()
            elif action == "sair":
                quit()
                
    else:
        pygame.draw.rect(tela, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((290+(290/2)), (y+(h/2)))
    tela.blit(textSurf, textRect)


def TelaMenu():
    pygame.font.init()
    menu = Menu()
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        tela.blit(menu.image, menu.rect)
        largeText = pygame.font.Font('freesansbold.ttf',60)
        TextSurf, TextRect = text_objects("RunStudentRun", largeText)
        TextRect.center = ((LARGURA/2),(ALTURA/6))
        tela.blit(TextSurf, TextRect)

        
        botao("Novo Jogo",340, 310, 200, 35,dark_green,green, "novo jogo")
        botao("Mudar Avantar",340, 355, 200, 35,dark_green,green, "mudar")
        botao("Recordes", 340, 400, 200, 35, dark_green, green, "recorde")
        botao("Sair", 340, 445, 200, 35, dark_red, red, "sair")   
        pygame.display.update()
        relogio.tick(15)
        
def main(): 
    pygame.init()
    audio = Audio()
    jogador = Player()
    fundo = Fundo()
    objeto = Obstaculo()
    pontuacao = Pontuacao()
    quit = False
    pygame.display.set_caption('Testando')
    cor_branca = (255, 255, 255)
    TRAND = random.randrange(0, 70)
    time = 40 + TRAND
    pontuacao_txt = Text("Pontos : {}".format(pontuacao.num), cor_branca)

    audio.play()
    pygame.font.init()

    
    while not (quit):

        relogio.tick(70)
        time -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_UP:
                    jogador.salto()
                if event.key == pygame.K_DOWN:
                    jogador.queda = 20
                    jogador.abaixa()

        if time == 0:
            objeto.dispara()
            TRAND = random.randrange(0, 70)
            time = 40 + TRAND

        jogador.movimento()
        jogador.limite()
        jogador.para()

        tela.blit(fundo.image, fundo.rect)
        tela.blit(jogador.image, jogador.rect)
        if len(objeto.list_obj) > 0:
            for x in objeto.list_obj:
                x.colocar(tela)
                x.trajetoria()
                if x.rect.right <= 0:
                    pontuacao.num += 1
                    objeto.list_obj.remove(x)

        pontuacao_txt = Text("Pontos : {}".format(pontuacao.num), cor_branca)
        tela.blit(pontuacao_txt.text, pontuacao_txt.rect)

        quit = colide(jogador, objeto)

        pygame.display.flip()

    print("Sua pontuação foi de : {}".format(pontuacao.num))

TelaMenu()
main()
