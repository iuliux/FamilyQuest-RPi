
class GameConsoleActuator:
    '''Enables RaspberryPi to control PS3/XBox's on/off state'''
    def __init__(self):
        self.img_name = 'games.png'

    def start(self):
        print 'GameConsole started'

    def stop(self):
        print 'GameConsole stopped'
