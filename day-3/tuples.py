"""
tuples.py

Learn Python Tuples (immutable).

Covers:
- Creating tuples
- Indexing and slicing
- Tuple unpacking
- Returning multiple values
- Using tuples as dict keys
- enumerate() and zip()
"""

from __future__ import annotations


def demo_tuples() -> None:
    point = (10, 20)
    rgb = (255, 100, 50)

    print("point:", point)
    print("point[0]:", point[0])
    print("point[-1]:", point[-1])
    print("point[0:2]:", point[0:2])

    # Tuples are immutable: you can't change point[0]
    # point[0] = 99  # <- would raise an error

    # Loop through tuple values
    for x in point:
        print("value:", x)


def demo_tuple_unpacking() -> None:
    a, b = (1, 2)
    print("unpacked a, b:", a, b)

    # Using "_" when you don't care about a value
    x, _ = (50, 999)
    print("x (ignoring second):", x)


def return_multiple_values() -> tuple[int, int]:
    # Common pattern: return multiple related values as a tuple
    return (3, 7)


def demo_dict_with_tuple_key() -> None:
    # Tuples can be used as keys if they are immutable.
    # Example: (row, col) -> value
    grid_value = {
        (0, 1): "A",
        (1, 1): "B",
    }
    print("grid_value[(0,1)]:", grid_value[(0, 1)])


def demo_enumerate_and_zip() -> None:
    names = ["Ada", "Bob", "Cory"]
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name}")

    # zip() combines two lists element-by-element
    nums = [10, 20, 30]
    pairs = list(zip(names, nums))  # [("Ada",10), ("Bob",20), ...]
    print("zip(names, nums):", pairs)


def main() -> None:
    demo_tuples()
    print("-" * 40)
    demo_tuple_unpacking()
    print("-" * 40)

    x, y = return_multiple_values()
    print("return_multiple_values():", (x, y))

    print("-" * 40)
    demo_dict_with_tuple_key()

    print("-" * 40)
    demo_enumerate_and_zip()

if __name__ == "__main__":
    main()

