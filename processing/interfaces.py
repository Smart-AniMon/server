"""
Módulo com definições das interfaces e classes abstratas utilizadas no sistema de processamento.

As Classes Observer e Subject são utilizadas para seguir o padrão de modelagem Observer.
"""

class Observer(object):
    """Classe para representar a Interface Observer
    """
    def __init__(self):
        pass

    def update(self, message: object):
        raise Exception("NotImplementedException")


class Subject(object):
    """Classe para representar o Subject
    """
    def __init__(self):
        self.__observers = []
        self.__state = None

    def add_observer(self, observer: Observer):
        pass

    def remove_observer(self, observer:Observer):
        pass

    def __notify_all(self):
        pass

class ConnectionDB(object):
    """Classe para representar a Interface Genérica para comunicação com banco de dados
    """
    def __init__(self):
        pass

    def create(self, message: object):
        raise Exception("NotImplementedException")

    def update(self, message: object):
        raise Exception("NotImplementedException")

    def delete(self, message: object):
        raise Exception("NotImplementedException")
