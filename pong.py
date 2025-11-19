import pygame
import sys
import time
import random

# Inizializza Pygame
pygame.init()
# Creazione della finestra
WIDTH=480
HEIGHT=800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

#Setting colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Setting player
PLAYERWIDTH = 50
PLAYERHEIGHT = 20
arr = (1, -1)

#Creazione di tutti i font
title = pygame.font.Font("font/score.ttf", int(WIDTH/5))
menu_font = pygame.font.Font("font/score.ttf", int(WIDTH/25))
score_font = pygame.font.Font("font/score.ttf", int(WIDTH/15))
impact = pygame.font.SysFont("Impact", int(WIDTH/10))

#Creazione del testo nel menu
menu_title = title.render("PONG", True, WHITE)
menu_title_rect = menu_title.get_rect(center =(WIDTH/2, HEIGHT/4))
menu_bot = menu_font.render("Gioca contro il computer", True, WHITE)
menu_bot_rect = menu_bot.get_rect(center =(WIDTH/2, HEIGHT/2))
menu_friend = menu_font.render("Gioca contro un amico", True, WHITE)
menu_friend_rect = menu_friend.get_rect(center =(WIDTH/2, HEIGHT/2 + 100))
#menu_shop = menu_font.render("Negozio", True, WHITE)
#menu_shop_rect = menu_shop.get_rect(center =(width/2, height/2 + 200))
menu_settings = menu_font.render("Impostazioni", True, WHITE)
menu_settings_rect = menu_settings.get_rect(center =(WIDTH/2, HEIGHT/2 + 300))
menu_exit = menu_font.render("Esci dal gioco", True, WHITE)
menu_exit_rect = menu_exit.get_rect(center =(WIDTH/2, HEIGHT/2 + 350))

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

# Creazione dei file audio
pygame.mixer.init()
pygame.mixer.music.load('music/%d.mp3' %random.randint(0,11))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops=-1)

#Definisci classi
class Player:
    def __init__(self, y, x = WIDTH/2, speed = 6, score = 0, color = WHITE):
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
        ball.vx = random.uniform(-0.99, 0.99)
        if ball.speed < 20:
            ball.speed += 0.25
        
    def move(self):
        self.x += self.speed * self.vx
        self.y += self.speed * self.vy
    
    def isTouchingWall(self):
        if ball.x <= ball.radius or ball.x >= WIDTH - ball.radius:
            return True

    def touchingPlayer1(self):
        if (player1.x - ball.radius <= ball.x < player1.x + PLAYERWIDTH + ball.radius) and (HEIGHT - (PLAYERHEIGHT + ball.radius) <= ball.y <= HEIGHT - ball.radius):
            return True
    def touchingPlayer2(self):
        if (player2.x - ball.radius <= ball.x <= player2.x + PLAYERWIDTH + ball.radius) and (ball.radius <= ball.y <= PLAYERHEIGHT + ball.radius):
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

#Crea la palla e i due giocatori
ball = Ball()
player1 = Player(y = HEIGHT - PLAYERHEIGHT)
player2 = Player(y = 0)

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logica del menu
    if menu == True:

        # Disegna menu
        drawMenu()

        #Eventi menu
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
        if event.type == pygame.MOUSEBUTTONUP and mouse_pressed == True:  
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
            mouse_pressed = False

    #Logica di gioco
    elif play == True:
                
        #Loop della pallina
        ball.move()

        #Logica dei rimbalzi della pallina sulla parete
        if ball.isTouchingWall():
            ball.vx = -ball.vx

        #Logica di quando la pallina rimbalza su un giocatore
        if (ball.touchingPlayer1()):
            ball.vy = -1
            ball.bounces()
        elif (ball.touchingPlayer2()):
            ball.vy = 1
            ball.bounces()
        
        #Logica di quando la pallina segna
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

        #Movimento giocatore 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if player1.x > 0:
                    player1.moveLeft()
            if event.key == pygame.K_RIGHT:
                if player1.x < WIDTH - PLAYERWIDTH:
                    player1.moveRight()

        # Movimento giocatore 2, a seconda se è un bot o meno
        if bot == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                if player2.x > 0:
                    player2.moveLeft()
            if keys[pygame.K_d]:
                if player2.x < WIDTH - PLAYERWIDTH:
                    player2.moveRight()
        else:
            #Insegue la pallina solo se sta andando verso di lui
            if ball.vy == -1:

                if 0 <= player2.x <= WIDTH - PLAYERWIDTH:
                    if ball.x >= player2.x + PLAYERWIDTH/2:
                        player2.moveRight()
                    if ball.x <= player2.x + PLAYERWIDTH/2:
                        player2.moveLeft()
                        
                #Fixa bordi
                if player2.x < 0:
                    player2.x = 0
                if player2.x > WIDTH - PLAYERWIDTH:
                    player2.x = WIDTH - PLAYERWIDTH

        #Entra nel menu di pausa con Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                key_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE and key_pressed:
                paused = not paused
                play = not play
                key_pressed = False

        #Disegna tutto
        drawPlay()
    
    #Logica del menu di pausa
    elif paused == True:

        pygame.mixer.music.pause()
        screen.blit(resume_text, resume_text_rect)
        screen.blit(goback, goback_rect)

        #Esci dal menu di pausa con Esc
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                key_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE and key_pressed:
                paused = not paused
                play = not play
                key_pressed = False

        #Esci dal menu di pausa cliccando sulle scritte
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and mouse_pressed == True:  
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
            mouse_pressed = False

    #Logica delle impostazioni
    elif settings == True:
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
        if event.type == pygame.MOUSEBUTTONUP and mouse_pressed:    
            if music_OFF_rect.collidepoint(event.pos):
                if music:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                music = not music

            if goback_center_rect.collidepoint(event.pos):
                menu = True
                settings = False
            mouse_pressed = False

        screen.fill(RED)
        if music:
            screen.blit(music_ON, music_ON_rect)
        else:
            screen.blit(music_OFF, music_OFF_rect)
        screen.blit(goback, goback_center_rect)

    #Aggiorna schermo periodicamente
    pygame.display.flip()
    pygame.time.Clock().tick(60)

closeAll()
