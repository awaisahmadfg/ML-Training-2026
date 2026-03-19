"""
inheritance.py

Inheritance examples:
- Base class + derived class
- Overriding methods
- Calling base behavior
"""

from __future__ import annotations


class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        # ye default behavior hai jo child class override kar sakti hai
        return "..."


class Dog(Animal):
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)  # ye is liye use hora hai taake base class init ho jaye
        self.breed = breed

    def speak(self) -> str:
        return "woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "meow!"


def main() -> None:
    a = Animal("Some Animal")
    d = Dog("Rex", "Labrador")
    c = Cat("Mimi")

    print(a.name, "says", a.speak())
    print(d.name, "says", d.speak(), "| breed:", d.breed)
    print(c.name, "says", c.speak())


if __name__ == "__main__":
    main()

