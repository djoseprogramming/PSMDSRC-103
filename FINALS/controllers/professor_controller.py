import os
from config import WIDTH
from views.views import p_home, p_view_classes, p_update_profile

class ProfController:
    def __init__(self, db, username):
        """
        Initialize the controller with the database instance and locate
        the professor's record using the provided username.
        """
        self.db = db
        self.username = username
        self.prof_id = self.db.get_professor_id_by_username(self.username)
    
    def home(self, name):
        """
        Display the professor's homepage and route based on user selection.
        """
        while True:
            os.system("cls")  # Clear the screen.
            choice = p_home(name)  # Show homepage view and get user option.
            if choice == "1":
                self.view_classes()  # Display classes taught by the professor.
            elif choice == "2":
                self.update_profile()  # Handle profile update (via view).
            elif choice == "0":
                break  # Exit the homepage loop.
            else:
                input("Invalid option. Press Enter to try again...")  # Prompt for a valid option.
    
    def view_classes(self):
        """
        Retrieve the list of classes the professor teaches and delegate display to the view.
        """
        if not self.prof_id:
            os.system("cls")
            print("Error: Professor record not found. Please contact admin.".center(WIDTH))
            input("Press Enter to return...")
            return
        
        classes = self.db.get_professor_classes(self.prof_id)
        p_view_classes(self.db, classes, self.prof_id)  # Delegate display to the view.
    
    def update_profile(self):
        """
        Direct profile update is not available; delegate display to the view.
        """
        p_update_profile()  # Display the profile update view.
