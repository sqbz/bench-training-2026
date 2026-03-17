def calculate_average(scores):
    return sum(scores) / len(scores)


def get_grade(avg):
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def class_topper(students):
    topper = None
    best_avg = None
    for s in students:
        avg = calculate_average(s["scores"])
        if best_avg is None or avg > best_avg:
            best_avg = avg
            topper = s
    return topper


students = [
    {"name": "Ayesha", "scores": [88, 92, 81], "subject": "Math"},
    {"name": "Bilal", "scores": [65, 71, 69], "subject": "Math"},
    {"name": "Hassan", "scores": [94, 90, 96], "subject": "Math"},
    {"name": "Maryam", "scores": [78, 84, 80], "subject": "Math"},
    {"name": "Umar", "scores": [55, 60, 58], "subject": "Math"},
]

topper = class_topper(students)
sorted_students = sorted(students, key=lambda s: calculate_average(s["scores"]), reverse=True)

print("Name | Avg | Grade")
for s in sorted_students:
    avg = calculate_average(s["scores"])
    grade = get_grade(avg)
    line = f"{s['name']:<6} | {avg:>5.1f} | {grade}"
    if s is topper:
        line += " *** TOP ***"
    print(line)

