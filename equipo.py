# coding=utf-8
from rastreador import Rastreador
from util import Util


class Equipo(Rastreador):
    """ clase para rastrear informacion del equipo y del estadio """

    def __init__(self, equipo):
        self.equipo = equipo

        url = "https://www.resultados-futbol.com/{}/".format(equipo)
        super().__init__(url)

        self.modelo = {
            'type': 'equipo',
            'id': Util.lista_equipos()[Util.equipo_equivalente_local(equipo)],
            'name': Util.equipo_equivalente_local(equipo),
            'data': {
            }
        }

        self.gethtml()  # transforma el html de la url a un objeto PyQuery

    def rastrea(self):
        entrenador = self.html('#titlehc').find('.info>p').eq(0).find('span').text()
        print('Entrenador:', entrenador)

        presidente = self.html('#titlehc').find('.info>p').eq(1).find('span').text()
        print('Presidente:', presidente)

        # informacion del estadio
        capacidad = self.html('.bi-stadium').find('li').eq(1).find('span').eq(1).text()
        print('Capacidad:', capacidad, 'espectadores')

        if self.html('.bi-stadium').find('li').eq(4).find('span').eq(0).text() == 'Fax':
            incremento = 1
        else:
            incremento = 0

        construccion = self.html('.bi-stadium').find('li').eq(4+incremento).find('span').eq(1).text()
        print('Construccion:', construccion)

        dimensiones = self.html('.bi-stadium').find('li').eq(5+incremento).find('span').eq(1).text()
        print('Dimensiones:', dimensiones)

        self.modelo['data'] = {
            'presidente': presidente,
            'entrenador': entrenador,
            'estadio': {
                'capadidad': int(capacidad),
                'construccion': int(construccion),
                'dimensiones': dimensiones
            }
        }
