"""
functions.py

Learn Python Functions.

Covers:
- Defining functions with `def`
- Parameters and return values
- Default parameters
- *args and **kwargs
"""


# f use kerty ho taaky string k saath app variable use kersko: 
# Same kaam, lekin f wala clean aur easy hai ✅ For example: msg = "Hello, " + name
# Ager function call kerty waqt argument pass nahi karte to Python default value use kar leta hai
def greet(name: str, excited: bool = False) -> str:
    """Return a greeting string."""
    msg = f"Hello, {name}"
    if excited:
        msg += "!"
    return msg


def area_circle(radius: float) -> float:
    """Compute the area of a circle."""
    import math

    if radius < 0:
        raise ValueError("radius must be >= 0")
    return math.pi * radius * radius


def is_even(n: int) -> bool:
    """Return True if n is even."""
    return n % 2 == 0

# *nums = “jitne bhi values aayen, sab ko ek tuple mein pack kar do”
def sum_many(*nums: float) -> float:
    """
    Collect positional arguments into a tuple and sum them.
    sum_many(1,2,3) -> 6
    """
    total = 0.0
    for x in nums:
        total += x
    return total

# Ab ye function call kerty waqt isay value required hogi
def format_user(*, username: str, role: str = "user") -> str:
    """
    Keyword-only parameters.
    Example: format_user(username="alice", role="admin")
    """
    return f"{username} ({role})"

# Agar tum key + value pair bhejna chahte ho function me → hamesha **kwargs use karo
# Agar sirf values hain aur order matter karta hai → *args use karo
def merge_counts(**counts: int) -> dict[str, int]:
    """
    Collect keyword args into a dictionary.
    merge_counts(apples=3, bananas=7) -> {"apples":3,"bananas":7}
    """
    return dict(counts)


def main() -> None:
    print(greet("Ada"))
    print(greet("Ada", excited=True))

    print("area_circle(2):", area_circle(2))
    print("is_even(10):", is_even(10))
    print("is_even(7):", is_even(7))

    print("sum_many(1,2,3):", sum_many(1, 2, 3))
    print("sum_many():", sum_many())

    print(format_user(username="alice"))
    print(format_user(username="alice", role="admin"))

    print(merge_counts(apples=3, bananas=7))

if __name__ == "__main__":
    main()

