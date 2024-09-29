import uuid
from datetime import datetime
import json

file_path1 = "files/reservas.json"
file_path2 = "files/habitacionesRegistradas.json"


class Reserva:
    def __init__(self, titular, fechaEnt, fechaSal, numDias, cantPersonas, cantHabitaciones, habitacionesSolicitadas):
        self._codReserva = str(uuid.uuid4())
        self._titular = titular
        self._fechaEnt = fechaEnt
        self._fechaSal = fechaSal
        self._numDias = numDias
        self._cantPersonas = cantPersonas
        self._cantHabitaciones = cantHabitaciones
        self._habitacionesSolicitadas = habitacionesSolicitadas

    def separarHabitaciones(cantHabitaciones):
        habitacionesSolicitadas = []
        for i in range(cantHabitaciones):
            habitacionesSolicitadas.append(
                input(
                    "Ingrese el numero de la "
                    + str(i + 1)
                    + " habitacion que desea reservar:"
                )
            )
        return habitacionesSolicitadas

    def calcularMonto(habitacionesSolicitadas, numDias):
        monto = 0
        for element in habitacionesSolicitadas:
            with open(file_path2, "r") as f:
                data = json.load(f)
            for habitacionSolicitada in data:
                if str(habitacionSolicitada["numHabitacion"]) == element:
                    monto = monto + habitacionSolicitada["precio"]

        return monto * numDias

    def reservar(self):
        reservan = dict(
            codReserva=self._codReserva,
            titular=self._titular,
            fechaEnt=self._fechaEnt,
            fechaSal=self._fechaSal,
            numDias=self._numDias,
            cantPersonas=self._cantPersonas,
            canthabitaciones=self._cantHabitaciones,
            habitacionesSolicitadas=self._habitacionesSolicitadas
        )
        with open(file_path1, "r") as f:
            data = json.load(f)

        data.append(reservan)

        with open(file_path1, "w") as f:
            json.dump(data, f, indent=4)

    def cambiarEstado(habitacionesSolicitadas):
        for element in habitacionesSolicitadas:
            with open(file_path2, "r") as f:
                data = json.load(f)
            for habitacionSolicitada in data:
                if str(habitacionSolicitada["numHabitacion"]) == element:
                    habitacionSolicitada["estado"] = "No disponible"

            with open(file_path2, "w") as f:
                json.dump(data, f, indent=4)

    def mostrarReserva(codReserva):
        with open(file_path1, "r") as f:
            data = json.load(f)
        for element in data:
            if element["codReserva"] == codReserva:
                print("------------------------------------------------------")
                print("DATOS DE LA RESERVA DE LA HABITACION")
                print("Codigo de reserva:" + str(element["codReserva"]))
                print("Titular:" + str(element["titular"]))
                print("Fecha de entrada:" + str(element["fechaEnt"]))
                print("Fecha de salida:" + str(element["fechaSal"]))
                print("Numero de dias de la estadia:", element["numDias"])
                print("Cantidad de personas:", element["cantPersonas"])
                print("Cantidad de habitaciones:", element["canthabitaciones"])
                print(
                    "Habitaciones solicitadas:"
                    + str(element["habitacionesSolicitadas"])
                )
                print("------------------------------------------------------")

    def tiempoDeEstadia(E, S):
        fEnt = datetime.strptime(str(E), "%d-%m-%Y")
        fSal = datetime.strptime(str(S), "%d-%m-%Y")
        t = fSal - fEnt 
        return (t.days + 1)

    def comprobar_personas(self, cod_reserva):
        def calcular_personas(tipo_habitacion):
            if tipo_habitacion == "Simple":
                return 1
            elif tipo_habitacion in ["Doble", "Matrimonial"]:
                return 2
            elif tipo_habitacion == "Triple":
                return 3
            return 0
        def obtener_num_personas(tipo_habitaciones, data2):
            return sum(calcular_personas(element["tipoHabitacion"])
                    for element in data2
                    if element["numHabitacion"] in tipo_habitaciones)
        with open(file_path1, "r") as f:
            data = json.load(f)
        for element in data:
            if element["cod_reserva"] == cod_reserva:
                tipo = element["habitacionesSolicitadas"]
                cantpers = element["cantPersonas"]
                with open(file_path2, "r") as g:
                    data2 = json.load(g)
                num_pers = obtener_num_personas(tipo, data2)
                if cantpers > num_pers:
                    print("La cantidad de personas para la reserva es mayor al espacio pedido. Por favor pedir más habitaciones.")
                    return False            
                return True
        return False

