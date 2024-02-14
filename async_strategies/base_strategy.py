from abc import ABC, abstractmethod
from model_api import AsyncModelAPI

class BaseStrategy(ABC):

    def __init__(self):
        self.model_api = AsyncModelAPI()

    @abstractmethod
    async def run(self) -> (str, dict):
        pass

    def post_process(self, model_output):
        code = ""
        if model_output and "```" in model_output:
            in_code_block = False
            for line in model_output.split("\n"):
                if "```" in line:
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    code += line + "\n"
        else:
            code = model_output
        return code