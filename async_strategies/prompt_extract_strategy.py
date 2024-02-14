from .base_strategy import BaseStrategy
from prompts import BASIC_EXTRACT_PROMPT_PY, BASIC_EXTRACT_PROMPT_RS


class PromptExtractStrategy(BaseStrategy):

    async def run(self, problem_item, language, model_args):
        if language == "py":
            prompt = BASIC_EXTRACT_PROMPT_PY.format(prompt=problem_item["prompt"])
        elif language == "rs":
            prompt = BASIC_EXTRACT_PROMPT_RS.format(prompt=problem_item["prompt"])
        messages = [{"role": "user", "content": prompt}]
        kwargs = {
            "messages": messages,
            "model": model_args["model"],
            "temperature": model_args["temperature"],
            "max_tokens": model_args["max_tokens"],
            "top_p": model_args["top_p"],
            #"stop": model_args["stop"],
        }

        result = await self.model_api.with_retry(kwargs) 
        if model_args.get("post_process", False):
            clean_result = self.post_process(result)
            return clean_result, {"messages": messages, "original_result": result}
        return result, {"messages": messages}