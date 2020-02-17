# coding=utf-8
from rastreador import Rastreador
from jugador import Jugador
from util import Util

from pyquery import PyQuery


class Plantilla(Rastreador):
    """ clase para rastrear la plantilla de un equipo """

    def __init__(self, equipo):
        self.equipo = equipo

        url = "https://www.resultados-futbol.com/plantilla/{}".format(equipo)
        super().__init__(url)

        self.gethtml()

        self.modelo = {
            'type': 'plantilla',
            'id': Util.lista_equipos()[Util.equipo_equivalente_local(equipo)],
            'data': []
        }

    def rastrea(self):
        for fila in self.html("table.sdata_table>tbody>tr[itemprop='employee']"):
            info = PyQuery(fila)

            nombre = info('.sdata_player_name').text()
            url = info('.sdata_player_name>a').attr('href')

            """ hay jugadores que no tienen dorsal, peso o altura (muy pocos) si no tienen se quedan con este valor """
            dorsal = 0
            altura = 0
            peso = 0

            print("Rastreando", nombre, "......")

            if info('td').eq(0).text().strip() != '':
                dorsal = int(info('td').eq(0).text())

            if info('td.dat').eq(0).text() != '-':
                altura = int(info('td.dat').eq(0).text())

            if info('td.dat').eq(1).text() != '-':
                peso = int(info('td.dat').eq(1).text())

            imagen = info('.sdata_player_img>a>img').attr('src')
            id_rf = Util.get_id_jugador(imagen, url)

            # print(, info('.sdata_player_name>a').attr('href'))
            jugador = Jugador("https://www.resultados-futbol.com" + url)
            jugador.rastrea()

            self.modelo['data'].append({
                'id_resultados_futbol': int(id_rf),
                'nombre': nombre,
                'nombre_completo': jugador.nombre_completo,
                'fecha_nacimiento': jugador.fecha_nacimiento,
                'pais': jugador.pais_nacimiento,
                'nacionalidad': jugador.nacionalidad,
                'dorsal': dorsal,
                'altura': altura,
                'peso': peso,
                'posicion': jugador.posicion,
                'imagen': imagen[:imagen.find('?')]
            })
