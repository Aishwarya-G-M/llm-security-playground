from abc import ABC, abstractmethod

from app.schemas.security import SecurityVerdict


class BaseInspector(ABC):
    @abstractmethod
    def inspect_input(self, text: str) -> SecurityVerdict:
        pass

    @abstractmethod
    def inspect_output(self, text: str) -> SecurityVerdict:
        pass