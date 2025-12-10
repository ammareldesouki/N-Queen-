# functional.py
from typing import List, Tuple

N = 8

def safe(col: int, cols: Tuple[int,...]) -> bool:
    r = len(cols)
    return all(
        cc != col and abs(cc - col) != abs(rr - r)
        for rr, cc in enumerate(cols)
    )

def extend_solutions(cols: Tuple[int,...]) -> List[Tuple[int,...]]:
    if len(cols) == N:
        return [cols]
    return [
        solution
        for c in range(N)
        if safe(c, cols)
        for solution in extend_solutions(cols + (c,))
    ]

def all_solutions() -> List[Tuple[int,...]]:
    return extend_solutions(tuple())


def get_solutions():
    return all_solutions()

if __name__ == "__main__":
    sols = all_solutions()
    print(f"Found {len(sols)} solutions for N={N}")
    for s in sols[:3]:
        print(s)