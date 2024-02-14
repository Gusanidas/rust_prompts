from .base_strategy import BaseStrategy

class BasicStrategy(BaseStrategy):

    async def run(self, problem_item, language, model_args):
        prompt = problem_item["prompt"]
        messages = [{"role": "user", "content": prompt}]
        kwargs = {
            "messages": messages,
            "model": model_args["model"],
            "temperature": model_args["temperature"],
            "max_tokens": model_args["max_tokens"],
            "top_p": model_args["top_p"],
        }

        result = await self.model_api.with_retry(kwargs) 
        out = prompt + "\n" + result
        return out, {}
