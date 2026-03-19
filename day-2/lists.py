"""
lists.py

Learn Python Lists (lists).

Covers:
- Creating lists
- Indexing and slicing
- Mutating lists (append/extend/insert/remove/pop)
- Sorting
- Looping and list comprehensions


Real Project Example
Scenario: Notifications system
    notifications = ["msg1", "msg2"]
-> New single notification:
        notifications.append("msg3")
-> Bulk notifications from API:
        notifications.extend(["msg4", "msg5"])
-> Important notification at top:
        notifications.insert(0, "URGENT")
"""

def demo_basic_lists() -> None:
    nums = [10, 20, 30]
    fruits = ["apple", "banana", "cherry"]

    print("nums:", nums)
    print("nums[0]:", nums[0])     # 10
    print("nums[-1]:", nums[-1])   # 30

    # Slicing: start inclusive, end exclusive
    print("nums[0:2]:", nums[0:2]) # [10, 20]
    print("nums[1:]:", nums[1:])   # [20, 30]
    print("nums[:2]:", nums[:2])   # [10, 20]
    print("nums[::2]:", nums[::2]) # step -> [10, 30]

    # Mutations
    nums.append(40)
    print("after append(40):", nums)

    nums.extend([50, 60])
    print("after extend([50,60]):", nums)

    nums.insert(0, 5)
    print("after insert(0,5):", nums)

    nums.remove(20)  # removes first matching value
    print("after remove(20):", nums)

    last = nums.pop()  # removes last element and returns it
    print("popped:", last)
    print("after pop:", nums)

    # Sorting
    a = [3, 1, 4, 1, 5]
    a.sort()  # in-place
    print("sorted in place:", a)

    b = [3, 2, 9, 1]
    b2 = sorted(b)  # returns a NEW list
    print("sorted() new list:", b2)
    print("original unchanged:", b)


def list_comprehensions_demo() -> None:
    nums = [1, 2, 3, 4]
    squares = [n * n for n in nums]
    print("squares:", squares)

    mixed = [1, 2, 3, 4, 5, 6]
    evens = [n for n in mixed if n % 2 == 0]
    print("evens:", evens)


def chunk(lst: list[int], size: int) -> list[list[int]]:
    """
    Split lst into chunks of length `size`.
    Example: chunk([1,2,3,4,5], 2) -> [[1,2],[3,4],[5]]
    """
    if size <= 0:
        raise ValueError("size must be > 0")

    chunks: list[list[int]] = []
    for i in range(0, len(lst), size):
        chunks.append(lst[i : i + size])
    return chunks


def flatten_one_level(nested: list[list[int]]) -> list[int]:
    """Flatten one level: [[1,2],[3]] -> [1,2,3]."""
    out: list[int] = []
    for inner in nested:
        out.extend(inner)
    return out


def main() -> None:
    demo_basic_lists()
    print("-" * 40)
    list_comprehensions_demo()
    print("-" * 40)

    print("chunk([1,2,3,4,5], 2):", chunk([1, 2, 3, 4, 5], 2))
    nested = [[1, 2], [3], [4, 5, 6]]
    print("flatten_one_level:", flatten_one_level(nested))

if __name__ == "__main__":
    main()

