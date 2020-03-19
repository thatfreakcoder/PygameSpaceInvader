import pygame
import random
import math

# initialise PyGame Module
pygame.init()

# Setup Display
Display = pygame.display.set_mode((800, 600))

# Setup Clock
clock = pygame.time.Clock()

# Set Title and Icon of the Window
pygame.display.set_caption("Arcade Gamer")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


# -------------------------------------PLAYER-----------------------------------------

# Player Coordinates
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0.0
playerY_change = 0


# Player Display
def player(x, y):
    Display.blit(playerImg, (int(x), int(y)))


# ------------------------------------ENEMY-------------------------------------------
# Enemy Coordinates
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_number = 10

# Creating Multiple Enemies
for i in range(enemy_number):
    enemy_type = random.choice(["01.png", "02.png", "03.png", "04.png"])
    enemyImg.append(pygame.image.load(enemy_type))
    enemyX.append(random.randint(0, 733))
    enemyY.append(random.randint(25, 250))
    enemyX_change.append(random.choice([-0.6, 0.8, -1.0, 1.2]))
    enemyY_change.append(random.choice([20, 30, 40, 50]))

# Enemy Display
def enemy(x, y, i):
    Display.blit(enemyImg[i], (int(x), int(y)))


# ------------------------------------BULLET----------------------------------------
# Bullet Coordinates
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 490
bulletX_change = 0
bulletY_change = 4.5
bullet_state = "ready"
bullet_num = 20
bullet_damage = 5

# Bullet Display
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    Display.blit(bulletImg, (int(x + 20), int(y + 10)))


# Bullet Text and Fonts
font_bul = pygame.font.Font("freesansbold.ttf", 32)
textX_bul = 500
textY_bul = 10


# Bullet Count Display
def show_bulletCount(x, y):
    bullet_count = font_bul.render(f"Bullets Left : {bullet_num}", True, (0, 0, 0))
    Display.blit(bullet_count, (x, y))


# -------------------------------BLAST------------------------------------
# Blast Coordinates
blastImg = pygame.image.load("gift.png")
blastX = 0
blastY = 0


# --------------------------------BOMB-------------------------------------
# Bomb Coordinates
bombImg = pygame.image.load("bomb.png")
bombX = 0
bombY = 0
bombY_change = 1
bomb_state = "ready"


# Bomb Display
def drop_bomb(x, y):
    global bomb_state
    bomb_state = "dropping"
    Display.blit(bombImg, (int(x + 20), int(y + 10)))


# ---------------------------------------GIFT-----------------------------------------
# Gift Coordinates
giftImg = pygame.image.load("gift.png")
giftX = 0
giftY = 0
giftY_change = 0.5
gift_state = "ready"


# Gift Display
def drop_gift(x, y):
    global gift_state
    gift_state = "dropping"
    Display.blit(giftImg, (int(x + 20), int(y + 10)))


# --------------------------------SCORING-----------------------------------
# Scorer
score = 0

# Score Text and Fonts
font_sc = pygame.font.Font("freesansbold.ttf", 32)
textX_sc = 10
textY_sc = 10


# Score Display
def dispScore():
    global score
    print(f'YOU KILLED {score} ENEMIES')


# Score
def show_score(x, y):
    scoreText = font_sc.render(f"Score : {score}", True, (0, 0, 200))
    Display.blit(scoreText, (x, y))


# -------------------------------GAME OVER------------------------------
# Game Over Text and Fonts
font_end = pygame.font.Font("freesansbold.ttf", 60)
textX_end = 200
textY_end = 230


# Game Over
def end_game(x, y):
    endText = font_end.render("GAME OVER", False, (200, 0, 0))
    Display.blit(endText, (x, y))


# ------------------------Collision Mathematics--------------------------------
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x2 - x1, 2)) + (math.pow(y2 - y1, 2)))
    if distance < 32:
        return True
    else:
        return False


# ------------------------------Game Loop---------------------------------------
running = True
while running:
    # Setting Background Color
    Display.fill((175, 255, 175))

    # Dropping Bomb
    if bomb_state == "ready":
        bombX = playerX
        drop_bomb(bombX, bombY)

    # Dropping Gift
    if gift_state == "ready":
        giftX = random.randint(20, 700)
        drop_gift(giftX, giftY)

    # Finding Event
    for event in pygame.event.get():

        # End Game by Closing Window
        if event.type == pygame.QUIT:
            dispScore()
            running = False

        # Checking Key Press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Left Movement
                playerX_change = -2
            if event.key == pygame.K_RIGHT:  # Right Movement
                playerX_change = 2
            if event.key == pygame.K_SPACE:  # Shoot
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_ESCAPE:  # Exit Game by Esc Button
                dispScore()
                running = False

        # Checking Key Release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                bullet_num -= 1

    # Handling Specific Enemies
    for i in range(enemy_number):

        # Display Enemy
        enemy(enemyX[i], enemyY[i], i)

        # Enemies Automatic Movement
        enemyX[i] = enemyX[i] + enemyX_change[i]
        if enemyX[i] >= 735:
            enemyX_change[i] = random.choice([-0.6, -0.8, -1.0, -1.2])
            enemyY[i] = enemyY[i] + enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = random.choice([0.6, 0.8, 1.0, 1.2])
            enemyY[i] = enemyY[i] + enemyY_change[i]

        # Bullet Collision
        bullCollision = isCollision(bulletX, enemyX[i], bulletY, enemyY[i])
        if bullCollision and bullet_state == "fire":
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 733)
            enemyY[i] = random.randint(25, 250)

        # Run out of ammo
        if bullet_num < 1:
            for j in range(enemy_number):
                enemyX[j] = 2000
                enemyY[j] = 2000
                end_game(textX_end, textY_end)
                bomb_state = "game end"
                gift_state = "game end"

        # Player and enemy collision
        enemCollision = isCollision(playerX, enemyX[i], playerY, enemyY[i])
        if enemCollision:
            for k in range(enemy_number):
                enemyX[k] = 2000
                enemyY[k] = 2000
                end_game(textX_end, textY_end)
                bomb_state = "game end"
                gift_state = "game end"
                bullet_num = 0

    # Bomb and Player Collision
    bombCollision = isCollision(playerX, bombX, playerY, bombY)
    if bombCollision:
        for i in range(enemy_number):
            enemyX[i] = 2000
            enemyY[i] = 2000
            end_game(textX_end, textY_end)
            bomb_state = "game end"
            gift_state = "game end"
            bullet_num = 0

    # Gift and Player Collision
    giftCollision = isCollision(playerX, giftX, playerY, giftY)
    if giftCollision:
        gift_state = "ready"
        giftY = 0
        bullet_num += 5
        if bullet_num > 20:
            bullet_num = 20

    # Player Movement
    playerX = playerX + playerX_change
    playerY = playerY + playerY_change
    if playerX >= 735:
        playerX = 735
    if playerX <= 0:
        playerX = 0

    # Bullet Firing
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bulletY = 490
        bullet_state = "ready"

    # Dropping Bomb
    if bomb_state == "dropping":
        drop_bomb(bombX, bombY)
        bombY += bombY_change
    if bombY >= 550 and bomb_state == "dropping":
        bomb_state = "ready"
        bombY = 0

    # Dropping Gift
    if gift_state == "dropping":
        drop_gift(giftX, giftY)
        giftY += giftY_change
    if giftY >= 550 and gift_state == "dropping":
        gift_state = "ready"
        giftY = 0

    # Display Player
    player(playerX, playerY)

    # Show Text
    show_score(textX_sc, textY_sc)
    show_bulletCount(textX_bul, textY_bul)

    # Update Display
    pygame.display.update()
