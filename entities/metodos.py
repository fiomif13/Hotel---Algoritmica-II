from abc import ABC, abstractmethod


class Metodo(ABC):
    @abstractmethod
    def verificar(self):
        pass

    @abstractmethod
    def verificarCaducidad(self):
        pass

    @abstractmethod
    def verificarBloqueo(self):
        pass
