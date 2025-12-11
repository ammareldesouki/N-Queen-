from typing import Tuple

N = 8

def safe(col: int, cols: Tuple[int, ...]) -> bool:

    def check(i: int) -> bool:
        if i == len(cols):
            return True

        cc = cols[i]
        r = len(cols)

        valid = (cc != col) and (abs(cc - col) != abs(i - r))
        return valid and check(i + 1)

    return check(0)


def extend_solutions(cols: Tuple[int, ...]) -> Tuple[Tuple[int, ...]]:
    if len(cols) == N:
        return [cols]

    def try_column(c: int) -> Tuple[Tuple[int, ...]]:
        if c == N:
            return []

        if safe(c, cols):
            placed = extend_solutions(cols + (c,))
            rest = try_column(c + 1)
            return placed + rest
        else:
            return try_column(c + 1)

    return try_column(0)



def all_solutions() -> Tuple[Tuple[int, ...]]:
    return extend_solutions(tuple())


def get_solutions():
    return all_solutions()



if __name__ == "__main__":
    sols = all_solutions()
    print(f"Found {len(sols)} solutions for N={N}")
    print(sols)
