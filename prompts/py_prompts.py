BASIC_PROMPT_PY = """
# You are an expert python programer. Continue the implementation of the function below.
# The docstring of the function describes what the function should do.
# 
{prompt}
"""

BASIC_EXTRACT_PROMPT_PY = """
You are an expert python programer. Below there is a function signature and a docstring.
Repond by implementing the function described in the docstring. Your answer should be a valid python function.

{prompt}
"""

FEW_SHOT_PROMPT_PY = """
You are an expert python programer. You will be given a programming problem to solve.
The problem description will be either a comment above the function signature or a docstring inside the function.
Implement a solution to the problem using python. The function signature and the problem description will be provided.
You can write helper functions if needed.
Your solution should be a valid python code, so write any reasoning as a comment.

{prompt}
""" 

COT_PROMPT_PY = """
You are an expert python programer. You will be given a programming problem to solve.
The problem description will be either a comment above the function signature or a docstring inside the function.
First provide a step by step plan to solve the problem, writen as a python comment. Then implement the solution using python.
The function signature and the problem description will be provided. You can write helper functions if needed.
Your solution should be a valid python code, so write any reasoning as a comment.

{prompt}
"""


# Few Shot Examples

problem_statement_1 = """
def sum_of_unique_digits(s: str, max_length: int) -> int:
    /"/"/"
    Given a string `s` representing a number and an integer `max_length`, return the sum of its 
    unique digits. The input string may contain non-digit characters, which should be ignored.
    If the length of `s` exceeds `max_length`, return -1.
    
    Examples:
    - sum_of_unique_digits("a123bc34d8", 10) should return 18.
    - sum_of_unique_digits("cc1111", 6) should return 1.
    - sum_of_unique_digits("123", 3) should return 6.
    - sum_of_unique_digits("1234", 3) should return -1 (since the length of "1234" is greater than 3).

    Args:
    s (str): The input string containing digits and possibly non-digit characters.
    max_length (int): The maximum allowable length of the input string.

    Returns:
    int: The sum of the unique digits in `s`, or -1 if the length of `s` exceeds `max_length`.
    /"/"/"
"""

step_by_step_1 = """
# Step 1: Check if the length of `s` exceeds `max_length`.
# Step 2: Collect unique digits from `s`.
# Step 3: Sum the unique digits.
# Step 4: Return the calculated sum.
"""

problem_solution_1 = """
def sum_of_unique_digits(s: str, max_length: int) -> int:
    if len(s) > max_length:
        return -1

    unique_digits = set()
    for char in s:
        if char.isdigit():
            unique_digits.add(char)

    return sum(int(digit) for digit in unique_digits)
"""

problem_statement_2 = """
def find_name_combinations(names, target):
    /"/"/"
    Miss Umbridge wants to find all combinations of students whose name lengths, when combined, sum up to a specific target number.
    
    :param names: A list of student names (str).
    :param target: An integer representing the target sum of the lengths of the names.
    
    The function should return a list of lists, where each inner list represents a combination of student names. 
    The sum of the length of the names in each combination should be equal to the target number. 
    Each student can only appear once in each combination.
    
    Example:
    >>> find_name_combinations(["Harry", "Ron", "Hermione", "Draco"], 8)
    [["Harry", "Ron"], ["Hermione"], ["Draco", "Ron"]]
    /"/"/"
    pass
"""

step_by_step_2 = """
# Step 1: Identify the Problem Type - This is a combinatorial problem where we need to find all subsets of names that sum up to a specific target length.
# Step 2: Generate All Possible Combinations - Use backtracking to generate combinations.
# Step 3: Check Each Combination - For each generated combination, sum the lengths of the names.
# Step 4: Compare with Target - If the sum of the lengths equals the target number, add this combination to the result list.
# Step 5: Return Results - After considering all combinations, return the list of valid combinations.
"""


problem_solution_2 = """
def find_name_combinations(names, target):
    # Helper function to generate all possible combinations of names
    def backtrack(start, path):
        length_sum = sum(len(name) for name in path)
        if length_sum == target:
            result.append(path.copy())
            return
        if length_sum > target:
            return

        # Generate all possible combinations
        for i in range(start, len(names)):
            path.append(names[i])
            backtrack(i + 1, path)
            path.pop()

    result = []
    backtrack(0, [])
    return result
"""

problem_statement_3 = """
# Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
#
# The lowest common ancestor is defined between two nodes p and q as the lowest node in T that
# has both p and q as descendants (where we allow a node to be a descendant of itself).
#
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
#
def find_lowest_common_ancestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
"""

step_by_step_3 = """
// 1: Create a helper function to count the number of matches of p and q in the tree.
// 2: The match count will be the count of the descendants plus 1 if the node is p or q.
// 3: If the count is 2, return the current node as the LCA.
// 4: When we call the helper function in a descendant, if the LCA is found, we can return early.
"""

problem_solution_3 = """
from typing import Tuple

# Helper function to count the number of matches of p and q in the tree
def count_matches(root: 'TreeNode', p: int, q: int) -> Tuple['TreeNode', int]:
    if not root:
        return None, 0
    count = 0
    # If the current node is p or q, increment the count
    if root.val == p or root.val == q:
        count += 1
    left_node, left_count = count_matches(root.left, p, q)
    # If the LCA is found in the left subtree, return early
    if left_node:
        return (left_node, 2)

    right_node, right_count = count_matches(root.right, p, q)
    # If the LCA is found in the right subtree, return early
    if right_node:
        return (right_node, 2)
    count += left_count + right_count
    # If the count is 2, return the current node as the LCA
    return (root, count) if count==2 else (None, count)

def find_lowest_common_ancestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    p_val, q_val = p.val, q.val
    return count_matches(root, p_val, q_val)[0]
"""

problem_statement_4 = """
# You are given an array nums representing a circular array.
# Each nums[i] denotes the number of indices forward/backward you must move if you are located at index i:# 
# - If nums[i] is positive, move nums[i] steps forward.
# - If nums[i] is negative, move nums[i] steps backward.
#  
# Since the array is circular, you may assume that moving forward from the last element puts you 
# on the first element, and moving backwards from the first element puts you on the last element.
# 
# A valid loop is a loop that:
# - Starts and ends at the same index.
# - Has more than one element.
# - Every element in the loop has the same direction.# 
# Return true if there exists a valid loop in the array. Otherwise, return false.
# 
# Example:
# Input: nums = [2,-1,1,2,2]
# Output: true
# Explanation: There is a valid loop (0 -> 2 -> 3 -> 0).
def circularArrayLoop(self, nums: List[int]) -> bool:
"""

step_by_step_4 = """
# 1: Create a helper function "has_loop" to check if a loop exists starting from a given index.
# 2: In has_loop, we keep track of indices visited in the current path and indices visited in previous paths.
# 3: If we end up in an index that has been visited by previous paths, we can mark all indices in the current path as visited and return false.
# 4: If we end up in an index that has been visited by the current path, we check if the loop is valid by calling "is_valid_loop" and return true if it is.
# 5: The helper function "is_valid_loop" will:
#    - Extract the loop from the current path.
#    - Check if the loop has more than 2 elements and all elements have the same direction.
# 6: Call "has_loop" for each index in the array and return true if any of them returns true.
"""

problem_solution_4 = """
# Helper function to check if a loop is valid
def is_valid_loop(path, nums):
    # Extract the loop from the current path
    rcycle = []
    for i, x in enumerate(reversed(path)):
        rcycle.append(x)
        if i > 0 and x == rcycle[0]:
            break
    # Check if the loop has more than 2 elements and all elements have the same direction
    return len(rcycle) > 2 and all(nums[x] * nums[rcycle[0]] > 0 for x in rcycle)

def has_loop(start, nums, seen):
    path = []
    curr = start
    nums_len = len(nums)
    while curr not in seen and curr not in path:
        path.append(curr)
        curr = (curr + nums[curr]) % nums_len
    path.append(curr)
    # If curr has been visited by a previous path, mark all indices in the current path as visited and return false.
    # If the loop is invalid, mark all indices in the current path as visited and return false.
    if curr in seen or not is_valid_loop(path, nums):
        seen.update(path)
        return False
    return True

def circularArrayLoop(self, nums: List[int]) -> bool:
    seen = set()
    return any([has_loop(i, nums, seen) for i,_ in enumerate(nums)])
"""

problem_statement_5 = """
# You are given an array of strings words and a string chars.
# A string is good if it can be formed by characters from chars (each character can only be used once).
# Return the sum of lengths of all good strings in words.
#
# Example:
# Input: words = ["cat","bt","hat","tree"], chars = "atach"
# Output: 6
# Explanation: The strings that can be formed are "cat" and "hat" so the answer is 3 + 3 = 6.
def count_characters(words: List[str], chars: str) -> int:
"""

step_by_step_5 = """
# 1: Create a helper function to check if a word can be formed from the characters in chars.
# 2: In the helper function, we keep track of the count of each character in chars.
# 3: We iterate through the characters in the word and decrement the count of each character in the map.
# 4: If the count of any character becomes negative, we return false.
# 5: If we reach the end of the word, we return true.
# 6: Iterate through the words and call the helper function for each word.
# 7: Return the sum of the lengths of the words for which the helper function returns true.
"""

problem_solution_5 = """
from typing import List

def can_form_word(word, chars):
    char_count = dict()
    for char in chars:
        char_count[char] = char_count.get(char, 0) + 1
    for char in word:
        if char_count.get(char, 0) == 0:
            return False
        char_count[char] -= 1
    return True

def count_characters(words: List[str], chars: str) -> int:
    return sum(len(word) for word in words if can_form_word(word, chars))
"""

problem_statement_6 = """
# In a visit to the goverment office you are informed that there are some documents that are not in the correct order.
# Some of the documents you need require other documents to be presented first.
# You suspect that it is impossible to present all the documents in the correct order.
# You are given a list of documents and their dependencies. You need to determine if it is possible to present all the documents in the correct order.
#
# The input is given as a list of tuples where each tuple contains two indices (a, b) representing that document a needs to be presented before document b.
# Return True if it is possible to present all the documents in the correct order, otherwise return False.
#
# Example:
# Input: [(1, 0), (0, 1)]
# Output: False
# Explanation: Document 1 needs to be presented before document 0 and document 0 needs to be presented before document 1. This is impossible.
#
# def can_present_documents(dependencies: List[Tuple[int, int]]) -> bool:
"""

step_by_step_6 = """
1: Create a graph from the input list of dependencies.
2: Create a helper function to check if there is a cycle in the graph.
3: In the helper function, we keep track of visited nodes and nodes in the current recursion stack.
4: For each node in the graph, we call the helper function to check for a cycle.
5: If a cycle is found, return False.
"""

problem_solution_6 = """
from typing import List, Tuple

def can_present_documents(dependencies: List[Tuple[int, int]]) -> bool:
    graph = dict()
    for a, b in dependencies:
        if a not in graph:
            graph[a] = []
        graph[a].append(b)

    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
        rec_stack.remove(node)
        return False

    for node in graph:
        visited = set()
        rec_stack = set()
        if has_cycle(node, visited, rec_stack):
            return False
    return True
"""

problem_statement_7 = """
def next_divisible_by_7_not_2(n):
    '''
    Find the next number bigger than n that is divisible by 7 but not by 2.
    >>> next_divisible_by_7_not_2(14)
    21
    >>> next_divisible_by_7_not_2(20)
    21
    >>> next_divisible_by_7_not_2(21)
    35
    >>> next_divisible_by_7_not_2(28)
    35
    '''
    pass
"""

step_by_step_7 = """
# Step 1: Start with the next number after n.
# Step 2: Check if the number is divisible by 7 and not by 2.
# Step 3: If it is, return the number. Otherwise, increment the number and repeat from step 2.
"""

problem_solution_7 = """
def next_divisible_by_7_not_2(n):
    candidate = n + 1
    while candidate % 7 != 0 or candidate % 2 == 0:
        candidate += 1
    return candidate
"""

problem_statement_8 = """
def elements_divisible_by_3_desc(input_list):
    '''
    Given a list of integers, return a list of the elements that are divisible by 3, sorted in decreasing order.
    >>> elements_divisible_by_3_desc([3, 6, 9, 12, 15, 1, 2])
    [15, 12, 9, 6, 3]
    >>> elements_divisible_by_3_desc([5, 7, 11])
    []
    >>> elements_divisible_by_3_desc([9, 8, 3, 6])
    [9, 6, 3]
    '''
    pass
"""

step_by_step_8 = """
# Step 1: Filter the elements in the input list that are divisible by 3.
# Step 2: Sort the filtered elements in decreasing order.
# Step 3: Return the sorted list.
"""

problem_solution_8 = """
def elements_divisible_by_3_desc(input_list):
    divisible_by_3 = [x for x in input_list if x % 3 == 0]  # Step 1: Filter elements divisible by 3
    divisible_by_3.sort(reverse=True)  # Step 2: Sort in decreasing order
    return divisible_by_3  # Step 3: Return the sorted list
"""




problem_statements_py = [problem_statement_1, problem_statement_2, problem_statement_7, problem_statement_8, problem_statement_3, problem_statement_4, problem_statement_5, problem_statement_6]
step_by_steps_py = [step_by_step_1, step_by_step_2, step_by_step_7, step_by_step_8, step_by_step_3, step_by_step_4, step_by_step_5, step_by_step_6]
problem_solutions_py = [problem_solution_1, problem_solution_2, problem_solution_7, problem_solution_8, problem_solution_3, problem_solution_4, problem_solution_5, problem_solution_6]

###

ITERATIVE_PROMPT_PY = """
To this problem:

{prompt}

The solution provided:

{solution}

Fails with this message:

{message}

Please provide a better solution.
Remeber to write any reasoning as a comment. Remeber to import any needed module.
"""