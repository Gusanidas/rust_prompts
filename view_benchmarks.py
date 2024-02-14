import streamlit as st
import json
import os
import glob

def analyze_jsonl(file_path):
    total_problems = 0
    problems = []

    with open(file_path, 'r') as file:
        for line in file:
            try:
                problem = json.loads(line)
                problems.append(problem)
                total_problems += 1
            except json.JSONDecodeError:
                print("Error decoding JSON line:", line)
                continue
    return {
        "file_path": file_path,
        "total_problems": total_problems,
        "problems": problems
    }

def process_path(path):
    results = []
    if os.path.isdir(path):
        for file_path in glob.glob(os.path.join(path, "*.jsonl")):
            results.append(analyze_jsonl(file_path))
    else:
        results.append(analyze_jsonl(path))
    return results

def set_file_state(*args, **kwargs):
    st.session_state["file"] = kwargs["file"]

def set_problem_state(*args, **kwargs):
    st.session_state["problem"] = kwargs["problem"]

def display_file_button(file, i):
    with st.container():
        name = file["file_path"].split("/")[-1]
        st.write(f"Total problems: {file['total_problems']}")
        st.button(name, key=file["file_path"], on_click=set_file_state, kwargs={"file": i})
        st.write("-------------------------------------------------")

def display_problem_button(problem, i):
    with st.container():
        st.button(problem["name"], key=problem["name"], on_click=set_problem_state, kwargs={"problem": i})
        st.write(f"Language: {problem['language']}")
        st.write("-------------------------------------------------")

def main_page(results):
    st.title("Benchmark Viewer")
    for i, file in enumerate(results):
        display_file_button(file, i)

def file_page(results):
    st.title("Benchmark Viewer")
    st.button("Back", key="back", on_click=set_file_state, kwargs={"file": None})
    idx = st.session_state["file"]
    file = results[idx]
    st.write("File Path:", file["file_path"])
    st.write("Total Problems:", file["total_problems"])
    for i, problem in enumerate(file["problems"]):
        display_problem_button(problem, i)
    st.button("Back", key="back2", on_click=set_file_state, kwargs={"file": None})

def problem_page(results):
    st.title("Benchmark Viewer")
    file = st.session_state["file"]
    problem_idx = st.session_state["problem"]
    problem = results[file]["problems"][problem_idx]
    st.write("Name:", problem["name"])
    st.write("Language:", problem["language"])
    st.button("Back", key="back", on_click=set_problem_state, kwargs={"problem": None})
    st.write("Prompt:")
    st.code(problem["prompt"], language=problem["language"])
    if "test" in problem:
        st.write("Test:")
        st.code(problem["test"], language=problem["language"])

    st.button("Back", key="back2", on_click=set_problem_state, kwargs={"problem": None})

default_path = "benchmarks/"
file_path = default_path if len(os.sys.argv) < 2 else os.sys.argv[1]
results = process_path(file_path)

if "file" in st.session_state and st.session_state["file"] is not None:
    if "problem" in st.session_state and st.session_state["problem"] is not None:
        problem_page(results)
    else:
        file_page(results)
else:
    main_page(results)
