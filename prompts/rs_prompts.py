BASIC_PROMPT_RS = """
// You are an expert rust programer. Continue the implementation of the function below.
// The docstring of the function describes what the function should do.
// Remember that the first line of the function is already written and you should continue from there. 
// And remember to close the function with a `}}`.
//
{prompt}
"""

BASIC_EXTRACT_PROMPT_RS = """
You are an expert rust programer. Below there is a function signature and a description of what the function should do.
Repond by implementing the function described in rust. Your answer should be a valid rust function. Answer only with the rust code.

{prompt}
"""


# Few Shot Examples

problem_statement_1 = """
/// Given a string `s` representing a number and an integer `max_length`, return the sum of its 
/// unique digits. The input string may contain non-digit characters, which should be ignored.
/// If the length of `s` exceeds `max_length`, return -1.
///
/// Examples:
/// - sum_of_unique_digits("a123bc34d8", 10) should return 18.
/// - sum_of_unique_digits("cc1111", 6) should return 1.
/// - sum_of_unique_digits("123", 3) should return 6.
/// - sum_of_unique_digits("1234", 3) should return -1 (since the length of "1234" is greater than 3).
///
/// Args:
/// s (str): The input string containing digits and possibly non-digit characters.
/// max_length (usize): The maximum allowable length of the input string.
///
/// Returns:
/// i32: The sum of the unique digits in `s`, or -1 if the length of `s` exceeds `max_length`.
fn sum_of_unique_digits(s: &str, max_length: usize) -> i32 {
"""

step_by_step_1 = """
// Step 1: Check if the length of `s` exceeds `max_length`.
// Step 2: Collect unique digits from `s`.
// Step 3: Sum the unique digits.
// Step 4: Return the calculated sum.
"""

problem_solution_1 = """
use std::collections::HashSet;

fn sum_of_unique_digits(s: &str, max_length: usize) -> i32 {
    // Step 1: Check if the length of `s` exceeds `max_length`.
    if s.len() > max_length {
        return -1;
    }

    // Step 2: Collect unique digits from `s`.
    let mut unique_digits = HashSet::new();
    for c in s.chars() {
        if c.is_digit(10) {
            unique_digits.insert(c);
        }
    }

    // Step 3: Sum the unique digits.
    // Step 4: Return the calculated sum.
    unique_digits.iter().map(|d| d.to_digit(10).unwrap() as i32).sum()
}
"""

problem_statement_2 = """
//Miss Umbridge wants to find all combinations of students whose name lengths, when combined, sum up to a specific target number.
//
//:param names: A list of student names (str).
//:param target: An integer representing the target sum of the lengths of the names.
//
//The function should return a list of lists, where each inner list represents a combination of student names.
//The sum of the length of the names in each combination should be equal to the target number.
//Each student can only appear once in each combination.

//Example:
//assert_eq!(
//    find_name_combinations(vec!["Harry", "Ron", "Hermione", "Draco"], 8),
//    vec![vec!["Harry", "Ron"], vec!["Hermione"], vec!["Draco", "Ron"]]
//);
//
fn find_name_combinations<'a>(names: Vec<&'a str>, target: usize) -> Vec<Vec<&'a str>> {
"""

step_by_step_2 = """
// Step 1: Identify the Problem Type - This is a combinatorial problem where we need to find all subsets of names that sum up to a specific target length.
// Step 2: Generate All Possible Combinations - Use backtracking to generate combinations.
// Step 3: Check Each Combination - For each generated combination, sum the lengths of the names.
// Step 4: Compare with Target - If the sum of the lengths equals the target number, add this combination to the result list.
// Step 5: Return Results - After considering all combinations, return the list of valid combinations.
"""

problem_solution_2 = """
fn find_name_combinations<'a>(names: Vec<&'a str>, target: usize) -> Vec<Vec<&'a str>> {
    // Helper function to generate all possible combinations of names.
    fn backtrack<'a>(start: usize, path: &mut Vec<&'a str>, names: &[&'a str], target: usize, result: &mut Vec<Vec<&'a str>>) {
        let length_sum: usize = path.iter().map(|&name| name.len()).sum(); // Step 3: Sum the lengths of the names.

        if length_sum == target {
            result.push(path.clone());
            return;
        }
        if length_sum > target {
            return;
        }
        for i in start..names.len() {
            path.push(names[i]);
            backtrack(i + 1, path, names, target, result);
            path.pop();
        }
    }

    let mut result = Vec::new();
    backtrack(0, &mut Vec::new(), &names, target, &mut result);
    result
}
"""

problem_statement_3 = """
// Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
//
// The lowest common ancestor is defined between two nodes p and q as the lowest node in T that
// has both p and q as descendants (where we allow a node to be a descendant of itself).
// Nodes p and q will exist in the tree and the arguments wont be None.
//
// #[derive(Debug, PartialEq, Eq)]
// pub struct TreeNode {
//   pub val: i32,
//   pub left: Option<Rc<RefCell<TreeNode>>>,
//   pub right: Option<Rc<RefCell<TreeNode>>>,
// }
// 
// impl TreeNode {
//   #[inline]
//   pub fn new(val: i32) -> Self {
//     TreeNode {
//       val,
//       left: None,
//       right: None
//     }
//   }
// }
fn find_lowest_common_ancestor(
    root: Option<Rc<RefCell<TreeNode>>>,
    p: Option<Rc<RefCell<TreeNode>>>,
    q: Option<Rc<RefCell<TreeNode>>>,
) -> Option<Rc<RefCell<TreeNode>>> {
"""

step_by_step_3 = """
// 1: Create a helper function to count the number of matches of p and q in the tree.
// 2: The match count will be the count of the descendants plus 1 if the node is p or q.
// 3: If the count is 2, return the current node as the LCA.
// 4: When we call the helper function in a descendant, if the LCA is found, we can return early.
"""

problem_solution_3 = """
fn find_lowest_common_ancestor(
    root: Option<Rc<RefCell<TreeNode>>>,
    p: Option<Rc<RefCell<TreeNode>>>,
    q: Option<Rc<RefCell<TreeNode>>>,
) -> Option<Rc<RefCell<TreeNode>>> {
    // We can safely unwrap the options since the nodes p and q will exist.
    let p_val = p.unwrap().borrow().val;
    let q_val = q.unwrap().borrow().val;
    count_matches(root, p_val, q_val).0
}

fn count_matches(
    node: Option<Rc<RefCell<TreeNode>>>,
    p: i32,
    q: i32,
) -> (Option<Rc<RefCell<TreeNode>>>, i32) {
    if let Some(node) = node {
        let mut count = 0;
        // If the current node is p or q, increment the count.
        if node.borrow().val == p || node.borrow().val == q {
            count = 1;
        }
        let (left_node, left_count) = count_matches(node.borrow().left.clone(), p, q);
        // If we find the LCA in the left subtree, return early.
        if left_node.is_some() {
            return (left_node, left_count);
        }
        let (right_node, right_count) = count_matches(node.borrow().right.clone(), p, q);
        // If we find the LCA in the right subtree, return early.
        if right_node.is_some() {
            return (right_node, right_count);
        }
        count += left_count + right_count;
        if count == 2 {
            // If the count is 2, return the current node as the LCA.
            (Some(node), count)
        } else {
            (None, count)
        }
    } else {
        (None, 0)
    }
}
"""

problem_statement_4 = """
// You are given an array nums representing a circular array.
// Each nums[i] denotes the number of indices forward/backward you must move if you are located at index i:
//
// - If nums[i] is positive, move nums[i] steps forward.
// - If nums[i] is negative, move nums[i] steps backward.
//
// Since the array is circular, you may assume that moving forward from the last element puts you 
// on the first element, and moving backwards from the first element puts you on the last element.
// 
// A valid loop is a loop that:
// - Starts and ends at the same index.
// - Has more than one element.
// - Every element in the loop has the same direction.
//
// Return true if there exists a valid loop in the array. Otherwise, return false.
// 
// Example:
// Input: nums = [2,-1,1,2,2]
// Output: true
// Explanation: There is a valid loop (0 -> 2 -> 3 -> 0).
pub fn circular_array_loop(nums: Vec<i32>) -> bool {
"""

step_by_step_4 = """
// 1: Create a helper function "has_loop" to check if a loop exists starting from a given index.
// 2: In has_loop, we keep track of indices visited in the current path and indices visited in previous paths.
// 3: If we end up in an index that has been visited by previous paths, we can mark all indices in the current path as visited and return false.
// 4: If we end up in an index that has been visited by the current path, we check if the loop is valid by calling "is_valid_loop" and return true if it is.
// 5: The helper function "is_valid_loop" will:
//    - Extract the loop from the current path.
//    - Check if the loop has more than 2 elements and all elements have the same direction.
// 6: Call "has_loop" for each index in the array and return true if any of them returns true.
"""



problem_solution_4 = """
fn is_valid_loop(path: &Vec<usize>, nums: &Vec<i32>) -> bool {
    // Extract the loop from the current path.
    let mut rcycle = vec![];
    for (i, x) in path.iter().rev().enumerate() {
        rcycle.push(*x);
        if i > 0 && *x == rcycle[0] {
            break;
        }
    }
    // Check if the loop has more than 2 elements and all elements have the same direction.
    rcycle.len() > 2 && rcycle.iter().all(|x| nums[*x] * nums[rcycle[0]] > 0)
}

fn has_loop(start: usize, nums: &Vec<i32>, seen: &mut HashSet<usize>) -> bool {
    let mut path: Vec<usize> = vec![];
    let mut curr = start;
    let nums_len_i32 = nums.len() as i32;
    while !seen.contains(&curr) && !path.contains(&curr) {
        path.push(curr);
        curr = (((((curr as i32) + nums[curr]) % nums_len_i32) + nums_len_i32) % nums_len_i32)
            as usize;
    }
    path.push(curr);
    // If we end up in an index that has been visited by previous paths, we can mark all indices in the current path as visited and return false.
    // If the loop is not valid, we can mark all indices in the current path as visited and return false.
    if seen.contains(&curr) || !is_valid_loop(&path, nums) {
        seen.extend(path.iter());
        false
    } else {
        true
    }
}

pub fn circular_array_loop(nums: Vec<i32>) -> bool {
    let mut seen: HashSet<usize> = HashSet::new();
    (0..nums.len()).any(|x| has_loop(x, &nums, &mut seen))
}
"""

problem_statement_5 = """
// You are given an array of strings words and a string chars.
// A string is good if it can be formed by characters from chars (each character can only be used once).
// Return the sum of lengths of all good strings in words.
//
// Example:
// Input: words = ["cat","bt","hat","tree"], chars = "atach"
// Output: 6
// Explanation: The strings that can be formed are "cat" and "hat" so the answer is 3 + 3 = 6.
fn count_characters(words: Vec<String>, chars: String) -> i32 {
"""

step_by_step_5 = """
// 1: Create a helper function to check if a word can be formed from the characters in chars.
// 2: In the helper function, we keep track of the count of each character in chars.
// 3: We iterate through the characters in the word and decrement the count of each character in the map.
// 4: If the count of any character becomes negative, we return false.
// 5: If we reach the end of the word, we return true.
// 6: Iterate through the words and call the helper function for each word.
// 7: Return the sum of the lengths of the words for which the helper function returns true.
"""

problem_solution_5 = """
fn count_characters(words: Vec<String>, chars: String) -> i32 {
    fn can_form_word(word: &String, chars: &mut HashMap<char, i32>) -> bool {
        let mut char_count = chars.clone();
        for c in word.chars() {
            if let Some(count) = char_count.get_mut(&c) {
                *count -= 1;
                if *count < 0 {
                    return false;
                }
            } else {
                return false;
            }
        }
        true
    }

    let mut char_map: HashMap<char, i32> = HashMap::new();
    for c in chars.chars() {
        *char_map.entry(c).or_insert(0) += 1;
    }

    words
        .iter()
        .filter(|word| can_form_word(word, &mut char_map))
        .map(|word| word.len() as i32)
        .sum()
}
"""

problem_statement_6 = """
// In a visit to the goverment office you are informed that there are some documents that are not in the correct order.
// Some of the documents you need require other documents to be presented first.
// You suspect that it is impossible to present all the documents in the correct order.
// You are given a list of documents and their dependencies. You need to determine if it is possible to present all the documents in the correct order.
//
// The input is given as a list of tuples where each tuple contains two indices (a, b) representing that document a needs to be presented before document b.
// Return True if it is possible to present all the documents in the correct order, otherwise return False.
//
// Example:
// Input: [(1, 0), (0, 1)]
// Output: False
// Explanation: Document 1 needs to be presented before document 0 and document 0 needs to be presented before document 1. This is impossible.
fn can_present_documents(dependencies: Vec<(usize, usize)>, num_documents: usize) -> bool {
"""

step_by_step_6 = """
// 1: Create a helper function to check if there is a cycle in the dependencies graph.
// 2: The helper function will use depth-first search (DFS) to traverse the graph and detect cycles.
// 3: We will use a status array to keep track of the status of each document (Todo, InProgress, Done).
// 4: A cycle is detected if we find a document that is InProgress during the DFS traversal.
// 5: If we find a cycle, we return false. Otherwise, we return true.
"""

problem_solution_6 = """
#[derive(Copy, Clone)]
enum Status {
    Todo,
    InProgress,
    Done,
}

fn can_present_documents(dependencies: Vec<(usize, usize)>, num_documents: usize) -> bool {
    let mut graph = vec![Vec::new(); num_documents]; // Dependencies graph between documents.
    for edge in dependencies.iter() {
        graph[edge.0].push(edge.1);
    }

    let mut status = vec![Status::Todo; num_documents];
    (0..num_documents).all(|doc| !has_cycle(doc, &mut status, &graph))
}

// Helper function to detect cycles in the dependencies graph.
fn has_cycle(doc: usize, status: &mut Vec<Status>, graph: &Vec<Vec<usize>>) -> bool {
    match status[doc] {
        Status::Done => false,
        Status::InProgress => true, // Cycle detected.
        _ => {
            // Mark the current document as InProgress and continue the DFS traversal.
            status[doc] = Status::InProgress;
            if graph[doc]
                .iter()
                .any(|&next_doc| has_cycle(next_doc, status, graph))
            {
                return true;
            }
            // Mark the current document as Done after the DFS traversal.
            status[doc] = Status::Done;
            false
        }
    }
}
"""

problem_statement_7 = """
/// Find the next number bigger than n that is divisible by 7 but not by 2.
/// >>> next_divisible_by_7_not_2(14)
/// 21
/// >>> next_divisible_by_7_not_2(20)
/// 21
/// >>> next_divisible_by_7_not_2(21)
/// 35
/// >>> next_divisible_by_7_not_2(28)
/// 35
fn next_divisible_by_7_not_2(n: isize) -> isize {
"""

step_by_step_7 = """
// Step 1: Start with the next number after n.
// Step 2: Check if the number is divisible by 7 and not by 2.
// Step 3: If it is, return the number. Otherwise, increment the number and repeat from step 2.
"""

problem_solution_7 = """
fn next_divisible_by_7_not_2(n: isize) -> isize {
    let mut candidate = n + 1;
    while candidate % 7 != 0 || candidate % 2 == 0 {
        candidate += 1;
    }
    candidate
}
"""

problem_statement_8 = """
/// Given a vector of integers, return a vector of the elements that are divisible by 3, sorted in decreasing order.
/// 
/// Examples:
/// assert_eq!(elements_divisible_by_3_desc(vec![3, 6, 9, 12, 15, 1, 2]), vec![15, 12, 9, 6, 3]);
/// assert_eq!(elements_divisible_by_3_desc(vec![5, 7, 11]), vec![]);
/// assert_eq!(elements_divisible_by_3_desc(vec![9, 8, 3, 6]), vec![9, 6, 3]);
fn elements_divisible_by_3_desc(input_list: Vec<i32>) -> Vec<i32> {
"""

step_by_step_8 = """
// Step 1: Filter the elements in the input vector that are divisible by 3.
// Step 2: Sort the filtered elements in decreasing order.
// Step 3: Return the sorted vector.
"""

problem_solution_8 = """
fn elements_divisible_by_3_desc(input_list: Vec<i32>) -> Vec<i32> {
    let mut divisible_by_3: Vec<i32> = input_list.into_iter().filter(|&x| x % 3 == 0).collect();
    divisible_by_3.sort_by(|a, b| b.cmp(a)); // Sort in decreasing order
    divisible_by_3
}
"""


problem_statements_rs = [problem_statement_1, problem_statement_2, problem_statement_7, problem_statement_8, problem_statement_3, problem_statement_4, problem_statement_5, problem_statement_6]
step_by_steps_rs = [step_by_step_1, step_by_step_2, step_by_step_7, step_by_step_8, step_by_step_3, step_by_step_4, step_by_step_5, step_by_step_6]
problem_solutions_rs = [problem_solution_1, problem_solution_2, problem_solution_7, problem_solution_8, problem_solution_3, problem_solution_4, problem_solution_5, problem_solution_6]

###

ITERATIVE_PROMPT_RS = """
To this problem:

{prompt}

The solution provided:

{solution}

Fails with this message:

{message}

Please provide a better solution.
Remeber to write any reasoning as a comment. Remeber to import any needed module.
Do not write a main function to test the solution.
"""