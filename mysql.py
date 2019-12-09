import configparser
import pymysql


class Mysql:
    """ clase para conectar con la base de datos utilizando el patron singleton para mantener una unica conexion """

    __conexion = None
    __cursor = None

    @classmethod
    def conectar(cls):
        if cls.__conexion is None:
            config = configparser.ConfigParser()
            config.read('config.ini')

            cls.__conexion = pymysql.connect(host=config['DATABASE']['host'],
                                             user=config['DATABASE']['user'],
                                             passwd=config['DATABASE']['password'],
                                             db=config['DATABASE']['database'],
                                             charset='utf8',
                                             autocommit=True,
                                             cursorclass=pymysql.cursors.DictCursor)

            cls.__cursor = cls.__conexion.cursor()

        return cls.__cursor

    @classmethod
    def cerrar(cls):
        if cls.__cursor is not None:
            cls.__cursor.close()
