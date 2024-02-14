import argparse
import time
import os
import asyncio
from itertools import islice

from utils import enumerate_resume, read_jsonl, read_jsonl_gz, write_jsonl, enumerate_resume_rep
from async_strategies import BasicStrategy, PromptStrategy, PromptExtractStrategy, FewShotStrategy, CotStrategy, CotStrategy2, FewShotStrategy2, RetryStrategy, IterativeStrategy
from executors import get_result

DATABASE_ROOT = "benchmarks" 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_name", type=str, help="The name of the run", default="cotfs")
    parser.add_argument("--root_dir", type=str,
                        help="The root logging directory", default="root")
    parser.add_argument("--benchmark", type=str,
                        help="Which dataset to use", default="humaneval")
    parser.add_argument("--strategy", type=str,
                        help="Strategy: `simple`, `reflexion`", default="simple")
    parser.add_argument("--few_shot", type=int,
                        help="How many examples to use in few shot", default=4)
    parser.add_argument("--language", type=str, help="Strategy: `py` or `rs`", default="rs")
    parser.add_argument(
        "--model", type=str, help="OpenAI models only for now. For best results, use GPT-4",default="gpt-3.5-turbo")
    parser.add_argument("--pass_at_k", type=int,
                        help="Pass@k metric", default=1)
    parser.add_argument("--max_iters", type=int,
                        help="The maximum number of self-improvement iterations", default=30)
    parser.add_argument("--expansion_factor", type=int,
                        help="The expansion factor for the reflexion UCS and A* strategy", default=3)
    parser.add_argument("--verbose", type = bool,
                        help="To print live logs")
    parser.add_argument("--post_process", help='process model outout', type = bool,
                        default=True)
    args = parser.parse_args()
    return args

def get_dataset_path(dataset, language):
    #to lowercase
    dataset = dataset.lower()
    language = language.lower()
    return DATABASE_ROOT + "/" + dataset + "-" + language + ".jsonl"

def get_strategy(strategy):
    if strategy == "simple":
        return BasicStrategy()
    elif strategy == "prompt":
        return PromptStrategy()
    elif strategy == "prompt_extract":
        return PromptExtractStrategy()
    elif strategy == "few_shot":
        return FewShotStrategy()
    elif strategy == "few_shot_2":
        return FewShotStrategy2()
    elif strategy == "cot":
        return CotStrategy()
    elif strategy == "cot_2":
        return CotStrategy2()
    elif strategy == "retry":
        return RetryStrategy()
    elif strategy == "iterative":
        return IterativeStrategy()
    else:
        raise ValueError(f"Strategy `{strategy}` is not supported")

async def process_item_timeout(item, strategy, args, log_path, semaphore, t0, timeout = 120):
    if strategy in ["recursive", "iterative"]:
        timeout *= 3
    async with semaphore:
        try:
            await asyncio.wait_for(process_item(item, strategy, args, log_path, t0), timeout=timeout)
        except Exception as e:
            result = {
                "process_error": str(e),
                "name": item["name"],
                "prompt": item["prompt"],
                "valid": False,
                "model_output": None,
                "passes": False,
                "status" : "PROCESS_ERROR \n" + str(e),
                "timeout": e == asyncio.TimeoutError 
            }
            write_jsonl(log_path, [result], append=True)
            print(f"Error: {e}") 

async def process_item(item, strategy, args, log_path, t0):
    model_args = {
        "model": args.model,
        "temperature": 0.2,
        "top_p": 1,
        "max_tokens": None, # "max_tokens": 1024,
        "few_shot": args.few_shot,
        "post_process": args.post_process,
    }
    model_output, others = await strategy.run(item, args.language, model_args)
    result = get_result(model_output, item, args.language)
    if others and "messages" in others:
        result["messages"] = others["messages"]
    if others and "original_result" in others:
        result["original_result"] = others["original_result"]
    if others and "intermediate_results" in others:
        result["intermediate_results"] = others["intermediate_results"]
    result["model_output"] = model_output
    result["time_taken"] = time.time() - t0 
    write_jsonl(log_path, [result], append=True)
    

def get_log_path(args):
    log_dir = os.path.join(args.root_dir, args.run_name)
    strategy_name = args.strategy
    if strategy_name not in ["prompt", "prompt_extract"]:
        strategy_name = f"{strategy_name}_{args.few_shot}"
    if args.post_process:
        strategy_name += "_postp"
    log_path = os.path.join(
        log_dir, f"async_{args.benchmark}_{strategy_name}_{args.model}_{args.language}.jsonl")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_path

def get_database(args):
    dataset_path = get_dataset_path(args.benchmark, args.language)
    if args.verbose:
        print(f'Loading the dataset from {dataset_path}...')
    if dataset_path.endswith(".jsonl"):
        dataset = read_jsonl(dataset_path)
    elif dataset_path.endswith(".jsonl.gz"):
        dataset = read_jsonl_gz(dataset_path)
    else:
        raise ValueError(
            f"Dataset path `{args.dataset}` is not supported")
    return dataset



async def main(args):
    t0 = time.time()
    semaphore = asyncio.Semaphore(8)
    if not os.path.exists(args.root_dir):
        os.makedirs(args.root_dir)

    log_path = get_log_path(args)
    dataset = get_database(args)

    strategy = get_strategy(args.strategy)

    tasks = [process_item_timeout(item, strategy, args, log_path, semaphore,t0) for i,item in islice(enumerate_resume_rep(dataset, log_path, repetitions=3), args.max_iters)]
    await asyncio.gather(*tasks)

    
if __name__ == "__main__":
    args = get_args()
    asyncio.run(main(args)) 