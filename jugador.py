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

        self.__demarcacion = {
            'Portero': 'POR',
            'Defensa': 'DEF',
            'Centrocampista': 'MED',
            'Delantero': 'DEL'
        }

    def rastrea(self):
        """
        primero hay que sacar la posicion que tiene el hijo que queremos obtener, por ejemplo hay algunos jugadores
        que no tienen lugar de nacimiento, por lo que todas los hijos que iban detrás de este tendrán una pocición
        menos que en los que si aparece
        """
        posicion = 0
        posiciones = {}
        for nodo in self.html("#pinfo>.contentitem>dl>dt"):
            texto = PyQuery(nodo).text()
            if texto == 'Completo':
                posiciones['nombre_completo'] = posicion
            elif texto == 'País':
                posiciones['pais_nacimiento'] = posicion
            elif texto == 'Nacionalidad':
                posiciones['nacionalidad'] = posicion
            elif texto == 'Fecha de nacimiento':
                posiciones['fecha_nacimiento'] = posicion
            elif texto == 'Demarcación':
                posiciones['posicion'] = posicion

            posicion += 1

        box = self.html("#pinfo>.contentitem>dl>dd")
        self.nombre_completo = box.eq(posiciones['nombre_completo']).text()
        self.pais_nacimiento = box.eq(posiciones['pais_nacimiento']).text()
        self.nacionalidad = box.eq(posiciones['nacionalidad']).text()
        self.fecha_nacimiento = box.eq(posiciones['fecha_nacimiento']).text()
        self.posicion = self.__demarcacion[box.eq(posiciones['posicion']).text()]
