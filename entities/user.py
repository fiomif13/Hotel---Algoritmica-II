import json
from werkzeug.security import generate_password_hash, check_password_hash

file_path = "files/usuarios.json"


def codificar(dato):
    encriptado = generate_password_hash(dato)
    return encriptado


class Usuario:
    def __init__(self, usuario, contrasenia, nombre, apellido, correo):
        self._usuario = usuario
        self._contrasenia = contrasenia
        self._nombre = nombre
        self._apellido = apellido
        self._correo = correo

    def verify_session(given_User, given_Password):
        with open(file_path, "r") as f:
            usuario = json.load(f)

        for element in usuario:
            if element["usuario"] == given_User and check_password_hash(
                element["contrasenia"], given_Password
            ):
                print("Bienvenido, " + element["nombre"])
                return Usuario(
                    element["usuario"],
                    given_Password,
                    element["nombre"],
                    element["apellido"],
                    element["correo"]
                )

    def registrar(self):
        usern = dict(
            usuario=self._usuario,
            contrasenia=codificar(self._contrasenia),
            nombre=self._nombre,
            apellido=self._apellido,
            correo=self._correo
        )
        with open(file_path, "r") as f:
            data = json.load(f)

        data.append(usern)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def actualizar(self, dato):
        with open(file_path, "r") as f:
            usuarios = json.load(f)

        for element in usuarios:
            if element["usuario"] == self._usuario:
                if dato == "contrasenia":
                    element[dato] = generate_password_hash(
                        input("Ingrese actualiazación de su " + dato + ": ")
                    )
                else:
                    element[dato] = input("Ingrese actualiazación de su " + dato + ": ")

        with open(file_path, "w") as f:
            json.dump(usuarios, f, indent=4)

    def actualizarDatos(self):
        menu = """ACTUALIZAR
            1. Usuario
            2. Contraseña
            3. Nombre
            4. Apellido
            5. Correo
        OPCION: """
        opcion = int(input(menu))

        while opcion > 5 or opcion < 1:
            print("Elija una opción valida")
            opcion = int(input(menu))

        if opcion == 1:
            dato = "usuario"
        elif opcion == 2:
            contraseniaActual = input("Ingrese contrasenia actual: ")
            while self._contrasenia != contraseniaActual:
                print("Contrasenia incorrecta")
                contraseniaActual = input("Ingrese contrasenia actual: ")
            dato = "contrasenia"
        elif opcion == 3:
            dato = "nombre"
        elif opcion == 4:
            dato = "apellido"
        elif opcion == 5:
            dato = "correo"
        self.actualizar(dato)
