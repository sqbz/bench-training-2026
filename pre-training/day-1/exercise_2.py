def grade_classifier(score: int) -> str:
    if score >= 90:
        return "Distinction"
    if score >= 60:
        return "Pass"
    return "Fail"


test_values = [0, 59, 60, 89, 90]
for value in test_values:
    print(value, "->", grade_classifier(value))


scores = [45, 72, 91, 60, 38, 85]
for score in scores:
    print(score, "->", grade_classifier(score))

