# coding=utf-8
from rastreador import Rastreador
from partido import Partido

from pyquery import PyQuery


class Jornada(Rastreador):
    """ clase para rastrear todos los partidos de una jornada """

    def __init__(self, jornada):
        url = "https://www.resultados-futbol.com/primera/grupo1/jornada{}".format(jornada)
        super().__init__(url)

        self.gethtml()

        """ lista para guardar los partidos rastreados para despues poder enviarlos """
        self.partidos = []

    def rastrea(self):
        partidos = self.html("#tabla1>tr.vevent")
        # print(partidos)

        for fila in partidos:
            url = PyQuery(fila)

            partido = Partido("https://www.resultados-futbol.com" + url("td.rstd>a").attr("href"))
            if url("td.rstd>a").text().strip() not in ('Apl', 'x-x') and '-' in url("td.rstd>a").text().strip():
                """ solo se rastrean los partidos no aplazados y los que ya se han jugado"""
                partido.rastrea()
                self.partidos.append(partido)

    def envia(self, debug):
        """ se redefine para no enviar la jornada al completo, recorre la lista de partidos y los envia por separado """
        for partido in self.partidos:
            partido.envia(debug)
