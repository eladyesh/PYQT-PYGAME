
# importing the required modules
import pygame
import random
from math import *
from pygame import mixer
from pygame.surface import Surface, SurfaceType

# Initialize the pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space.jpg')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_Change = 0

# Enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
number_of_enemies = 6

for i in range(number_of_enemies):

    # Appending the required data for each enemy
    # image, start x,y coordinates, their change in speed
    enemy_image.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(50, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(3)
    enemyY_Change.append(40)

# Bullet
# Ready - the player charges the bullet
# Fire - the player fires the bullet
bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 10
bullet_state = "ready"

# Score
score_value = 0

# Font
font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 10, 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 50)


def show_score(x, y):

    # Showing the score on the left north corner of the screen
    score = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():

    # Showing the participant game is over
    over_text = over_font.render(f"GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))


def player(x, y):

    """
    :param x: player x coordinate
    :param y: player y coordinate
    the function places the image - spaceship in the x,y coordinates
    """

    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    # Showing enemy on screen
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):

    # Firing the bullet
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):

    # Distance between enemy and bullet
    distance = sqrt(pow((enemyX - bulletX), 2) + pow((enemyY - bulletY), 2))

    # if distance between player and the enemy is less then 27 - there is a collision
    if distance < 27:
        return True
    else:
        return False


# Game loop
run = True
while run:

    # RGB - RED, GREEN , BLUE
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # if keystroke is pressed check whether is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -5
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5

            # firing the bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":

                    # playing bullet sound
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()

                    # Get the current x coordinate of the spaceship, and shoot the bullet
                    bulletX = playerX
                    fire_bullet(playerX, playerY)

        # release of the key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    # Moving the player and the enemy displaying the new position
    # Checking boundaries of spaceship and enemy
    playerX += playerX_Change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(number_of_enemies):

        # Game Over
        if enemyY[i] > 420:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        # Checking and changing enemy's boundaries
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 3
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] = -3
            enemyY[i] += enemyY_Change[i]

        # Checking for collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(50, 735)
            enemyY[i] = random.randint(50, 150)

        # displaying the enemy
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # firing bullet
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    # displaying the player and running the game
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
