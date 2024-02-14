import streamlit as st
import json
import sys
import os
import glob



def analyze_jsonl(file_path):
    total_problems = 0
    unique_names = set()
    total_valid = 0
    total_passes = 0
    problems = []
    max_time = 0
    timeouts = 0

    with open(file_path, 'r') as file:
        for line in file:
            try:
                problem = json.loads(line)
                problems.append(problem)
                total_problems += 1
                unique_names.add(problem['name'])
                if problem['valid']:
                    total_valid += 1
                if problem['passes']:
                    total_passes += 1
                if "time_taken" in problem:
                    max_time = max(max_time, problem["time_taken"])
                if "timeout" in problem and problem["timeout"]:
                    timeouts += 1
            except json.JSONDecodeError:
                print("Error decoding JSON line:", line)
                continue
    return {
        "file_path": file_path,
        "total_problems": total_problems,
        "unique_names": len(unique_names),
        "total_valid": total_valid,
        "total_passes": total_passes,
        "ratio_valid": total_valid / total_problems if total_problems > 0 else 0,
        "ratio_passes": total_passes / total_problems if total_problems > 0 else 0,
        "max_time": max_time,
        "timeouts": timeouts,
        "problems": problems
    }
        

def process_path(path):
    results = []
    if os.path.isdir(path):
        # Process all .jsonl files in the directory
        for file_path in glob.glob(os.path.join(path, "*.jsonl")):
            results.append(analyze_jsonl(file_path))
    else:
        # Process a single file
        results.append(analyze_jsonl(path))
    return results

def set_file_state(*args, **kwargs):
    st.session_state["file"] = kwargs["file"]

def set_problem_state(*args, **kwargs):
    st.session_state["problem"] = kwargs["problem"]

def display_file_button(file, i):
    with st.container():
        name = file["file_path"].split("/")[-1]
        st.write(f" Total {file['total_problems']}, unique = {file['unique_names']}, valid = {file['total_valid']}, passes = {file['total_passes']}")
        # Only 3 significant digits
        st.write(f" Ratio valid = {file['ratio_valid']:.3f}, ratio passes = {file['ratio_passes']:.3f}, max time = {file['max_time']:.3f}, timeouts = {file['timeouts']}")
        st.button(name, key=file["file_path"], on_click= set_file_state, kwargs={"file": i})
        st.write("-------------------------------------------------")

def display_problem_button(problem, i):
    with st.container():
        st.button(problem["name"], key=str(i)+problem["name"], on_click= set_problem_state, kwargs={"problem": i})
        if "time_taken" in problem:
            st.write(f" Valid: {problem['valid']}, Passes: {problem['passes']}, Time: {problem['time_taken']:.3f}")
        else:
            st.write(f" Valid: {problem['valid']}, Passes: {problem['passes']}")
        st.write("-------------------------------------------------")


def main_page(results):
    st.title("Run Viewer")
    for i, file in enumerate(results):
        display_file_button(file, i)
    st.button("Main", key="main", on_click= set_file_state, kwargs={"file": None})


def file_page(results):
    st.title("Run Viewer")
    st.button("Back", key="back", on_click= set_file_state, kwargs={"file": None})
    idx = st.session_state["file"]
    file = results[idx]
    st.write("File Path:", file["file_path"])
    st.write("Total Problems:", file["total_problems"])
    for i, problem in enumerate(file["problems"]):
        display_problem_button(problem, i)
    st.button("Back", key="back2", on_click= set_file_state, kwargs={"file": None})

def extract_language(file_path):
    if file_path.endswith(".py.jsonl"):
        return "python"
    elif file_path.endswith(".rs.jsonl"):
        return "rust"
    else:
        return "unknown"


def problem_page(results):
    st.title("Run Viewer")
    file = st.session_state["file"]
    problem_idx = st.session_state["problem"]
    problem = results[file]["problems"][problem_idx]
    language = extract_language(results[file]["file_path"])
    st.write("Name:", problem["name"])
    print(language)
    st.button("Back", key="back", on_click= set_problem_state, kwargs={"problem": None})
    if "time_taken" in problem:
        st.write(f" Valid: {problem['valid']}, Passes: {problem['passes']}, Time: {problem['time_taken']:.3f}")
    else:
        st.write(f" Valid: {problem['valid']}, Passes: {problem['passes']}")
    st.write("Prompt:")
    st.code(problem["prompt"], language=language)
    if "model_output" in problem:
        st.write("Model Output:")
        st.code(problem["model_output"], language=language)
    if "output" in problem:
        st.write("Output:")
        st.code(problem["output"], language=language)
    st.write("Status:", problem["status"])
    if "errors" in problem:
        st.write("Error:", problem["errors"])
    if "traceback" in problem:
        st.write("Traceback:")
        st.code(problem["traceback"], language="python")
    if "intermediate_results" in problem:
        st.write("Intermediate Results:")
        for i, result in enumerate(problem["intermediate_results"]):
            st.write(f"Result {i}:")
            st.code(result, language=language)
    if "original_result" in problem:
        st.write("Original Result:")
        st.code(problem["original_result"], language=language)
    if "messages" in problem and problem["messages"]:
        st.write("Messages:")
        for message in problem["messages"]:
            st.write(message)

    st.button("Back", key="back2", on_click= set_problem_state, kwargs={"problem": None})

default_path = "root/cotfs_mm2/"
file_path = default_path if len(sys.argv) < 2 else sys.argv[1]
results = process_path(file_path)



print(st.session_state)
if "file" in st.session_state and st.session_state["file"] is not None:
    if "problem" in st.session_state and st.session_state["problem"] is not None:
        problem_page(results)
    else:
        file_page(results)
else:
    main_page(results)