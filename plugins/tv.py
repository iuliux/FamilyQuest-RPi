
class TvActuator:
    '''Enables RaspberryPi to control TV's on/off state'''
    def __init__(self):
        self.img_name = 'tv.png'

    def start(self):
        print 'TV started'

    def stop(self):
        print 'TV stopped'
