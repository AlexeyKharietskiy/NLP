from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> str:
        pass