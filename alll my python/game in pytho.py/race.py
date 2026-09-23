import sys
import pygame

# ============================================================
# JOGO DA VELHA - PYGAME
# ============================================================

pygame.init()

# -------------------- CONFIGURAÇÕES --------------------

LARGURA = 600
ALTURA = 700
TAMANHO_TABULEIRO = 600

LINHAS = 3
COLUNAS = 3
TAMANHO_QUADRADO = TAMANHO_TABULEIRO // 3

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Velha")

relogio = pygame.time.Clock()

# -------------------- CORES --------------------

COR_FUNDO = (28, 170, 156)
COR_TABULEIRO = (23, 145, 135)
COR_X = (84, 84, 84)
COR_O = (239, 231, 200)
COR_BRANCO = (255, 255, 255)
COR_AMARELO = (255, 215, 0)
COR_HOVER = (40, 190, 175)

# -------------------- FONTES --------------------

fonte_titulo = pygame.font.Font(None, 50)
fonte_mensagem = pygame.font.Font(None, 42)
fonte_pequena = pygame.font.Font(None, 30)

# -------------------- ESTADO DO JOGO --------------------

tabuleiro = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

turno = "X"
jogo_acabou = False
vencedor = None
linha_vencedora = None

placar = {
    "X": 0,
    "O": 0
}


# ============================================================
# DESENHAR TABULEIRO
# ============================================================

def desenhar_tabuleiro():
    tela.fill(COR_FUNDO)

    # Linhas verticais
    for coluna in range(1, 3):
        x = coluna * TAMANHO_QUADRADO

        pygame.draw.line(
            tela,
            COR_TABULEIRO,
            (x, 0),
            (x, TAMANHO_TABULEIRO),
            12
        )

    # Linhas horizontais
    for linha in range(1, 3):
        y = linha * TAMANHO_QUADRADO

        pygame.draw.line(
            tela,
            COR_TABULEIRO,
            (0, y),
            (TAMANHO_TABULEIRO, y),
            12
        )


# ============================================================
# DESENHAR X E O
# ============================================================

def desenhar_figuras():
    margem = 55

    for linha in range(3):
        for coluna in range(3):

            centro_x = (
                coluna * TAMANHO_QUADRADO
                + TAMANHO_QUADRADO // 2
            )

            centro_y = (
                linha * TAMANHO_QUADRADO
                + TAMANHO_QUADRADO // 2
            )

            valor = tabuleiro[linha][coluna]

            # ---------------- X ----------------

            if valor == "X":

                inicio_x = coluna * TAMANHO_QUADRADO + margem
                inicio_y = linha * TAMANHO_QUADRADO + margem

                fim_x = (
                    (coluna + 1) * TAMANHO_QUADRADO
                    - margem
                )

                fim_y = (
                    (linha + 1) * TAMANHO_QUADRADO
                    - margem
                )

                pygame.draw.line(
                    tela,
                    COR_X,
                    (inicio_x, inicio_y),
                    (fim_x, fim_y),
                    18
                )

                pygame.draw.line(
                    tela,
                    COR_X,
                    (inicio_x, fim_y),
                    (fim_x, inicio_y),
                    18
                )

            # ---------------- O ----------------

            elif valor == "O":

                pygame.draw.circle(
                    tela,
                    COR_O,
                    (centro_x, centro_y),
                    75,
                    15
                )


# ============================================================
# VERIFICAR VITÓRIA
# ============================================================

def verificar_vitoria(jogador):

    # Linhas
    for linha in range(3):

        if (
            tabuleiro[linha][0] == jogador
            and tabuleiro[linha][1] == jogador
            and tabuleiro[linha][2] == jogador
        ):
            return [
                (linha, 0),
                (linha, 1),
                (linha, 2)
            ]

    # Colunas
    for coluna in range(3):

        if (
            tabuleiro[0][coluna] == jogador
            and tabuleiro[1][coluna] == jogador
            and tabuleiro[2][coluna] == jogador
        ):
            return [
                (0, coluna),
                (1, coluna),
                (2, coluna)
            ]

    # Diagonal principal
    if (
        tabuleiro[0][0] == jogador
        and tabuleiro[1][1] == jogador
        and tabuleiro[2][2] == jogador
    ):
        return [
            (0, 0),
            (1, 1),
            (2, 2)
        ]

    # Diagonal inversa
    if (
        tabuleiro[0][2] == jogador
        and tabuleiro[1][1] == jogador
        and tabuleiro[2][0] == jogador
    ):
        return [
            (0, 2),
            (1, 1),
            (2, 0)
        ]

    return None


# ============================================================
# VERIFICAR SE TABULEIRO ESTÁ CHEIO
# ============================================================

def tabuleiro_cheio():

    for linha in range(3):
        for coluna in range(3):

            if tabuleiro[linha][coluna] is None:
                return False

    return True


# ============================================================
# DESENHAR HOVER
# ============================================================

def desenhar_hover():

    if jogo_acabou:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mouse_y >= TAMANHO_TABULEIRO:
        return

    coluna = mouse_x // TAMANHO_QUADRADO
    linha = mouse_y // TAMANHO_QUADRADO

    if tabuleiro[linha][coluna] is None:

        x = coluna * TAMANHO_QUADRADO
        y = linha * TAMANHO_QUADRADO

        pygame.draw.rect(
            tela,
            COR_HOVER,
            (x + 8, y + 8, TAMANHO_QUADRADO - 16, TAMANHO_QUADRADO - 16),
            4
        )


# ============================================================
# DESTACAR VITÓRIA
# ============================================================

def desenhar_linha_vencedora():

    if linha_vencedora is None:
        return

    inicio = linha_vencedora[0]
    fim = linha_vencedora[2]

    linha1, coluna1 = inicio
    linha2, coluna2 = fim

    x1 = coluna1 * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
    y1 = linha1 * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2

    x2 = coluna2 * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
    y2 = linha2 * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2

    pygame.draw.line(
        tela,
        COR_AMARELO,
        (x1, y1),
        (x2, y2),
        12
    )


# ============================================================
# DESENHAR INTERFACE
# ============================================================

def desenhar_interface():

    # Área inferior
    pygame.draw.rect(
        tela,
        (20, 120, 110),
        (0, 600, 600, 100)
    )

    if vencedor:

        mensagem = f"{vencedor} venceu!"

    elif jogo_acabou:

        mensagem = "Empate!"

    else:

        mensagem = f"Vez do jogador: {turno}"

    texto = fonte_mensagem.render(
        mensagem,
        True,
        COR_BRANCO
    )

    tela.blit(
        texto,
        (
            LARGURA // 2 - texto.get_width() // 2,
            615
        )
    )

    # Placar
    placar_texto = fonte_pequena.render(
        f"X: {placar['X']}     O: {placar['O']}     |     R = Reiniciar",
        True,
        COR_BRANCO
    )

    tela.blit(
        placar_texto,
        (
            LARGURA // 2 - placar_texto.get_width() // 2,
            670
        )
    )


# ============================================================
# REINICIAR JOGO
# ============================================================

def reiniciar():

    global tabuleiro
    global turno
    global jogo_acabou
    global vencedor
    global linha_vencedora

    tabuleiro = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]

    turno = "X"
    jogo_acabou = False
    vencedor = None
    linha_vencedora = None


# ============================================================
# FAZER JOGADA
# ============================================================

def fazer_jogada(posicao):

    global turno
    global jogo_acabou
    global vencedor
    global linha_vencedora

    if jogo_acabou:
        return

    mouse_x, mouse_y = posicao

    # Ignorar cliques na área inferior
    if mouse_y >= TAMANHO_TABULEIRO:
        return

    coluna = mouse_x // TAMANHO_QUADRADO
    linha = mouse_y // TAMANHO_QUADRADO

    # Espaço ocupado
    if tabuleiro[linha][coluna] is not None:
        return

    # Colocar peça
    tabuleiro[linha][coluna] = turno

    # Verificar vitória
    resultado = verificar_vitoria(turno)

    if resultado:

        vencedor = turno
        linha_vencedora = resultado
        jogo_acabou = True

        placar[turno] += 1

        return

    # Verificar empate
    if tabuleiro_cheio():

        jogo_acabou = True

        return

    # Trocar jogador
    turno = "O" if turno == "X" else "X"


# ============================================================
# LOOP PRINCIPAL
# ============================================================

while True:

    # ---------------- EVENTOS ----------------

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                fazer_jogada(evento.pos)

        # Teclado
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                reiniciar()
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # ---------------- DESENHO ----------------
    desenhar_tabuleiro()
    desenhar_hover()
    desenhar_figuras()
    desenhar_linha_vencedora()
    desenhar_interface()
    pygame.display.flip()

    # 60 FPS
    relogio.tick(60)

# quem venceu, recerbera parabens e o placar sera atualizado, caso o jogo termine empatado, sera exibido a mensagem "Empate!" na tela.
# depois de o jogado acabar, o jogador pode pressionar a tecla "R" para reiniciar o jogo e começar uma nova partida.