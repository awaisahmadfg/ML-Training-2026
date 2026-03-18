def grade_classifier(score):
    if score >= 90:
        return "Distinction"
    elif score >= 60:
        return "Pass"
    else:
        return "Fail"


# Test
test_scores = [0, 59, 60, 89, 90, 100]
for s in test_scores:
    print(s, "->", grade_classifier(s))

print("\nClass results:")
scores = [45, 72, 91, 60, 38, 85]
for s in scores:
    print(s, "->", grade_classifier(s))



