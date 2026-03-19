"""
classes_static_class.py

Classes examples:
- instance methods
- class variables
- @classmethod
- @staticmethod
"""

from __future__ import annotations


class Person:
    # class variable: har instance ke liye same hota hai
    species = "Homo sapiens"

    def __init__(self, name: str) -> None:
        self.name = name

    def greet(self) -> str:
        # instance method: instance ke data (self) use karta hai
        return f"Hi, I'm {self.name}"

    @classmethod
    def species_info(cls) -> str:
        # classmethod: class (cls) par depend karta hai, instance par nahi
        return f"Species is {cls.species}"

    @staticmethod
    def normalize_name(name: str) -> str:
        # staticmethod: self/cls ki zarurat nahi hoti (utility function jaisa)
        return " ".join(part.capitalize() for part in name.split())


def main() -> None:
    p1 = Person("coding cops")
    print(Person.species_info())
    print(p1.greet())
    print("Normalized:", Person.normalize_name("coding cOps"))


if __name__ == "__main__":
    main()

