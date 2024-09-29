from entities.metodos import Metodo
import json
from werkzeug.security import check_password_hash

file_path1 = "files/cuentasPayPal.json"
file_path2 = "files/cuentasSuspendidas.json"


class PayPal(Metodo):
    def __init__(self, correoPayPal, contraseniaPayPal):
        self._correoPayPal = correoPayPal
        self.__contraseniaPayPal = contraseniaPayPal

    def verificar(self):  # verificar correo y contrasenia
        print("----------------------PAYPAL----------------------")
        with open(file_path1, "r") as f:
            usuarioPayPal = json.load(f)
        for element in usuarioPayPal:
            passed = False
            if check_password_hash(
                element["correoPayPal"], self._correoPayPal
            ) and check_password_hash(
                element["contraseniaPayPal"], self.__contraseniaPayPal
            ):
                passed = True
        return passed

    def verificarCaducidad(self):  # verificar si la cuenta está desactivada
        passed = False
        with open(file_path1, "r") as f:
            usuarioPaypal = json.load(f)
        for element in usuarioPaypal:
            if check_password_hash(element["correoPayPal"], self._correoPayPal):
                if element["estado"] == "activa":
                    passed = True
        return passed

    def verificarBloqueo(self):  # verificar banneada}
        passed = False
        with open(file_path2, "r") as f:
            usuarioPaypal = json.load(f)
        for element in usuarioPaypal:
            if element["correoPayPal"] == self._correoPayPal:
                passed = True
        return passed
