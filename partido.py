# coding=utf-8
import json

from pyquery import PyQuery

from rastreador import Rastreador
from util import Util


class Partido(Rastreador):
    """ clase para rastrear la información de un partido """

    def __init__(self, url):
        super().__init__(url)

        self.gethtml()

        self.modelo = {
            'type': 'partido',
            'local': None,
            'visitante': None,
            'data': {}
        }

    def rastrea(self):
        equipo_local = Util.equipo_equivalente_local(self.html('#marcador .equipo1 b').attr('title'))
        equipo_visitante = Util.equipo_equivalente_local(self.html('#marcador .equipo2 b').attr('title'))

        self.modelo['local'] = equipo_local
        self.modelo['visitante'] = equipo_visitante

        goles_local = int(self.html('.resultado span').eq(0).text())
        goles_visitante = int(self.html('.resultado span').eq(1).text())

        fecha = self.html('.jor-date').attr('content').replace('T', ' ').replace('+02:00', '')

        arbitro = self.html('.referee').eq(0).text()
        # arbitro = texto_arbitro[texto_arbitro.find(':')+1:].strip()

        arbitro_var = self.html('.referee').eq(4).text()
        # arbitro_var = texto_arbitro[texto_arbitro.find(':')+1:].strip()

        texto_asistencia = self.html('.as>span').text()
        if texto_asistencia != '':
            asistencia = int(texto_asistencia[texto_asistencia.find(':')+1:].strip().split(' ')[0].replace('.', ''))
        else:
            asistencia = 0

        print(fecha, "->", equipo_local, goles_local, "-", goles_visitante, equipo_visitante)
        """
        print(arbitro, '| VAR:', arbitro_var)
        print(asistencia, 'espectadores')
        """

        eventos = []
        cambio = {
            'tipo': 'cambio'
        }

        events = self.html('.evento>.event-content')
        for content in events:
            evento = PyQuery(content)

            imagen_jugador = evento('img.event-avatar').attr('src')
            url_jugador = evento('.name>a').attr('href')
            jugador = Util.get_id_jugador(imagen_jugador, url_jugador)

            minuto = int(evento('.minutos').text().replace('\'', '').replace('minuto', '').strip())

            if evento.find('.event_1'):
                tipo = 'gol'
            elif evento.find('.event_12'):
                tipo = 'gol_pp'
            elif evento.find('.event_11'):
                tipo = 'gol_penalti'
            elif evento.find('.event_8'):
                tipo = 'tarjeta_amarilla'
            elif evento.find('.event_9'):
                tipo = 'tarjeta_roja'
            elif evento.find('.event_6'):
                tipo = 'sale'
            elif evento.find('.event_7'):
                tipo = 'entra'
            else:
                continue

            if tipo not in ('sale', 'entra'):
                eventos.append({
                    'tipo': tipo,
                    'jugador': jugador,
                    'minuto': minuto
                })
            elif tipo == 'entra':
                cambio['entra'] = jugador
                cambio['minuto'] = minuto
            elif tipo == 'sale':
                cambio['sale'] = jugador
                cambio['minuto'] = minuto

            if 'entra' in cambio.keys() and 'sale' in cambio.keys():
                eventos.append(cambio)
                cambio = {'tipo': 'cambio'}

        self.modelo['data'] = {
            'fecha': fecha,
            'goles_local': goles_local,
            'goles_visitante': goles_visitante,
            'arbitro': arbitro,
            'arbitro_var': arbitro_var,
            'asistencia': asistencia,
            'eventos': eventos
        }

        with open('log.json', 'w') as file:
            file.write(json.dumps(self.modelo, indent=4))
