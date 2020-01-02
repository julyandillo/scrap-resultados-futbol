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

            dorsal = int(info('td').eq(0).text())
            url = info('.sdata_player_name>a').attr('href')
            nombre = info('.sdata_player_name').text()
            altura = int(info('td.dat').eq(0).text())
            peso = int(info('td.dat').eq(1).text())
            imagen = info('.sdata_player_img>a>img').attr('src')
            # hay algunos jugadores que no tienen el id en la url, pero siempre esta en la imagen
            id_rf = imagen[:imagen.find('?')].split('/')[-1].split('.')[0]

            print("Rastreando", nombre, "......")
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
