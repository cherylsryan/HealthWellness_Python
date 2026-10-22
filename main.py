
"""
Health & Wellness Assistant
Feature - Daily Wellness Log, BMI & Calorie Calculator, Step Counter Log
Author : Liang Keze, Tan Huey Sryan, Chew Xian Nee
"""


import tkinter as tk
import datetime
import os
from pathlib import Path
from tkinter import simpledialog, ttk, messagebox


# ---------------- Main Background Colour ----------------
main_bg = "#F0F8FF"


# ---------------- Basic Health Module ----------------
class HealthModule:
    """
    All health modules (Wellness, BMI, Step Counter)
    Provides common functionalities like clearing screen and going back
    """
    def __init__(self, root, main_menu_callback=None):
        self.root = root
        self.main_menu_callback = main_menu_callback


    def clear_screen(self):
        # Remove all widgets from the root window
        for widget in self.root.winfo_children():
            widget.destroy()
    def back_to_main_menu(self):
        # Return to the main menu if callback provided
        if self.main_menu_callback:
            self.main_menu_callback()


# ---------------- Data ----------------
wellness_data = []      # Store daily wellness entries


# ---------------- Helper Functions ----------------
def validation(value, field_name, min_val=None, max_val=None, allow_float=False):
    value = value.strip()
    if value == "" or value.lower() == "none":
        return None  # allow empty
    try:
        num = float(value) if allow_float else int(value)
    except:
        messagebox.showerror("Input Error", f"{field_name} must be a number")
        return "ERROR"
    if min_val is not None and num < min_val:
        messagebox.showerror("Input Error", f"{field_name} must be ≥ {min_val}")
        return "ERROR"
    if max_val is not None and num > max_val:
        messagebox.showerror("Input Error", f"{field_name} must be ≤ {max_val}")
        return "ERROR"
    return num


def validate_text(value, field_name):
    # Validates that the input may be empty and does not contain any digits
    value = value.strip()
    if value == "":
        return None
    if any(char.isdigit() for char in value):
        messagebox.showerror("Input Error", f"{field_name} cannot contain numbers.")
        return "ERROR"
    return value


def is_entry_complete(entry):
    # Check if all required fields in the entry are filled
    required = ["sleep_hours","steps","water","mood","stress","exercise_type"]
    for field in required:
        if entry.get(field) in [None,"None",""]:
            return False
    return True


def save_to_file(filename="wellness_records.txt", show_msg=True):
    # Save all wellness entries to a text file
    with open(filename, "w", encoding="utf-8") as file:
        for entry in wellness_data:
            file.write(f"DATE: {entry.get('date','')}\n\n")
            file.write("Sleep:\n")
            file.write(f"  Sleep Hours: {entry.get('sleep_hours','None')}\n")
            file.write(f"  Sleep Quality: {entry.get('sleep_quality','None')}\n")
            file.write(f"  Dreams: {entry.get('dreams','None')}\n\n")
            file.write("Meals:\n")
            file.write(f"  Breakfast: {entry.get('breakfast','None')}\n")
            file.write(f"  Lunch: {entry.get('lunch','None')}\n")
            file.write(f"  Dinner: {entry.get('dinner','None')}\n")
            file.write(f"  Snacks: {entry.get('snacks','None')}\n\n")
            file.write("Hydration:\n")
            water_val = entry.get('water','None')
            file.write(f"  Water: {water_val}\n")
            file.write(f"  Juice: {entry.get('juice','None')}\n")
            file.write(f"  Caffeine: {entry.get('caffeine','None')}\n")
            file.write(f"  Alcohol: {entry.get('alcohol','None')}\n\n")
            file.write("Exercise:\n")
            file.write(f"  Type: {entry.get('exercise_type','None')}\n")
            file.write(f"  Duration: {entry.get('duration','None')}\n")
            file.write(f"  Intensity: {entry.get('intensity','None')}\n")
            file.write(f"  Feeling: {entry.get('feeling','None')}\n")
            file.write(f"  Steps: {entry.get('steps','None')}\n\n")
            file.write("Mood & Reflection:\n")
            file.write(f"  Mood: {entry.get('mood','None')}\n")
            file.write(f"  Stress: {entry.get('stress','None')}\n")
            file.write(f"  Reflection: {entry.get('reflection','None')}\n")
            file.write("-"*40 + "\n\n")
    if show_msg:
        messagebox.showinfo("Saved", f"All records saved to {filename}")


def load_from_file(filename="wellness_records.txt"):
    global wellness_data
    wellness_data = []


    if not os.path.exists(filename):
        return


    with open(filename, "r", encoding="utf-8") as file:
        content = file.read().split("-"*40)
        for block in content:
            block = block.strip()
            if not block:
                continue


            entry = {}
            lines = block.split("\n")
            for line in lines:
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip().lower().replace(" ", "_")
                    val = val.strip()
                    if val == "None" or val == "":
                        val = None
                    entry[key] = val
            if entry:
                wellness_data.append(entry)


# ---------------- Wellness Tracker GUI ----------------
class DailyWellnessLog(HealthModule):
    # GUI for Daily Wellness Tracker
    def __init__(self, root, main_menu_callback):
        super().__init__(root, main_menu_callback)
        self.root.configure(bg="#FFFFFF")
        self.root.title("Wellness Tracker")
        load_from_file()
        self.main_menu()


        # Font for labels and entries
        self.label_font = ("Helvetica", 16, "bold")
        self.entry_font = ("Helvetica", 16)
        self.button_font = ("Helvetica", 16, "bold")


    def clear_today_entry(self):
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        global wellness_data


        before = len(wellness_data)
        wellness_data = [e for e in wellness_data if e.get("date") != today]
        save_to_file(show_msg=False)


        if len(wellness_data) < before:
            messagebox.showinfo("Cleared", "Today's entry has been cleared.")
        else:
            messagebox.showinfo("Info", "No entry to clear for today.")
        self.main_menu()


    # --- Main menu inside wellness tracker ---
    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()


        tk.Label(self.root, text="Wellness Tracker", font=("Helvetica", 40, "bold"), bg="#FFFFFF").pack(pady=(55,30))


        btn_config = {"width":30, "height":2, "font":("Helvetica",18), "bg":"#000000", "fg":"white"}
        tk.Button(self.root, text="Add Today's Entry", command=self.add_entry_screen, **btn_config).pack(pady=10)
        tk.Button(self.root, text="View Today's Entry", command=self.view_today_screen, **btn_config).pack(pady=10)
        tk.Button(self.root, text="Weekly Summary", command=self.weekly_summary_screen, **btn_config).pack(pady=10)
        tk.Button(self.root, text="Save All Records", command=save_to_file, **btn_config).pack(pady=10)
        tk.Button(self.root, text="Back", width=30, height=2, font=("Helvetica", 18),
                  bg="#FF4500", fg="white", command=lambda: [self.root.title("Health & Wellness Assistant"),
                                                             self.back_to_main_menu()]).pack(pady=10)
        # Right side clear entry box
        right_frame = tk.Frame(self.root, bg="#ffcccc", width=250, height=150, bd=2, relief="ridge")
        right_frame.pack(side="right", padx=10, pady=20)  # Pack to right side
        right_frame.pack_propagate(False)


        tk.Label(right_frame, text="Clear Today's Entry", font=("Helvetica",16,"bold"), bg="#ffcccc").pack(pady=15)
        tk.Button(right_frame, text="Clear", width=12, height=2, font=("Helvetica",14), bg="white", fg="red", command=self.clear_today_entry).pack(pady=10)
       
    def back_to_main_menu(self):
        # Return to main Health & Wellness Menu
        self.main_menu_callback()


     # ---------------- Add Entry ----------------
    def add_entry_screen(self):
        """
        GUI for adding or updating daily wellness entry.
        Includes tabs: Sleep, Meals, Hydration, Exercise, Mood
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        tk.Label(self.root, text=f" Add Entry for {today}", font=("Helvetica", 26, "bold"), bg="#FFFFFF").pack(pady=15)


        # Check if today already exists
        existing_entry = next((e for e in wellness_data if e["date"]==today), None)
        if existing_entry:
            entry = existing_entry
            if is_entry_complete(existing_entry):
                messagebox.showinfo("Info", "Updating existing entry for today.")
        else:
            entry = {
                "date": today,
                "sleep_hours": None,
                "sleep_quality": None,
                "dreams": None,
                "breakfast": None,
                "lunch": None,
                "dinner": None,
                "snacks": None,
                "water": None,
                "juice": None,
                "caffeine": None,
                "alcohol": None,
                "exercise_type": None,
                "duration": None,
                "intensity": None,
                "feeling": None,
                "steps": None,
                "mood": None,
                "stress": None,
                "reflection": None
            }
            wellness_data.append(entry)
       
        # ---------------- Notebook Tabs ----------------
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")


        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=('Helvetica','14','bold'), padding=[10,8])


        # ---------------- Sleep Tab ----------------
        sleep_tab = tk.Frame(notebook, bg="#E6F2FF")
        notebook.add(sleep_tab, text="Sleep")


        # Variables
        sleep_hours_var = tk.StringVar(value=str(entry.get("sleep_hours") or ""))
        sleep_quality_var = tk.StringVar(value=str(entry.get("sleep_quality") or ""))
        dreams_var = tk.StringVar(value=str(entry.get("dreams") or ""))


        # Sleep Hours
        tk.Label(sleep_tab, text="Hours slept:", bg="#E6F2FF", font=self.label_font).pack(pady=8)
        tk.Entry(sleep_tab, textvariable=sleep_hours_var, font=self.entry_font, width=40, bg="#FFFFFF").pack(pady=5)


        # Sleep Quality dropdown 1-5
        tk.Label(sleep_tab, text="Sleep quality (1-5):", bg="#E6F2FF", font=self.label_font).pack(pady=8)
        sleep_quality_dropdown = ttk.Combobox(
            sleep_tab,
            textvariable=sleep_quality_var,
            values=[1, 2, 3, 4, 5],
            font=self.entry_font,
            width=10,
            state="readonly"  # ensures only selection, no typing
        )
        sleep_quality_dropdown.pack(pady=5)


        tk.Label(sleep_tab, text="Dreams? (Y/N):", bg="#E6F2FF", font=self.label_font).pack(pady=8)
        dreams_dropdown = ttk.Combobox(
            sleep_tab,
            textvariable=dreams_var,
            values=["Yes","No"],
            font=self.entry_font,
            width=10,
            state="readonly"
        )
        dreams_dropdown.pack(pady=5)


        # ---------------- Meals Tab ----------------
        meal_tab = tk.Frame(notebook, bg="#FFF0F5")
        notebook.add(meal_tab, text="Meals")


        # Variables
        breakfast_var = tk.StringVar(value=entry.get("breakfast") or "")
        lunch_var = tk.StringVar(value=entry.get("lunch") or "")
        dinner_var = tk.StringVar(value=entry.get("dinner") or "")
        snacks_var = tk.StringVar(value=entry.get("snacks") or "")


        for meal, var in [("Breakfast", breakfast_var), ("Lunch", lunch_var), ("Dinner", dinner_var), ("Snacks", snacks_var)]:
            tk.Label(meal_tab, text=f"{meal}:", bg="#FFF0F5", font=self.label_font).pack(pady=8)
            tk.Entry(meal_tab, textvariable=var, font=self.entry_font, width=40).pack(pady=5)


       # ---------------- Hydration Tab ----------------
        hyd_tab = tk.Frame(notebook, bg="#F0FFF0")
        notebook.add(hyd_tab, text= "Hydration")


        # Variables
        water_var = tk.StringVar(value=str(entry.get("water") or ""))
        juice_var = tk.StringVar(value=entry.get("juice") or "")
        caffeine_var = tk.StringVar(value=entry.get("caffeine") or "")
        alcohol_var = tk.StringVar(value=entry.get("alcohol") or "")


        for drink, var in [("Water glasses", water_var), ("Juice (glass)", juice_var), ("Caffeine drinks (glass)", caffeine_var), ("Alcohol drinks (glass)", alcohol_var)]:
            tk.Label(hyd_tab, text=f"{drink}:", bg="#F0FFF0", font=self.label_font).pack(pady=8)
            tk.Entry(hyd_tab, textvariable=var, font=self.entry_font, width=40, bg="#FFFFFF").pack(pady=5)


        # ---------------- Exercise Tab ----------------
        ex_tab = tk.Frame(notebook, bg="#FFF8DC")
        notebook.add(ex_tab, text="Exercise")


        # Variables
        ex_type_var = tk.StringVar(value=entry.get("exercise_type") or "")
        duration_var = tk.StringVar(value=str(entry.get("duration") or ""))
        intensity_var = tk.StringVar(value=entry.get("intensity") or "")
        feeling_var = tk.StringVar(value=entry.get("feeling") or "")
        steps_var = tk.StringVar(value=str(entry.get("steps") or ""))


        for label, var in [("Exercise Type:", ex_type_var),("Duration (min):", duration_var),("Intensity:", intensity_var),("Feeling:", feeling_var),("Steps:", steps_var)]:
            tk.Label(ex_tab, text=label, bg="#FFF8DC", font=self.label_font).pack(pady=8)
           
            if label == "Intensity":
                intensity_dropdown = ttk.Combobox(ex_tab, textvariable=var, values=["Light", "Medium", "Hard"], font=self.entry_font, width=40, state="readonly")
                intensity_dropdown.pack(pady=5)
            else:
                tk.Entry(ex_tab, textvariable=var, font=self.entry_font, width=40, bg="#FFFFFF").pack(pady=5)


       # ---------------- Mood Tab ----------------
        mood_tab = tk.Frame(notebook, bg="#FFE4E1")
        notebook.add(mood_tab, text="Mood")


        mood_var = tk.StringVar(value=str(entry.get("mood") or ""))
        stress_var = tk.StringVar(value=str(entry.get("stress") or ""))
        reflection_text = tk.Text(mood_tab, width=60, height=6, font=("Helvetica",16), bg="#ffffff")
        reflection_text.insert("1.0", entry.get("reflection") or "")


        # Mood dropdown 1-5
        tk.Label(mood_tab, text="Mood (1-5):", bg="#FFE4E1", font=self.label_font).pack(pady=8)
        mood_dropdown = ttk.Combobox(mood_tab, textvariable=mood_var, values=[1, 2, 3, 4, 5], font=self.entry_font, width=10,
        state="readonly"  # ensures only selection, no typing
        )
        mood_dropdown.pack(pady=5)


        # Stress dropdown 1-5 (change values to 1-10 if needed)
        tk.Label(mood_tab, text="Stress (1-10):", bg="#FFE4E1", font=self.label_font).pack(pady=8)
        stress_dropdown = ttk.Combobox(mood_tab, textvariable=stress_var, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], font=self.entry_font, width=10,
            state="readonly"  
        )
        stress_dropdown.pack(pady=5)


        tk.Label(mood_tab, text="Reflection:", bg="#FFE4E1", font=("Helvetica",16,"bold")).pack(pady=10)
        reflection_text.pack(pady=5)


        # ---------------- Save Button ----------------
        def save_all():
            # Sleep
            entry["sleep_hours"] = validation(sleep_hours_var.get(), "Sleep Hours", 0, 24, allow_float=True)
            entry["sleep_quality"] = sleep_quality_var.get() or "None"
            entry["dreams"] = dreams_var.get() or "None"
            # Meals
            entry["breakfast"] = validate_text(breakfast_var.get(), "Breakfast")
            entry["lunch"] = validate_text(lunch_var.get(), "Lunch")
            entry["dinner"] = validate_text(dinner_var.get(), "Dinner")
            entry["snacks"] = validate_text(snacks_var.get(), "Snacks")
            # Hydration
            entry["water"] = validation(water_var.get(), "Water", 0, 30)
            entry["juice"] = validation(juice_var.get(), "juice", 0, 30) or ""
            entry["caffeine"] = validation(caffeine_var.get(), "caffeine", 0, 30) or ""
            entry["alcohol"] = validation(alcohol_var.get(), "alcohol", 0, 30) or ""
            # Exercise
            entry["exercise_type"] = validate_text(ex_type_var.get(),"Exercise Type") or "None"
            entry["duration"] = validation(duration_var.get(), "Exercise Duration", 0, 30000)
            entry["steps"] = validation(steps_var.get(), "Steps", 0, 100000)
            entry["intensity"] = intensity_var.get() or "None"
            entry["feeling"] = validate_text(feeling_var.get(),"Feeling") or "None"
            # Mood
            entry["mood"] = mood_var.get()
            entry["stress"] = stress_var.get()
            entry["reflection"] = reflection_text.get("1.0","end").strip() or "None"
           
            if "ERROR" in entry.values():
                return


            if not is_entry_complete(entry):
                messagebox.showwarning("Warning","Some required fields may be missing.")


            save_to_file()
            self.main_menu()


        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text=" Save Entry", width=20, height=2, font=("Helvetica",16),
                  bg="#32cd32", fg="white", command=save_all).pack(side="left", padx=30)
        tk.Button(btn_frame, text=" Back", width=20, height=2, font=("Helvetica",16),
                  bg="#ff4500", fg="white", command=self.main_menu).pack(side="right", padx=30)


    # ---------------- View Today's Entry ----------------
    def view_today_screen(self):
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        today_entry = next((e for e in wellness_data if e.get("date") == today), None)


        if not today_entry:
            messagebox.showinfo("Info", "No entry for today.")
            return


        for widget in self.root.winfo_children():
            widget.destroy()


        tk.Label(
            self.root, text=f" Entry for {today}", font=("Helvetica", 22, "bold"), bg="#FFFFFF").pack(pady=20)


        main_frame = tk.Frame(self.root, bg="#FFFFFF")
        main_frame.pack(padx=30, pady=20)


        def info_box(col, title, bg_color, fields):
            BOX_WIDTH = 260
            BOX_HEIGHT = 260


            frame = tk.Frame(main_frame, bg=bg_color, bd=2, relief="ridge", width=BOX_WIDTH, height=BOX_HEIGHT)
            frame.grid(row=0, column=col, padx=15)
            frame.pack_propagate(False)  # This make size fized


            tk.Label(frame, text=title, font=("Helvetica", 16, "bold"), bg=bg_color).pack(anchor="w", pady=(0, 10))


            for label, key in fields:
                value = today_entry.get(key)
                if value not in [None, "", "None"]:
                    # Format rating fields
                    if key in ["sleep_quality", "mood"]:
                        display_value = f"{value}/5"
                    elif key == "stress":
                        display_value = f"{value}/10"
                    else:
                        display_value = value
                    tk.Label(frame, text=f"{label}: {display_value}", font=("Helvetica", 14), bg=bg_color,
                        wraplength=220,   # prevent long text overflow
                        justify="left"
                    ).pack(anchor="w", pady=2)


        # === LEFT → RIGHT BOXES ===
        info_box(0, "Sleep", "#E6F2FF", [("Hours", "sleep_hours"), ("Quality", "sleep_quality"), ("Dreams", "dreams")])
        info_box(1, "Meals", "#FFF0F5", [("Breakfast", "breakfast"), ("Lunch", "lunch"), ("Dinner", "dinner"), ("Snacks", "snacks")])
        info_box(2, "Hydration", "#F0FFF0", [("Water (glass)", "water"), ("Juice (glass)", "juice"), ("Caffeine (glass)", "caffeine"), ("Alcohol (glass)", "alcohol")])
        info_box(3, "Exercise", "#FFF8DC", [("Type", "exercise_type"), ("Duration(min)", "duration"), ("Intensity", "intensity"), ("Steps", "steps")])
        info_box(4, "Mood", "#FFE4E1", [("Mood", "mood"), ("Stress", "stress"), ("Reflection", "reflection")])


        tk.Button(
            self.root, text="⬅ Back", width=20, height=2, font=("Helvetica", 16), bg="#FF4500", fg="white",
            command=self.main_menu).pack(pady=30)


    # ---------------- Weekly Summary ----------------
    def weekly_summary_screen(self):
        import datetime
        today_str = datetime.datetime.now().strftime("%d-%m-%Y")
       
        # Get today's entry
        today_entry = next((e for e in wellness_data if e.get("date") == today_str), None)
        if not today_entry:
            messagebox.showwarning("Warning", " No entry for today. Add today's entry first.")
            return
        if not is_entry_complete(today_entry):
            messagebox.showwarning("Warning", " Today's entry is not complete. Fill all required fields first.")
            return


        # Past 6 days hardcoded
        past_week = [
            {"sleep_hours": 6, "steps": 5000, "water": 5, "mood": 3, "stress": 6, "exercise": True},
            {"sleep_hours": 7.5, "steps": 6500, "water": 6, "mood": 4, "stress": 5, "exercise": False},
            {"sleep_hours": 5, "steps": 4000, "water": 5, "mood": 2, "stress": 7, "exercise": True},
            {"sleep_hours": 8, "steps": 7000, "water": 8, "mood": 5, "stress": 3, "exercise": True},
            {"sleep_hours": 6.5, "steps": 5200, "water": 6, "mood": 3, "stress": 6, "exercise": False},
            {"sleep_hours": 9, "steps": 6000, "water": 5, "mood": 4, "stress": 4, "exercise": True}
        ]


        # Add today's actual data
        past_week.append({
            "sleep_hours": today_entry.get("sleep_hours", 0),
            "steps": today_entry.get("steps", 0),
            "water": today_entry.get("water", 0),
            "mood": int(today_entry.get("mood", 0)),
            "stress": int(today_entry.get("stress", 0)),
            "exercise": today_entry.get("exercise_type") not in [None, "None", ""]
        })


        # Compute averages
        avg_sleep = sum(d["sleep_hours"] for d in past_week) / 7
        avg_steps = sum(d["steps"] for d in past_week) / 7
        avg_water = sum(d["water"] for d in past_week) / 7
        avg_mood = sum(d["mood"] for d in past_week) / 7
        avg_stress = sum(d["stress"] for d in past_week) / 7
        exercise_days = sum(1 for d in past_week if d["exercise"])


        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()


        tk.Label(self.root, text=" Weekly Summary", font=("Helvetica", 20, "bold"), bg="#FFFFFF").pack(pady=20)


        # --- Box for Averages ---
        avg_frame = tk.Frame(self.root, bg="#E6F2FF", bd=2, relief="ridge", padx=20, pady=20)
        avg_frame.pack(pady=10, padx=30, fill="x")


        tk.Label(avg_frame, text=f"Average Sleep: {avg_sleep:.1f} hours/day", font=("Helvetica", 16), bg="#E6F2FF").pack(anchor="w", pady=2)
        tk.Label(avg_frame, text=f"Average Steps: {avg_steps:.0f} steps/day", font=("Helvetica", 16), bg="#E6F2FF").pack(anchor="w", pady=2)
        tk.Label(avg_frame, text=f"Average Water: {avg_water:.1f} glasses/day", font=("Helvetica", 16), bg="#E6F2FF").pack(anchor="w", pady=2)
        tk.Label(avg_frame, text=f"Average Mood: {avg_mood:.1f}/5", font=("Helvetica", 16), bg="#E6F2FF").pack(anchor="w", pady=2)
        tk.Label(avg_frame, text=f"Average Stress: {avg_stress:.1f}/10", font=("Helvetica", 16), bg="#E6F2FF").pack(anchor="w", pady=2)
        tk.Label(avg_frame, text=f"Days Exercised: {exercise_days} out of 7", font=("Helvetica", 16), bg="#E6F2FF").pack(anchor="w", pady=2)
       
        # --- Box for Conclusion ---
        conclusion_frame = tk.Frame(self.root, bg="#FFF8DC", bd=2, relief="ridge", padx=20, pady=20)
        conclusion_frame.pack(pady=20, padx=30, fill="both", expand=True)


        tk.Label(conclusion_frame, text="Conclusion", font=("Helvetica", 18, "bold"), bg="#FFF8DC").pack(anchor="w", pady=(0,10))
        conclusion_text = (
            "You had a fairly balanced week overall — sleep was generally good, "
            "and you managed to stay active on multiple days. Although there were "
            "moments of higher stress and a few low-mood days, you still maintained "
            "healthy habits like drinking water and exercising. Keep taking small "
            "steps forward; you’re building steady momentum even through tougher days."
        )
        tk.Label(conclusion_frame, text=conclusion_text, font=("Helvetica", 14), wraplength=800, justify="left", bg="#FFF8DC").pack(anchor="w")


        # Back button
        tk.Button(self.root, text=" Back", width=20, height=2, font=("Helvetica", 16), bg="#FF4500", fg="white", command=self.main_menu).pack(pady=20)


# ---------------- BMI calculation ----------------
class BMICalculatorGUI(HealthModule):
    """
    GUI for BMI & Calorie Calculator.
    Allows user to input height, weight, age, gender and activity level.
    Calculates BMI, BMR, TDEE and provides calorie recommendations.
    Stores records to a text file for future reference.
    """
    def __init__(self, parent):
        super().__init__(parent.root, parent.show_main_menu)
        self.parent = parent
        self.records = []   # Stores all BMI calculation records
        self.records_file = "bmi_records.txt"
        self.load_records() # Load records from file if exists


    def load_records(self):
        # Load existing BMI records from file
        if os.path.exists(self.records_file):
            with open(self.records_file, "r") as f:
                for line in f:
                    try:
                        record = eval(line.strip())
                        self.records.append(record)
                    except:
                        pass


    def load_previous_records(self):
        # Return a list of previously saved BMI records
        records = []
        if os.path.exists(self.records_file):
            with open(self.records_file, "r") as f:
                for line in f:
                    try:
                        record = eval(line.strip())
                        records.append(record)
                    except:
                        continue
        return records
       
   
    def show_previous_records(self,records):
        # Display all previous BMI records in a popup message box
        if not records:
            messagebox.showinfo("Previous Records", "No previous records found.")
            return
   
        msg = ""
        for i, r in enumerate(records, 1):
            msg += f"Record {i}:\n"
            for k, v in r.items():
                msg += f"  {k}: {v}\n"
            msg += "\n"
   
        messagebox.showinfo("Previous Records", msg)
       
    def save_records(self):
        # Save the last BMI record to file
        with open(self.records_file, "a") as f:
            for r in self.records[-1:]:  # only save last added record
                f.write(str(r) + "\n")
        messagebox.showinfo("Saved", f"Record saved to {self.records_file}")
       
    def view_previous_records(self):
        # Load and display all previously saved BMI records
        records = self.load_previous_records()
        self.show_previous_records(records)


    def show_gui(self):
        # Clear previous content
        for widget in self.parent.root.winfo_children():
            widget.destroy()


        self.parent.root.configure(bg=main_bg)
        self.root.title("BMI & Calorie Calculator")
        frame = tk.Frame(self.parent.root, bg=main_bg)
        frame.pack(expand=True, fill="both", padx=50, pady=20)


        tk.Label(frame, text="BMI & Calorie Calculator", font=("Helvetica", 35, "bold"), bg=main_bg).pack(pady=(40,13))


        # --- Input Fields ---
        label_font = ("Helvetica", 20, "bold")
        entry_font = ("Helvetica", 20)


        self.height_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.activity_var = tk.StringVar()


        form_frame = tk.Frame(frame, bg=main_bg)
        form_frame.pack(pady=45)


        # ---------------- Input Form (Centered) ----------------
        row = 0
   
        for label_text, var in [
            ("Height (50cm~280cm):", self.height_var),
            ("Weight (10kg~500kg):", self.weight_var),
            ("Age (10~120):", self.age_var)]:
                tk.Label(form_frame,text=label_text,font=label_font,bg=main_bg
                        ).grid(row=row, column=0, sticky="e", padx=(0,15), pady=(10))
   
                tk.Entry(form_frame,textvariable=var,font=entry_font,width=26
                        ).grid(row=row, column=1, pady=(10))
   
                row += 1
   
        tk.Label(form_frame,text="Gender:",font=label_font,bg=main_bg
                ).grid(row=row, column=0, sticky="e", padx=(0,15), pady=10)
        ttk.Combobox(form_frame,textvariable=self.gender_var,values=["M", "F"],font=entry_font,width=25,state="readonly"
                    ).grid(row=row, column=1, pady=10)


        row += 1
   
        tk.Label(form_frame,text="Activity Level:",font=label_font,bg=main_bg
                ).grid(row=row, column=0, sticky="e", padx=(0,15), pady=10)
        activity_levels = [
            "1 Sedentary (little or no exercise)",
            "2 Lightly active (1–3 days/week)",
            "3 Moderately active (3–5 days/week)",
            "4 Very active (6–7 days/week)",
            "5 Extra active (very intense exercise)"]
        ttk.Combobox(form_frame,textvariable=self.activity_var,values=activity_levels,font=entry_font,width=25,state="readonly"
                    ).grid(row=row, column=1, pady=10)
       
        # --- Buttons ---
        btn_frame = tk.Frame(frame, bg=main_bg)
        btn_frame.pack(pady=20)
       
        tk.Button(btn_frame, text="Back", font=("Helvetica",18), bg="#FF4500", fg="white", width=15,
                  command=lambda: [self.root.title("Health & Wellness Assisrant"),
                                    self.parent.show_main_menu()]).pack(side="left", padx=20)
        tk.Button(btn_frame, text="Calculate", font=("Helvetica",18), bg="#32CD32", fg="white", width=15,
                  command=self.calculate).pack(side="left", padx=20)
       
        below_frame = tk.Frame(frame, bg=main_bg)
        below_frame.pack(pady=(10, 0))
       
        tk.Button(below_frame,text="View Previous Records",font=("Helvetica",18),bg="#1E90FF",fg="white",width=22,
                  command=self.view_previous_records).pack()
       
    def calculate(self):
        """Calculate BMI, BMR, TDEE and display results"""
        # --- Check if inputs are filled ---
        if not self.height_var.get() or not self.weight_var.get() or not self.age_var.get():
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
   
        if not self.gender_var.get():
            messagebox.showerror("Error", "Please select gender.")
            return
   
        if not self.activity_var.get():
            messagebox.showerror("Error", "Please select activity level.")
            return
   
        # -------- Type and range check --------
        try:
            height = float(self.height_var.get())
            weight = float(self.weight_var.get())
        except ValueError:
            messagebox.showerror("Error", "Height, weight and age must be numbers.")
            return


        try:
            age = int(self.age_var.get())
        except ValueError:
            messagebox.showerror("Error", "Age must be a whole number.")
            return
       
        if height < 50 or height > 280:
            messagebox.showerror("Error", "Height must be between 50 and 280 cm.")
            return
   
        if weight < 10 or weight > 500:
            messagebox.showerror("Error", "Weight must be between 10 and 500 kg.")
            return
   
        if age < 10 or age > 120:
            messagebox.showerror("Error", "Age must be between 10 and 120.")
            return
       
        # Gender and activity
        gender = self.gender_var.get()
        if gender not in ["M", "F"]:
            messagebox.showerror("Error", "Invalid gender selection.")
            return
   
        activity_choice = self.activity_var.get().split(" ")[0]
        if activity_choice not in ["1", "2", "3", "4", "5"]:
            messagebox.showerror("Error", "Invalid activity level.")
            return
   
        # -------- BMI calculation --------
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
   
        if bmi < 18.5:
            category = "Underweight"
        elif bmi <= 24.9:
            category = "Healthy"
        elif bmi <= 29.9:
            category = "Overweight"
        else:
            category = "Obese"
   
        # -------- BMR calculation --------
        if gender == "M":
            bmr = round(10 * weight + 6.25 * height - 5 * age + 5, 1)
        else:
            bmr = round(10 * weight + 6.25 * height - 5 * age - 161, 1)


        # --- TDEE calculation based on activity factor ---
        activity_factor_map = {
            "1": 1.2,
            "2": 1.375,
            "3": 1.55,
            "4": 1.725,
            "5": 1.9
        }
        tdee = round(bmr * activity_factor_map[activity_choice], 1)


        weight_loss = tdee - 500
        weight_gain = tdee + 500
        weight_loss = round(weight_loss,2)
        weight_gain = round(weight_loss,2)
   
        # -------- Result --------
        result_msg = (
            f"BMI: {bmi} ({category})\n"
            f"BMR: {bmr} kcal/day\n"
            f"TDEE: {tdee} kcal/day\n\n"
            f"Calories Recommendation:\n"
            f"Maintenance: {tdee}\n"
            f"Weight Loss: {weight_loss:.2f}\n"
            f"Weight Gain: {weight_gain:.2f}"
        )
   
        messagebox.showinfo("BMI & Calorie Result", result_msg)
   
        # -------- Save record --------
        self.records.append({
            "Height": height,
            "Weight": weight,
            "Age": age,
            "Gender": gender,
            "BMI": bmi,
            "Category": category,
            "BMR": bmr,
            "TDEE": tdee
        })
   
        if messagebox.askyesno("Save Record", "Do you want to save this record?"):
            self.save_records()




# ---------------- Step Counter Log ----------------
class StepCounterGUI(HealthModule):
    """
    GUI for Step Counter Log
    Allows user to:
    - Set daily step goal
    - Log steps manually
    - Track daily step progress with progress bar
    - Reset all step data
    Steps are saved to a text file for persistent tracking.
    """
    def __init__(self, root, main_menu_callback):
        super().__init__(root, main_menu_callback)


        # File paths for step records and goal
        self.step_log_file = "step_records.txt"
        self.step_goal_file = "step_goal.txt"


        self.root = root


        # Initialize step records
        self.records = []  # list of dicts with {"date": str, "steps": int}
        self.today_steps = 0
        self.step_goal = 10000  # default goal


        # Load existing goal and today's step
        self.load_goal()
        self.load_steps_from_file()


        self.root.title("Step Counter")


        frame = tk.Frame(root, bg=main_bg)
        frame.pack()


        # Title
        tk.Label(self.root, text="Step Counter Log", font=("Helvetica", 35, "bold"),bg=main_bg).pack(pady=(45,15))


        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=800,
                                            mode="determinate", maximum=self.step_goal, variable=self.progress_var)
        self.progress_bar.pack(pady=(20,15))
       
        # Encourage label
        self.encourage_label = tk.Label(self.root, text="", font=("Helvetica", 18, "italic"), bg=main_bg)
        self.encourage_label.pack(pady=(1,17))


        # Progress label
        self.progress_label = tk.Label(self.root, text=f"Today's Steps: {self.today_steps}/{self.step_goal}", font=("Helvetica", 20),bg=main_bg)
        self.progress_label.pack(pady=(14,0))
       
        self.update_progress_bar()  # initialize progress


        step_counter_frame = tk.Frame(self.root, bg=main_bg)
        step_counter_frame.pack(fill='both', expand=True, pady=20)


        # Buttons
        btn_frame = tk.Frame(step_counter_frame, bg=main_bg)
        btn_frame.pack(side='left', fill='both', expand=True, padx=(500, 0))
        btn_font = ("Helvetica", 18, "bold")


        btn_center_frame = tk.Frame(btn_frame, bg=main_bg)
        btn_center_frame.place(relx=0.5, rely=0.44, anchor='center')


        tk.Button(btn_center_frame, text="Set Daily Step Goal", font=btn_font, width=25, height=2,
                bg="#32CD32", command=self.set_goal).pack(pady=10)


        tk.Button(btn_center_frame, text="Log Steps", font=btn_font, width=25, height=2,
                bg="#1E90FF", command=self.log_steps).pack(pady=10)


        tk.Button(btn_center_frame, text="Reset Data", font=btn_font, width=25, height=2,
                bg="#FF8C00", command=self.reset_data).pack(pady=10)


        tk.Button(btn_center_frame, text="Back to Main Menu", font=btn_font, width=25, height=2,
                bg="#FF4500", command=lambda: [self.root.title("Health & Wellness Assistant"),
                                                            self.back_to_main_menu()]).pack(pady=10)
       
         # ---------------- Step Records Table ----------------
        table_frame = tk.Frame(step_counter_frame, bg=main_bg)
        table_frame.pack(side='right', fill='both', padx=(0, 68))


        # Title
        table_title = tk.Label(table_frame, text="Step History",font=("Helvetica",20, "bold"), bg=main_bg)
        table_title.pack(pady=(0, 10))
       
        # Create a style for the Treeview
        style = ttk.Style()
        style.configure("Treeview", font=('Helvetica', 14))
        # Configure heading style separately
        style.configure("Treeview.Heading", font=('Helvetica', 15, 'bold'))  # Bold font for headings
       
        columns = ("date", "steps")
        self.record_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )


        self.record_table.heading("date", text="Date")
        self.record_table.heading("steps", text="Total Steps")


        self.record_table.column("date", width=200, anchor="center")
        self.record_table.column("steps", width=200, anchor="center")


        self.record_table.pack(side='left', fill='both')


        # Scroll bar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.record_table.yview)
        scrollbar.pack(side='right', fill='y')
        self.record_table.configure(yscrollcommand=scrollbar.set)
       
        self.record_table.pack()


        self.update_progress_bar()  # ensure progress bar is updated
        self.load_records_to_gui()




    # ---------------- File Operations ----------------
    def load_goal(self):
        self.step_goal = 10000  # force reset first
        # Load daily step goal from file or set default 10000
        if os.path.exists(self.step_goal_file):
            try:
                with open(self.step_goal_file, "r") as f:
                    content = f.read().strip()


                    # Case 1: pure number
                    if content.isdigit():
                        self.step_goal = int(content)
                        return


                    # Case 2: DATE + Goal format
                    for line in content.splitlines():
                        if "Goal:" in line:
                            self.step_goal = int(line.split(":")[1].strip())
                            return


            except:
                self.step_goal = 10000


    def save_goal(self, filename="step_goal.txt"):
        # Save current step goal to file
        today_str = datetime.datetime.now().strftime("%d-%m-%Y")
        with open(filename, "w") as f:
            f.write(f"DATE: {today_str}\n")
            f.write(f"Goal: {str(self.step_goal)}")
   
    def save_step(self, new_step, filename="step_records.txt"):


        """
        Save a new step entry.
        Aggregates steps for the same day.
        Updates file and progress bar.
        """
        today_str = datetime.datetime.now().strftime("%d-%m-%Y")
        total_steps = new_step
        other_days_records = []


        # Load existing records
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                blocks = f.read().split("-" * 40)
       
            for block in blocks:
                block = block.strip()
                if not block:
                    continue


                if today_str in block:
                    for line in block.split("\n"):
                        try:
                            total_steps += int(line.split(":")[1].strip())
                        except:
                            continue
                else:
                    other_days_records.append(block)


        with open(filename, "w", encoding="utf-8") as f:
            for rec in other_days_records:
                f.write(rec + "\n" + "-" * 40 + "\n")


            f.write(f"DATE: {today_str}\n")
            f.write(f"Total: {total_steps} \n")
            f.write("-" * 40 + "\n")


        self.today_steps = total_steps
        self.update_progress_bar()
        self.load_steps_from_file()
        self.load_records_to_gui()


    def reset_data(self):
        # Reset all step records and goal to default
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all step data?"):
            self.today_steps = 0


            today_str = datetime.datetime.now().strftime("%d-%m-%Y")
            self.records = [r for r in self.records if r["date"] != today_str]


            # Clear file
            with open(self.step_log_file, "w") as f:
                f.write("")  


            # Reset step goal
            self.step_goal = 10000
            with open(self.step_goal_file, "w") as f:
                f.write(str(self.step_goal))


            self.update_progress_bar()
            for row in self.record_table.get_children():
                self.record_table.delete(row)
           
            messagebox.showinfo("Reset", "All step data has been reset!")


    # ---------------- GUI Actions -----------------
    def update_progress_bar(self):
        # Update the progress bar and label to reflect today's steps
        self.progress_bar.config(maximum=self.step_goal)
        self.progress_var.set(self.today_steps)
        self.progress_label.config(text=f"Today's Steps: {self.today_steps}/{self.step_goal}")


        if self.today_steps >= self.step_goal:
            encourage_text = "Awesome! You've reached your goal! Keep it up! "
        else:
            remain = self.step_goal - self.today_steps
            encourage_text = f"Keep going! Only {remain} steps to reach your goal! "


        self.encourage_label.config(text=encourage_text)


    def set_goal(self):
        # Prompt user to set a new daily step goal
        goal = simpledialog.askinteger("Set Step Goal", "Enter your daily step goal:", minvalue=1, maxvalue=100000)
        if goal:
            self.step_goal = goal
            self.save_goal()
            self.update_progress_bar()
        messagebox.showinfo("Success", f"Daily step goal set to {self.step_goal} steps!")


    def log_steps(self):
        # Prompt user to log steps and save to records
        step = simpledialog.askinteger("Log Steps", "Enter steps walked today:", minvalue=0, maxvalue=100000)
        if step is not None:
            today_str = datetime.datetime.now().strftime("%d-%m-%Y")
            for record in self.records:
                if record["date"] == today_str:
                    record["steps"] += step
                    break
            else:
                self.records.append({"date": today_str, "steps": step})
            self.save_step(step)
            messagebox.showinfo("Success", f"{step} steps logged!")
            self.update_progress_bar()
            self.load_records_to_gui()


    def load_steps_from_file(self, filename="step_records.txt"):
        # Load all steps from file into records list
        self.records = []
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read().split("-"*40)
                for block in content:
                    lines = block.strip().split("\n")
                    if len(lines) >= 2:
                        date_line = lines[0].replace("DATE:", "").strip()
                        steps_line = lines[1].replace("Total:", "").strip()
                        try:
                            self.records.append({"date": date_line, "steps": int(steps_line)})
                        except:
                            continue
       
        today_str = datetime.datetime.now().strftime("%d-%m-%Y")
        for record in self.records:
            if record["date"] == today_str:
                self.today_steps = record["steps"]
                break
        else:
            self.today_steps = 0


    def load_records_to_gui(self):
        # Clear existing rows
        for row in self.record_table.get_children():
            self.record_table.delete(row)


        sorted_records = sorted(self.records,
                          key=lambda x: datetime.datetime.strptime(x["date"], "%d-%m-%Y"),
                          reverse=True)
       
        # Insert records
        for record in sorted_records:
            self.record_table.insert(
                "",
                "end",
                values=(record["date"], record["steps"])
            )

# ---------------- Main Health & Wellness Menu ----------------
class HealthWellnessGUI:
    """
    Main GUI for the Health & Wellness Assistant.
    Provides access to:
    - Daily Wellness Log
    - BMI & Calorie Calculator
    - Step Counter Log
    - Exit the application
    """
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.configure(bg=main_bg)
        self.root.title("Health & Wellness Assistant")

        self.root.state("zoomed")   # maximize window
       
        # Initialize BMI Calculator module
        self.bmi_gui = BMICalculatorGUI(self)


        # Show the main menu
        self.show_main_menu()
       
    def show_main_menu(self):
        """
        Display the main menu with buttons to access different modules.
        Clears any previous widgets before displaying.
        """
       
        # Clear all previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()  # clear everything
       
            self.root.configure(bg=main_bg)


        # Title Label
        tk.Label(self.root, text="Health & Wellness Assistant", font=("Helvetica", 14, "bold"),bg=main_bg
                 ).pack(pady=(30,0))
        tk.Label(self.root, text="ZenTrack", font=("Helvetica", 48, "bold"),bg=main_bg
                 ).pack()
        tk.Label(self.root, text="Keep Moving, Stay Healthy! ", font=("Helvetica", 14, "bold"),bg=main_bg
                 ).pack(pady=(0,10))


        # Frame to hold the menu buttons
        btn_frame = tk.Frame(self.root, bg=main_bg)
        btn_frame.pack(pady=20)


        # Menu Buttons
        tk.Button(btn_frame, text="Daily Wellness Log", width=30, height=2, font=("Helvetica",18), bg="#000000", fg="white",
                command=self.open_wellness_tracker).pack(pady=10)
        tk.Button(btn_frame, text="BMI & Calorie Calculator", width=30, height=2, font=("Helvetica",18),bg="#000000", fg="white",
                command=self.open_bmi_calculator).pack(pady=10)
        tk.Button(btn_frame, text="Step Counter Log", width=30, height=2, font=("Helvetica",18),bg="#000000", fg="white",
                command=self.open_step_counter).pack(pady=10)
        tk.Button(btn_frame, text="Exit", width=30, height=2, font=("Helvetica",18),
                bg="#FF3B3B", fg="white", command=self.root.quit).pack(pady=20)     # exit application
       
    def open_wellness_tracker(self):
        """
        Open the Daily Wellness Log module.
        Pass main menu callback so user can return to main menu.
        """
        DailyWellnessLog(self.root, self.show_main_menu)


    def open_bmi_calculator(self):
        """
        Open the BMI & Calorie Calculator module.
        Clears main window widgets first.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        self.bmi_gui.show_gui()


    def open_step_counter(self):
        """
        Open the Step Counter Log module.
        Clears main window widgets first.
        """
        for widget in self.root.winfo_children():
            widget.destroy()  
        StepCounterGUI(self.root, self.show_main_menu)


    # ---------------- Run Application ----------------
    def run(self):
        self.root.mainloop()


# ---------------- Run Main Menu ----------------
if __name__ == "__main__":
    HealthWellnessGUI().run()




