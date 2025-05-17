from controllers.auth_controller import AuthController           # Handles authentication and default admin creation
from controllers.admin_controller import AdminController         # Contains admin functions (create/manage)
from controllers.student_controller import StudentController     # Student-specific functionality
from controllers.professor_controller import ProfController      # Professor-specific functionality
import reports as r                                              # Reporting functions
import views.views as v                                          # User interface views

def main():
    auth = AuthController()  # Initialize authentication; this sets up the database

    while True:
        choice = v.welcome()  # Display welcome screen and grab user input
        if choice == "1":
            username, role, name = auth.login()  # Process login; returns username, role, and display name
            if username and role:
                if role.lower() == "admin":
                    admin_controller = AdminController(auth.db)
                    while True:
                        admin_choice = v.a_home(name)  # Display the admin home screen with options
                        if admin_choice == "0":
                            break  # Exit admin menu
                        elif admin_choice == "10":
                            r.reports_menu(auth.db)  # Open the reports sub-menu
                        elif admin_choice in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                            # Map admin choices to corresponding table names
                            mapping = {
                                "1": "admin",
                                "2": "professor",
                                "3": "student",
                                "4": "class",
                                "5": "course",
                                "6": "department",
                                "7": "building",
                                "8": "room",
                                "9": "enrollment"
                            }
                            table = mapping[admin_choice]
                            if admin_choice == "9":
                                # Enrollment management is handled separately
                                v.a_home_crud(table, auth.db)
                            else:
                                # Present CRUD (Create/Manage) submenu for the chosen table
                                while True:
                                    sub_choice = v.a_home_crud(table)
                                    if sub_choice == "1":
                                        admin_controller.create(table)
                                    elif sub_choice == "2":
                                        admin_controller.manage(table)
                                    elif sub_choice == "0":
                                        break  # Exit the CRUD submenu
                        else:
                            input("Invalid admin option. Press Enter to try again...")
                elif role.lower() == "professor":
                    # Instantiate Professor controller and pass the username
                    prof_controller = ProfController(auth.db, username)
                    prof_controller.home(name)
                elif role.lower() == "student":
                    # Instantiate Student controller and pass the username
                    student_controller = StudentController(auth.db, username)
                    student_controller.home(name)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
