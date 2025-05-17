import os
import pwinput
from config import WIDTH
import utils.helpers as h
from database import Database

class AuthController:
    def __init__(self):
        # Initialize the database and ensure a default admin exists.
        self.db = Database()
        self.db.instantiate()
        self.default_admin()

    def default_admin(self):
        """Insert a default admin record if none exists."""
        # Check if any admin record exists.
        self.db.cursor.execute("SELECT * FROM admin")
        if not self.db.cursor.fetchone():
            # Define default admin credentials.
            default_admin = {
                "admin_lname": "LastName",
                "admin_fname": "FirstName",
                "admin_username": "admin",
                "admin_password": "admin"
            }
            self.db.create("admin", default_admin)
            print("Default admin created. Username: admin, Password: admin")
            input("Press Enter to continue...")

    def login(self):
        """
        Prompt the user for credentials and validate against admin, professor,
        or student records. Returns a tuple of (username, role, name) on success.
        """
        while True:
            # Clear the screen and display the login header.
            os.system("cls" if os.name == "nt" else "clear")
            print("\n" * 3)
            texts = [
                "=== LOGIN ===",
                "",
                "Enter your credentials below...",
                ""
            ]
            for text in texts:
                print(text.center(WIDTH))
            print("Username: ".rjust(WIDTH // 2), end="")
            username = input().strip().lower()
            # Use pwinput to securely prompt for a masked password.
            password = pwinput.pwinput(prompt="Password: ".rjust(WIDTH // 2), mask="*")
            h.pad()  # Adds layout padding for cleaner output.
            role, name = self.db.get_user(username, password)
            if role:
                input(f"Welcome, {role.title()} {name.upper()}! Press Enter to continue... ")
                return username, role, name
            # Ask the user if they want to retry on invalid credentials.
            retry = input("Invalid credentials. Retry [Yes/No]? ").strip().lower()
            if retry not in {"yes", "y"}:
                return None, None, None
