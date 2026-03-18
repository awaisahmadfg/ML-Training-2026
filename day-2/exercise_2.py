from __future__ import annotations

from typing import Dict, List


def calculate_average(scores: List[float]) -> float:
    if not scores:
        raise ValueError("scores list must not be empty")
    return sum(scores) / len(scores)


def get_grade(avg: float) -> str:
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def class_topper(students: List[Dict]) -> Dict:
    # topper = student with max average; tie -> first seen in original order
    best = None
    best_avg = float("-inf")
    for s in students:
        avg = calculate_average(s["scores"])
        if avg > best_avg:
            best_avg = avg
            best = s
    return best

def build_report(students: List[Dict]) -> List[str]:
    topper = class_topper(students)

    # Sort by average descending WITHOUT modifying original list.
    # We compute avg inline in the key function.
    sorted_students = sorted(
        students, key=lambda s: calculate_average(s["scores"]), reverse=True
    )

    report_lines: List[str] = []
    for s in sorted_students:
        avg = calculate_average(s["scores"])
        grade = get_grade(avg)
        top_marker = " *** TOP ***" if s is topper else ""
        report_lines.append(f"{s['name']} | {avg:.2f} | {grade}{top_marker}")

    return report_lines


def main() -> None:
    students: List[Dict] = [
        {"name": "Awais", "scores": [88, 92, 85], "subject": "Python"},
        {"name": "Sara", "scores": [75, 80, 70], "subject": "Python"},
        {"name": "Hassan", "scores": [95, 90, 92], "subject": "Python"},
        {"name": "Zain", "scores": [60, 65, 58], "subject": "Python"},
        {"name": "Mariam", "scores": [82, 78, 85], "subject": "Python"},
    ]

    print("Class Grade Report")
    print("-------------------")
    for line in build_report(students):
        print(line)


if __name__ == "__main__":
    main()

