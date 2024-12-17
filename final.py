# I.Initialize
import pygame
import math
import random

from pygame import mixer

pygame.init()
# Kích thước màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("PYTHON GAME")
icon = pygame.image.load('galaxy.png')
pygame.display.set_icon(icon)

#background music
mixer.music.load('rocketman.mp3')
mixer.music.play(-1)

# Hình nền và nút
main_background = pygame.image.load('thumbnail.png')  # Hình nền màn chính
start_button_img = pygame.image.load('startbutton.png')  # Nút start

# Chỉnh lại kích thước của nút start
start_button_width = 200  # Chiều rộng mới
start_button_height = 100  # Chiều cao mới
start_button_img = pygame.transform.scale(start_button_img, (start_button_width, start_button_height))

# Đặt nút start vào giữa màn hình
start_button_x = (screen_width - start_button_width) // 2
start_button_y = (400)

start_button_width = start_button_img.get_width()
start_button_height = start_button_img.get_height()

background = pygame.image.load('finalbackground.png')

# Biến trạng thái game
game_state = "main_menu"  # "main_menu" hoặc "play_game"

# II.Player Setup
    # 2.1/ Tạo các biến
playerImg =  pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

    # 2.2/ Tạo hàm để liên kết các biến
def player(x,y):
    screen.blit(playerImg, (x, y))

# III. Enemy Setup
    # 3.1/ Tạo các biến
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)


    # 3.2/ Tạo hàm để liên kết các biến
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

# IV. Bullet Setup
    # 3.1/ Tạo các biên
    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving
bulletImg =  pygame.image.load('bullet.png') #Tải ảnh monster
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('Kid Games.ttf',32)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("SCORE:" + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

#game over text
over_font = pygame.font.Font('Kid Games.ttf',84)
def game_over_text():
    over_text = over_font.render('GAME OVER', True,(255,255,255))
    screen.blit(over_text, (100,250))

    # 3.2/ tạo hàm để liên kết các biến
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire" #change the state of bullet
    screen.blit(bulletImg, (x + 16,y + 10))

#isCollision
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance <= 27:
        return True
    else:
         return False

# Vẽ màn hình chính
def draw_main_menu():
    screen.blit(main_background, (0, 0))
    screen.blit(start_button_img, (start_button_x, start_button_y))
    pygame.display.update()

# Kiểm tra nếu nút được nhấn
def is_button_clicked(mouse_x, mouse_y, button_x, button_y, button_width, button_height):
    return button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
    
# V.Game loop
running = True
while running:
    if game_state == "main_menu":
        # Hiển thị màn hình chính
        draw_main_menu()

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if is_button_clicked(mouse_x, mouse_y, start_button_x, start_button_y, start_button_width, start_button_height):
                    game_state = "play_game"  # Chuyển sang màn chơi

    elif game_state == "play_game":
        # Hiển thị màn chơi
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        #5.3/ Khởi tạo điều kiện vòng lặp     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #a. Player and Bullet movement    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -2
                if event.key == pygame.K_RIGHT:
                    playerX_change = 2
                if event.key == pygame.K_SPACE:
                    
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        #Boundary
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        
        #Enemy Movement
        for i in range(num_of_enemies):

            #Game over
            if enemyY[i] > 400:
                for i in range(num_of_enemies):
                    enemyY[i] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] =0.3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.3
                enemyY[i] += enemyY_change[i]
            
            #Collision
            collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
            if collision:
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0,735)
                enemyY[i] = random.randint(50,150)
            
            enemy(enemyX[i],enemyY[i],i)

        #Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "Ready"

        if bullet_state is "fire":
            fire_bullet(bulletX,bulletY)
            bulletY -= bulletY_change

        player(playerX,playerY)
        show_score(textX,textY)
    pygame.display.update()

