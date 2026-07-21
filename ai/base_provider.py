from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def generate(self, prompt):
        pass