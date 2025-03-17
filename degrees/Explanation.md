# Explanation of the Implementation

Our goal was to write a function that finds the shortest path between a source actor and a target actor. The function `shortest_path` implements this using a Breadth-First Search (BFS) algorithm.

## Choice of Search Algorithm

Since the problem is an uninformed search problem, we can choose between Depth-First Search (DFS) and Breadth-First Search (BFS). For finding the shortest path, **BFS** is generally preferred because it explores all nodes at the current depth before moving to the next level. This guarantees that when the target is found, the path is the shortest possible.

## The `shortest_path` function Implementation

The code starts by creating a node for the source actor. This node is built using a Node class that stores the current actor’s state, a reference to its parent node, and the action (the movie) that connected it from its parent. Since the source is the starting point, its parent and action are set to None. A QueueFrontier is then initialized to perform a breadth-first search (BFS) and the source node is added to this frontier. A set named visited is also created to keep track of actors that have already been explored, preventing redundant work.

Inside the main loop, the algorithm removes a node from the frontier and marks its state (the actor) as visited. It then immediately checks if the current node’s actor matches the target. If it does, the code reconstructs the path by following the parent pointers from the target node back to the source. This path is built as a list of (movie_id, person_id) pairs, which is then reversed to display the connection from source to target. The code snippet that performs this reconstruction looks like this:

```python
if node.state == target:
    path = []
    while node.parent is not None:
        path.append((node.action, node.state))
        node = node.parent
    path.reverse()
    return path
```
If the current actor is not the target, the algorithm uses the neighbors_for_person function to fetch all neighbors, which returns pairs of (movie_id, person_id) for every actor who has appeared in a movie with the current actor. For each neighbor, the code checks whether that actor has already been visited or is present in the frontier. If not, a new Node is created with the neighbor’s actor ID, the current node as its parent, and the movie that connects them as the action. This new node is then added to the frontier for later exploration:
```python
for movie, person in neighbors_for_person(node.state):
    if person not in visited and not frontier.contains_state(person):
        child = Node(state=person, parent=node, action=movie)
        frontier.add(child)
```
For example, imagine Actor A (the source) has acted with Actor B in a movie, and Actor B has acted with Actor C (the target) in another movie. The function first adds Actor B to the frontier from Actor A. If Actor B is not the target, the algorithm then explores Actor B’s neighbors and finds Actor C. When Actor C is eventually reached, the algorithm backtracks from Actor C to Actor B and then to Actor A to construct the path that details which movie connects each pair of actors.

If no connection exists between the source and target, the frontier will eventually be empty and the function will return None. This ensures that the code either provides the shortest path between two actors or indicates that no such path exists.