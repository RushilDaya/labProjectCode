import sys, random, pygame
from pygame.locals import *

w = 1000
h = 1000

image1 = pygame.image.load('pattern/pattern1.png')
image2 = pygame.image.load('pattern/pattern2.png')

screen = pygame.display.set_mode((w,h))
rectA = pygame.Surface((200,200))

rectB = pygame.Surface((200,200))


rec1 = Rect(400,400,200,200)


clock = pygame.time.Clock()
toggle = True
while True:
    ft = clock.tick_busy_loop(60)
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
    if toggle == True:
    	toggle = False
    	screen.blit(image1, rec1)
    	pygame.display.update(rec1)
    else:
    	toggle = True
    	screen.blit(image2, rec1)
    	pygame.display.update(rec1)
    print(ft)

