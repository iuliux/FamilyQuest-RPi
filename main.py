import pygame

# Sound init
pygame.mixer.init()
pygame.mixer.music.load("alrighty.wav")

# Play happy sound
pygame.mixer.music.play()
