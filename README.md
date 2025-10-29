# Course Scheduler (Python)

A Python-based course scheduling system that helps students build personalized weekly timetables without time conflicts. The program reads course data from a file, checks for overlapping schedules, and displays a clean, formatted timetable in the console.

## Features

File Input: Automatically loads course information from a .txt file.

Conflict Detection: Prevents overlapping course times.

Dynamic Updates: Add or remove courses easily.

Timetable Visualization: Displays a clear weekday-hour table view.

User Interaction: Simple console-based interface.

## How It Works

The program reads all courses from a file (e.g., courses.txt).

The user selects which courses to add based on available slots.

Conflicting courses are automatically filtered out.

The final timetable and schedule are printed neatly at the end.

## Example Input File

courses.txt

EEE 445,1,9,11,Monday
CENG 213,2,11,13,Tuesday
MATH 241,1,10,12,Wednesday

## Example Output
Welcome to the course scheduler!

Available courses:
EEE 445 (Section 1) on Monday: 9:00-11:00
CENG 213 (Section 2) on Tuesday: 11:00-13:00
...

Final Timetable:
Hour  Monday              Tuesday             Wednesday          
8:00  Free                Free                Free
9:00  EEE 445 (Section 1) Free                Free
...

Final Schedule:
Day       Time                Course (Section)
----------------------------------------------
Monday    9:00 - 11:00        EEE 445 (Section 1)
Tuesday   11:00 - 13:00       CENG 213 (Section 2)

## File Structure
course_scheduler.py    # Main program file
courses.txt            # Input data file

## Author

Berrak Yıldırım, Part of a Team with İhsan Efe Yücel, Hande Sağlam and Damla Yıldız
