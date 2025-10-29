
import pandas as pd
import random
import re
import os
import argparse
import subprocess


# Part 1: Command Line İnterface
parser = argparse.ArgumentParser(description="Transcript Generator")
group = parser.add_mutually_exclusive_group(required=True) #Needed in order to accept only one argument, required=True means at least one argument must be passsed
group.add_argument("--student", type=int) #student argument only accepted with an integer
group.add_argument("--department", type=str)#department argument only accepted with an integer
group.add_argument("--all", action="store_true")#sets a flag  if its written as argument it sets flag true else false
args = parser.parse_args() #sets given argument to args

# Part 2: Config
student_files = { #sets department argument meanings in a dict
    "CS": "updated_students_cs.csv",
    "ASE": "updated_students_ase.csv",
    "EEE": "updated_students_eee.csv"
}
letter_scores = { #sets grade meanings in a dict
    "AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5,
    "CC": 2.0, "DC": 1.5, "DD": 1.0,
    "FF": 0.0, "NA": 0.0, "EX": None
}
grade_letter_list = list(letter_scores.keys()) #returns dict keys "AA, BB,..." as a list

def extract_year(course_code): #sets year according to course_code
    num = int(str(course_code)[3:]) #according to ciriculumns in METU last 3 digit means the year that student supposed to take the course
    if num >= 400:
        return 4
    elif num >= 300:
        return 3
    elif num >= 200:
        return 2
    else:
        return 1

def clean_prereqs(s):
    if pd.isna(s):
        return ""
    comment_removed = re.sub(r'#.*', '', s) #remove commands

    splited_line = comment_removed.split(",")

    cleaned_parts = []
    for parts in splited_line:
        stripped_part = parts.strip()  # remove whitespaces
        if stripped_part.isdigit():  # keep digits
            cleaned_parts.append(stripped_part)

    result = ",".join(cleaned_parts)
    return result


# Part 3: Load Students
students_DF = pd.DataFrame()  # initiliaze data frame

if args.student:# load and concatenate all student files that exist
    all_students = []
    for f in student_files.values():
        if os.path.exists(f):
            data_frame = pd.read_csv(f)
            all_students.append(data_frame)

    all_students_DF = pd.concat(all_students, ignore_index=True) #reset row indexes of data frames as it concatenates them

    check_student = all_students_DF["student_id"] == args.student# create a boolean mask where student_id equals the target student
    selected_students_DF = all_students_DF[check_student]# use the mask to filter rows in the DataFrame

    students_DF = selected_students_DF

elif args.department:# get department from arg and try to load file by its name

    department_key = args.department.upper()
    student_department = student_files.get(department_key) #get correct filename from department key

    if os.path.exists(student_department):
        students_DF = pd.read_csv(student_department) #read file if exist
    else:
        students_DF = pd.DataFrame() #set empty dataframe

elif args.all:
    # load and concatenate all student files that exist
    all_students = []
    for f in student_files.values():
        if os.path.exists(f):
            data_frame = pd.read_csv(f)
            all_students.append(data_frame)

    students_DF = pd.concat(all_students, ignore_index=True)


if students_DF.empty:# check if students found
    print("No students found!")
    exit()


# Part 4: Process Each Student
for ignore, student in students_DF.iterrows():
    student_id = student["student_id"]
    student_name = student["name"]
    student_surname = student["surname"]
    student_DEP = student["department"]
    student_cirr_version = student["curriculum_version"].split("_")[-1] #takes last part after splitting
    valid_department = {
        "CS": "cs_curriculum",
        "ASE": "ase_curriculum",
        "EEE": "eee_curriculum"
    }
    if student_DEP not in valid_department:
        print("Invalid department:" + student_DEP)
        exit()
    valid_value = valid_department[student_DEP]
    curriculum_file = f"{valid_value}_{student_cirr_version}.csv" #creates correct filename

    if not os.path.exists(curriculum_file):
        print("Missing curriculum file!")
        continue

    comment_map = {}
    with open(curriculum_file, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"\s*(\d+);.*?#\s*(.*)", line)
            if match:
                course_code = int(match.group(1))
                comment = match.group(2).strip().strip(",")
                comment_map[course_code] = comment

    # Part 5: Load and prepare curriculum for each student
    data_frame = pd.read_csv(curriculum_file, sep=";", comment="#",
                             names=["course_code", "metu_credit", "ects_credit", "prerequisites", "description"],
                             dtype={"course_code": str})   #read csv file and seperate into tokens
    data_frame["course_code"] = data_frame["course_code"].str.strip() #handle whitespaces
    data_frame = data_frame[data_frame["course_code"].str.isdigit()] #valids if course code consists digits
    data_frame["course_code"] = data_frame["course_code"].astype(int) #cobnverts string to int
    data_frame["year"] = data_frame["course_code"].apply(extract_year) #sets year of course to take in df
    data_frame["prerequisites"] = data_frame["prerequisites"].apply(clean_prereqs)#sets prereqs of course to take in df
    data_frame["credit"] = data_frame["metu_credit"].str.extract(r"(\d+)").astype(float)#dses regex (\d+) to extract the first digit in line.

    year_courses = []

    for year in range(1, 5):
        year_of_courses = data_frame[data_frame["year"] == year]#create a boolean for rows in data frame

        courses_list = list(year_of_courses.itertuples(index=False)) #create a list of named tuples without index from filtered rows
        year_courses.append(courses_list) # add course list  for this year to the year_courses list
    passed = set()
    failed = []
    not_taken = []
    records = []

    year_count = 0
    extra_year = 5
    semester_count = 0
    MAX_SEMESTERS = 14 #max 7 years
    escape_loop = False

    while (year_count < 4 or failed or not_taken) and not escape_loop:
        for season in ["Fall", "Spring"]: #loop twice for each year
            if year_count < 4:
                semester = f"{year_count+1}_{season}"
            else:
                semester = f"{extra_year}_{season}"
            semester_records = []
            semester_credit = 0
            scheduled = []

            # Part 5.1: Retry failed courses
            retry = []
            for failed_course in failed[:]:
                course_row = data_frame[data_frame["course_code"] == failed_course] #filter df to get rows where course codes match the failed courses
                if not course_row.empty:
                    for ignore, course in course_row.iterrows():
                        credit = float(course["credit"])
                        if semester_credit + credit <= 21:
                            retry.append(course)
                            failed.remove(failed_course)
                            semester_credit += credit
                        break #only process first row


            # Part 5.2: Retry non-taken courses
            take_course = []
            not_take_course = []
            for course in not_taken:
                prereqs = []
                for prereq_course in course.prerequisites.split(","): #take prereq courses if multiple split with ","
                    if prereq_course:
                        prereqs.append(int(prereq_course))
                credit = float(course.credit)

                prereqs_satisfied = True
                for prereq_course in prereqs:
                    if prereq_course not in passed:
                        prereqs_satisfied = False
                        break
                if prereqs_satisfied and (semester_credit + credit) <= 21:
                    take_course.append(course)
                    semester_credit += credit
                else:
                    not_take_course.append(course)

            not_taken = not_take_course

            # Part 5.3: New courses from current year
            new_courses = []
            if year_count < 4:
                keep_courses = []
                for course in year_courses[year_count]:
                    code = course.course_code
                    if code in passed:
                        continue
                    prereqs = []
                    for prereq_course in course.prerequisites.split(","):  # take prereq courses if multiple split with ","
                        if prereq_course:
                            prereqs.append(int(prereq_course))
                    credit = float(course.credit)

                    prereqs_satisfied = True
                    for prereq_course in prereqs:
                        if prereq_course not in passed:
                            prereqs_satisfied = False
                            break
                    if prereqs_satisfied and (semester_credit + credit) <= 21:
                        new_courses.append(course)
                        semester_credit += credit
                    else:
                        exist_in_not_taken = False
                        for not_taken_course in not_taken:
                            if not_taken_course.course_code == code:
                                exist_in_not_taken = True
                                break

                        if code not in passed and not exist_in_not_taken: #avoid merge with non taken
                            not_taken.append(course)
                        else:
                            keep_courses.append(course)
                year_courses[year_count] = keep_courses

            # Part 6: Combine all scheduled
            scheduled = retry + take_course + new_courses

            for course in scheduled:
                code = course.course_code
                if float(course.credit) == 0:
                    grade = random.choices(["S", "U"], weights=[80, 20])[0] #make sure 0 credit courses only get S or U as letter grade

                else:
                    grade = random.choices(grade_letter_list, weights=[15, 13, 12, 10, 10, 8, 7, 5, 5, 5])[0]
                course_name = comment_map.get(code, "")  # fetch course name from map
                semester_records.append({
                    "student_id": student_id,
                    "name": student_name,
                    "surname": student_surname,
                    "department": student_DEP,
                    "semester": semester,
                    "course_code": code,
                    "course_name": course_name,
                    "grade": grade,
                    "credit": course.credit,
                    "prerequisites": course.prerequisites
                })
                if grade == "S":
                    passed.add(code)
                elif grade == "U":
                    failed.append(code)
                elif grade == "EX":
                    passed.add(code)
                elif grade in letter_scores and letter_scores[grade] is not None and letter_scores[grade] > 0:
                    passed.add(code)
                else:
                    failed.append(code)

            records.extend(semester_records)
            semester_count += 1
            if semester_count > MAX_SEMESTERS:
                print(f"Max semesters reached for student {student_id}!!!")
                escape_loop = True
                break

        if year_count < 4:
            year_count += 1
        else:
            extra_year += 1

    # Part 7: GPA/CGPA Calculation
    record_DF = pd.DataFrame(records)
    record_DF["grade_point"] = record_DF["grade"].map(letter_scores) #get letter grades int values
    record_DF["weighted_point"] = record_DF["grade_point"] * record_DF["credit"]

    final = []
    cumulative_credits = 0
    cumulative_points = 0

    sorted_DF = record_DF.sort_values(by=["semester"]) #sort record data frame in order of semester
    grouped_DF = sorted_DF.groupby("semester") #groups sorted record data frame  by semester
    for sem, group in grouped_DF:
        sem_credits = group["credit"].sum() #sum all credits from group
        sem_points = group["weighted_point"].sum() #sum all weighted_points from group

        if sem_credits != 0:
            gpa = round(sem_points / sem_credits, 2)
        else:
            gpa = 0

        cumulative_credits += sem_credits
        cumulative_points += sem_points

        if cumulative_credits != 0:
            cgpa = round(cumulative_points / cumulative_credits, 2)
        else:
            cgpa = 0

        for ignore, row in group.iterrows():
            row_dict = {**row.to_dict(), "GPA": gpa, "CGPA": cgpa} #unpacks row and add new items which are gpa and cgpa
            final.append(row_dict)

    # Part 8: Save Transcript
    output_dir = "student_transcripts"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"transcript_{student_id}.csv")
    pd.DataFrame(final).to_csv(file_path, index=False)
    print(f"* Transcript saved for student {student_id}")

# Part 7: Final Output
print("\nAll transcripts saved in: student_transcripts")
print("▶ Generating HTML transcripts...")
subprocess.run(["python", "html_formater.py"])

