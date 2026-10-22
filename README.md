# HealthWellness_Python

Project Title:
Health & Wellness Assistant (ZenTrack)
Authors:
- Liang Keze
- Tan Huey Sryan
- Chew Xian Nee

--------------------------------------------------
Project Description
--------------------------------------------------
This is a Python GUI-based Health & Wellness Assistant developed using Tkinter.
The system provides three main features:

1. Daily Wellness Log
   - Record daily sleep, meals, hydration, exercise, mood, and stress
   - View today’s entry and weekly summary
   - Save and load wellness records from text files

2. BMI & Calorie Calculator
   - Calculate BMI, BMR, and TDEE
   - Provide calorie recommendations
   - Save and view previous BMI records
3. Step Counter Log
   - Set daily step goals
   - Log steps manually
   - Display progress using a progress bar
   - Save step history persistently

--------------------------------------------------
System Requirements
--------------------------------------------------
- Python 3.9 or later
- Operating System: Windows (recommended)

--------------------------------------------------
Required Libraries
--------------------------------------------------
The program uses only standard Python libraries:

- tkinter
- tkinter.ttk
- tkinter.messagebox
- tkinter.simpledialog
- datetime
- os
- pathlib

No external libraries are required.

--------------------------------------------------
Files Used / Generated
--------------------------------------------------
The program will automatically create and use the following text files
in the same directory as the source code:

- wellness_records.txt   (Daily wellness data)
- bmi_records.txt        (BMI calculation records)
- step_records.txt       (Step counter history)
- step_goal.txt          (Daily step goal)

--------------------------------------------------
Notes
--------------------------------------------------
- The application opens in full-screen mode.
- All data is saved locally in text files.
- Ensure Icon.png is present in the same directory to avoid icon loading errors.

--------------------------------------------------
Academic Integrity
--------------------------------------------------
This project is an original work completed by the listed authors and
complies with academic integrity rules and regulations.
