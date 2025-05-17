import os
from views.views import s_home, s_update_profile, manage_enrollment, s_view

class StudentController:
    def __init__(self, db, username):
        # Initialize with the database instance and retrieve the student's ID.
        self.db = db
        self.username = username
        self.stud_id = db.get_student_id(username)

    def home(self, name):
        """Display the student home menu and route choices."""
        while True:
            # Clear the screen based on the operating system.
            os.system("cls" if os.name == "nt" else "clear")
            choice = s_home(name)  # Display the home menu and capture user selection.
            if choice == "1":
                self.view_classes()  # View classes listing.
            elif choice == "2":
                self.manage_enrollment()  # Manage enrollment.
            elif choice == "3":
                self.update_profile()  # Update profile.
            elif choice == "0":
                break  # Logout and exit the loop.
            else:
                input("Invalid option. Press Enter to continue...")

    def view_classes(self):
        """Delegate to the view function that lists available classes."""
        s_view(self.db)

    def manage_enrollment(self):
        """
        Invoke the centralized enrollment management function.
        This call filters records to show only those pertaining to the student.
        """
        manage_enrollment(role="student", db=self.db, stud_id=self.stud_id)

    def update_profile(self):
        """Delegate to the view function that handles profile updates."""
        s_update_profile()
