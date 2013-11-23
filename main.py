import pygame
from pygame.color import THECOLORS
from pygame.locals import *

pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('RPG@Home Actuator')

screen.fill(THECOLORS['white'])
font = pygame.font.Font(None, 36)
text = font.render("Initializing...", 1, (10, 10, 10))
textpos = text.get_rect()
textpos.centerx = screen.get_rect().centerx
screen.blit(text, textpos)
pygame.display.flip()


# Sound init
print 'Load sound'
pygame.mixer.music.load("alrighty.wav")

# Play happy sound
print 'Play sound'
pygame.mixer.music.play()


shouldRun = True


# Main loop
while shouldRun:
    # rgb_frame = refresh_image()

    # Display in window
    # screen.blit(rgb_frame, (0, 0))
    # pygame.display.flip()

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_RETURN or \
                event.type == MOUSEBUTTONUP:
            pass
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            print 'Quitting'
            shouldRun = False
            break