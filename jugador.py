# coding=utf-8
from rastreador import Rastreador
from util import Util

from pyquery import PyQuery


class Jugador(Rastreador):
    """ clase para rastrear la web con los detalles de los jugadores """

    def __init__(self, url):
        super().__init__(url)

        self.gethtml()

        self.nombre_completo = ''
        self.nacionalidad = ''
        self.pais_nacimiento = ''
        self.fecha_nacimiento = ''
        self.posicion = ''

        self.__posiciones = {
            'Portero': 'POR',
            'Defensa': 'DEF',
            'Centrocampista': 'MED',
            'Delantero': 'DEL'
        }

    def rastrea(self):
        box = self.html("#pinfo>.contentitem>dl>dd")
        self.nombre_completo = box.eq(1).text()
        self.pais_nacimiento = box.eq(5).text()
        self.nacionalidad = box.eq(6).text()
        self.fecha_nacimiento = box.eq(3).text()
        self.posicion = self.__posiciones[box.eq(7).text()]
