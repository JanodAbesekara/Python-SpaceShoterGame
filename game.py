import pygame
import math
import random
from  pygame import mixer
# Initialize the pygame library
pygame.init()

# Create display
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('ai.jpg')

#background sound
mixer.music.load("back.wav")
mixer.music.play(-1)

# Set title and icon
pygame.display.set_caption("Space Fighter")
icon = pygame.image.load('01.png')
pygame.display.set_icon(icon)

# Load the "play" image
playG = pygame.image.load("spaceship.png")
playGX = 380
playGY = 480
playGX_change = 0

# Load the "missile" image
missile = []
missileX = []
missileY = []
missileX_change = []
missileY_change = []
num_of_count = 6

for i in range(num_of_count):
    missile.append(pygame.image.load("alien.png"))
    missileX.append(random.randint(0, 735))
    missileY.append(random.randint(50, 150))
    missileX_change.append(0.3)
    missileY_change.append(40)

# Attack to enemy
attack = pygame.image.load("missiles.png")
attackX = 0
attackY = 480
attackX_change = 0
attackY_change = 1
attack_state = "ready"

scroe = 0
# score font
font = pygame.font.Font('freesansbold.ttf',34)

textX = 620
textY = 10

# game over text
Over = pygame.font.Font('freesansbold.ttf',64)

def show_score(X,Y):
    score_count = font.render("Score : " + str(scroe),True, (255,255,255))
    screen.blit(score_count,(X,Y))

def over_game():
    over = Over.render("GAME OVER ",True, (255,255,255))
    screen.blit(over,(200,250))
# Function to display the "play" image
def playgame(X, Y):
    screen.blit(playG, (X, Y))


def missilegame(X, Y,i):
    screen.blit(missile[i], (X, Y))


def attack_enemy(X, Y):
    global attack_state
    attack_state = "fire"
    screen.blit(attack, (X, Y))


def collision(missileX, missileY, attackX, attackY):
    distance = math.sqrt(math.pow(missileX - attackX, 2) + (math.pow(missileY - attackY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Main game loop
runtime = True
while runtime:
    # Background color change
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runtime = False

        # Adding moving left and right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playGX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playGX_change = 0.3

            if event.key == pygame.K_SPACE:
                if attack_state == "ready":
                    bullet_sound = mixer.Sound("shoot.wav")
                    bullet_sound.play()
                    attackX = playGX
                    attack_enemy(attackX, attackY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playGX_change = 0

    playGX += playGX_change

    if playGX <= 0:
        playGX = 0
    elif playGX >= 735:
        playGX = 735

    # Enemy movement

    for i in range(num_of_count):

        #game over
        if missileY[i] > 440:
            for j in range(num_of_count):
                missileY[j] = 2000
            over_game()
            break

        missileX[i] += missileX_change[i]

        if missileX[i] <= 0:
           missileX_change[i] = 0.3
           missileY[i] += missileY_change[i]
        elif missileX[i] >= 735:
           missileX_change[i] = -0.3
           missileY[i] += missileY_change[i]


        is_collision = collision(missileX[i], missileY[i], attackX, attackY)
        if is_collision:
            enemy_sound = mixer.Sound("enemyA.wav")
            enemy_sound.play()
            attackY = 480
            attack_state = "ready"
            scroe += 1
            print(scroe)
            missileX[i] = random.randint(0, 735)
            missileY[i] = random.randint(50, 150)

        missilegame(missileX[i], missileY[i],i)

    # Missile fire

    if attackY <= 0:
        attackY = 480
        attack_state = "ready"

    if attack_state == "fire":
        attack_enemy(attackX, attackY)
        attackY -= attackY_change



    playgame(playGX, playGY)
    show_score(textX,textY)
    pygame.display.update()
