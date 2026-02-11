

class Node:
    def __init__(self, puzzle, g_cost, h_cost, parent=None):
        self.puzzle = puzzle
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent
        

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
        

if __name__ == "__main__":
    main()