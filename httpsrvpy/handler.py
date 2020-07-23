from abc import ABC, abstractmethod

class MyHandler(ABC):
    """
    class MyHandler is the generic class for handling incoming request to the
    TCP server.

    The custom TCP request handler class must inherit from this class. For 
    example, the class MyHttpServer inherits from this class and override the 
    function `handle(raw)`.

    Methods
    -------
    handle(raw)
        Define what to do upon receiving a request from a client.
    """
    @abstractmethod
    def handle(self, raw):
        """
        Define what to do upon receiving a request from a client.

        Parameters
        ----------
        raw : bytearray
            The data sent by the client.
        """
        pass
