import pygame

pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()

# Sound init
pygame.mixer.music.load("alrighty.wav")

# Play happy sound
pygame.mixer.music.play()
