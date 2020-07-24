from abc import ABC, abstractmethod

class MyHandler(ABC):
    """
    class MyHandler is a generic class for handling incoming request to the
    TCP server.

    The custom TCP request handler class must inherit from this class. For 
    example, the class MyHttpServer inherits from this class and override the 
    function `handle(raw)`.

    Methods
    -------
    handle(raw)
        Defines what to do upon receiving a request from a client.
    """
    @abstractmethod
    def handle(self, raw):
        """
        Defines what to do upon receiving a request from a client.

        Parameters
        ----------
        raw : bytearray
            The data sent by the client.
        """
        pass
