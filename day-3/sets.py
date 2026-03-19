"""
sets.py

Learn Python Sets (unique items).

Covers:
- Creating sets
- Membership with `in`
- add/remove/discard
- set operations (union/intersection/difference/symmetric difference)
- set comprehensions
"""

from __future__ import annotations


def demo_sets_basics() -> None:
    nums = {1, 2, 3}
    letters = {"a", "b", "c", "a"}  # duplicates are removed automatically

    print("nums set:", nums)
    print("letters set:", letters)

    print("2 in nums?", 2 in nums)
    print("5 in nums?", 5 in nums)

    nums.add(10)
    print("after add(10):", nums)

    # remove() raises an error if missing
    # nums.remove(999)
    # discard() does not raise an error if missing
    nums.discard(999)
    print("after discard(999):", nums)

    nums.remove(1)
    print("after remove(1):", nums)


def demo_set_operations() -> None:
    a = {1, 2, 3, 4}
    b = {3, 4, 5}

    print("a:", a)
    print("b:", b)

    print("union (a | b):", a | b)                 # all unique items
    print("intersection (a & b):", a & b)          # common items
    print("difference (a - b):", a - b)           # items only in a
    print("sym diff (a ^ b):", a ^ b)              # in one but not both


def demo_deduping_with_set() -> None:
    # Remove duplicates while ignoring order (sets don't keep order reliably)
    raw = [1, 2, 2, 3, 3, 4]
    unique = set(raw)
    print("raw:", raw)
    print("unique via set(raw):", unique)


def demo_set_comprehension() -> None:
    nums = [1, 2, 3, 4, 5]
    squares = {n * n for n in nums}
    print("squares set:", squares)


def main() -> None:
    demo_sets_basics()
    print("-" * 40)
    demo_set_operations()
    print("-" * 40)
    demo_deduping_with_set()
    print("-" * 40)
    demo_set_comprehension()

if __name__ == "__main__":
    main()

