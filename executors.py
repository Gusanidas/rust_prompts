from threading import Thread
from typing import Tuple, List, Optional
import os
import signal
import subprocess
import json
import time
import traceback


cargo_harness_dir = "rust_execution"

class CompileErr:
    def __init__(self, rendered):
        self.rendered = rendered

    def __str__(self):
        return self.rendered

    def __repr__(self):
        return "{" + str(self) + "}"


class RuntimeErr:
    def __init__(self, left, right, line, column, panic_reason):
        # right and left are only used for assert_eq! errors
        self.left = left
        self.right = right
        # NOTE: currently not using the below
        self.line = line
        self.column = column
        self.panic_reason = panic_reason

    def __str__(self):
        if self.left is not None and self.right is not None:
            return f"assertion failed: {self.left} == {self.right}"
        else:
            return self.panic_reason

    def __repr__(self):
        return "{" + str(self) + "}"

def create_temp_project() -> Tuple[str, str]:
    print("Creating temp project")
    # get pid of the process
    pid = os.getpid()
    # get random number
    rand = os.urandom(8).hex()
    # create a temp directory
    temp_dir = f"/tmp/cargo_harness-{pid}-{rand}"
    # delete the temp directory if it exists
    if os.path.exists(temp_dir):
        os.system(f"rm -rf {temp_dir}")
    os.mkdir(temp_dir)
    # move the cargo harness into the temp directory
    os.system(f"cp -r {cargo_harness_dir}/* {temp_dir}")
    main_path = os.path.join(temp_dir, "src", "main.rs")
    print(f"Created temp project at {temp_dir}")
    time.sleep(1) # wait for
    return temp_dir, main_path

class PropagatingThread(Thread):
    def run(self):
        self.exc = None
        try:
            if hasattr(self, '_Thread__target'):
                # Thread uses name mangling prior to Python 3.
                self.ret = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self, timeout=None):
        super(PropagatingThread, self).join(timeout)
        if self.exc:
            raise self.exc
        return self.ret
    

def function_with_timeout(func, args, timeout):
    result_container = []

    def wrapper():
        result_container.append(func(*args))

    thread = PropagatingThread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutError()
    else:
        return result_container[0]


def execute_python(code, timeout=1):
    status = "init"
    try:
        output = function_with_timeout(exec, (code, {}), timeout)
        status = "OK"
    except Exception as e:
        output = str(e) + e.__class__.__name__ + traceback.format_exc()
        status = "ERROR"
    return  output, status

def execute_code(code, language, timeout=1):
    if language == "py":
        output, status = execute_python(code, timeout)
    elif language == "rs":
        passes, valid, status, output, errors = evaluate_rs("code", code)
        output = f"output: {output}, \n errors: {errors}"
    return output, status

def get_output(func: str, timeout: int = 5) -> str:
    try:
        exec(f"from typing import *\n{func}", globals())
        output = function_with_timeout(eval, (func, globals()), timeout)
        return output
    except TimeoutError:
        return "TIMEOUT"
    except Exception as e:
        return str(e)


def get_result(func: str, problem_item: dict, language: str) -> dict:
    if language == "py":
        return get_result_py(func, problem_item)
    elif language == "rs":
        return get_result_rs(func, problem_item)
    else:
        raise ValueError(f"Language `{language}` is not supported.")

def get_result_py(func: str, problem_item: dict) -> dict:
    passes, valid, status, output, tback = True, True, "INIT", None, None
    try:
        func_with_tests = func+"\n"+problem_item["test"]
        code = f"from typing import *\n{func_with_tests}"
        output = function_with_timeout(exec, (code, globals()), 5)
        status = "OK"
    except TimeoutError:
        passes = False
        status = "TIMEOUT"
    except Exception as e:
        tback = traceback.format_exc()
        passes, valid, status = False, False, "exception"+str(e)+e.__class__.__name__
    return {
        "name": problem_item["name"],
        "passes": passes,
        "valid": valid,
        "status": status,
        "output": output,
        "prompt": problem_item["prompt"],
        "traceback": tback if tback else ""
    }

def get_result_rs(func: str, problem_item: dict) -> dict:
    print("Evaluating rust")
    passes, valid,status, output, errors = evaluate_rs(problem_item["name"], func+"\n"+problem_item["test"])
    return {
        "name": problem_item["name"],
        "passes": passes,
        "valid": valid,
        "status": status,
        "output": output,
        "errors": errors,
        "prompt": problem_item["prompt"]
    }

def timeout_handler(_, __):
    raise TimeoutError()

def run_with_timeout(cmd: str, tmp_cargo_path: str, timeout: int = 5, print_debug: bool = False) -> Optional[Tuple[str, str]]:
    """
    Runs the given command with a timeout. Produces a tuple of stdout and stderr.
    If the command times out, returns None.
    """
    # set up the timeout handler
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    # run the command
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, cwd=tmp_cargo_path)
    try:
        out, err = p.communicate()
        # reset the timeout handler
        signal.alarm(0)
    except TimeoutError:
        p.kill()
        return None

    # decode the output
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    if print_debug:
        print("## RUN OUTPUTS ##")
        print("STDOUT:")
        print(out)
        print("STDERR:")
        print(err, flush=True)

    return out, err



def evaluate_rs(name: str, func: str, timeout: int = 5) -> Tuple:
    """
    Evaluates the implementation on Human-Eval Rust (MultiPL-E generated,

    Federico Cassano, John Gouwar, Daniel Nguyen, Sydney Nguyen, Luna Phipps-Costin, Donald Pinckney, Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson, Molly Q Feldman, Arjun Guha, Michael Greenberg, Abhinav Jangda ).
    If you use this function please cite:
    @misc{cassano2022multiple,
      title={MultiPL-E: A Scalable and Extensible Approach to Benchmarking Neural Code Generation}, 
      author={Federico Cassano and John Gouwar and Daniel Nguyen and Sydney Nguyen and Luna Phipps-Costin and Donald Pinckney and Ming-Ho Yee and Yangtian Zi and Carolyn Jane Anderson and Molly Q Feldman and Arjun Guha and Michael Greenberg and Abhinav Jangda},
      year={2022},
      eprint={2208.08227},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
    })

    TODO: do it actually
    """
    tmp_dir, tmp_path = create_temp_project()
    passes, valid, status, output,errors = True, True, "OK", None, None
    print(f"Created temp project at {tmp_dir}")
    print(f"Evaluating\n{func}", flush=True)
    write_to_file_toplevel(tmp_path, func)

    res = run_with_timeout(
        "cargo check --message-format=json", tmp_dir, timeout=timeout, print_debug=True)
    assert res is not None, "Timeout in cargo check, wow"

    errs = grab_compile_errs(res[0])  # (check returns stdin)
    if len(errs) > 0:
        # cleanup the temp directory
        os.system(f"rm -rf {tmp_dir}")
        print("Compile errors. Failed eval", flush=True)
        return False, False, "Compile errors", None, [str(err) for err in errs]

    # compile and run the binary
    res = run_with_timeout("cargo run", tmp_dir,
                           timeout=timeout, print_debug=True)
    os.system(f"rm -rf {tmp_dir}")

    if res is None:
        print("Timeout?. Failed eval", flush=True)
        return False, True, "Timeout", None, None
    else:
        errs = grab_runtime_errs(res[1])
        if len(errs) > 0:
            print("Runtime errors. Failed eval", flush=True)
            return False, True, "Runtime errors", None, [str(err) for err in errs]

        print("Passed eval", flush=True)
        return True, True, "OK", None, None

def grab_compile_errs(inp: str) -> List[CompileErr]:
    # we get a stream of json objects, so we need to parse them one by one
    objs = []
    for line in inp.splitlines():
        if line == "":
            continue
        o = json.loads(line)
        if o is not None and o["reason"] == "compiler-message" and \
                o["message"]["level"] == "error" and \
                o["message"]["spans"] != []:
            rendered = o["message"]["rendered"]
            objs.append(CompileErr(rendered))

    return objs

def write_to_file_toplevel(path: str, code: str):
    # delete the file if it exists
    if os.path.exists(path):
        os.remove(path)
    # write the code to the file
    print("Code to be written")
    print(code)
    with open(path, "w") as f:
        f.write(code)

def indent_code(code: str, spaces: int = 4) -> str:
    """
    Indent the code by the given number of spaces.
    """
    return "\n".join([" " * spaces + line for line in code.splitlines()])

def write_to_file(path: str, code: str):
    prelude = "fn main() {\n"
    postlude = "\n}"
    code = prelude + indent_code(code) + postlude
    # delete the file if it exists
    if os.path.exists(path):
        os.remove(path)
    # write the code to the file
    print("Code to be written")
    print(code)
    with open(path, "w") as f:
        f.write(code)

def grab_runtime_errs(inp: str) -> List[RuntimeErr]:
    failed_asserts = []
    split = inp.splitlines()
    curr_left = None
    panic_reason = None
    for line in split:
        if "fatal runtime" in line:
            # we have a panic
            panic_idx = line.index("fatal runtime")
            panic_reason = line[panic_idx + len("fatal runtime") + 1:]
        elif "panicked at" in line:
            panic_idx = line.index("panicked at")
            # strip source line if it exists
            if "src/main.rs" in line:
                line = line[:line.index("src/main.rs")]
            panic_reason = line[panic_idx + len("panicked at") + 1:]
        elif "left:" in line:
            split = line.split("`")
            if len(split) < 2:
                continue
            curr_left = split[1]
        elif "right:" in line:
            split = line.split("`")
            if len(split) < 2:
                continue
            curr_right = split[1]
            # get the line and column number
            fileinto = line.split(",")[-1]
            line = int(fileinto.split(":")[1])
            column = int(fileinto.split(":")[2])
            failed_asserts.append(RuntimeErr(
                curr_left, curr_right, line, column, panic_reason))
            curr_left = None
            panic_reason = None

    if panic_reason is not None:
        failed_asserts.append(RuntimeErr(None, None, None, None, panic_reason))

    return failed_asserts

