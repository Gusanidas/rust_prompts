from abc import ABC, abstractmethod
from model_api import SyncModelAPI

class BaseStrategy(ABC):

    def __init__(self):
        self.model_api = SyncModelAPI()

    @abstractmethod
    def run(self):
        pass