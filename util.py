from mysql import Mysql
import configparser


class Util:
    __equipos = {}  # diccionario que almacenara los nombres de los equipos y el id de la base de datos
    __equipos_pendientes = {}

    equipos_rf = {
        'Atletico-Madrid': 'Atlético',
        'Athletic-Bilbao': 'Athletic',
        'Real-Sociedad': 'Real Sociedad',
        'R. Sociedad': 'Real Sociedad',
        'Alaves': 'Alavés',
        'Valencia-Cf': 'Valencia',
        'Leganes': 'Leganés',
        'Real-Madrid': 'Real Madrid',
        'Real Betis': 'Betis',
        'Real Valladolid': 'Valladolid'
    }

    __config = None  # objeto que almacenara la informacion del ini

    @classmethod
    def equipo_equivalente_local(cls, equipo):
        """ convierte el nombre del equipo de resultados-futbol.com al equipo de la base de datos """
        if equipo in cls.equipos_rf.keys():
            return cls.equipos_rf[equipo]

        return equipo

    @classmethod
    def equipo_equivalente_rf(cls, equipo):
        """ convierte el nombre del equipo almacenado en la base de datos al de resultados-fultbol.com """
        if equipo in cls.equipos_rf.values():
            for equipo_rf, equipo_local in cls.equipos_rf.items():
                if equipo == equipo_local:
                    return equipo_rf

        return equipo

    @classmethod
    def lista_equipos(cls):
        """ carga en un diccionario los nombres de los equipos de la base de datos, lay key el nombre el valor el id """
        if len(cls.__equipos.keys()) == 0:
            bd = Mysql.conectar()
            bd.execute('SELECT nombre, id_equipo FROM equipo ORDER BY nombre')
            for equipo in bd.fetchall():
                cls.__equipos[equipo['nombre']] = equipo['id_equipo']

        return cls.__equipos

    @classmethod
    def lista_equipos_sin_plantilla(cls):
        """ carga en un diccionario los equipos que no tienen jugadores (key: valor, nombre: id) """
        if len(cls.__equipos_pendientes.keys()) == 0:
            bd = Mysql.conectar()
            bd.execute("select id_equipo, nombre "
                       "from equipo "
                       "where id_equipo not in (select distinct id_equipo from jugador) "
                       "order by nombre")
            for equipo in bd.fetchall():
                cls.__equipos_pendientes[equipo['nombre']] = equipo['id_equipo']

        return cls.__equipos_pendientes

    @classmethod
    def load_ini(cls):
        """ carga la configuracion del archivo ini usando el patron singleton """
        if cls.__config is None:
            cls.__config = configparser.ConfigParser()
            cls.__config.read('config.ini')

    @classmethod
    def puerto(cls):
        """ devuelve el numero de puerto que se utiliza para el la conexion con el socket """
        Util.load_ini()
        return int(cls.__config['SOCKET']['port'])

    @classmethod
    def host(cls):
        """ devuelve el host que utilizara el socket para el envio de la informacion """
        cls.load_ini()
        return cls.__config['SOCKET']['host']

    @classmethod
    def get_id_jugador(cls, imagen, url):
        """
        devuelve el id que tiene el jugador el resultados futbol a partir de la ruta de la imagen o la url
        hay algunos jugadores que no tienen el id en la url, pero esta en la imagen siempre y cuando
        la imagen no sea una por defecto (avatar-player.jpg), entonces el id se saca de la url
        """
        if 'avatar-player' not in imagen:
            return imagen[:imagen.find('?')].split('/')[-1].split('.')[0]

        return url.split('-')[-1]
