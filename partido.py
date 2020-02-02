# coding=utf-8
from rastreador import Rastreador


class Partido(Rastreador):
    """ clase para rastrear la información de un partido """

    def __init__(self, url):
        super().__init__(url)
        self.url = url

        self.gethtml()

    def rastrea(self):
        print(self.url)
