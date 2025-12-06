"""
GradeBook Analyzer
NAME: PRIYANSHI
DATE:6/12/2025
"""

import csv

# -- Task 3: statistical functions --

def calculate_average(marks_dict):
    scores = list(marks_dict.values())
    if not scores:
        return 0
    return sum(scores) / len(scores)

def calculate_median(marks_dict):
    scores = sorted(marks_dict.values())
    n = len(scores)
    if n == 0:
        return 0
    mid = n // 2
    if n % 2 == 1:
        return scores[mid]
    else:
        return (scores[mid - 1] + scores[mid]) / 2

def find_max_score(marks_dict):
    if not marks_dict:
        return None, None
    name = max(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

def find_min_score(marks_dict):
    if not marks_dict:
        return None, None
    name = min(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]



# -- Task 2: input methods --

def manual_entry():
    marks = {}
    print("Enter student data (blank name to stop).")
    while True:
        name = input("Student name (or press Enter to finish): ").strip()
        if name == "":
            break
        score_str = input(f"Marks for {name}: ")
        try:
            score = float(score_str)
            if score < 0 or score > 100:
                print("Marks must be between 0 and 100. Try again.")
                continue
        except ValueError:
            print("Invalid marks, try again.")
            continue
        marks[name] = score
    return marks

def load_from_csv(filename):
    marks = {}
    try:
        with open(filename, newline="", encoding='utf-8') as f:
            reader = csv.reader(f)
            # if file has header, uncomment the next line:
            # next(reader, None)
            for row_num, row in enumerate(reader, 1):
                if len(row) < 2:
                    print(f"Skipping row {row_num}: insufficient columns")
                    continue
                name = row[0].strip()
                if not name:
                    print(f"Skipping row {row_num}: empty name")
                    continue
                try:
                    score = float(row[1])
                    if score < 0 or score > 100:
                        print(f"Skipping row {row_num}: score {score} out of range")
                        continue
                except ValueError:
                    print(f"Skipping row {row_num}: invalid score '{row[1]}'")
                    continue
                marks[name] = score
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return {}
    return marks
# -- Task 4: grade assignment --

def assign_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def build_grades_dict(marks_dict):
    grades = {}
    for name, score in marks_dict.items():
        grades[name] = assign_grade(score)
    return grades

def grade_distribution(grades_dict):
    dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for g in grades_dict.values():
        if g in dist:
            dist[g] += 1
    return dist

# -- Task 5: pass / fail using list comprehension --

def get_pass_fail_lists(marks_dict):
    passed_students = [name for name, score in marks_dict.items() if score >= 40]
    failed_students = [name for name, score in marks_dict.items() if score < 40]
    return passed_students, failed_students

# -- Task 6: table printing --

def print_results_table(marks_dict, grades_dict):
    print("\nName".ljust(15) + "Marks".ljust(8) + "Grade")
    print("-" * 30)
    for name, score in sorted(marks_dict.items()):
        grade = grades_dict.get(name, "-")
        print(f"{name[:12]:<12} {score:>6.1f}  {grade}")

# -- Task 1 & 6: CLI loop --

def main():
    print("===== GradeBook Analyzer =====")
    while True:
        print("\n1. Manual entry")
        print("2. Load from CSV")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "3":
            print("Goodbye!")
            break

        if choice == "1":
            marks = manual_entry()
        elif choice == "2":
            filename = input("Enter CSV filename (with path if needed): ").strip()
            if not filename:
                print("No filename provided.")
                continue
            marks = load_from_csv(filename)
        else:
            print("Invalid option, try again.")
            continue

        if not marks:
            print("No valid student data found.")
            continue

        # -- Task 3: statistics --
        avg = calculate_average(marks)
        med = calculate_median(marks)
        max_name, max_score = find_max_score(marks)
        min_name, min_score = find_min_score(marks)

        print("\n--- Statistical Summary ---")
        print(f"Average score: {avg:.2f}")
        print(f"Median score:  {med:.2f}")
        print(f"Highest score: {max_score} ({max_name})")
        print(f"Lowest score:  {min_score} ({min_name})")

        # -- Task 4: grades & distribution --
        grades = build_grades_dict(marks)
        dist = grade_distribution(grades)

        print("\n--- Grade Distribution ---")
        for g, count in sorted(dist.items()):
            print(f"{g}: {count} student(s)")

        # -- Task 5: pass / fail --
        passed, failed = get_pass_fail_lists(marks)
        print("\n--- Pass / Fail ---")
        print(f"Passed ({len(passed)}): {', '.join(passed) if passed else 'None'}")
        print(f"Failed ({len(failed)}): {', '.join(failed) if failed else 'None'}")

        # -- Task 6: table --
        print_results_table(marks, grades)

if __name__ == "__main__":
    main()
