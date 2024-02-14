import json
import sys
import os
import glob



def analyze_jsonl(file_path):
    total_problems = 0
    unique_names = set()
    total_valid = 0
    total_passes = 0

    with open(file_path, 'r') as file:
        for line in file:
            try:
                problem = json.loads(line)
                total_problems += 1
                unique_names.add(problem['name'])
                if problem['valid']:
                    total_valid += 1
                if problem['passes']:
                    total_passes += 1
            except json.JSONDecodeError:
                print("Error decoding JSON line:", line)
                continue

    print(f"File: {file_path}")
    print("Total number of problems:", total_problems)
    print("Total number of unique names:", len(unique_names))
    print("Total number of valid problems:", total_valid)
    print("Total number of problems that pass:", total_passes)
    print("Ratio of valid problems:", total_valid / total_problems if total_problems > 0 else 0)
    print("Ratio of problems that pass:", total_passes / total_problems if total_problems > 0 else 0)
    print()

def process_path(path):
    if os.path.isdir(path):
        # Process all .jsonl files in the directory
        for file_path in glob.glob(os.path.join(path, "*.jsonl")):
            analyze_jsonl(file_path)
    else:
        # Process a single file
        analyze_jsonl(path)


if __name__ == "__main__":
    default_path = "root/defaultRunName/"
    file_path = default_path if len(sys.argv) < 2 else sys.argv[1]
    process_path(file_path)
