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

def solve_immutable(n):
    solutions = []

    def backtrack(row, cols_tuple):
        if row == n:
            solutions.append(tuple(cols_tuple))
            return
        for col in range(n):  # if you want, convert this loop too (left as loop for clarity)
            safe = is_safe(cols_tuple, row, col)
            if safe:
                backtrack(row + 1, cols_tuple + (col,))

    backtrack(0, ())
    return solutions

def is_safe(cols, row, col):
    # previous implementation used a for-loop over rows < row;
    # converted to recursion checking rows row-1, row-2, ..., 0
    def check(r):
        if r < 0:
            return True
        c = cols[r]
        if c == col or abs(c - col) == row - r:
            return False
        return check(r - 1)
    return check(row - 1)

if __name__ == "__main__":
    sols = solve_imperative()
    print(f"Found {len(sols)} solutions for N={N}")
    for s in sols[:3]:
        print(s)

    def show_current_solution(self):
        sol = self.solutions[self.current_index]

        # clear board (converted from nested loops to recursion)
        def clear_cell(r, c):
            if r >= self.n:
                return
            if c >= self.n:
                clear_cell(r+1, 0)
                return
            self.board[r][c].configure(bg='white')
            clear_cell(r, c+1)

        clear_cell(0, 0)

        # draw solution (converted from for/enumerate to recursion)
        def draw_row(i):
            if i >= len(sol):
                return
            r = i
            c = sol[i]
            self.board[r][c].configure(bg='black')
            draw_row(i+1)

        draw_row(0)
