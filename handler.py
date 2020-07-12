from abc import ABC, abstractmethod

class MyHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, raw):
        pass
