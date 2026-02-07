from abc import ABC, abstractmethod

class BaseModule(ABC):
    def __init__(self):
        self.name = "BaseModule"
        self.description = "Abstract Base Class"
        self.category = "generic"

    @abstractmethod
    async def run(self, target: str, http_client) -> dict:
        pass