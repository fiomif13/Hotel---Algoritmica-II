from entities.user import Usuario
from entities.tarjeta import Tarjeta
from entities.habitacion import Habitacion
from entities.administrador import Administrador
from entities.cliente import Cliente
from entities.paypal import PayPal
from processes.reserva import Reserva
from processes.pago import Pago


def menu():
    menu = """
    ---------BIENVENIDOS AL HOTEL VIRUS PELUCHE----------
    1.- Iniciar Sesion
    2.- Registrarse
    Elija una opcion: """
    option = int(input(menu))
    if option == 1:
        usuarioEnSesion, tipo = buscar_usuario()
        while usuarioEnSesion == None:
            print("     No tenemos a ese usuario registrado, intentelo de nuevo")
            usuarioEnSesion, tipo = buscar_usuario()
        if tipo == "admin":
            menu_admin(usuarioEnSesion, tipo)
        else:
            menu_usuarios(usuarioEnSesion, tipo)

    elif option == 2:
        user = input("Ingrese nuevo usuario: ")
        password = input("Ingrese nueva contrasenia: ")
        name = input("Ingrese su nombre: ")
        lastname = input("Ingrese su apellido: ")
        mail = input("Ingrese su correo: ")
        new_User = Usuario(user, password, name, lastname, mail)
        new_User.registrar()

    else:
        print("Opcion no valida")


def buscar_usuario():
    user = input("      Usuario: ")
    password = input("      Contrasenia: ")
    usuarioEnSesion = Usuario.verify_session(user, password)
    tipo = "user"
    if usuarioEnSesion is None:
        usuarioEnSesion = Cliente.verify_session(user, password)
        tipo = "client"
    if usuarioEnSesion is None:
        usuarioEnSesion = Administrador.verify_session(user, password)
        tipo = "admin"
    return usuarioEnSesion, tipo


def menu_admin(usuarioEnSesion, tipo):
    menu = """
    1.- Registrar habitacion
    2.- Actualizar datos de habitacion
    3.- Actualizar contrasenia
    4.- Buscar habitacion y mostrar datos
    5.- Mostrar catalogo de habitaciones
    Elija una opcion: """
    option = int(input(menu))
    if option == 1:
        Administrador.registrarHab()

    elif option == 2:
        usuarioEnSesion.actualizarDatos()

    elif option == 3:
        usuarioEnSesion.actualizarContrasenia()

    elif option == 4:
        Habitacion.buscarHabitacion()

    elif option == 5:
        Habitacion.mostrarDatos(tipo)

    else:
        print("Opcion no valida")


def menu_usuarios(usuarioEnSesion, tipo):
    menu = """
    1.- Actualizar Datos
    2.- Comprar
    Elija una opcion: """
    op = int(input(menu))

    if op == 1:
        usuarioEnSesion.actualizarDatos()
    elif op == 2:
        print("**************SOLICITUD DE RESERVA*********************")
        fechaEnt = str(input("Llegada (dd-mm-aaaa):"))
        fechaSal = str(input("Salida (dd-mm-aaaa):"))
        numDias = Reserva.tiempoDeEstadia(fechaEnt, fechaSal)
        cantPersonas = int(input("Ingrese la cantidad de personas: "))
        cantHabitaciones = int(input("Ingrese el numero de habitaciones:"))
        Habitacion.mostrarDatos(tipo)
        habitacionesSolicitadas = Reserva.separarHabitaciones(cantHabitaciones)
        titular = usuarioEnSesion._usuario
        new_Reserva = Reserva(titular, fechaEnt, fechaSal, numDias, cantPersonas, cantHabitaciones, habitacionesSolicitadas)
        monto = Reserva.calcularMonto(habitacionesSolicitadas, numDias)
        print("Monto=" + str(monto))
        menuPago = """
        Seleccione el metodo de pago:
        1.- Tarjeta VISA/Mastercard
        2.- PayPal
        Elija una opcion: """

        opSelec = int(input(menuPago))

        if opSelec == 1:
            metPago = "Tarjeta"
            print("Ingresar los datos de la tarjeta:")
            nombreTarjeta = input("Nombre: ")
            apellidoTarjeta = input("Apellido: ")
            numeroTarjeta = int(input("Tarjeta: "))

            while len(str(numeroTarjeta)) != 16:
                print("El numero de tarjeta debe contener 16 digitos")
                numeroTarjeta = int(input("Tarjeta: "))

            codigoTarjeta = int(input("Codigo de seguridad (CVV): "))

            while len(str(codigoTarjeta)) != 3:
                print("El codigo de verificación debe contener 3 digitos")
                codigoTarjeta = int(input("Tarjeta: "))

            emisorTarjeta = input("Emisor: ")
            fechaCaducidadTarjeta = input("Fecha Caducidad: ")

            metPagoIngresado = Tarjeta(numeroTarjeta, fechaCaducidadTarjeta, codigoTarjeta, nombreTarjeta, apellidoTarjeta, emisorTarjeta)
            cuenta = metPagoIngresado._numTarjeta

        elif opSelec == 2:
            metPago = "PayPal"
            correoPayPal = input("Ingrese su correo:")
            contraseniaPayPal = input("Ingrese su contrasenia:")

            metPagoIngresado = PayPal(correoPayPal, contraseniaPayPal)
            cuenta = metPagoIngresado._correoPayPal

        a = metPagoIngresado.verificar()
        b = metPagoIngresado.verificarBloqueo() == False
        c = metPagoIngresado.verificarCaducidad()

        if a and b and c:
            nuevoPago = Pago(habitacionesSolicitadas, monto, metPago, cuenta)

            if nuevoPago.pagar():
                nuevoPago.registrarTransaccion()
                print("Pago exitoso")
                new_Reserva.reservar()
                Reserva.cambiarEstado(habitacionesSolicitadas)
                pago = nuevoPago.cambiarFormato()
                nuevo_cliente = Cliente(usuarioEnSesion._usuario, usuarioEnSesion._contrasenia, usuarioEnSesion._nombre, usuarioEnSesion._apellido, usuarioEnSesion._correo, metPago, pago)
                nuevo_cliente.registrar()
            else:
                print("Monto insuficiente para realizar el pago.")
        else:
            print("Compruebe la información de su " + metPago + "   e inténtalo de nuevo")


if __name__ == "__main__":
    menu()
