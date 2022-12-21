import abc


class SerialBase(metaclass=abc.ABCMeta):
    """
    """

    @abc.abstractmethod
    def read(self):
        pass

    @abc.abstractmethod
    def write(self, data):
        pass
