import sqlite3
import csv      
import os       
import pandas as pd

class Database:
    def __init__(self):
        # Connect to the SQLite database and create a cursor for executing SQL commands.
        self.conn = sqlite3.connect("minicollege.db")
        self.cursor = self.conn.cursor()

    def instantiate(self):
        """Instantiate tables if they don't exist, ensuring rollback on error."""
        try:
            # Using a transaction block to execute multiple SQL statements.
            with self.conn:
                self.cursor.executescript("""
                    CREATE TABLE IF NOT EXISTS admin (
                        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin_lname TEXT,
                        admin_fname TEXT,
                        admin_username TEXT UNIQUE,
                        admin_password TEXT
                    );
                    CREATE TABLE IF NOT EXISTS student (
                        stud_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        stud_lname TEXT,
                        stud_fname TEXT,
                        stud_username TEXT UNIQUE,
                        stud_password TEXT
                    );
                    CREATE TABLE IF NOT EXISTS department (
                        dept_code TEXT PRIMARY KEY,
                        dept_name TEXT
                    );
                    CREATE TABLE IF NOT EXISTS professor (
                        prof_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        prof_lname TEXT,
                        prof_fname TEXT,
                        prof_title TEXT,
                        dept_code TEXT,
                        prof_username TEXT UNIQUE,
                        prof_password TEXT,
                        FOREIGN KEY (dept_code) REFERENCES department(dept_code)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                    );
                    CREATE TABLE IF NOT EXISTS course (
                        crs_code TEXT PRIMARY KEY,
                        crs_title TEXT,
                        crs_description TEXT,
                        crs_credit TEXT,
                        dept_code TEXT,
                        FOREIGN KEY (dept_code) REFERENCES department(dept_code)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                    );
                    CREATE TABLE IF NOT EXISTS enrollment (
                        enroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        class_id INTEGER NOT NULL,
                        stu_id INTEGER NOT NULL,
                        UNIQUE (class_id, stu_id),
                        FOREIGN KEY (class_id) REFERENCES class(class_id)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
                        FOREIGN KEY (stu_id) REFERENCES student(stud_id)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                    );
                    CREATE TABLE IF NOT EXISTS class (
                        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        crs_code TEXT NOT NULL,
                        prof_id INTEGER NOT NULL,
                        class_section TEXT,
                        class_time TEXT,
                        room_code TEXT,
                        sem_code TEXT,
                        FOREIGN KEY (crs_code) REFERENCES course(crs_code)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
                        FOREIGN KEY (prof_id) REFERENCES professor(prof_id)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
                        FOREIGN KEY (room_code) REFERENCES room(room_code)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
                        FOREIGN KEY (sem_code) REFERENCES semester(sem_code)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                    );
                    CREATE TABLE IF NOT EXISTS building (
                        bldg_code TEXT PRIMARY KEY,
                        bldg_name TEXT
                    );
                    CREATE TABLE IF NOT EXISTS room (
                        room_code TEXT PRIMARY KEY,
                        room_type TEXT,
                        bldg_code TEXT,
                        FOREIGN KEY (bldg_code) REFERENCES building(bldg_code)
                            ON UPDATE CASCADE ON DELETE RESTRICT
                    );
                """)
                print("Tables instantiated successfully.")

                # Import CSV data if not previously imported.
                if not os.path.exists("csv_import_done.txt"):
                    self.import_csv_data()
                    with open("csv_import_done.txt", "w") as flag_file:
                        flag_file.write("CSV import done.")

        except sqlite3.Error as e:
            self.conn.rollback()  # Rollback if any error occurs during instantiation.
            print(f"Database instantiation failed: {e}")

    def import_csv_data(self):
        """
        Import CSV data into each table from the ./database/ directory.
        CSV files should be named as table_name.csv.
        """
        tables = [
            'student',
            'department',
            'professor',
            'course',
            'enrollment',
            'class',
            'building',
            'room'
        ]
        csv_dir = "database"

        try:
            # Begin transaction for CSV import.
            with self.conn:
                for table in tables:
                    filepath = os.path.join(csv_dir, f"{table}.csv")
                    if os.path.exists(filepath):
                        print(f"Importing data for table '{table}' from {filepath}")
                        with open(filepath, newline='', encoding="utf-8") as csvfile:
                            reader = csv.reader(csvfile)
                            try:
                                columns = next(reader)  # Get header row containing column names.
                            except StopIteration:
                                continue  # Skip empty CSV files.
                            placeholders = ", ".join(["?"] * len(columns))
                            col_names = ", ".join(columns)
                            query = f"INSERT OR IGNORE INTO {table} ({col_names}) VALUES ({placeholders})"
                            # Insert each row from CSV into the table.
                            for row in reader:
                                self.cursor.execute(query, row)
                    else:
                        print(f"CSV file for table '{table}' not found at {filepath}.")
                print("CSV data import complete.")
        except sqlite3.Error as e:
            self.conn.rollback()  # Rollback if any error occurs during CSV import.
            print(f"CSV data import failed: {e}")

    def create(self, table, data):
        """
        Insert a new record into the specified table with rollback handling.
        Returns the last inserted row ID or None if the operation fails.
        """
        try:
            with self.conn:
                # Prepare column names and placeholders for SQL query.
                columns = ", ".join(data.keys())
                placeholders = ", ".join("?" for _ in data)
                query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"
                self.cursor.execute(query, tuple(data.values()))
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Create operation failed for {table}: {e}")
            return None

    def read(self, table=None):
        """
        Read records from the database.
        """
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records or []

    def update(self, table, record_id, updates):
        """
        Update a record in the specified table.
        Uses a mapping of primary keys to identify the record.
        Returns True if successful, False otherwise.
        """
        primary_keys = {
            "admin": "admin_id",
            "student": "stud_id",
            "professor": "prof_id",
            "course": "crs_code",
            "department": "dept_code",
            "enrollment": "enroll_id",
            "class": "class_id",
            "building": "bldg_code",
            "room": "room_code"
        }
        # Get the primary key field for the table.
        pk = primary_keys.get(table)

        if not updates:
            print("No fields provided for update.")
            return False
        # Build the SET clause parts.
        query_parts = [f"{col} = ?" for col in updates.keys()]
        query = f"UPDATE {table} SET {', '.join(query_parts)} WHERE {pk} = ?"
        parameters = list(updates.values()) + [record_id]

        try:
            with self.conn:
                self.cursor.execute(query, tuple(parameters))
                print(f"Successfully updated {table} (ID: {record_id}).")
                return True
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Database error: {e}. Changes have been rolled back.")
            return False

    def delete(self, table, record_id):
        """
        Delete a record from a table based on its primary key.
        Returns True if a record was deleted, False otherwise.
        """
        primary_keys = {
            "admin": "admin_id",
            "student": "stud_id",
            "professor": "prof_id",
            "course": "crs_code",
            "department": "dept_code",
            "enrollment": "enroll_id",
            "class": "class_id",
            "building": "bldg_code",
            "room": "room_code"
        }
        pk = primary_keys.get(table)
        query = f"DELETE FROM {table} WHERE {pk} = ?"

        try:
            with self.conn:
                self.cursor.execute(query, (record_id,))
                if self.cursor.rowcount > 0:
                    print(f"Successfully deleted record {record_id} from {table}.")
                    return True
                else:
                    print(f"No matching record found in {table} for ID {record_id}.")
                    return False
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Database error: {e}. Changes have been rolled back.")
            return False

    def get_user(self, username, password):
        """
        Validates user credentials across admin, professor, and student tables.
        Returns (table, user_name) on success or (None, None) if authentication fails.
        """
        credential_fields = {
            "admin": ("admin_username", "admin_password", "admin_fname"),
            "professor": ("prof_username", "prof_password", "prof_fname"),
            "student": ("stud_username", "stud_password", "stud_fname")
        }
        username_lower = username.lower()
        for table, (user_field, pass_field, name_field) in credential_fields.items():
            query = f"SELECT {name_field} FROM {table} WHERE LOWER({user_field})=? AND {pass_field}=?"
            self.cursor.execute(query, (username_lower, password))
            row = self.cursor.fetchone()
            if row:
                return table.capitalize(), row[0]
        return None, None

    def get_professor_id_by_username(self, username):
        # Retrieve the professor's ID given their unique username.
        query = "SELECT prof_id FROM professor WHERE prof_username = ?"
        self.cursor.execute(query, (username,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_professor_classes(self, prof_id):
        # Retrieve classes taught by the professor along with course info.
        query = """
            SELECT class.class_id, course.crs_code, course.crs_title, class.class_section, class.class_time
            FROM class
            JOIN course ON class.crs_code = course.crs_code
            WHERE class.prof_id = ?
            ORDER BY class.class_id;
        """
        self.cursor.execute(query, (prof_id,))
        return self.cursor.fetchall()
    
    def get_course_title(self, course_code):
        # Return the title of a course given its code.
        self.cursor.execute("SELECT crs_title FROM course WHERE crs_code = ?", (course_code,))
        row = self.cursor.fetchone()
        return row[0] if row else ""
    
    def get_professors_by_course(self, course_code):
        # Get a distinct list of professors teaching a specific course.
        query = """
            SELECT DISTINCT professor.prof_id, professor.prof_fname, professor.prof_lname
            FROM class
            JOIN professor ON class.prof_id = professor.prof_id
            WHERE class.crs_code = ?
            ORDER BY professor.prof_lname;
        """
        self.cursor.execute(query, (course_code,))
        return self.cursor.fetchall()

    def count_classes_by_course_and_prof(self, course_code, prof_id):
        # Count the number of classes for a given course and professor.
        self.cursor.execute("SELECT COUNT(*) FROM class WHERE crs_code = ? AND prof_id = ?",
                            (course_code, prof_id))
        return self.cursor.fetchone()[0]

    def get_professor_fullname(self, prof_id):
        # Retrieve the full name (first and last) for a professor.
        self.cursor.execute("SELECT prof_fname, prof_lname FROM professor WHERE prof_id = ?", (prof_id,))
        row = self.cursor.fetchone()
        return f"{row[0]} {row[1]}" if row else "Unknown"

    def get_enrolled_students(self, course_code, prof_id):
        # Retrieve students enrolled in a class for a specific course and professor.
        query = """
            SELECT student.stud_id, student.stud_fname, student.stud_lname
            FROM enrollment
            JOIN class ON enrollment.class_id = class.class_id
            JOIN student ON enrollment.stu_id = student.stud_id
            WHERE class.crs_code = ? AND class.prof_id = ?
            ORDER BY student.stud_id;
        """
        self.cursor.execute(query, (course_code, prof_id))
        return self.cursor.fetchall()

    def get_student_timetable(self, stud_id):
        """
        Retrieve the timetable for a student by joining enrollment, class, course,
        and professor data.
        """
        query = """
            SELECT
                course.crs_code,
                course.crs_title,
                class.class_time,
                (professor.prof_fname || ' ' || professor.prof_lname) AS professor_name
            FROM enrollment
            JOIN class ON enrollment.class_id = class.class_id
            JOIN course ON class.crs_code = course.crs_code
            LEFT JOIN professor ON class.prof_id = professor.prof_id
            WHERE enrollment.stu_id = ?
            ORDER BY course.crs_code;
        """
        self.cursor.execute(query, (stud_id,))
        return self.cursor.fetchall()

    def get_course_credit_map(self):
        """
        Build and return a dictionary mapping course codes (uppercased) to their credit values.
        """
        query = "SELECT crs_code, crs_credit FROM course"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return {row[0].upper(): int(row[1]) for row in rows if row[1]}
    
    def get_student_id(self, username):
        """
        Retrieve the student ID given a student username.
        """
        self.cursor.execute("SELECT stud_id FROM student WHERE stud_username = ?", (username,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_department_summary(self):
        """
        Retrieve department summary data including the number of courses, enrollments,
        and average class size per department.
        Returns a pandas DataFrame with the result.
        """
        query = """
        SELECT 
            department.dept_code AS dept_id,
            department.dept_name AS department_name,
            COUNT(DISTINCT class.class_id) AS num_classes,
            COUNT(enrollment.enroll_id) AS num_enrollments,
            CASE 
                WHEN COUNT(DISTINCT class.class_id) > 0 
                    THEN ROUND(COUNT(enrollment.enroll_id) * 1.0 / COUNT(DISTINCT class.class_id), 2)
                ELSE 0
            END AS avg_class_size
        FROM department
        LEFT JOIN course ON department.dept_code = course.dept_code
        LEFT JOIN class ON course.crs_code = class.crs_code
        LEFT JOIN enrollment ON class.class_id = enrollment.class_id
        GROUP BY department.dept_code
        ORDER BY department.dept_code;
        """
        df = pd.read_sql_query(query, self.conn)
        return df

    def close(self):
        # Close the database connection.
        self.conn.close()
