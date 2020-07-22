from abc import ABC, abstractmethod

class MyHandler(ABC):
    @abstractmethod
    def handle(self, raw):
        pass
