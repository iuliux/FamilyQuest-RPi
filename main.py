import pygame
from pygame.color import THECOLORS
from pygame.locals import *

import datetime, time
from os import path
from threading import Thread
from Queue import Queue

from plugins import plugins
import rest
from config import *


pygame.mixer.pre_init(44100, -16, 1, 4096) # freq, size, channels, buffsize
pygame.init()

# Sound init
pygame.mixer.music.load("notif.wav")

screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption('FamilyQuest Actuator')

screen.fill(THECOLORS['white'])
font = pygame.font.Font(None, 36)
text = font.render("Initializing...", 1, (10, 10, 10))
textpos = text.get_rect()
textpos.centerx = screen.get_rect().centerx
screen.blit(text, textpos)
pygame.display.flip()


class RewardType:
    TV = 0
    GAMES = 1

class RewardsHandler:
    def __init__(self, font, screen):
        self.pending = []
        self.tobedone = Queue()
        self.font = font
        self.screen = screen
        # Images
        self.unknown_img = pygame.image.load(path.join(IMGS_PATH, UNKN_IMAGE))
        # Actuators
        self.actuators = [ac() for ac in plugins]
        self.act_imgs = [pygame.image.load(path.join(IMGS_PATH, ac.img_name))
                            for ac in self.actuators]

    def startReward(self, fname, user, rtype, rname, timespan):
        self.tobedone.put(
                (fname, user, rtype, rname, datetime.timedelta(seconds=timespan), datetime.datetime.now())
            )
        # SIMULATED: execute real REWARD-START action
        if rtype >= 0 and rtype < len(self.actuators):
            # Execute action
            self.actuators[rtype].start()
        # Play notification sound
        pygame.mixer.music.play()

    def check_for_entries(self):
        while not self.tobedone.empty():
            self.pending.append(self.tobedone.get())

    def display(self):
        finished = []
        top = 100
        left = 0
        for i, r in enumerate(self.pending):
            fname, usr, rtype, rname, timespan, starttime = r
            timepassed = datetime.datetime.now() - starttime
            timeremain = timespan - timepassed
            if timeremain.total_seconds() < 0:
                finished.append(i)
                # SIMULATED: execute real REWARD-STOP action
                if rtype >= 0 and rtype < len(self.actuators):
                    # Execute action
                    self.actuators[rtype].stop()
            else:
                counter = str(timeremain).split('.')[0] # Get rid of miliseconds
                tcolor = (10, 10, 10)
                if timeremain.total_seconds() < 1:
                    tcolor = (255, 0, 0) # Color text red
                fnametext = font.render(fname, 1, tcolor)
                usertext = font.render(usr, 1, tcolor)
                counttext = font.render(counter, 1, tcolor)
                rnametext = font.render(rname, 1, (120, 120, 120))
                # Get an image
                img = self.unknown_img
                # Look for an installed plugin
                if rtype >= 0 and rtype < len(self.actuators):
                    # Set the custom image
                    img = self.act_imgs[rtype]

                # Do the drawings
                screen.blit(fnametext, (left + 5, top + 0))
                screen.blit(usertext, (left + 15, top + 32))
                screen.blit(img, (left + 0, top + 64))
                screen.blit(counttext, (left + 25, top + 194))
                screen.blit(rnametext, (left + 15, top + 236))
                left += 140
        # Remove the finished ones
        for i in finished[::-1]:
            self.pending.pop(i)




shouldRun = True
rewardStartTime = datetime.datetime.now()
rewHandler = RewardsHandler(font, screen)


# Start a thread that does polling for new rewards
def polling_loop():
    while shouldRun:
        members = rest.poll()
        for m in members:
            fname, uname, rewards = m
            for r in rewards:
                rewHandler.startReward(fname, '#%s' % uname,
                                       r[u'reward_type'],
                                       r[u'name'],
                                       r[u'duration_seconds'])
Thread(target=polling_loop).start()
            

time.sleep(1)
# Main loop
while shouldRun:
    # Check the rewards queue for new entries
    rewHandler.check_for_entries()

    # Display in window
    screen.fill(THECOLORS['white'])
    rewHandler.display()

    pygame.display.flip()

    # Handle actions
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_RETURN or \
                event.type == MOUSEBUTTONUP:
            rewHandler.startReward('Filica', 'fily', 0, 'Watch TV', 10)
            rewHandler.startReward('Tita', 'tity', 1, 'Play Xbox', 2)
            rewHandler.startReward('Fane', 'fany', 3, 'Visit girlfriend', 4)

        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            print 'Quitting'
            shouldRun = False
            screen.fill(THECOLORS['white'])
            font = pygame.font.Font(None, 36)
            text = font.render("Quitting...", 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = screen.get_rect().centerx
            screen.blit(text, textpos)
            pygame.display.flip()
            break
