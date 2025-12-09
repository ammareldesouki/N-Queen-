# imperative.py
# Imperative-style solver that uses mutable state during backtracking.

N = 8

def solve_imperative():
    solutions = []
    cols = [-1] * N  # cols[row] = col index or -1

    def is_safe(row, col):
        for r in range(row):
            c = cols[r]
            if c == col: return False
            if abs(c - col) == abs(r - row): return False
        return True

    def backtrack(row=0):
        if row == N:
            solutions.append(tuple(cols))
            return
        for c in range(N):
            if is_safe(row, c):
                cols[row] = c
                backtrack(row + 1)
                cols[row] = -1  # undo (mutable state)
    backtrack()
    return solutions

if __name__ == "__main__":
    sols = solve_imperative()
    print(f"Found {len(sols)} solutions for N={N}")
    for s in sols[:3]:
        print(s)
