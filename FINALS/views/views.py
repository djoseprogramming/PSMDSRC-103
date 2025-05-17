import utils.helpers as h
from config import WIDTH, MAX_UNIT
from reports import report_course_roster 

# Define a logo to be shown on the welcome screen.
LOGO = [
    "  __  __ _                _    _       _  ",
    " |  \/  (_)              | |  | |     (_) ",
    " | \  / |_  ___ _ __ ___ | |  | |_ __  _  ",
    " | |\/| | |/ __| '__/ _ \| |  | | '_ \| | ",
    " | |  | | | (__| | | (_) | |__| | | | | | ",
    " |_|  |_|_|\___|_|  \___/ \____/|_| |_|_| "
]

def welcome():
    """
    Display the welcome screen.
    Clears the screen, prints the logo, shows the login/exit options,
    and returns the user's choice.
    """
    h.clear()  # Clear the console screen
    print("\n" * 3)  # Add vertical space before the logo
    for line in LOGO:
        # Print each line of the logo, centered horizontally based on WIDTH
        print(line.center(WIDTH))
    print("\n")
    
    # Define the welcome options for the user
    opts = [
        "=== WELCOME ===",
        "",
        "1. Login",
        "0. Exit "
    ]
    for o in opts:
        # Center each option and print it
        print(o.center(WIDTH))
    h.pad()  # Print a bottom divider using the pad helper
    return input("Enter option: ").strip()  # Return the user's trimmed input

# -----------------------------------------------------------------
# ADMIN - NAVIGATION
# -----------------------------------------------------------------
def a_home(name):
    """
    Display the admin home screen.
    Shows different management options (e.g., Admin, Professor, Student, etc.)
    based on the user's role and returns the chosen option.
    """
    h.clear()  # Clear the screen before displaying the admin menu
    print(" ADMIN HOME ".center(WIDTH, "="))
    print("\n")
    print(f"Welcome, {name}!".center(WIDTH))
    print()
    print("Choose an option below.".center(WIDTH))
    print()
    # Define the admin menu options as a list of formatted strings
    opts = [
        "1. Admin     ",
        "2. Professor ",
        "3. Student   ",
        "4. Class     ", 
        "5. Course    ", 
        "6. Department",
        "7. Building  ",
        "8. Room      ", 
        "9. Enrollment",
        "10. Reports  ",
        "",
        "0. Logout    "
    ]
    for o in opts:
        # Center each option by WIDTH and print it
        print(o.center(WIDTH))
    h.pad()  # Add a horizontal divider at the bottom of the menu
    return input("Enter option: ")  # Return the user's selection

def a_home_crud(table, db=None):
    """
    Provide a CRUD action selection for a given table.
    If the table is "enrollment", it directly calls the enrollment management function.
    Otherwise, it loops until a valid CRUD option is selected.
    """
    if table == "enrollment":
        # Directly manage enrollment records without CRUD submenu
        manage_enrollment(role="admin", db=db)
    else:
        while True:
            h.clear()  # Clear the screen for a fresh view
            # Display the management header for the current table
            print(f" {table.upper()} MANAGEMENT ".center(WIDTH, "="))
            print("\n")
            # Define the CRUD options for the current table
            opts = [
                "Choose an action:",
                "",
                "1. Create",
                "2. Manage",
                "",
                "0. Back  "
            ]
            for o in opts:
                print(o.center(WIDTH))  # Center and print each option
            h.pad()  # Print the divider/footer
            choice = input("Enter option: ").strip()  # Get the user's action selection
            if choice in {"1", "2", "0"}:
                return choice  # Return a valid choice
            else:
                print("Invalid option. Try again.")
                input("Press Enter to retry...")  # Pause before re-displaying the menu

# -----------------------------------------------------------------
# ADMIN - CREATE (C)
# -----------------------------------------------------------------
def a_create(table, db=""):
    """
    Collect input from the user to create a new record.
    The prompts depend on the table (admin, professor, student, etc.).
    """
    h.clear()  # Clear the screen for the create form
    print(f" CREATE {table.upper()} ".center(WIDTH, "="))
    print("\n")
    if table == "admin":
        # Prompt for admin information
        admin_lname = input("Last name: ".rjust(WIDTH//2)).strip()
        admin_fname = input("First name: ".rjust(WIDTH//2)).strip()
        return admin_lname, admin_fname
    elif table == "professor":
        # Collect professor's last name, first name, title, and department code
        prof_lname = input("Last name: ".rjust(WIDTH//2)).strip()
        prof_fname = input("First name: ".rjust(WIDTH//2)).strip()
        prof_title = input("Title: ".rjust(WIDTH//2)).strip()
        dept_code = input("Department Code: ".rjust(WIDTH//2)).strip()
        return prof_lname, prof_fname, prof_title, dept_code
    elif table == "student":
        # Prompt for student details (last and first name)
        stud_lname = input("Last name: ".rjust(WIDTH//2)).strip()
        stud_fname = input("First name: ".rjust(WIDTH//2)).strip()
        return stud_lname, stud_fname
    elif table == "class":
        # Collect details for class creation (course code, professor ID, etc.)
        crs_code = input("Course Code: ".rjust(WIDTH // 2)).strip()
        prof_id = input("Professor ID: ".rjust(WIDTH // 2)).strip()
        class_section = input("Class Section: ".rjust(WIDTH // 2)).strip()
        class_time = input("Class Time: ".rjust(WIDTH // 2)).strip()
        room_code = input("Room Code: ".rjust(WIDTH // 2)).strip()
        sem_code = input("Semester Code: ".rjust(WIDTH // 2)).strip()
        return crs_code, prof_id, class_section, class_time, room_code, sem_code
    elif table == "course":
        # Gather course creation inputs including code, title, description, credit, and department
        crs_code = input("Course Code: ".rjust(WIDTH // 2)).strip()
        crs_title = input("Course Title: ".rjust(WIDTH // 2)).strip()
        crs_description = input("Course Description: ".rjust(WIDTH // 2)).strip()
        crs_credit = input("Course Credit: ".rjust(WIDTH // 2)).strip()
        dept_code = input("Department Code: ".rjust(WIDTH // 2)).strip()
        return crs_code, crs_title, crs_description, crs_credit, dept_code
    elif table == "department":
        # Prompt for department specific details
        dept_code = input("Department Code: ".rjust(WIDTH//2)).strip()
        dept_name = input("Department Name: ".rjust(WIDTH//2)).strip()
        return dept_code, dept_name
    elif table == "building":
        # Gather building details (code and name)
        bldg_code = input("Building Code: ".rjust(WIDTH // 2)).strip()
        bldg_name = input("Building Name: ".rjust(WIDTH // 2)).strip()
        return bldg_code, bldg_name
    elif table == "room":
        # Collect room details: code, type, and associated building code
        room_code = input("Room Code: ".rjust(WIDTH // 2)).strip()
        room_type = input("Room Type: ".rjust(WIDTH // 2)).strip()
        bldg_code = input("Building Code: ".rjust(WIDTH // 2)).strip()
        return room_code, room_type, bldg_code

# -----------------------------------------------------------------
# ADMIN - SUCCESS CREATION
# -----------------------------------------------------------------
def a_success(username="", password="", prof_id="", crs_code="", crs_title="", dept_code="", dept_name="",
              bldg_code="", bldg_name="", room_code="", room_type="", class_code="", stud_id=""):
    """
    Display a success message after creating a record.
    The message content depends on which parameters are provided.
    """
    h.pad()  # Print a divider before the success message
    if username and password:
        # If username and password are provided, assume a user was created.
        print("User created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
    elif crs_code and prof_id:
        # For a class creation, show both class code and professor ID.
        print("Class created successfully!")
        print(f"Class Code: {crs_code}-{prof_id}")
    elif crs_code and crs_title:
        # For course creation, display its code and title.
        print("Course created successfully!")
        print(f"Course Code: {crs_code}")
        print(f"Course Title: {crs_title}")
    elif dept_code and dept_name:
        # For department creation.
        print("Department created successfully!")
        print(f"Department Code: {dept_code}")
        print(f"Department Name: {dept_name}")
    elif class_code and stud_id:
        # For enrollment records, show class code and student ID.
        print("Enrollment created successfully!")
        print(f"Class Code: {class_code}")
        print(f"Student ID: {stud_id}")
    elif bldg_code and bldg_name:
        # For building creation.
        print("Building created successfully!")
        print(f"Building Code: {bldg_code}")
        print(f"Building Name: {bldg_name}")
    elif room_code and room_type:
        # For room creation.
        print("Room created successfully!")
        print(f"Room Code: {room_code}")
        print(f"Room Type: {room_type}")
    input("Press Enter to return...")  # Wait for user input before proceeding

# -----------------------------------------------------------------
# ADMIN - READ, UPDATE, DELETE (RUD)
# -----------------------------------------------------------------
def a_manage(db, table):
    """
    Manage records for the specified table with search, update, and delete options.
    This function displays the records, provides filtering, paging, and allows record
    updates or deletions.
    """
    query = "*"  # Start with a wildcard query meaning "show all"
    page = 0
    searches = db.read(table)  # Retrieve all records from the database
    
    # Map field aliases for nicer display in the output
    if table == "admin":
        aliases = {"admin": {"admin_lname": "Last Name", "admin_fname": "First Name",
                              "admin_username": "Username", "admin_password": "Password"}}
    elif table == "professor":
        aliases = {"professor": {"prof_lname": "Last Name", "prof_fname": "First Name",
                                  "prof_title": "Title", "dept_code": "Dept Code",
                                  "prof_username": "Username", "prof_password": "Password"}}
    elif table == "student":
        aliases = {"student": {"stud_lname": "Last Name", "stud_fname": "First Name",
                                "stud_username": "Username", "stud_password": "Password"}}
    elif table == "department":
        aliases = {"department": {"dept_code": "Department Code", "dept_name": "Department Name"}}
    elif table == "enrollment":
        aliases = {"enrollment": {"enroll_id": "Enrollment ID", "class_code": "Class Code", "stu_id": "Student ID"}}
    elif table == "building":
        aliases = {"building": {"bldg_code": "Building Code", "bldg_name": "Building Name"}}
    elif table == "room":
        aliases = {"room": {"room_code": "Room Code", "room_type": "Room Type", "bldg_code": "Building Code"}}
    
    # Main loop for managing records
    while True:
        h.clear()  # Clear screen before displaying management interface
        print(f" {table.upper()} MANAGE ".center(WIDTH, "="))
        print("Commands: ? = Update     - = Delete     * = Show All     ! = Return to menu     < = Prev page     > = Next page")
        
        # Filter records based on the query
        if query == "*" or query == "":
            filtered = searches
        else:
            if table == "admin":
                filtered = [
                    search for search in searches
                    if (query in str(search[0]).lower() or query in search[1].lower() or
                        query in search[2].lower() or query in search[3].lower() or
                        query in search[4].lower())
                ]
            elif table == "professor":
                filtered = [
                    search for search in searches
                    if (query in str(search[0]).lower() or query in search[1].lower() or
                        query in search[2].lower() or query in search[3].lower() or
                        query in search[4].lower() or query in search[5].lower())
                ]
            elif table == "student":
                filtered = [
                    search for search in searches
                    if (query in str(search[0]).lower() or query in search[1].lower() or
                        query in search[2].lower() or query in search[3].lower())
                ]
            elif (table == "department" or table == "building"):
                filtered = [
                    search for search in searches
                    if query in str(search[0]).lower() or query in search[1].lower()
                ]
            elif (table == "enrollment" or table == "room"):
                filtered = [
                    search for search in searches
                    if (query in str(search[0]).lower() or query in search[1].lower() or
                        query in search[2].lower())
                ]
        
        # Display the table of records (if any match the query)
        if filtered:
            print_table(filtered=filtered, page=page, table=table, db=db)
        else:
            print("No match found.".center(WIDTH))
            print("=" * WIDTH)
        
        h.pad()  # Show footer divider
        new_input = input("Search/Manage: ").strip().lower()
        
        # Check for exit command
        if new_input == "!":
            break
        
        # Pagination controls: next page
        elif new_input == ">":
            if (page + 1) * 15 < len(filtered):
                page += 1
            else:
                input("No more pages. Press Enter to continue...")
            continue
        
        # Pagination controls: previous page
        elif new_input == "<":
            if page > 0:
                page -= 1
            else:
                input("Already at first page. Press Enter to continue...")
            continue
        
        # Handle record updates
        elif new_input == "?":
            record_id = input("Enter the Record ID to update: ").strip()
            if record_id == "":
                input("Record ID/Code cannot be empty. Press Enter to continue...")
                continue
            if not any(str(rec[0]) == record_id for rec in filtered):
                input("Record ID not found in the current results. Press Enter to continue...")
                continue
            record_data = [rec for rec in searches if str(rec[0]) == record_id]
            h.clear()
            print("Record details for update:".center(WIDTH))
            print_table(filtered=record_data, page=0, table=table, db=db)
            
            # For simplicity, only allow updating of one field identified by the table name
            editable_fields = [table]
            print("")
            print("Fields available for update:")
            for i, field in enumerate(editable_fields, start=1):
                alias_name = aliases.get(table, {}).get(field, field)
                print(f"{i}. {alias_name}")
            h.pad()
            field_choice = input("Select field number to update: ").strip()
            try:
                field_index = int(field_choice)
                if field_index < 1 or field_index > len(editable_fields):
                    input("Invalid field selection. Press Enter to continue...")
                    continue
                field = editable_fields[field_index - 1]
            except ValueError:
                input("Invalid field selection. Press Enter to continue...")
                continue
            
            new_value = input(f"Enter new value for {aliases.get(table, {}).get(field, field)}: ").strip()
            if new_value == "":
                input("New value cannot be empty. Press Enter to continue...")
                continue
            db.update(table, record_id, {field: new_value})
            input("Press Enter to continue...")
            # Refresh data after update
            searches = db.read(table)
            query = "*"
            page = 0
            continue
        
        # Handle record deletion
        elif new_input == "-":
            record_id = input("Enter the Record ID to delete: ").strip()
            if record_id == "":
                input("Record ID cannot be empty. Press Enter to continue...")
                continue
            if not any(str(rec[0]) == record_id for rec in filtered):
                input("Record ID not found in the current results. Press Enter to continue...")
                continue
            record_data = [rec for rec in searches if str(rec[0]) == record_id]
            h.clear()
            print("Record details for deletion:".center(WIDTH))
            print_table(filtered=record_data, page=0, table=table, db=db)
            confirm = input("Are you sure you want to delete this record? (y/n): ").strip().lower()
            if confirm != "y":
                input("Deletion cancelled. Press Enter to continue...")
                continue
            db.delete(table, record_id)
            input("Press Enter to continue...")
            # Refresh records after deletion
            searches = db.read(table)
            query = "*"
            page = 0
            continue
        
        else:
            # Any other input is treated as a new search query
            query = new_input
            page = 0

def print_table(filtered, page=0, table="", db=""):
    """
    Print a formatted table for the given set of records with pagination.
    Uses fixed column widths depending on the table type.
    """
    start = page * 15
    end = start + 15
    slice_records = filtered[start:end]

    if table == "admin":
        idw = 6
        namew = 37
        userw = 12
        passw = 12
        print("=" * WIDTH)
        # Print header for admin table
        print(
            f"| {'ID'.ljust(idw)} | {'Last Name'.ljust(namew)} | "
            f"{'First Name'.ljust(namew)} | {'Username'.ljust(userw)} | "
            f"{'Password'.ljust(passw)} |"
        )
        print("=" * WIDTH)
        for admin in slice_records:
            print(
                f"| {str(admin[0]).ljust(idw)} | {admin[1][:namew].ljust(namew)} | "
                f"{admin[2][:namew].ljust(namew)} | {admin[3][:userw].ljust(userw)} | "
                f"{admin[4][:passw].ljust(passw)} |"
            )
        print("=" * WIDTH)

    elif table == "professor":
        idw = 6
        lnamew = 24
        fnamew = 24
        titlew = 10
        userw = 12
        passw = 12
        deptw = 10
        print("=" * WIDTH)
        # Print header for professor table with column labels
        print(
            f"| {'ID'.ljust(idw)} | {'Last Name'.ljust(lnamew)} | {'First Name'.ljust(fnamew)} | "
            f"{'Title'.ljust(titlew)} | {'Username'.ljust(userw)} | {'Password'.ljust(passw)} | {'Dept'.ljust(deptw)} |"
        )
        print("=" * WIDTH)
        for prof in slice_records:
            print(
                f"| {str(prof[0]).ljust(idw)} | {prof[1][:lnamew].ljust(lnamew)} | {prof[2][:fnamew].ljust(fnamew)} | "
                f"{prof[3][:titlew].ljust(titlew)} | {prof[4][:userw].ljust(userw)} | {prof[5][:passw].ljust(passw)} | {prof[6][:deptw].ljust(deptw)} |"
            )
        print("=" * WIDTH)
        
    elif table == "student":
        idw = 6
        namew = 37
        userw = 12
        passw = 12
        print("=" * WIDTH)
        # Print header for student table
        print(
            f"| {'ID'.ljust(idw)} | {'Last Name'.ljust(namew)} | "
            f"{'First Name'.ljust(namew)} | {'Username'.ljust(userw)} | "
            f"{'Password'.ljust(passw)} |"
        )
        print("=" * WIDTH)
        for student in slice_records:
            print(
                f"| {str(student[0]).ljust(idw)} | {student[1][:namew].ljust(namew)} | "
                f"{student[2][:namew].ljust(namew)} | {student[3][:userw].ljust(userw)} | "
                f"{student[4][:passw].ljust(passw)} |"
            )
        print("=" * WIDTH)
        
    elif table == "class":
        idw = 3       # Width for record ID (class_code)
        sectionw = 3  # Width for class section
        timew = 15    # Width for class time
        crs_w = 11    # Width for course code
        titlew = 37   # Width for course title
        profw = 25    # Width for professor name
        roomw = 4     # Width for room code
        # Retrieve lookup dictionaries for professor and course details
        prof_dict = h.get_lookup_dict(db, "professor")
        course_dict = h.get_lookup_dict(db, "course")
        print("=" * WIDTH)
        header = (
            f"| {'ID'.ljust(idw)} | "
            f"{'Sec'.ljust(sectionw)} | "
            f"{'Time'.ljust(timew)} | "
            f"{'Course Code'.ljust(crs_w)} | "
            f"{'Course Title'.ljust(titlew)} | "
            f"{'Professor'.ljust(profw)} | "
            f"{'Room'.ljust(roomw)} |"
        )
        print(header)
        print("=" * WIDTH)
        for rec in slice_records:
            record_id = str(rec[0])
            course_code = str(rec[1])
            prof_id = rec[2]
            section = str(rec[3])
            time_val = str(rec[4])
            room_code = str(rec[5])
            # Look up professor and course title using the helper dictionaries
            professor_name = prof_dict.get(str(prof_id), "Unknown")
            course_title = course_dict.get(course_code, "Unknown")
            print(
                f"| {record_id.ljust(idw)} | "
                f"{section[:sectionw].ljust(sectionw)} | "
                f"{time_val[:timew].ljust(timew)} | "
                f"{course_code[:crs_w].ljust(crs_w)} | "
                f"{course_title[:titlew].ljust(titlew)} | "
                f"{professor_name[:profw].ljust(profw)} | "
                f"{room_code[:roomw].ljust(roomw)} |"
            )
        print("=" * WIDTH)

    elif table == "course":
        codew = 10      # Width for Course Code
        titlew = 36     # Width for Course Title
        descw = 40      # Width for Description
        creditw = 8     # Width for Course Credit
        deptw = 10      # Width for Department Code
        print("=" * WIDTH)
        header = (
            f"| {'Course Code'.ljust(codew)} | "
            f"{'Course Title'.ljust(titlew)} | "
            f"{'Description'.ljust(descw)} | "
            f"{'Credit'.ljust(creditw)} | "
            f"{'Dept Code'.ljust(deptw)} |"
        )
        print(header)
        print("=" * WIDTH)
        for course in slice_records:
            print(
                f"| {str(course[0])[:codew].ljust(codew)} | "
                f"{course[1][:titlew].ljust(titlew)} | "
                f"{course[2][:descw].ljust(descw)} | "
                f"{str(course[3])[:creditw].ljust(creditw)} | "
                f"{str(course[4])[:deptw].ljust(deptw)} |"
            )
        print("=" * WIDTH)

    elif table == "department":
        codew = 9   # Width for Department Code
        namew = 40  # Width for Department Name
        tempwidth = codew + namew + 7
        print("=" * tempwidth)
        header = f"| {'Dept Code'.ljust(codew)} | {'Dept Name'.ljust(namew)} |"
        print(header)
        print("=" * tempwidth)
        for dept in slice_records:
            print(f"| {str(dept[0])[:codew].ljust(codew)} | {dept[1][:namew].ljust(namew)} |")
        print("=" * tempwidth)

    elif table == "enrollment":
        # Retrieve lookup dictionaries for classes, courses, and students for display purposes
        class_dict = h.get_lookup_dict(db, "class")
        courses_dict = h.get_lookup_dict(db, "course")
        students_dict = h.get_lookup_dict(db, "student")
        idw = 10       # Width for Enrollment ID
        classw = 10    # Width for Class Code
        coursew = 20   # Width for Course Name
        studw = 3      # Width for Student ID
        studnamew = 30 # Width for Student Name
        print("=" * WIDTH)
        header = (
            f"| {'Enroll ID'.ljust(idw)} | "
            f"{'Class Code'.ljust(classw)} | "
            f"{'Course Name'.ljust(coursew)} | "
            f"{'SID'.ljust(studw)} | "
            f"{'Student Name'.ljust(studnamew)} |"
        )
        print(header)
        print("=" * WIDTH)
        for enroll in slice_records:
            enroll_id = str(enroll[0])
            class_code = str(enroll[1])
            stud_id = str(enroll[2])
            # Look up additional details for courses and students
            class_rec = class_dict.get(class_code)
            crs_code = str(class_rec[1])
            course_name = courses_dict.get(crs_code, "Unknown")
            student_name = students_dict.get(stud_id, "Unknown")
            print(
                f"| {enroll_id.ljust(idw)} | "
                f"{class_code.ljust(classw)} | "
                f"{course_name.ljust(coursew)} | "
                f"{stud_id.ljust(studw)} | "
                f"{student_name.ljust(studnamew)} |"
            )

    elif table == "building":
        codew = 12
        namew = 25
        tempwidth = codew + namew + 7
        print("=" * tempwidth)
        header = f"| {'Bldg Code'.ljust(codew)} | {'Bldg Name'.ljust(namew)} |"
        print(header)
        print("=" * tempwidth)
        for bldg in slice_records:
            print(f"| {str(bldg[0])[:codew].ljust(codew)} | {bldg[1][:namew].ljust(namew)} |")
        print("=" * tempwidth)

    elif table == "room":
        roomw = 10
        typew = 12
        bldgw = 9
        tempwidth = roomw + typew + bldgw + 10
        print("=" * tempwidth)
        header = f"| {'Room Code'.ljust(roomw)} | {'Room Type'.ljust(typew)} | {'Bldg Code'.ljust(bldgw)} |"
        print(header)
        print("=" * tempwidth)
        for room in slice_records:
            print(f"| {str(room[0])[:roomw].ljust(roomw)} | {room[1][:typew].ljust(typew)} | {str(room[2])[:bldgw].ljust(bldgw)} |")
        print("=" * tempwidth)

    total_records = len(filtered)
    print(f"Showing records {start+1}-{min(end, total_records)} of {total_records}")


# -----------------------------------------------------------------
# ENROLLMENT MANAGEMENT
# -----------------------------------------------------------------
def manage_enrollment(role, db, stud_id=None):
    # Determine the student ID to work with. For admins, allow selection via browse_students.
    if role == "admin":
        selected_stud_id = browse_students(db)
        if not selected_stud_id:
            return
    else:
        selected_stud_id = stud_id

    # Build a credit map from course records, mapping course code (upper case) to its credit value.
    credit_map = {rec[0].upper(): int(rec[3]) for rec in db.read("course") if rec[3]}
    
    while True:
        h.clear()  # Clear the screen before displaying enrollment info.
        # Retrieve lookup dictionaries for students, classes, courses, and professors.
        students_dict = h.get_lookup_dict(db, "student")
        class_dict = h.get_lookup_dict(db, "class")
        courses_dict = h.get_lookup_dict(db, "course")
        prof_dict = h.get_lookup_dict(db, "professor")
        
        # Get the current student's name from the lookup.
        student_name = students_dict.get(str(selected_stud_id))
        # Retrieve all enrollment records; default to an empty list if none.
        all_enrollments = db.read("enrollment") or []
        # Filter enrollments to include only those for the selected student.
        enrollments = [enr for enr in all_enrollments if str(enr[2]) == str(selected_stud_id)]
        
        total_credits = 0
        # Calculate the total credits from the enrolled courses.
        for enr in enrollments:
            class_id = str(enr[1])
            class_rec = class_dict.get(class_id)
            if class_rec:
                crs_code = str(class_rec[1]).upper()
                total_credits += credit_map.get(crs_code, 0)
        
        # Display the enrollment summary.
        print(" ENROLLMENT SUMMARY ".center(WIDTH, "="))
        print(f"Student Name: {student_name}")
        print(f"Total Credits: {total_credits}")
        print("")
        
        # Set fixed column widths.
        enroll_id_w = 3
        time_w = 15
        course_w = 49
        professor_w = 40
        header = (f"| {'EID'.ljust(enroll_id_w)} | "
                  f"{'Time'.ljust(time_w)} | "
                  f"{'Course'.ljust(course_w)} | "
                  f"{'Professor'.ljust(professor_w)} |")
        print("=" * WIDTH)
        print(header)
        print("=" * WIDTH)
        
        # Loop through each enrollment and display its details.
        for enr in enrollments:
            enroll_id = str(enr[0])
            class_id = str(enr[1])
            class_rec = class_dict.get(class_id)
            if class_rec:
                time_str = str(class_rec[4])
                crs_code = str(class_rec[1])
                course_title = courses_dict.get(crs_code, "Unknown")
                course_display = f"{crs_code} - {course_title}"
                prof_id = str(class_rec[2])
                professor_name = prof_dict.get(prof_id, "Unknown")
            else:
                time_str = "N/A"
                course_display = "N/A"
                professor_name = "N/A"
            row = (
                f"| {enroll_id.ljust(enroll_id_w)} | "
                f"{time_str.ljust(time_w)} | "
                f"{course_display.ljust(course_w)} | "
                f"{professor_name.ljust(professor_w)} |"
            )
            print(row)
        print("=" * WIDTH)
        
        print("\nOptions:")
        # If maximum credits reached, disable new enrollment.
        if total_credits >= MAX_UNIT:
            print("Maximum credits (18) reached. New course enrollment is disabled.")
        else:
            print("+: Enroll")
        print("-: Unenroll")
        print("!: Back")
        h.pad()
        option = input("Select an option: ").strip()
        
        if option == "!":
            # For admin role, allow switching to another student.
            if role == "admin":
                new_student = browse_students(db)
                if new_student:
                    selected_stud_id = new_student
                    continue
                else:
                    break
            else:
                break
        elif option == "+":
            # Check if adding a course would exceed the maximum credits.
            if total_credits >= MAX_UNIT:
                input("Cannot enroll new course as maximum credits have been attained. Press Enter to continue...")
                continue
            h.clear()
            print(" ENROLL COURSE ".center(WIDTH, "="))
            print(f"Student Name: {student_name}")
            print(f"Total Credits: {total_credits}")
            print("")
            
            # Refresh lookup dictionaries.
            class_dict = h.get_lookup_dict(db, "class")
            courses_dict = h.get_lookup_dict(db, "course")
            prof_dict = h.get_lookup_dict(db, "professor")
            all_enrollments = db.read("enrollment") or []
            enrollments = [enr for enr in all_enrollments if str(enr[2]) == str(selected_stud_id)]
            
            # If there are enrollments, display them
            if enrollments:
                enroll_id_w = 3
                time_w = 15
                course_w = 49
                prof_w = 40
                header = (
                    f"| {'EID'.ljust(enroll_id_w)} | "
                    f"{'Time'.ljust(time_w)} | "
                    f"{'Course'.ljust(course_w)} | "
                    f"{'Professor'.ljust(prof_w)} |"
                )
                print("=" * WIDTH)
                print(header)
                print("=" * WIDTH)
                for enr in enrollments:
                    enroll_id = str(enr[0])
                    class_id = str(enr[1])
                    class_rec = class_dict.get(class_id)
                    if class_rec:
                        time_str = str(class_rec[4])
                        crs_code = str(class_rec[1])
                        course_title = courses_dict.get(crs_code, "Unknown")
                        course_display = f"{crs_code} - {course_title}"
                        prof_id = str(class_rec[2])
                        professor_name = prof_dict.get(prof_id, "Unknown")
                    else:
                        time_str = "N/A"
                        course_display = "N/A"
                        professor_name = "N/A"
                    row = (
                        f"| {enroll_id.ljust(enroll_id_w)} | "
                        f"{time_str.ljust(time_w)} | "
                        f"{course_display.ljust(course_w)} | "
                        f"{professor_name.ljust(prof_w)} |"
                    )
                    print(row)
                print("=" * WIDTH)
            else:
                print("No current enrollments.".center(WIDTH))
            print("")
            print("Commands: ! = Back")
            course_code = input("Enter Course Code to Enroll: ").strip().upper()
            if course_code == "!":
                continue
            else:
                # Verify that the student is not already enrolled in the selected course.
                enrolled_course_codes = set()
                for enr in enrollments:
                    class_rec = class_dict.get(str(enr[1]))
                    if class_rec:
                        enrolled_course_codes.add(str(class_rec[1]).upper())
                if course_code in enrolled_course_codes:
                    input("You are already enrolled in this course. Press Enter to continue...")
                    continue
                # Find available classes for the course.
                all_classes = db.read("class") or []
                available_classes = [cls for cls in all_classes if str(cls[1]).upper() == course_code]
                available_classes = [
                    cls for cls in available_classes
                    if str(cls[0]) not in [str(enr[1]) for enr in enrollments]
                ]
                if not available_classes:
                    input("No available classes for this course. Press Enter to continue...")
                    continue
                print("")
                print(f"Available classes for Course: {course_code}:".center(WIDTH))
                print("")
                prof_dict = h.get_lookup_dict(db, "professor")
                course_dict = h.get_lookup_dict(db, "course")
                # Define column widths for available classes display.
                col_id = 3
                col_course = 49
                col_section = 7
                col_time = 15
                col_prof = 30
                header = (
                    f"| {'CID'.ljust(col_id)} | "
                    f"{'Course'.ljust(col_course)} | "
                    f"{'Section'.ljust(col_section)} | "
                    f"{'Time'.ljust(col_time)} | "
                    f"{'Professor'.ljust(col_prof)} |"
                )
                print("=" * WIDTH)
                print(header)
                print("=" * WIDTH)
                # Display each available class.
                for cls in available_classes:
                    class_id = str(cls[0])
                    course_code_val = str(cls[1])
                    course_title = course_dict.get(course_code_val, "Unknown")
                    course_str = f"{course_code_val} - {course_title}"
                    section = str(cls[3])
                    time_val = str(cls[4])
                    prof_id = str(cls[2])
                    professor = prof_dict.get(prof_id, "Unknown")
                    row = (
                        f"| {class_id.ljust(col_id)} | "
                        f"{course_str.ljust(col_course)} | "
                        f"{section.ljust(col_section)} | "
                        f"{time_val.ljust(col_time)} | "
                        f"{professor.ljust(col_prof)} |"
                    )
                    print(row)
                print("=" * WIDTH)
                # Complete enrollment by selecting a class.
                selected_class_id = input("\nEnter the Class ID to enroll: ").strip()
                new_enrollment = {"class_id": selected_class_id, "stu_id": selected_stud_id}
                db.create("enrollment", new_enrollment)
                print("")
                input("Enrollment successful! Press Enter to continue...")
        elif option == "-":
            # Unenroll: Delete an existing course enrollment.
            if not enrollments:
                input("No enrollments available to delete. Press Enter to continue...")
                continue
            h.clear()
            print(" UNENROLL COURSE ".center(WIDTH, "="))
            print(f"Student Name: {student_name}")
            print(f"Total Credits: {total_credits}")
            print("")
            del_eid_w = 3
            time_w_d = 15
            course_w_d = 49
            professor_w_d = 40
            del_header = (
                f"| {'EID'.ljust(del_eid_w)} | "
                f"{'Time'.ljust(time_w_d)} | "
                f"{'Course'.ljust(course_w_d)} | "
                f"{'Professor'.ljust(professor_w_d)} |"
            )
            print("=" * WIDTH)
            print(del_header)
            print("=" * WIDTH)
            for enr in enrollments:
                enroll_id = str(enr[0])
                class_id = str(enr[1])
                class_rec = class_dict.get(class_id)
                if class_rec:
                    time_str = str(class_rec[4])
                    crs_code = str(class_rec[1])
                    course_title = courses_dict.get(crs_code, "Unknown")
                    course_display = f"{crs_code} - {course_title}"
                    prof_id = str(class_rec[2])
                    professor_name = prof_dict.get(prof_id, "Unknown")
                else:
                    time_str = "N/A"
                    course_display = "N/A"
                    professor_name = "N/A"
                row = (
                    f"| {enroll_id.ljust(del_eid_w)} | "
                    f"{time_str.ljust(time_w_d)} | "
                    f"{course_display.ljust(course_w_d)} | "
                    f"{professor_name.ljust(professor_w_d)} |"
                )
                print(row)
            print("=" * WIDTH)
            print("")
            print("Commands: ! = Back")
            eid_to_delete = input("Enter the EID to unenroll: ").strip()
            if eid_to_delete == "!":
                continue
            matching = [enr for enr in enrollments if str(enr[0]) == eid_to_delete]
            if not matching:
                input("Invalid EID. Press Enter to return...")
                continue
            selected_enrollment = matching[0]
            confirm = input("Are you sure you want to unenroll this course? (Y/N): ").strip().upper()
            if confirm != "Y":
                input("Unenroll cancelled. Press Enter to return...")
                continue
            db.delete("enrollment", selected_enrollment[0])
            print("")
            input("Enrollment record deleted. Press Enter to continue...")
        else:
            input("Invalid option. Press Enter to continue...")

# -----------------------------------------------------------------
# BROWSE STUDENTS
# -----------------------------------------------------------------
def browse_students(db):
    # Read student records from the database.
    students = db.read("student")
    if not students:
        print("No student records found.")
        input("Press Enter to return...")
        return None
    page = 0
    page_size = 15
    # Set column widths.
    id_w = 6
    lname_w = 20
    fname_w = 20
    tempwidth = id_w + lname_w + fname_w + 10
    filtered_students = students
    while True:
        h.clear()
        print(" STUDENT LIST ".center(WIDTH, "="))
        print("Commands: ? = Search     * = All    < = Previous     > = Next     ! = Back")
        header = f"| {'ID'.ljust(id_w)} | {'Last Name'.ljust(lname_w)} | {'First Name'.ljust(fname_w)} |"
        print("=" * tempwidth)
        print(header)
        print("=" * tempwidth)
        start = page * page_size
        end = start + page_size
        for student in filtered_students[start:end]:
            stud_id = str(student[0])
            stud_lname = student[1]
            stud_fname = student[2]
            print(f"| {stud_id.ljust(id_w)} | {stud_lname.ljust(lname_w)} | {stud_fname.ljust(fname_w)} |")
        print("=" * tempwidth)
        print(f"Showing {start+1}-{min(end, len(filtered_students))} of {len(filtered_students)}")
        h.pad()
        cmd = input("Enter command/ID: ").strip()
        if cmd == "!":
            return None
        elif cmd == "*":
            filtered_students = students
            page = 0
        elif cmd == ">":
            if (page + 1) * page_size < len(filtered_students):
                page += 1
            else:
                input("No more pages. Press Enter to continue...")
        elif cmd == "<":
            if page > 0:
                page -= 1
            else:
                input("Already at first page. Press Enter to continue...")
        elif cmd == "?":
            keyword = input("Enter search keyword: ").strip().lower()
            if keyword:
                filtered_students = [s for s in students if keyword in s[1].lower() or keyword in s[2].lower()]
                if not filtered_students:
                    input("No matching students found. Press Enter to reset search...")
                    filtered_students = students
                page = 0
            else:
                input("Empty search. Press Enter to continue...")
        else:
            if any(str(s[0]) == cmd for s in filtered_students):
                return cmd
            else:
                input("Invalid student ID. Press Enter to try again...")

# -----------------------------------------------------------------
# STUDENT NAVIGATION
# -----------------------------------------------------------------
def s_home(name):
    h.clear()
    print(" STUDENT HOME ".center(WIDTH, "="))
    print("\n")
    print(f"Welcome, {name}!".center(WIDTH))
    print()
    print("Choose an option below.".center(WIDTH))
    print()
    opts = [
        "",
        "1. View Classes     ",
        "2. Manage Enrollment",
        "3. Update Profile   ",
        "",
        "0. Logout           "
    ]
    for o in opts:
        print(o.center(WIDTH))
    h.pad()
    return input("Enter option: ").strip()

def s_view(db):
    """
    Display a list of all classes with schedule and course info.
    Allow navigation using previous and next commands.
    """
    h.clear()
    classes = db.read("class")
    if not classes:
        print("No classes available.".center(WIDTH))
        h.pad()
        input("Press Enter to return...")
        return
    page_size = 10
    page = 0
    # Build lookup dictionaries for professor and course info.
    prof_dict = h.get_lookup_dict(db, "professor")
    course_dict = h.get_lookup_dict(db, "course")
    while True:
        h.clear()
        start = page * page_size
        end = start + page_size
        slice_records = classes[start:end]
        print(" ALL CLASSES ".center(WIDTH, "="))
        print("Commands: < = Prev     > = Next     ! = Back")
        # Define column widths for class table.
        idw = 3
        sectionw = 3
        timew = 15
        crs_w = 11
        titlew = 37
        profw = 25
        roomw = 4
        print("=" * WIDTH)
        header = (
            f"| {'ID'.ljust(idw)} | "
            f"{'Sec'.ljust(sectionw)} | "
            f"{'Time'.ljust(timew)} | "
            f"{'Course Code'.ljust(crs_w)} | "
            f"{'Course Title'.ljust(titlew)} | "
            f"{'Professor'.ljust(profw)} | "
            f"{'Room'.ljust(roomw)} |"
        )
        print(header)
        print("=" * WIDTH)
        for rec in slice_records:
            class_id = str(rec[0])
            course_code = str(rec[1])
            prof_id = rec[2]
            section = str(rec[3])
            time_val = str(rec[4])
            room_code = str(rec[5])
            professor_name = prof_dict.get(str(prof_id), "Unknown")
            course_title = course_dict.get(course_code, "Unknown")
            print(
                f"| {class_id.ljust(idw)} | "
                f"{section[:sectionw].ljust(sectionw)} | "
                f"{time_val[:timew].ljust(timew)} | "
                f"{course_code[:crs_w].ljust(crs_w)} | "
                f"{course_title[:titlew].ljust(titlew)} | "
                f"{professor_name[:profw].ljust(profw)} | "
                f"{room_code[:roomw].ljust(roomw)} |"
            )
        print("=" * WIDTH)
        total_records = len(classes)
        print(f" Showing records {start+1}-{min(end, total_records)} of {total_records}")
        h.pad()
        command = input("Enter command: ").strip().lower()
        if command == ">":
            if end < total_records:
                page += 1
            else:
                input("No more pages. Press Enter to continue...")
        elif command == "<":
            if page > 0:
                page -= 1
            else:
                input("Already at first page. Press Enter to continue...")
        elif command == "!":
            break
        else:
            input("Invalid command. Press Enter to continue...")

def s_update_profile():
    h.clear()
    print(" UPDATE PROFILE ".center(WIDTH, "="))
    print("")
    print("Profile update functionality is not available in the Student view.")
    print("Please contact admin for changes.")
    input("Press Enter to return...")

# -----------------------------------------------------------------
# PROFESSOR NAVIGATION
# -----------------------------------------------------------------
def p_home(name):
    h.clear()
    print(" PROFESSOR HOME ".center(WIDTH, "="))
    print("\n")
    print(f"Welcome, {name}!".center(WIDTH))
    print()
    print("Choose an option below.".center(WIDTH))
    print()
    opts = [
        "",
        "1. View My Classes",
        "2. Update Profile ",
        "",
        "0. Logout         "
    ]
    for o in opts:
        print(o.center(WIDTH))
    h.pad()
    return input("Enter option: ").strip()

def p_view_classes(db, classes, prof_id):
    while True:
        h.clear()
        print(" VIEW MY CLASSES ".center(WIDTH, "="))
        print("Commands: ! = Back")
        if not classes:
            print("No classes found.".center(WIDTH))
        else:
            col_id = 8
            col_code = 11
            col_title = 63
            col_section = 7
            col_time = 15
            print("=" * WIDTH)
            header = (f"| {'Class ID'.ljust(col_id)} | {'Course Code'.ljust(col_code)} | "
                      f"{'Course Title'.ljust(col_title)} | {'Section'.ljust(col_section)} | "
                      f"{'Time'.ljust(col_time)} |")
            print(header)
            print("=" * WIDTH)
            valid_ids = []
            for rec in classes:
                class_id = str(rec[0])
                valid_ids.append(class_id)
                course_code = rec[1]
                course_title = rec[2]
                section = rec[3]
                class_time = rec[4]
                print(f"| {class_id.ljust(col_id)} | {course_code.ljust(col_code)} | "
                      f"{course_title.ljust(col_title)} | {section.ljust(col_section)} | "
                      f"{class_time.ljust(col_time)} |")
            print("=" * WIDTH)
            h.pad()
            choice = input("Enter a Class ID: ").strip()
            if choice == "!":
                break
            elif choice not in valid_ids:
                input("Invalid Class ID. Press Enter to retry...")
                continue
            else:
                matching_class = next(rec for rec in classes if str(rec[0]) == choice)
                selected_course = matching_class[1]
                report_course_roster(db, role="professor", prof_id=prof_id, selected_course=selected_course)

def p_update_profile():
    h.clear()
    print(" UPDATE PROFILE ".center(WIDTH, "="))
    print("")
    print("Profile update functionality is not available in the Professor view.")
    print("Please contact admin for changes.")
    input("Press Enter to return...")