from abc import ABC, abstractmethod

from app.schemas.security import SecurityVerdict


class BaseInspector(ABC):
    @abstractmethod
    def inspect_text(self, text: str) -> SecurityVerdict:
        pass