# coding=utf-8
import urllib.request
from pyquery import PyQuery
from abc import ABC, abstractmethod
import json
import socket

from util import Util


class Rastreador(ABC):
    def __init__(self, url):
        self.__url = url
        self.html = None
        self.modelo = {}

    def gethtml(self):
        """ convierte el contenido html de la pagina completa en un obejto pyquery """
        request = urllib.request.Request(self.__url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})
        self.html = PyQuery(urllib.request.urlopen(request).read())

    def envia(self, debug):
        """ envia el modelo del objeto en formato json al socket servidor """
        info = json.dumps(self.modelo)

        if debug is True:
            print(info)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((Util.host(), Util.puerto()))

            cliente.send(bytes(info, "utf-8"))

    @abstractmethod
    def rastrea(self):
        """ se definira la implementacion en las clases hijas """
        raise NotImplemented()
