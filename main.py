import argparse
from itertools import islice
import time
import os

from utils import enumerate_resume, read_jsonl, read_jsonl_gz, write_jsonl
from strategies import BasicStrategy, PromptStrategy, PromptExtractStrategy
from executors import execute_python, execute_rust, get_output, get_result

DATABASE_ROOT = "benchmarks" 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_name", type=str, help="The name of the run", default="defaultRunName")
    parser.add_argument("--root_dir", type=str,
                        help="The root logging directory", default="root")
    parser.add_argument("--benchmark", type=str,
                        help="Which dataset to use", default="humaneval")
    parser.add_argument("--strategy", type=str,
                        help="Strategy: `simple`, `reflexion`", default="simple")
    parser.add_argument("--language", type=str, help="Strategy: `py` or `rs`", default="rs")
    parser.add_argument(
        "--model", type=str, help="OpenAI models only for now. For best results, use GPT-4",default="gpt-3.5-turbo")
    parser.add_argument("--pass_at_k", type=int,
                        help="Pass@k metric", default=1)
    parser.add_argument("--max_iters", type=int,
                        help="The maximum number of self-improvement iterations", default=30)
    parser.add_argument("--expansion_factor", type=int,
                        help="The expansion factor for the reflexion UCS and A* strategy", default=3)
    parser.add_argument("--verbose", action='store_true',
                        help="To print live logs")
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
    else:
        raise ValueError(f"Strategy `{strategy}` is not supported")
    

def main(args):
    if not os.path.exists(args.root_dir):
        os.makedirs(args.root_dir)
    
    dataset_path = get_dataset_path(args.benchmark, args.language)
    log_dir = os.path.join(args.root_dir, args.run_name)
    log_path = os.path.join(
        log_dir, f"{args.benchmark}_{args.strategy}_{args.model}_{args.language}.jsonl")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if dataset_path.endswith(".jsonl"):
        dataset = read_jsonl(dataset_path)
    elif dataset_path.endswith(".jsonl.gz"):
        dataset = read_jsonl_gz(dataset_path)
    else:
        raise ValueError(
            f"Dataset path `{args.dataset}` is not supported")

    strategy = get_strategy(args.strategy)
    c1, c2 = 0, 0
    for i, item in islice(enumerate_resume(dataset, log_path), args.max_iters):
        t0 = time.time()
        model_args = {
            "model": args.model,
            "temperature": 0.2,
            "max_tokens": 350,
            "top_p": 1,
            "stop": ["\n", "Human:"],
        }
        model_output = strategy.run(item, args.language, model_args)
        t1 = time.time()
        result = get_result(model_output, item, args.language)
        t2 = time.time()
        c1, c2 = c1 + t1-t0, c2 + t2-t1
        write_jsonl(log_path, [result], append=True)
    print(f"Total time spent in strategy: {c1}")
    print(f"Total time spent in executor: {c2}")

    
if __name__ == "__main__":
    args = get_args()
    main(args)