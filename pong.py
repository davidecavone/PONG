import pygame
import sys
import time
import random
import os

def get_path(percorso_relativo):
    """
    Trova il percorso assoluto del file, sia che siamo in .py sia in .exe
    """
    try:
        # Se siamo in un exe (PyInstaller)
        base_path = sys._MEIPASS
    except Exception:
        # Se siamo in un file .py normale, prendiamo la cartella dove sta questo file
        base_path = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(base_path, percorso_relativo)
    return full_path

# Inizializza Pygame
pygame.init()
# Creazione della finestra
WIDTH = 480
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

# Setting colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setting player
PLAYERWIDTH = 50
PLAYERHEIGHT = 20
arr = (1, -1)

# --- DEBUG FILE SYSTEM ---
# Questo blocco ti aiuta a capire se i percorsi sono giusti
print("--- CONTROLLO FILE ---")
font_path_check = get_path("assets/font/score.ttf")
if os.path.exists(font_path_check):
    print(f"[OK] Font trovato in: {font_path_check}")
else:
    print(f"[ERRORE] Font NON trovato. Il sistema cerca qui: {font_path_check}")
    print("Verifica di avere la cartella 'assets', poi 'font' e dentro 'score.ttf'")
print("----------------------")

# --- CARICAMENTO FONT ---
# Tenta di caricare il font corretto, altrimenti usa quello di sistema ma ti avvisa
path_font = get_path("assets/font/score.ttf")
try:
    title = pygame.font.Font(path_font, int(WIDTH/5))
    menu_font = pygame.font.Font(path_font, int(WIDTH/25))
    score_font = pygame.font.Font(path_font, int(WIDTH/15))
except FileNotFoundError:
    print("!!! IMPOSSIBILE CARICARE IL FONT CUSTOM. USO ARIAL !!!")
    title = pygame.font.SysFont("Arial", int(WIDTH/5))
    menu_font = pygame.font.SysFont("Arial", int(WIDTH/25))
    score_font = pygame.font.SysFont("Arial", int(WIDTH/15))

impact = pygame.font.SysFont("Impact", int(WIDTH/10))

# Creazione del testo nel menu
menu_title = title.render("PONG", True, WHITE)
menu_title_rect = menu_title.get_rect(center=(WIDTH/2, HEIGHT/4))
menu_bot = menu_font.render("Gioca contro il computer", True, WHITE)
menu_bot_rect = menu_bot.get_rect(center=(WIDTH/2, HEIGHT/2))
menu_friend = menu_font.render("Gioca contro un amico", True, WHITE)
menu_friend_rect = menu_friend.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))
menu_settings = menu_font.render("Impostazioni", True, WHITE)
menu_settings_rect = menu_settings.get_rect(center=(WIDTH/2, HEIGHT/2 + 300))
menu_exit = menu_font.render("Esci dal gioco", True, WHITE)
menu_exit_rect = menu_exit.get_rect(center=(WIDTH/2, HEIGHT/2 + 350))

# Creazione del testo in game
score_player1_text = score_font.render("0", True, WHITE)
score_player1_text_rect = score_player1_text.get_rect(center=(WIDTH/2, HEIGHT*(3/4)))
score_player2_text = score_font.render("0", True, WHITE)
score_player2_text_rect = score_player2_text.get_rect(center=(WIDTH/2, HEIGHT/4))

# Creazione del testo in pausa
resume_text = menu_font.render("Riprendi", True, WHITE)
resume_text_rect = resume_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))

# Creazione del testo nelle impostazioni
music_ON = menu_font.render("Musica: ON", True, WHITE)
music_ON_rect = music_ON.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
music_OFF = menu_font.render("Musica: OFF", True, WHITE)
music_OFF_rect = music_OFF.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
goback = menu_font.render("Torna al menu", True, WHITE)
goback_rect = goback.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))
goback_center_rect = goback.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))

# --- CARICAMENTO AUDIO ---
pygame.mixer.init()
# Cerchiamo di caricare una canzone
song_number = random.randint(0, 11)
music_path = get_path(f'assets/music/{song_number}.mp3')

print(f"--- CONTROLLO MUSICA ---")
if os.path.exists(music_path):
    print(f"[OK] Musica trovata: {music_path}")
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=-1)
    except Exception as e:
        print(f"[ERRORE] File trovato ma impossibile riprodurre: {e}")
else:
    print(f"[ERRORE] File musica NON trovato: {music_path}")
    print(f"Assicurati che dentro 'assets/music' ci siano file chiamati 0.mp3, 1.mp3... fino a 11.mp3")
print("------------------------")


# Definisci classi
class Player:
    def __init__(self, y, x=WIDTH/2, speed=6, score=0, color=WHITE):
        self.x = x
        self.y = y
        self.speed = speed
        self.score = score
        self.color = color

    def moveLeft(self):
        self.x -= self.speed

    def moveRight(self):
        self.x += self.speed

    def reset(self):
        self.x = WIDTH/2

    def resetScore(self):
        self.score = 0

class Ball:
    def __init__(self, x=WIDTH/2, y=HEIGHT/2, radius=10, speed=6, color=WHITE, vx=1, vy=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.vx = vx
        self.vy = vy

    def reset(self):
        self.x = WIDTH/2
        self.y = HEIGHT/2
        self.radius = 10
        self.speed = 6
        self.color = WHITE
        self.vx = 1
        self.vy = 1

    def bounces(self):
        self.vx = random.uniform(-0.99, 0.99)
        if self.speed < 20:
            self.speed += 0.25

    def move(self):
        self.x += self.speed * self.vx
        self.y += self.speed * self.vy

    def isTouchingWall(self):
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            return True

    def touchingPlayer1(self):
        if (player1.x - self.radius <= self.x < player1.x + PLAYERWIDTH + self.radius) and (HEIGHT - (PLAYERHEIGHT + self.radius) <= self.y <= HEIGHT - self.radius):
            return True
    def touchingPlayer2(self):
        if (player2.x - self.radius <= self.x <= player2.x + PLAYERWIDTH + self.radius) and (self.radius <= self.y <= PLAYERHEIGHT + self.radius):
            return True

def drawMenu():
    screen.fill(BLACK)
    screen.blit(menu_title, menu_title_rect)
    screen.blit(menu_bot, menu_bot_rect)
    screen.blit(menu_friend, menu_friend_rect)
    screen.blit(menu_settings, menu_settings_rect)
    screen.blit(menu_exit, menu_exit_rect)

def drawPlay():
    screen.fill(BLACK)
    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.radius)
    pygame.draw.rect(screen, player1.color, (player1.x, player1.y, PLAYERWIDTH, PLAYERHEIGHT))
    pygame.draw.rect(screen, player2.color, (player2.x, player2.y, PLAYERWIDTH, PLAYERHEIGHT))
    screen.blit(score_font.render(str(player1.score), True, WHITE), score_player1_text_rect)
    screen.blit(score_font.render(str(player2.score), True, WHITE), score_player2_text_rect)

def closeAll():
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

# Crea la palla e i due giocatori
ball = Ball()
player1 = Player(y=HEIGHT - PLAYERHEIGHT)
player2 = Player(y=0)

# Setting dello stato del gioco iniziale
paused = False
play = False
settings = False
shop = False
bot = False
music = True
menu = True

# Loop principale
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Logica del menu
    if menu == True:
        drawMenu()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                if menu_bot_rect.collidepoint(mouse_pos):
                    menu = False
                    play = True
                    bot = True
                elif menu_friend_rect.collidepoint(mouse_pos):
                    menu = False
                    play = True
                    bot = False
                elif menu_settings_rect.collidepoint(mouse_pos):
                    menu = False
                    settings = True
                elif menu_exit_rect.collidepoint(mouse_pos):
                    closeAll()

    # Logica di gioco
    elif play == True:
        ball.move()

        if ball.isTouchingWall():
            ball.vx = -ball.vx

        if (ball.touchingPlayer1()):
            ball.vy = -1
            ball.bounces()
        elif (ball.touchingPlayer2()):
            ball.vy = 1
            ball.bounces()

        if ball.y >= HEIGHT + ball.radius:
            ball.reset()
            player1.reset()
            player2.reset()
            player2.score += 1
        elif ball.y <= -ball.radius:
            ball.reset()
            player1.reset()
            player2.reset()
            player1.score += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if player1.x > 0:
                player1.moveLeft()
        if keys[pygame.K_RIGHT]:
            if player1.x < WIDTH - PLAYERWIDTH:
                player1.moveRight()

        if bot == False:
            if keys[pygame.K_a]:
                if player2.x > 0:
                    player2.moveLeft()
            if keys[pygame.K_d]:
                if player2.x < WIDTH - PLAYERWIDTH:
                    player2.moveRight()
        else:
            if ball.vy == -1:
                if 0 <= player2.x <= WIDTH - PLAYERWIDTH:
                    if ball.x >= player2.x + PLAYERWIDTH/2:
                        player2.moveRight()
                    if ball.x <= player2.x + PLAYERWIDTH/2:
                        player2.moveLeft()
                if player2.x < 0:
                    player2.x = 0
                if player2.x > WIDTH - PLAYERWIDTH:
                    player2.x = WIDTH - PLAYERWIDTH

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    play = not play

        drawPlay()

    elif paused == True:
        pygame.mixer.music.pause()
        screen.blit(resume_text, resume_text_rect)
        screen.blit(goback, goback_rect)

        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    play = not play
                    pygame.mixer.music.unpause()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                if resume_text_rect.collidepoint(mouse_pos):
                    paused = not paused
                    play = not play
                    pygame.mixer.music.unpause()
                if goback_rect.collidepoint(mouse_pos):
                    ball.reset()
                    player1.reset()
                    player1.resetScore()
                    player2.reset()
                    player2.resetScore()
                    menu = True
                    play = False
                    pygame.mixer.music.stop()
                    pygame.mixer.music.play(-1)
                    paused = False

    elif settings == True:
        screen.fill(RED)
        if music:
            screen.blit(music_ON, music_ON_rect)
        else:
            screen.blit(music_OFF, music_OFF_rect)
        screen.blit(goback, goback_center_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if music_OFF_rect.collidepoint(event.pos):
                    if music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    music = not music
                if goback_center_rect.collidepoint(event.pos):
                    menu = True
                    settings = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)

closeAll()