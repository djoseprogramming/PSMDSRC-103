# MicroUni Enrollment System

A CLI-based enrollment system that supports multiple user roles—admin, professor, and student. This project demonstrates modular Python design with clear separation between database operations, business logic, user interface, reporting, and utility functions.
## Table of Contents
- [Project Overview](#project-overview)
- [Video Demo](#video-demo)
- [Features](#features)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Reports & Average Students per Class](#reports--average-students-per-class)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)
- [License](#license)

## Project Overview

This MicroUni enrollment system is a command-line application that allows administrators to create and manage records for users (admins, professors, and students), classes, courses, departments, enrollments, and room/building details. Each user role has tailored functionality, and the application includes comprehensive reporting features.

## Video Demo
Youtube: [https://youtu.be/w2y9RMOzJnM](https://youtu.be/uAHaOJp1Xzg)

## Features

- **User Authentication:** Logs in users and routes them based on their role.
- **Modular Design:** Separates concerns into dedicated modules: database, controllers, views, reports, utilities, and configuration.
- **Robust Database Operations:** Performs CRUD operations with transaction handling and rollback for data integrity.
- **CSV Data Import:** Automatically imports initial data if available.
- **Comprehensive Reporting:** Provides department summary reports that reflect the latest update—calculating the average students per class.
- **Interactive CLI Navigation:** User-friendly, paginated menus for managing large datasets.

## Project Structure

- **Main Module (`main.py`):**  
  Acts as the entry point and coordinator—it initializes the environment (database and default admin), displays the welcome screen, and then directs users to role-specific controllers or the reports module.

- **Database Module (`database.py`):**  
  Contains the `Database` class which encapsulates all CRUD operations, CSV data import, table instantiation, and transactional integrity. It also uses Pandas for post-query processing in reporting.

- **Controllers:**  
  - **Admin Controller (`admin_controller.py`):** Manages system-level record creation and enrollment operations.  
  - **Professor Controller (`prof_controller.py`):** Handles professor-specific functions like viewing classes.
  - **Student Controller (`student_controller.py`):** Provides student functionalities such as class browsing and enrollment management.

- **Views (`views.txt`):**  
  Implements user interface functions to display menus, paginate listings, and prompt for user input.

- **Reports Module (`reports.py`):**  
  Generates analytics and visualizations (like department summaries) using formatted tables and Matplotlib bar charts.

- **Utils/Helpers (`utils/helpers.py`):**  
  Offers utility functions for tasks such as screen clearing, padding output, browsing data, and generating usernames/passwords.

- **Config Module (`config.txt`):**  
  Stores project constants like terminal dimensions, database filename, and other configuration variables.

## Database Schema

The schema consists of well-defined tables for:
- **Admin, Student, Professor,** and **Department**
- **Course** (linked to departments)
- **Class** (associates courses with professors and schedules)
- **Enrollment** (links classes with students and enforces uniqueness)
- **Building** and **Room** (for class location management)

Foreign key constraints enforce referential integrity across tables.

## Reports & Average Students per Class

The reporting module includes a department summary report. In the latest update, the calculation has been refined to compute the average number of students per class instead of per course. This change provides a more accurate reflection of class-level enrollment activity across departments and is incorporated into the department summary analysis.

## Setup & Installation

1. **Requirements:**
   - Python 3.x
   - SQLite3 (bundled with Python)
   - Python packages: `pwinput`, `pandas`, `matplotlib`

2. **Installation:**
   - Clone the repository.
   - Install the dependencies using:
     ```bash
     pip install pwinput pandas matplotlib
     ```

3. **Running the Application:**
   - Launch the application by running:
     ```bash
     python main.py
     ```

## Usage

- **Authentication:**  
  Start at the welcome screen to log in as admin, professor, or student. (Changed the initial credentials to UN/PW: admin)
  
- **Admin Functions:**  
  Create and manage records (students, professors, courses, etc.) and view enrollment details.
  
- **Professor & Student Functions:**  
  Professors can view their class rosters while students can browse classes and manage enrollments.
  
- **Reporting:**  
  Access the reports module from the admin menu to view department summaries and visualizations and can be exported to CSV.

## Future Improvements

- Enhance security by implementing password hashing.
- Add more advanced search and filtering capabilities.
- Extend the update functionalities for professor and student profiles.
- Consider a graphical user interface (GUI) for improved usability.

## License

This project is provided "as is" without warranty of any kind.
