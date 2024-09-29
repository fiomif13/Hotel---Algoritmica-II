from entities.metodos import Metodo
import datetime
import json
from werkzeug.security import check_password_hash

file_path = "files/tarjetas.json"


class Tarjeta(Metodo):
    def __init__(self, numTarjeta, fechCaducidad, codSeguridad, nomTarjeta, apellTarjeta, emisorTarjeta):
        self.__emisor = emisorTarjeta
        self._numTarjeta = numTarjeta
        self.__fechCaducidad = fechCaducidad
        self.__codSeguridad = codSeguridad
        self.__nombTarjeta = nomTarjeta
        self.__apellTarjeta = apellTarjeta

    def verificar(self):
        passed = False
        with open(file_path, "r") as f:
            tarjetas = json.load(f)

        for element in tarjetas:
            p = True if element["emisor"] == self.__emisor else False
            q = check_password_hash(element["numTarjeta"], str(self._numTarjeta))
            r = check_password_hash(element["fechCaducidad"], self.__fechCaducidad)
            s = check_password_hash(element["codSeguridad"], str(self.__codSeguridad))
            t = True if element["nombTarjeta"] == self.__nombTarjeta else False
            u = True if element["apellTarjeta"] == self.__apellTarjeta else False
            if p and q and r and s and t and u:
                passed = True
        return passed

    def verificarCaducidad(self):
        passed = False
        fechaActual = datetime.datetime.now()
        fechaV = datetime.datetime.strptime(self.__fechCaducidad, "%m/%Y")
        if fechaV > fechaActual:
            passed = True
        return passed

    def verificarBloqueo(self):
        passed = False
        with open("files/numeroBloqueado.json", "r") as f:
            numerosBloqueados = json.load(f)

        for element in numerosBloqueados:
            if element["numero"] == self._numTarjeta:
                passed = True
        return passed
