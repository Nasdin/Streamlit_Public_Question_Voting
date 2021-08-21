import time

class RealTimeUpdater(object):

    def __init__(self):
        self.elements = []

    def register(self, element):
        self.elements.append(element)

    def update(self):
        for element in self.elements:
            element.update()

    def start(self):
        while True:
            self.update()
            time.sleep(0.1)


class RealTimeElement(object):


    def update(self):
        pass


