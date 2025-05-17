import matplotlib.pyplot as plt  # For plotting charts and graphs
from config import WIDTH
from utils.helpers import clear, pad, browse_courses, browse_students  # Utility functions for screen management and student/course browsing

def reports_menu(db):
    # Main loop for the reports submenu
    while True:
        clear()  # Clear the console for a fresh menu display
        print(" REPORTS MENU ".center(WIDTH, "="))  # Display the menu header
        print("")
        # Options available in the reports menu
        opts = [
            "1. Course Roster     ",
            "2. Student Timetable ",
            "3. Department Summary",
            "",
            "0. Back              "
        ]
        # Center-print each menu option
        for o in opts:
            print(o.center(WIDTH))
        pad()  # Print a divider at the bottom of the menu
        choice = input("Enter your choice: ").strip()  # Get user selection
        # Call the corresponding report function based on the user's choice
        if choice == "1":
            report_course_roster(db)
        elif choice == "2":
            report_student_timetable(db)
        elif choice == "3":
            report_department_summary(db)
        elif choice == "0":
            print("Returning to Admin Home...")  # Inform the user they are leaving the reports menu
            break  # Exit the reports menu loop
        else:
            print("Invalid option. Please try again.")
            input("Press Enter to continue...")

def report_course_roster(db, role="admin", prof_id=None, selected_course=None):
    # This report displays the roster for a specific course.
    if selected_course is not None:
        # Use the provided course code if available (typically from a previous selection)
        course_code = selected_course
        course_title = db.get_course_title(course_code)  # Retrieve course title from the database
        if role.lower() == "professor":
            # For professors, ensure they actually teach the selected course.
            if db.count_classes_by_course_and_prof(course_code, prof_id) == 0:
                input("You do not teach this course. Press Enter to return...")
                return
            selected_prof_id = prof_id
            prof_fullname = db.get_professor_fullname(prof_id)
        else:
            # For admins, allow selecting one of the professors teaching the course
            professors = db.get_professors_by_course(course_code)
            if not professors:
                input("No professor found for the selected course. Press Enter to return...")
                return
            if len(professors) == 1:
                selected_prof = professors[0]
            else:
                clear()  # Clear the screen to display professor choices
                title_prof = f" PROFESSORS FOR {course_code.upper()} - {course_title.upper()} "
                print(title_prof.center(WIDTH, "="))
                print("Commands: < = Prev     > = Next     ! = Back")
                print("")
                print("Select a professor:")
                for prof in professors:
                    # Display professor ID and full name
                    print(f"{prof[0]}: {prof[1]} {prof[2]}")
                pad()
                prof_choice = input("Enter Professor ID: ").strip()
                if prof_choice in ["!", "B"]:
                    return
                selected_prof = next((prof for prof in professors if str(prof[0]) == prof_choice), None)
                if not selected_prof:
                    input("Invalid Professor ID. Press Enter to return...")
                    return
            selected_prof_id = selected_prof[0]
            prof_fullname = f"{selected_prof[1]} {selected_prof[2]}"
    
        # Retrieve the list of students enrolled in the selected course taught by the chosen professor.
        students = db.get_enrolled_students(course_code, selected_prof_id)
        page = 0  # Start pagination at page 0
        page_size = 15  # Define number of records per page
        col_id = 10  # Column width for student ID
        col_fname = 50  # Column width for first name
        col_lname = 50  # Column width for last name
        total_width = col_id + col_fname + col_lname + 10  # Total table width
    
        # Loop to paginate through the enrolled students
        while True:
            clear()  # Clear the screen for a fresh display
            title_students = f" ENROLLED STUDENTS FOR {course_code.upper()} - {course_title.upper()} "
            title_prof = f"Professor: {prof_fullname}"
            print(title_students.center(WIDTH, "="))
            print("Commands: < = Prev     > = Next     ! = Back")
            print("")
            print(title_prof)
            print("=" * total_width)
            header = f"| {'ID'.ljust(col_id)} | {'First Name'.ljust(col_fname)} | {'Last Name'.ljust(col_lname)} |"
            print(header)
            print("=" * total_width)
            start = page * page_size
            end = start + page_size
            # Print enrolled student records for the current page
            for s in students[start:end]:
                stud_id, stud_fname, stud_lname = s
                print(f"| {str(stud_id).ljust(col_id)} | {stud_fname.ljust(col_fname)} | {stud_lname.ljust(col_lname)} |")
            print("=" * total_width)
            print(f"Showing records {start+1}-{min(end, len(students))} of {len(students)}")
            pad()
            cmd = input("Enter Command: ").strip().upper()
            # Handle pagination commands: next page (">"), previous page ("<"), or exit ("!" or "B")
            if cmd == ">":
                if end < len(students):
                    page += 1
                    continue
                else:
                    input("No more pages. Press Enter...")
                    continue
            elif cmd == "<":
                if page > 0:
                    page -= 1
                    continue
                else:
                    input("Already at first page. Press Enter...")
                    continue
            elif cmd in ["!", "B"]:
                break  # Exit the course roster report
            else:
                input("Invalid command. Press Enter to continue...")
        return  # End of the branch for provided selected_course
    
    # Alternative branch: let the user select a course via the browse_courses utility
    while True:
        course_code = browse_courses(db)
        if not course_code:
            break  # Exit if no course is chosen
        course_title = db.get_course_title(course_code)
        professors = db.get_professors_by_course(course_code)
        if not professors:
            input("No professor found for the selected course. Press Enter to return...")
            continue
        if role.lower() == "professor":
            # For professors, filter so that the course matches the logged-in professor
            professors = [p for p in professors if str(p[0]) == str(prof_id)]
            if not professors:
                input("You do not teach the selected course. Press Enter to return...")
                continue
            selected_prof = professors[0]
        else:
            if len(professors) == 1:
                selected_prof = professors[0]
            else:
                clear()
                title_prof = f" PROFESSORS FOR {course_code.upper()} - {course_title.upper()} "
                print(title_prof.center(WIDTH, "="))
                print("Commands: < = Prev     > = Next     ! = Back")
                print("")
                print("Select a professor:")
                for prof in professors:
                    print(f"{prof[0]}: {prof[1]} {prof[2]}")
                pad()
                prof_choice = input("Enter Professor ID: ").strip()
                if prof_choice in ["!", "B"]:
                    continue
                selected_prof = next((prof for prof in professors if str(prof[0]) == prof_choice), None)
                if not selected_prof:
                    input("Invalid Professor ID. Press Enter to return to course selection...")
                    continue
        selected_prof_id = selected_prof[0]
        prof_fullname = f"{selected_prof[1]} {selected_prof[2]}"
        # Retrieve the list of enrolled students again for the chosen course and professor.
        students = db.get_enrolled_students(course_code, selected_prof_id)
        page = 0
        page_size = 15
        col_id = 10
        col_fname = 50
        col_lname = 50
        total_width = col_id + col_fname + col_lname + 10
    
        while True:
            clear()
            title_students = f" ENROLLED STUDENTS FOR {course_code.upper()} - {course_title.upper()} "
            title_prof = f"Professor: {prof_fullname}"
            print(title_students.center(WIDTH, "="))
            print("Commands: < = Prev     > = Next     ! = Back")
            print("")
            print(title_prof)
            print("=" * total_width)
            header = f"| {'ID'.ljust(col_id)} | {'First Name'.ljust(col_fname)} | {'Last Name'.ljust(col_lname)} |"
            print(header)
            print("=" * total_width)
            start = page * page_size
            end = start + page_size
            # Display students in the current page slice.
            for s in students[start:end]:
                stud_id, stud_fname, stud_lname = s
                print(f"| {str(stud_id).ljust(col_id)} | {stud_fname.ljust(col_fname)} | {stud_lname.ljust(col_lname)} |")
            print("=" * total_width)
            print(f"Showing records {start+1}-{min(end, len(students))} of {len(students)}")
            pad()
            cmd = input("Enter Command: ").strip().upper()
            if cmd == ">":
                if end < len(students):
                    page += 1
                    continue
                else:
                    input("No more pages. Press Enter...")
                    continue
            elif cmd == "<":
                if page > 0:
                    page -= 1
                    continue
                else:
                    input("Already at first page. Press Enter...")
                    continue
            elif cmd in ["!", "B"]:
                break  # Exit current pagination loop and return to course selection
            else:
                input("Invalid command. Press Enter to continue...")

def report_student_timetable(db):
    # This report displays the timetable for a selected student.
    while True:
        selected_student = browse_students(db)  # Allow user to select a student from a paginated list
        if not selected_student:
            break  # Exit the timetable report if no student is selected

        # Retrieve student's first and last name from the database
        cursor = db.conn.cursor()
        cursor.execute("SELECT stud_fname, stud_lname FROM student WHERE stud_id = ?;", (selected_student,))
        student_info = cursor.fetchone()
        student_name = f"{student_info[0]} {student_info[1]}" if student_info else "Unknown"

        # Get timetable data for the selected student
        rows = db.get_student_timetable(selected_student)

        clear()
        title = " TIMETABLE "
        print(title.center(WIDTH, "="))
        print(f"Student Name: {student_name}".center(WIDTH))
        
        # Define column widths for timetable display
        col_course_id     = 9
        col_course_name   = 48
        col_schedule      = 15
        col_professor     = 35
        header = (f"| {'Course ID'.ljust(col_course_id)} | "
                  f"{'Course Name'.ljust(col_course_name)} | "
                  f"{'Schedule'.ljust(col_schedule)} | "
                  f"{'Professor'.ljust(col_professor)} |")
        print("=" * WIDTH)
        print(header)
        print("=" * WIDTH)
        if rows:
            # Iterate through timetable rows and print each row formatted
            for row in rows:
                course_id, course_name, schedule, professor_name = row
                schedule = schedule if schedule else "Not set"
                professor_name = professor_name if professor_name else "N/A"
                print(f"| {str(course_id).ljust(col_course_id)} | "
                      f"{course_name.ljust(col_course_name)} | "
                      f"{schedule.ljust(col_schedule)} | "
                      f"{professor_name.ljust(col_professor)} |")
        else:
            print("No courses found for that student.".center(WIDTH))
        print("=" * WIDTH)
        pad()
        input("Press Enter to return to the student list...")

def report_department_summary(db):
    """
    Displays a Department-Level Summary Report.
    Retrieves summary data (e.g., courses, enrollments, average class size),
    prints a formatted table, and plots a bar graph for visual analysis.
    """
    clear()
    print(" DEPARTMENT SUMMARY ".center(WIDTH, "="))
    print("")
    
    # Fetch the summary data as a DataFrame using a database method
    df = db.get_department_summary()
    
    # Define column widths for the text summary table.
    col_dept_id = 10
    col_dept_name = 34
    col_num_courses = 20
    col_num_enrollments = 20
    col_avg_size = 20
    total_width = col_dept_id + col_dept_name + col_num_courses + col_num_enrollments + col_avg_size + 15
    header = (f"| {'Dept ID'.ljust(col_dept_id)} | "
              f"{'Department Name'.ljust(col_dept_name)} | "
              f"{'Courses Offered'.rjust(col_num_courses)} | "
              f"{'Enrolled Students'.rjust(col_num_enrollments)} | "
              f"{'Average Class Size'.rjust(col_avg_size)} |")
    print("=" * total_width)
    print(header)
    print("=" * total_width)
    if not df.empty:
        # Loop over each department row in the DataFrame and print the summary.
        for index, row in df.iterrows():
            line = (f"| {str(row['dept_id']).ljust(col_dept_id)} | "
                    f"{str(row['department_name']).ljust(col_dept_name)} | "
                    f"{str(row['num_classes']).rjust(col_num_courses)} | "
                    f"{str(row['num_enrollments']).rjust(col_num_enrollments)} | "
                    f"{str(row['avg_class_size']).rjust(col_avg_size)} |")
            print(line)
    else:
        print("No department data found.".center(total_width))
    print("=" * total_width)
    
    # Plot a bar chart of enrollment counts per department if data is available.
    if not df.empty:
        axis = df.plot(kind="bar", x="department_name", y="num_enrollments", legend=False,
                       title="Enrollment Counts per Department", figsize=(8, 4))
        axis.set_xlabel("Department")
        axis.set_ylabel("Number of Enrollments")
        plt.tight_layout()  # Adjust layout to prevent clipping
        plt.show()  # Display the plot window
    else:
        print("No data available for plotting.")

    pad()
    input("Press Enter to continue...")
