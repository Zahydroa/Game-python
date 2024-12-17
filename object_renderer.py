import pygame

#initialize the pygame
pygame.init()
screen = pygame.display.set_mode((800,600)) #Tạo kích thước màn hình

#Title and Icon
pygame.display.set_caption("PYTHON GAME")
icon = pygame.image.load('icon')
pygame.display.set_icon(icon)

#create an infinite loop (để game chạy) và break bằng tạo nút thoát (sự kiện quit programme)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #change the color of background due to RGB = Red,Green,Blue 
    screen.fill((255,0,0))
    pygame.display.update()

