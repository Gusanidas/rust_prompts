from .base_strategy import BaseStrategy
from prompts import BASIC_EXTRACT_PROMPT_PY, BASIC_EXTRACT_PROMPT_RS, problem_statements_py, problem_statements_rs, problem_solutions_py, problem_solutions_rs, step_by_steps_py, step_by_steps_rs, COT_PROMPT_PY

class CotStrategy2(BaseStrategy):

    async def run(self, problem_item, language, model_args) -> (str, dict):
        if language == "py":
            prompt = COT_PROMPT_PY.format(prompt=problem_statements_py[0])
            messages = [{"role": "user", "content": prompt}]
            messages += [{"role": "assistant", "content": step_by_steps_py[0] + problem_solutions_py[0]}]
            for i in range(1, min(model_args.get("few_shot", 1024), len(problem_statements_py))):
                messages.append({"role": "user", "content": COT_PROMPT_PY.format(prompt=problem_statements_py[i])})
                messages.append({"role": "assistant", "content": step_by_steps_py[i]+problem_solutions_py[i]})
            messages.append({"role": "user", "content": COT_PROMPT_PY.format(prompt=problem_item["prompt"])})
        elif language == "rs":
            prompt = BASIC_EXTRACT_PROMPT_RS.format(prompt=problem_statements_rs[0])
            messages = [{"role": "user", "content": prompt}]
            messages += [{"role": "assistant", "content": step_by_steps_rs[0] + problem_solutions_rs[0]}]
            for i in range(1, min(model_args.get("few_shot", 1024), len(problem_statements_rs))):
                messages.append({"role": "user", "content": problem_statements_rs[i]})
                messages.append({"role": "assistant", "content": step_by_steps_rs[i]+problem_solutions_rs[i]})
            messages.append({"role": "user", "content": problem_item["prompt"]})
        else:
            raise ValueError(f"Invalid language: {language}")
        print("-----------------------------------")
        print(messages)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
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