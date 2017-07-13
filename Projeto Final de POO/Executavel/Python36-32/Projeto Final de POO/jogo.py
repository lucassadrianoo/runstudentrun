import pygame, sys, os, random, sqlite3
from datetime import datetime
from pygame.locals import *

pygame.init()
LARGURA = 900
ALTURA = 500
CHAO = ALTURA - 20
white = (255, 255, 255)
black = (0, 0, 0)
bright_black = (89, 89, 89)
red = (255, 0, 0)
dark_red = (139, 0, 0)
green = (0, 255, 0)
dark_green = (0, 100, 0)
cor_branca = (255, 255, 255)
v_cor = [black, red, green]

pygame.display.set_caption('AGENTSTUDENTRUN')
tela = pygame.display.set_mode((LARGURA, ALTURA))


class Tela(object):
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))

        self.fundo = (0, 0, 0)

        self.cor_objeto = (255, 255, 255)

        self.cor_claro = (20, 0, 50)

        self.cor_creditos = (255, 255, 255)

    def getCorCreditos(self):
        return self.cor_creditos

    def getCorObjeto(self):
        return self.cor_objeto

    def getFundo(self):
        return self.fundo

    def getCorClaro(self):
        return self.cor_claro

    def Fundo(self):
        self.tela.fill(self.fundo)

    def getTela(self):
        return self.tela


class BancoDeDados(object):
    def __init__(self):
        try:
            self.banco = sqlite3.connect('pontuacaoDB.db')
        except:
            print('Inpossível conexão com o BD')

        self.cursor = self.banco.cursor()

        try:

            self.cursor.execute("""
            create table if not exists PONTUACAO(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , 
                data Text,
                pontos Integer
            );
            """)

        except:

            print("Erro ao construir banco de dados!!")

        self.__placar = []

    def salvarNoBanco(self, data, pontos):

        self.cursor.execute(""" 
        INSERT INTO PONTUACAO (data, pontos) 
        VALUES (?, ?)
        """, (data, pontos))

        try:
            self.banco.commit()  # Salva no banco de dados
        except:
            print('Não foi possível salvar no banco de dados')

    def fechaCursor(self):

        self.cursor.close()

    def fechaBanco(self):

        self.banco.close()

    def getCursor(self):

        return self.cursor

    def buscaNoBanco(self):

        self.cursor.execute("SELECT * FROM PONTUACAO order by pontos desc")

        for i in self.cursor.fetchall():
            self.__placar.append(i)

    def getPlacar(self):

        return self.__placar


class Ranking(Tela):
    def __init__(self):

        Tela.__init__(self)

        self.__cor = (255, 63, 63)
        self.__ranking = Text("Ranking", dark_red, 90)
        self.__ranking.rect.top = 0
        self.__ranking.rect.left = LARGURA / 2 - (self.__ranking.rect.width / 2) + 30

        self.__voltar = Text("Pressione ESPAÇO para voltar", black, 28)
        self.__voltar.rect.center = (LARGURA / 2, ALTURA - self.__voltar.rect.height/2)

    def blitaRanking(self, tela):

        tela.blit(self.__ranking.text, self.__ranking.rect)

        tela.blit(self.__voltar.text, self.__voltar.rect)

    def ranking(self):

        bd = BancoDeDados()

        bd.buscaNoBanco()

        placar = bd.getPlacar()

        y = 100

        x = 150

        if len(placar) == 0:

            mensagem = Text("BANCO DE DADOS VAZIO!!", black, 60)
            mensagem.rect.centerx = LARGURA / 2
            mensagem.rect.centery = ALTURA / 2

            Tela.getTela(self).blit(mensagem.text, mensagem.rect)

        else:

            if len(placar) > 21:

                tamanho = 21

            else:

                tamanho = len(placar)

            if tamanho > 14:
                for j in range(2):
                    for i in range(7):
                        aux = placar[i+j*7]

                        data, pontos = aux[1], aux[2]

                        temp = Text('{} -----> {}'.format(str(data), str(pontos)), cor_branca, 30)
                        temp.rect.left = x
                        temp.rect.top = y
                        Tela.getTela(self).blit(temp.text, temp.rect)
                        y += 50

                    x = temp.rect.right + 30
                    y = 100

                    for i in range(14, tamanho):
                        aux = placar[i]

                        data, pontos = aux[1], aux[2]

                        temp = Text('{} -----> {}'.format(str(data), str(pontos)), cor_branca, 30)
                        temp.rect.left = x
                        temp.rect.top = y
                        Tela.getTela(self).blit(temp.text, temp.rect)
                        y += 50


            elif tamanho > 7:
                for i in range(7):
                    aux = placar[i]

                    data, pontos = aux[1], aux[2]

                    temp = Text('{} -----> {}'.format(str(data), str(pontos)), cor_branca, 30)
                    temp.rect.left = x
                    temp.rect.top = y
                    Tela.getTela(self).blit(temp.text, temp.rect)
                    y += 50

                x = temp.rect.right + 30
                y = 100

                for i in range(7, tamanho):
                    aux = placar[i]

                    data, pontos = aux[1], aux[2]

                    temp = Text('{} -----> {}'.format(str(data), str(pontos)), cor_branca, 30)
                    temp.rect.left = x
                    temp.rect.top = y
                    Tela.getTela(self).blit(temp.text, temp.rect)
                    y += 50

            else:
                for i in range(tamanho):
                    aux = placar[i]

                    data, pontos = aux[1], aux[2]

                    temp = Text('{} -----> {}'.format(str(data), str(pontos)), cor_branca, 30)
                    temp.rect.left = x
                    temp.rect.top = y
                    Tela.getTela(self).blit(temp.text, temp.rect)
                    y += 50


class Imagem(object):
    def __init__(self, pasta, nome):
        self.image = self.load_image(pasta, nome)
        self.rect = self.image.get_rect()
        if (pasta == 'fundo'):
            self.rect.center = (LARGURA / 2, ALTURA / 2)

    def load_image(self, pasta, nome):
        fullname = os.path.join("images/{}".format(pasta), nome)
        try:
            image = pygame.image.load(fullname)
        except pygame.error.message:
            print('Impossível carregar imagem : ', fullname)
            # raise SystemExit, message
        return image


class Audio():
    def __init__(self, nome):
        fullname = os.path.join("audios", nome)
        try:
            self.music = pygame.mixer.music
            self.music.load(fullname)
        except pygame.error.message:
            print('Impossível carregar audio : ', fullname)
            # raise SystemExit, message

    def play(self):
        self.music.play(-1)

    def stop(self):
        self.music.stop()


class Obstaculo():
    def __init__(self):
        self.list_obj = []

    def dispara(self):
        object = Bloco()
        object.cria()
        self.list_obj.append(object)


class Bloco(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = []
        self.anime = 0
        self.rect = 0
        self.velocidade = -4
        self.pos_imagem = 0
        self.tempo = 4

    def cria(self):
        indice = random.randint(1, 3)
        pasta = "obstaculo\{}".format(indice)
        for i in range(8):
            aux = Imagem(pasta, "{}.png".format(i + 1))
            self.image.append(aux)

        self.rect = self.image[self.pos_imagem].rect
        self.rect.height -= 10
        self.rect.width -= 10
        self.rect.left = LARGURA + 1
        self.rect.bottom = random.randrange(int(CHAO - (self.rect.height * 3 / 2)), CHAO)

    def animacao(self, rect):
        if (self.tempo == 0):
            self.tempo = 4
            if (self.pos_imagem == 7):
                self.pos_imagem = 0
            else:
                self.pos_imagem += 1
        else:
            self.tempo -= 1

        self.anime = self.image[self.pos_imagem]
        self.rect = rect

    def colocar(self, superficie):
        superficie.blit(self.anime.image, self.rect)

    def trajetoria(self):
        self.rect.move_ip(self.velocidade, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.impulso = 0
        self.gravidade = 4
        self.queda = 0
        self.image = []
        self.image_pula = []
        self.pos_imagem = 0
        self.tempo = 5

        for i in range(28):
            aux = Imagem("player", "{}.png".format(i + 1))
            self.image.append(aux)
        for i in range(12):
            aux = Imagem("jump", "{}.png".format(i + 1))
            self.image_pula.append(aux)

        self.anime = self.image[self.pos_imagem]
        self.rect = self.anime.rect
        self.rect.left = 10
        self.rect.bottom = CHAO
        self.chao = self.rect.bottom

    def animacao(self, rect):
        if (self.pos_imagem >= 27):
            self.pos_imagem = 0
        else:
            self.pos_imagem += 1

        self.anime = self.image[self.pos_imagem]
        self.rect = rect

    def animacao_salto(self, rect):
        if (self.rect.bottom == CHAO):
            self.pos_imagem = 0
        elif (self.pos_imagem < 11):
            self.pos_imagem += 1

        self.anime = self.image_pula[self.pos_imagem]
        self.rect = rect

    def movimento(self):
        self.rect.move_ip(0, (self.gravidade + self.impulso + self.queda))

    def salto(self):
        if (self.rect.bottom == CHAO):
            self.impulso = -17

    def limite(self):
        if (self.rect.top <= CHAO - 4 * self.rect.height):
            self.impulso = -1
        elif self.rect.bottom >= CHAO:
            self.rect.bottom = CHAO
            self.impulso = 0
            self.queda = 0


class colide():
    def __init__(self, player, list, tela):
        self.player = player
        self.list = list
        self.tela = tela

    def testa(self):
        for retangulo in self.list.list_obj:
            if self.player.rect.colliderect(retangulo.rect):
                return True
            else:
                return False


class Pontuacao():
    def __init__(self):
        self.num = 0

    def incrementa(self):
        self.num += 1


class Text():
    def __init__(self, descricao, cor, tamanho=20):
        pygame.font.init()
        self.tamanho = tamanho
        self.font_text = pygame.font.SysFont(pygame.font.get_default_font(), self.tamanho)
        self.text = self.font_text.render(descricao, 1, cor)
        self.rect = self.text.get_rect()

    def coloca(self, tela):
        tela.blit(self.text, self.rect)


class tela_perdeu():
    def __init__(self, pontuacao):
        self.perdeu = Text("Sua pontuação foi de : {}".format(pontuacao), green, 40)
        self.perdeu.rect.centerx = LARGURA / 2
        self.perdeu.rect.centery = ALTURA / 2 + 100

    def coloca(self, tela):
        tela.blit(self.perdeu.text, self.perdeu.rect)


class Botao(Text):
    def __init__(self, desc, x, y, l, a):
        Text.__init__(self, desc, black, 30)

        self.surface = pygame.Surface((l, a))
        self.Brect = self.surface.get_rect()
        self.Brect.x = x
        self.Brect.y = y
        self.rect = self.Brect

    def coloca(self, tela):
        tela.blit(self.surface, self.Brect)
        Text.coloca(self, tela)

    def brilha(self, mouse, cor, corB):
        if (self.Brect.collidepoint(mouse)):
            self.surface.fill(corB)
        else:
            self.surface.fill(cor)


def gameover(tela, pontos):
    over = tela_perdeu(pontos)
    fundo = Imagem("fundo", "gameover.png")
    rect = fundo.rect
    rect.center = (LARGURA / 2, ALTURA / 2)
    tela.blit(fundo.image, rect)
    press = Text("Pressione ESPAÇO para voltar", black, 30)
    press.rect.center = (LARGURA / 2, ALTURA - 50)
    audio = Audio("gameover.mp3")
    quit = False

    audio.play()

    now = datetime.now()
    dataHoje = ('{}/{}/{}'.format(now.day, now.month, now.year))

    banco = BancoDeDados()

    pygame.font.init()

    banco.salvarNoBanco(dataHoje, pontos)
    banco.fechaCursor()
    banco.fechaBanco()

    while not (quit):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                quit = True

        tela.blit(fundo.image, rect)
        tela.blit(over.perdeu.text, over.perdeu.rect)
        tela.blit(press.text, press.rect)

        pygame.display.update()
        pygame.display.flip()

    audio.stop()
    TelaMenu(tela)


def TelaMenu(tela):
    menu = Imagem('fundo', 'menu.png')
    intro = True
    relogio = pygame.time.Clock()
    audio = Audio('menu.mp3')
    botao_inicia = Botao("Novo jogo", 340, 310, 200, 35)
    botao_mudar = Botao("Mudar Avatar", 340, 355, 200, 35)
    botao_recorde = Botao("Recordes", 340, 400, 200, 35)
    botao_sair = Botao("Sair", 340, 445, 200, 35)
    icone = []
    piscaText = 0
    for i in range(28):
        aux = Imagem("player", "{}.png".format(i + 1))
        icone.append(aux)


    pygame.font.init()
    audio.play()


    while intro:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN and botao_sair.Brect.collidepoint(
                    mouse):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_inicia.Brect.collidepoint(mouse):
                    audio.stop()
                    main(tela)

                elif botao_recorde.Brect.collidepoint(mouse):
                    audioRanking = Audio("ranking.mp3")
                    audioRanking.play()
                    ranking = Ranking()
                    rkg_op = True
                    while rkg_op:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    rkg_op = False
                                    TelaMenu(tela)

                        fundo = Imagem("fundo", "ranking.jpg")
                        tela.blit(fundo.image, (0, 0))
                        ranking.ranking()
                        ranking.blitaRanking(tela)

                        pygame.display.update()
                        pygame.display.flip()

                elif botao_mudar.Brect.collidepoint(mouse):
                    rkg_op = True
                    fundo = Imagem("fundo", "trocaravatar.png")
                    i = 0
                    tempo = 2
                    voltar = Text("Pressione ESPAÇO para voltar", black, 30)
                    voltar.rect.center = (LARGURA / 2, ALTURA - 50)

                    while rkg_op:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    rkg_op = False

                        if (tempo == 0):
                            if (i == 27):
                                i = 0
                            else:
                                i += 1
                            tempo = 2
                        else:
                            tempo -= 1

                        icone[i].rect.center = fundo.rect.center

                        tela.blit(fundo.image, (0, 0))
                        tela.blit(icone[i].image, icone[i].rect)
                        voltar.coloca(tela)

                        pygame.display.update()
                        pygame.display.flip()

        tela.blit(menu.image, menu.rect)
        if (piscaText == 2):
            piscaText = 0
        else:
            piscaText += 1

        TextSurf = Text("AgentStudentRun", v_cor[piscaText], 60)
        TextRect = TextSurf.rect
        TextRect.center = ((LARGURA / 2), (ALTURA / 6))
        tela.blit(TextSurf.text, TextRect)

        botao_inicia.brilha(mouse, dark_green, green)
        botao_recorde.brilha(mouse, dark_green, green)
        botao_mudar.brilha(mouse, dark_green, green)
        botao_sair.brilha(mouse, dark_red, red)

        botao_inicia.coloca(tela)
        botao_mudar.coloca(tela)
        botao_recorde.coloca(tela)
        botao_sair.coloca(tela)

        pygame.display.update()
        pygame.display.flip()
        relogio.tick(15)



def main(tela):
    audio = Audio('game.mp3')
    jogador = Player()
    fundo = Imagem('fundo', 'mapa.png')
    objeto = Obstaculo()
    pontuacao = Pontuacao()
    quit = False
    relogio = pygame.time.Clock()
    TRAND = random.randrange(0, 50)
    time = 55 + TRAND
    tempoAnime = 10
    pontuacao_txt = Text("Pontos : {}".format(pontuacao.num), black, 40)
    pontuacao_txt.rect.top = 0
    pontuacao_txt.rect.right = LARGURA

    audio.play()
    pygame.font.init()

    while not (quit):

        relogio.tick(70)
        time -= 1
        tempoAnime -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jogador.salto()
                elif event.key == pygame.K_DOWN:
                    pygame.key.set_repeat(1, 500)
                    jogador.queda = 20

        if time == 0:
            objeto.dispara()
            TRAND = random.randrange(0, 50)
            time = 55 + TRAND

        if (jogador.impulso == 0):
            jogador.animacao(jogador.rect)
        else:
            jogador.animacao_salto(jogador.rect)

        jogador.movimento()
        jogador.limite()

        tela.blit(fundo.image, fundo.rect)
        tela.blit(jogador.anime.image, jogador.rect)

        if len(objeto.list_obj) > 0:
            for x in objeto.list_obj:
                x.animacao(x.rect)
                x.colocar(tela)
                x.trajetoria()
                if x.rect.right <= 0:
                    pontuacao.incrementa()
                    objeto.list_obj.remove(x)

        pontuacao_txt = Text("Pontos : {}".format(pontuacao.num), black, 40)
        pontuacao_txt.coloca(tela)

        teste = colide(jogador, objeto, tela)
        quit = teste.testa()

        pygame.display.flip()

        if (quit):
            audio.stop()
            gameover(tela, pontuacao.num)


TelaMenu(tela)
