import sys

from equipo import Equipo
from plantilla import Plantilla
from util import Util


def main():
    if len(sys.argv) != 3:
        script = sys.argv[0].split('/')[-1]
        print("Usage: {} [equipo info|plantilla] [jornada n]".format(script))
        print("\t{} Atletico info".format(script))
        print("\t{} jornada 1".format(script))
        sys.exit(0)

    rastreo = sys.argv[1]
    valor = sys.argv[2]

    if rastreo == 'jornada':
        """ rastrea todos los partidos de la jornada pasada como argumento """
        pass
    elif rastreo == 'equipos':
        """ rastrea la informacion de todos los equipos """
        for equipo in Util.lista_equipos().keys():
            print("Rastreando", equipo, "......")
            info_equipo = Equipo(Util.equipo_equivalente_rf(equipo))
            info_equipo.rastrea()
            info_equipo.envia(True)
            print("----------------------------------------------")
    else:
        if valor == 'info':
            """ se rastreara la informacion del equipo pasado como argumento """
            print("Rastreando", rastreo, "......")
            equipo = Equipo(rastreo)
            equipo.rastrea()
            equipo.envia(True)
        else:
            """ se rastreara la plantilla del equipo pasado como argumento """
            print("Rastreando plantilla de ", rastreo, "......")
            plantilla = Plantilla(rastreo)
            plantilla.rastrea()
            print(plantilla.modelo)


if __name__ == '__main__':
    main()
