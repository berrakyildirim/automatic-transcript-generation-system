#  Automatic Transcript Generation System (Team B)

A Python-based transcript simulation and generation system that creates academic transcripts in both CSV and HTML formats.
It models students’ semester-by-semester progress according to departmental curricula, applying realistic rules such as prerequisite control, credit limits, course retakes, and GPA/CGPA calculations.

# Team Members
Name	Student	Main Contributions
Damla Yıldız	Project integration, command-line argument management, GPA/CGPA logic, report writing
Berrak Yıldırım	Advanced functions, prerequisite control, test and error management
İhsan Efe Yücel	Project planning, database design, main module development
Hande Sağlam	HTML formatter module, user interface, and visual design

## Project Overview

This system automatically generates academic transcripts for students by:

Simulating academic progress over up to 14 semesters,

Assigning grades and calculating GPA/CGPA,

Enforcing prerequisites and credit limits,

Producing output files in CSV and formatted HTML.

It supports multiple departments (CS, ASE, EEE) and multiple curriculum versions (v1, v2, v3).

## Software Architecture

The project is divided into two main Python modules:

main.py

Processes command-line arguments (--student, --department, or --all)

Loads student and curriculum data from CSV files

Simulates each semester, assigns grades, computes GPA/CGPA

Exports transcript results to CSV files

html_formater.py

Reads all generated transcript CSVs

Sorts and formats courses by semester

Produces visually clean HTML transcripts for each student

## File Structure
transcript_project/

│

├── main.py

├── html_formater.py

├── student_transcripts/        # CSV transcript outputs

├── html_transcripts/           # Formatted HTML transcripts

├── updated_students_cs.csv

├── updated_students_eee.csv

├── updated_students_ase.csv

├── cs_curriculum_v1.csv

├── cs_curriculum_v2.csv

├── cs_curriculum_v3.csv

└── ...

## Running the Program
### Prerequisites

Python 3.10+

Required libraries installed (e.g., argparse, pandas)

## Usage

Run the following commands in the terminal from the project directory:

### For a specific student
python main.py --student <student_id>

### For all students in a specific department
python main.py --department <CS | ASE | EEE>

### For all students in all departments
python main.py --all


### After execution, the system:

Creates CSV transcripts under student_transcripts/

Automatically converts them into HTML transcripts under html_transcripts/

## System Testing

The system was tested across:

3 departments (CS, ASE, EEE)

3 curriculum versions each (v1, v2, v3)

Randomized student profiles and academic data

## Verification Criteria:

Prerequisite and credit limit enforcement

GPA/CGPA accuracy

Correct semester sequencing

Proper HTML formatting

Error handling for invalid data or missing files

## Future Improvements

Add PDF transcript export

Develop a web interface for online transcript viewing

Integrate data analytics for academic performance trends

Improve grade assignment logic with weighted success models

## Conclusion

This project successfully models a realistic academic transcript generation system.
It demonstrates strong modularity, scalability across departments, and compliance with academic standards for GPA/CGPA computation and prerequisite validation.

Developed Damla Yıldız, Berrak Yıldırım, İhsan Efe Yücel, and Hande Sağlam
