import pygame
from pygame.color import THECOLORS
from pygame.locals import *

import datetime
from os import path

# -- CONFIGS --

IMGS_PATH = 'images'
UNKN_IMAGE = 'unknown.png'
TV_IMAGE = 'tv.png'
GAMES_IMAGE = 'games.png'

# -------------


pygame.mixer.pre_init(11025, 8, 1, 4096) #frequency, size, channels, buffersize
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('FamilyQuest Actuator')

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


class RewardType:
    TV = 0
    GAMES = 1

class RewardsHandler:
    def __init__(self, font, screen):
        self.pending = []
        self.font = font
        self.screen = screen
        # Images
        self.unknown_img = pygame.image.load(path.join(IMGS_PATH, UNKN_IMAGE))
        self.tv_img = pygame.image.load(path.join(IMGS_PATH, TV_IMAGE))
        self.games_img = pygame.image.load(path.join(IMGS_PATH, GAMES_IMAGE))

    def startReward(self, user, rtype, timespan):
        self.pending.append(
                (user, rtype, datetime.timedelta(seconds=timespan), datetime.datetime.now())
            )
        # SIMULATED: execute real REWARD-START action

    def display(self):
        finished = []
        top = 150
        left = 0
        for i, r in enumerate(self.pending):
            usr, rtype, timespan, starttime = r
            timepassed = datetime.datetime.now() - starttime
            timeremain = timespan - timepassed
            if timeremain.total_seconds() < 0:
                finished.append(i)
                # SIMULATED: execute real REWARD-STOP action
            else:
                counter = str(timeremain).split('.')[0] # Get rid of miliseconds
                tcolor = (10, 10, 10)
                if timeremain.total_seconds() < 1:
                    tcolor = (255, 0, 0) # Color text red
                usertext = font.render(usr, 1, tcolor)
                counttext = font.render(counter, 1, tcolor)
                img = self.unknown_img
                if rtype == RewardType.TV:
                    img = self.tv_img
                if rtype == RewardType.GAMES:
                    img = self.games_img
                screen.blit(usertext, (left + 25, top + 0))
                screen.blit(img, (left + 0, top + 32))
                screen.blit(counttext, (left + 25, top + 162))
                left += 140
        # Remove the finished ones
        for i in finished[::-1]:
            self.pending.pop(i)




shouldRun = True
rewardStartTime = datetime.datetime.now()
rewHandler = RewardsHandler(font, screen)


# Main loop
while shouldRun:
    # Display in window
    screen.fill(THECOLORS['white'])
    rewHandler.display()
    pygame.display.flip()

    # Handle actions
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_RETURN or \
                event.type == MOUSEBUTTONUP:
            rewHandler.startReward('Filica', 0, 10)
            rewHandler.startReward('Tita', 1, 2)
            rewHandler.startReward('Fane', 3, 4)

        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            print 'Quitting'
            shouldRun = False
            break