# Explanation of the impelementation

Our task is to implement several functions to solve the crossword puzzle as a constraint satisfaction problem (CSP). The functions include **enforce_node_consistency**, **revise**, **ac3**, **assignment_complete**, **consistent**, **order_domain_values**, **select_unassigned_variable**, and **backtrack**.

## enforce_node_consistency
In enforce_node_consistency we must ensure that every variable’s domain contains only words that satisfy its unary constraints. In our crossword puzzle, the unary constraint is that the word’s length must match the variable’s length. Initially, the domain for each variable is set to the entire set of words. The function iterates over each variable in self.domains and, for each word (using a copy to avoid modifying the set during iteration), removes any word whose length does not equal the required length of the variable. 

## revise
The revise function is responsible for enforcing arc consistency between two variables, x and y. It does this by examining each word in x’s domain and checking whether there is at least one word in y’s domain that is compatible with it given the overlapping cell constraint. The overlap between x and y is retrieved from self.crossword.overlaps, which is either None or a tuple (i, j) indicating the overlapping indices in x and y, respectively. If no word in y’s domain has a matching letter at the overlapping position, then the word in x’s domain is removed. 

## ac3
The ac3 function uses a queue to enforce arc consistency for every pair of variables that share an overlap. If no specific arcs are provided, the function initializes a queue with all arcs (x, y), where x is any variable and y is one of its neighbors. For each arc removed from the queue, ac3 calls revise to prune x’s domain. If x’s domain becomes empty after revision, ac3 returns False because no valid assignment is possible. Otherwise, for every neighbor z of x (except y), the arc (z, x) is added back to the queue to re-check consistency. 
ac3 reduces domain for each variable makes each variable compatible with its neighbors (their overlapping letters will be the same), but this method does not necessarily provide the solution. 
In order to find solution we need to implement backtracking algorithm.

## backtrack

After applying arc consistency using `ac3`, we aim to find a complete assignment that satisfies all crossword constraints. This is done via the `backtrack` method, which implements a recursive **backtracking search** strategy. The method takes as input a partial assignment (initially empty) and attempts to build a full assignment by adding one variable at a time.

The first step in the method is to check if the assignment is already complete using the helper function `assignment_complete`. If it is, the solution is returned immediately:

```python
if self.assignment_complete(assignment):
    return assignment
```

If the assignment is not complete, we proceed to select a variable that has not yet been assigned. This is done using `select_unassigned_variable`, which helps reduce the search space by choosing the most constrained variable.

```python
var = self.select_unassigned_variable(assignment)
```

Once a variable is chosen, we retrieve an ordered list of its domain values using `order_domain_values`, which prioritizes values that eliminate the fewest options for neighboring variables:

```python
for value in self.order_domain_values(var, assignment):
```

For each value, we tentatively assign it to the variable and check whether this assignment is consistent with the rest of the current assignment using the `consistent` method:

```python
assignment[var] = value
if self.consistent(assignment):
```

If the assignment is consistent, we recursively call `backtrack` with the updated assignment. If the recursive call returns a result, we propagate it back:

```python
result = self.backtrack(assignment)
if result is not None:
    return result
```

If no valid assignment is found, we remove the current tentative assignment and try the next value:

```python
del assignment[var]
```

If no values lead to a solution, we return `None`, signaling that backtracking needs to continue from an earlier state.

---

## assignment_complete

This helper method checks whether a given assignment includes every variable in the crossword. It iterates through all variables and confirms that each one appears in the `assignment` dictionary.

```python
for var in self.domains:
    if var not in assignment:
        return False
return True
```

This method is used as the base case of the backtracking algorithm: once the assignment is complete, the search terminates with a valid solution.

---

## select_unassigned_variable

To improve efficiency, we don’t just select a random unassigned variable. Instead, we apply heuristics to make a smart choice. First, we define the unassigned variables as those not yet included in the assignment:

```python
unassigned = [var for var in self.domains if var not in assignment]
```

Then, we apply the **Minimum Remaining Values (MRV)** heuristic to choose the variable with the fewest legal values in its domain. If there's a tie, we use the **Degree Heuristic** as a tie-breaker — favoring the variable with the most constraints on other unassigned variables (i.e., most neighbors):

```python
return min(unassigned, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))
```

This choice increases the chances of early failure detection and more efficient pruning of the search tree.

---

## order_domain_values

Once we have a variable, the next question is: in which order should we try its possible values? To answer this, we use the **Least Constraining Value (LCV)** heuristic. The idea is to pick the value that rules out the fewest options for the neighbors, thus keeping future options more open.

We define a list to store how many values each candidate would eliminate:

```python
value_counts = []
```

Then, for each value in the domain of the selected variable:

```python
for value in self.domains[var]:
    elimination_count = 0
```

We check each unassigned neighbor and count how many values would be invalidated if we assigned this value to the current variable:

```python
for neighbor in self.crossword.neighbors(var):
    if neighbor not in assignment:
        overlap = self.crossword.overlaps.get((var, neighbor))
        if overlap is not None:
            i, j = overlap
            for neighbor_val in self.domains[neighbor]:
                if value[i] != neighbor_val[j]:
                    elimination_count += 1
```

After calculating the elimination count, we store the result:

```python
value_counts.append((value, elimination_count))
```

Finally, we sort the values in ascending order of elimination count and return them:

```python
value_counts.sort(key=lambda tup: tup[1])
return [value for value, count in value_counts]
```

This ensures that the value that is least likely to cause problems later is tried first.

---

## consistent

Before accepting a tentative assignment, we must ensure it is valid. The `consistent` method enforces three constraints:

1. **Length Constraint**: Each assigned word must match the length of its variable:

   ```python
   if len(word) != var.length:
       return False
   ```

2. **Unique Words**: No word should be reused across different variables:

   ```python
   words = list(assignment.values())
   if len(set(words)) != len(words):
       return False
   ```

3. **Overlapping Characters Must Match**: For each pair of neighboring variables with assigned values, the characters at the overlapping index must be equal:

   ```python
   for neighbor in self.crossword.neighbors(var):
       if neighbor in assignment:
           overlap = self.crossword.overlaps.get((var, neighbor))
           if overlap is not None:
               i, j = overlap
               if word[i] != assignment[neighbor][j]:
                   return False
   ```

If all these conditions are satisfied, the method returns `True`; otherwise, it returns `False`.