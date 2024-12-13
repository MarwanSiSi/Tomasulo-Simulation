from abc import ABC, abstractmethod


class Station(ABC):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @abstractmethod
    def update(self, time):
        pass
