import secrets
import string
import os
import sys
from config import WIDTH, HEIGHT

def clear():
    # Clear the console screen.
    os.system("cls")

def pad():
    # Move the cursor near the bottom and print a divider line.
    sys.stdout.write(f"\033[{HEIGHT - 4};1H")
    sys.stdout.flush()
    print("-" * WIDTH)

def browse_courses(db):
    """Displays a paginated list of courses and returns the selected course's code."""
    cursor = db.conn.cursor()
    # Retrieve course code and title from the database.
    cursor.execute("SELECT crs_code, crs_title FROM course ORDER BY crs_code;")
    courses = cursor.fetchall()
    if not courses:
        print("No courses available.")
        input("Press Enter to continue...")
        return None

    page = 0
    page_size = 15

    # Fixed column widths for course display.
    col_course_id = 10
    col_course_title = 103 

    while True:
        clear()
        print(" COURSES ".center(WIDTH, "="))
        print("Commands: < = Prev     > = Next     ! = Back")
        header = f"| {'Course ID'.ljust(col_course_id)} | {'Course Title'.ljust(col_course_title)} |"
        print("=" * WIDTH)
        print(header)
        print("=" * WIDTH)
        # Determine the range of courses for the current page.
        start = page * page_size
        end = start + page_size
        for row in courses[start:end]:
            course_id, course_title = row
            print(f"| {course_id.ljust(col_course_id)} | {course_title.ljust(col_course_title)} |")
        print("=" * WIDTH)
        print(f"Showing courses {start+1}-{min(end, len(courses))} of {len(courses)}")
        pad()
        cmd = input("Enter Course ID: ").strip().upper()
        
        if cmd == "!":
            return None
        elif cmd == ">":
            if end < len(courses):
                page += 1  # Go to next page.
                continue
            else:
                input("Already at last page. Press Enter to continue...")
                continue
        elif cmd == "<":
            if page > 0:
                page -= 1  # Go back to previous page.
                continue
            else:
                input("Already at first page. Press Enter to continue...")
                continue
        else:
            # Check if the entered Course ID exists on the current page.
            selected = None
            for row in courses[start:end]:
                if row[0] == cmd:
                    selected = row[0]
                    break
            if selected:
                return selected
            else:
                input("Invalid Course ID. Press Enter to try again...")

def browse_students(db):
    """Displays a searchable, paginated list of students and returns the selected student's ID."""
    cursor = db.conn.cursor()
    # Fetch student details: ID, last name, and first name.
    cursor.execute("SELECT stud_id, stud_lname, stud_fname FROM student ORDER BY stud_id;")
    students = cursor.fetchall()
    if not students:
        print("No student records found.")
        input("Press Enter to continue...")
        return None

    page = 0
    page_size = 15
    # Define fixed column widths for student display.
    col_stud_id = 4
    col_last = 53            
    col_first = 53          

    while True:
        clear()
        print(" STUDENTS ".center(WIDTH, "="))
        print("Commands: < = Prev     > = Next     ! = Cancel")
        header = f"| {'ID'.ljust(col_stud_id)} | {'Last Name'.ljust(col_last)} | {'First Name'.ljust(col_first)} |"
        print("=" * WIDTH)
        print(header)
        print("=" * WIDTH)
        # Calculate indices for pagination.
        start = page * page_size
        end = start + page_size
        for row in students[start:end]:
            stud_id, stud_lname, stud_fname = row
            print(f"| {str(stud_id).ljust(col_stud_id)} | {stud_lname.ljust(col_last)} | {stud_fname.ljust(col_first)} |")
        print("=" * WIDTH)
        print(f"Showing students {start+1}-{min(end, len(students))} of {len(students)}")
        pad()
        cmd = input("Enter Student ID: ").strip()
        if cmd == "!":
            return None
        elif cmd == ">":
            if end < len(students):
                page += 1
                continue
            else:
                input("Already at last page. Press Enter to continue...")
                continue
        elif cmd == "<":
            if page > 0:
                page -= 1
                continue
            else:
                input("Already at first page. Press Enter to continue...")
                continue
        else:
            # Validate the entered Student ID.
            selected = None
            for row in students[start:end]:
                if str(row[0]) == cmd:
                    selected = row[0]
                    break
            if selected:
                return selected
            else:
                input("Invalid Student ID. Press Enter to try again...")

def generate_username(role, last_name, first_name):
    """
    Generates a username based on:
      - 'a' prefix for admin,
      - 'p' for professor,
      - 's' for student.
    Followed by up to 4 letters of last name and 3 letters of first name.
    """
    role_lower = role.lower()
    if role_lower == "admin":
        prefix = "a"
    elif role_lower == "professor":
        prefix = "p"
    elif role_lower == "student":
        prefix = "s"
    else:
        prefix = ""
    last_part = last_name[:4].lower()
    first_part = first_name[:3].lower()
    return prefix + last_part + first_part

def generate_password(length=8):
    """Generates a random password using letters and digits."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_lookup_dict(db, table):
    """
    Returns a lookup dictionary for a given table.
    Keys are cast to string for consistency.
    """
    lookup = {}
    records = db.read(table)

    if records is None:
        records = []
    if table == "class":
        for rec in records:
            key = str(rec[0])
            lookup[key] = rec
    elif table == "course":
        for rec in records:
            key = rec[0]  # crs_code is text.
            lookup[key] = rec[1]  # Use course title as value.
    elif table == "student":
        for rec in records:
            key = str(rec[0])
            # Concatenate first and last name for display.
            lookup[key] = f"{rec[2]} {rec[1]}"
    elif table == "professor":
        for rec in records:
            key = str(rec[0])
            # Format: title, last name, first name.
            lookup[key] = f"{rec[3]} {rec[1]} {rec[2]}"
    return lookup
