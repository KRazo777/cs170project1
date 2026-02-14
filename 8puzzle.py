import heapq
import time

class Node:
    def __init__(self, puzzle, g_cost, h_cost, parent=None):
        self.puzzle = puzzle
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent
        
    def __lt__(self, other):
        # if f cost is same just go with node with lower h cost
        if self.f_cost == other.f_cost:
            return self.h_cost < other.h_cost
        
        return self.f_cost < other.f_cost

def misplaced_tile(puzzle):
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    
    count = 0
    for i in range(3):
        for j in range(3):
            val = puzzle[i][j]

            if val != 0 and val != goal[i][j]:
                count += 1
    return count

def manhattan_distance(puzzle):
    goal_positions = { 1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1) }

    dist = 0
    for i in range(3):
        for j in range(3):
            val = puzzle[i][j]
            if val != 0:
                goal_i, goal_j = goal_positions[val]
                dist += abs(i - goal_i) + abs(j - goal_j)
    return dist

def expand(puzzle):
    blank_i = -1
    blank_j = -1

    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                blank_i = i
                blank_j = j
                break
                
    children = []

    # up down left right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for di, dj in directions:
        new_i, new_j = blank_i + di, blank_j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            # copy the puzzle for the new state
            new_puzzle = [row[:] for row in puzzle]

            # Swap blank with target tile
            new_puzzle[blank_i][blank_j], new_puzzle[new_i][new_j] = new_puzzle[new_i][new_j], new_puzzle[blank_i][blank_j]
            children.append(new_puzzle)

    return children

def is_goal(puzzle):
    return puzzle == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def general_search(problem, heuristic_type):

    # in seconds, 5 mins but can adjust if needed
    timeLimit = 300
    startTime = time.time()

    initial_node = Node(problem, 0, 0)

    if heuristic_type == 2:
        initial_node.h_cost = misplaced_tile(problem)
    elif heuristic_type == 3:
        initial_node.h_cost = manhattan_distance(problem)
    
    working_queue = []
    heapq.heappush(working_queue, initial_node)
    
    explored = []
    
    num_expanded = 0
    max_queue_size = 0
    
    while working_queue:

        # make sure it doesnt run for too long on harder problems for uniform cost
        if time.time() - startTime > timeLimit:
            print("\nTime limit exceeded! Search cancelled.")
            return None, num_expanded, max_queue_size

        max_queue_size = max(max_queue_size, len(working_queue))
        current_node = heapq.heappop(working_queue)
        
        # check goal state
        if is_goal(current_node.puzzle):
            return current_node, num_expanded, max_queue_size
            
        num_expanded += 1
        
        explored.append(current_node.puzzle)
        
        for child_puzzle in expand(current_node.puzzle):
            if child_puzzle not in explored:
                g = current_node.g_cost + 1
                h = 0
                if heuristic_type == 2:
                    h = misplaced_tile(child_puzzle)
                elif heuristic_type == 3:
                    h = manhattan_distance(child_puzzle)
                    
                child_node = Node(child_puzzle, g, h, current_node)
                heapq.heappush(working_queue, child_node)
            
    return None, num_expanded, max_queue_size

def trace_solution(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]

def main():
    print("Welcome to the 8-Puzzle Solver")
    print("Type '1' to use a default puzzle, or '2' to enter your own puzzle")
    choice = input()
    
    if choice == '1':
        puzzle = [[1, 5, 2], [4, 3, 6], [7, 8, 0]]
    elif choice == '2':
        print("Enter your puzzle, use zero to represent the blank. Please only enter valid 8-puzzles.")
        print("Enter the puzzle demilimiting the numbers with a space. Type RETURN only when finished.")

        r1 = list(map(int, input("Enter the first row: ").split()))
        r2 = list(map(int, input("Enter the second row: ").split()))
        r3 = list(map(int, input("Enter the third row: ").split()))

        puzzle = [r1, r2, r3]

    else:
        print("Invalid choice.")
        return
        
    print("Select algorithm.")
    print("(1) for Uniform Cost Search, (2) for the Misplaced Tile Heuristic, or (3) the Manhattan Distance Heuristic.")
    choice = int(input())
    
    solution_node, expanded, max_q = general_search(puzzle, choice)
    
    if solution_node:
        path = trace_solution(solution_node)

        for step in path:
            print(f"The best state to expand with a g(n) = {step.g_cost} and h(n) = {step.h_cost} is")
            for row in step.puzzle:
                print(row)
            print()
            
        print("Goal state!")
        print("Solution depth was", solution_node.g_cost)
        print("Number of nodes expanded:", expanded)
        print("Max queue size:", max_q)
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()