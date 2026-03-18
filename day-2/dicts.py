"""
dicts.py

Learn Python Dictionaries.

Covers:
- Creating dictionaries
- Accessing values (d[key] vs d.get(key))
- Updating/adding keys
- Membership with `in`
- Iterating items
- Building dictionaries with comprehensions
"""


def demo_dict_basics() -> None:
    person = {"name": "Ada", "age": 36, "role": "engineer"}

    print("person:", person)

    # Access
    print("name:", person["name"])

    # Safe access with get()
    print("country (missing):", person.get("country"))
    print("country (default):", person.get("country", "Unknown"))

    # Update
    person["age"] = 37
    person["country"] = "UK"
    print("after updates:", person)

    # Membership
    print("'role' in person:", "role" in person)
    print("'salary' in person:", "salary" in person)

    # Iteration
    print("keys:", list(person.keys()))
    print("values:", list(person.values()))
    print("items:", list(person.items()))


def count_words(words: list[str]) -> dict[str, int]:
    """Count word frequencies."""
    counts: dict[str, int] = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts


def invert_dict(d: dict[str, int]) -> dict[int, str]:
    """
    Invert dictionary values -> keys.
    Assumes values are unique.
    Example: {"a": 1, "b": 2} -> {1: "a", 2: "b"}
    """
    out: dict[int, str] = {}
    for k, v in d.items():
        out[v] = k
    return out


def demo_dict_comprehension() -> None:
    nums = [1, 2, 3, 4]
    squares = {n: n * n for n in nums}
    print("squares:", squares)


def main() -> None:
    demo_dict_basics()
    print("-" * 40)

    words = ["to", "be", "or", "not", "to", "be"]
    print("count_words:", count_words(words))

    print("invert_dict:", invert_dict({"a": 1, "b": 2}))

    print("-" * 40)
    demo_dict_comprehension()

    # Practice prompts:
    # 1) Given list of tuples like [("a", 10), ("b", 20)], build a dict.
    # 2) Merge two dictionaries: right dict overwrites left.
    # 3) Group items by a key (dict of lists).


if __name__ == "__main__":
    main()

