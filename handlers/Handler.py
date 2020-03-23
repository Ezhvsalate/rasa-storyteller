from abc import ABC, abstractmethod


class Handler(ABC):

    @abstractmethod
    def __init__(self, filename, *args):
        pass

    @abstractmethod
    def import_data(self):
        pass

    @abstractmethod
    def export_data(self):
        pass

    @abstractmethod
    def sort_alphabetically(self):
        pass
