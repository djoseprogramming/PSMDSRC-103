from views.views import a_create, a_success, a_manage
from utils.helpers import generate_username, generate_password

class AdminController:
    def __init__(self, db):
        self.db = db

    def create(self, table):
        """Create a record based on the specified table type."""
        if table == "admin":
            admin_lname, admin_fname = a_create(table)
            admin_username = generate_username("admin", admin_lname, admin_fname)
            admin_password = generate_password()
            new_admin = {
                "admin_lname": admin_lname,
                "admin_fname": admin_fname,
                "admin_username": admin_username,
                "admin_password": admin_password
            }
            self.db.create("admin", new_admin)
            a_success(username=admin_username, password=admin_password)

        elif table == "professor":
            # Process professor creation.
            prof_lname, prof_fname, prof_title, dept_code = a_create(table)
            prof_username = generate_username("professor", prof_lname, prof_fname)
            prof_password = generate_password()
            new_prof = {
                "prof_lname": prof_lname,
                "prof_fname": prof_fname,
                "prof_title": prof_title,
                "prof_username": prof_username,
                "prof_password": prof_password,
                "dept_code": dept_code
            }
            self.db.create("professor", new_prof)
            a_success(username=prof_username, password=prof_password)

        elif table == "student":
            # Process student creation.
            stud_lname, stud_fname = a_create(table)
            stud_username = generate_username("student", stud_lname, stud_fname)
            stud_password = generate_password()
            new_stud = {
                "stud_lname": stud_lname,
                "stud_fname": stud_fname,
                "stud_username": stud_username,
                "stud_password": stud_password,
            }
            self.db.create("student", new_stud)
            a_success(username=stud_username, password=stud_password)

        elif table == "class":
            # Process class creation.
            crs_code, prof_id, class_section, class_time, room_code, sem_code = a_create(table)
            new_class = {
                "crs_code": crs_code,
                "prof_id": prof_id,
                "class_section": class_section,
                "class_time": class_time,
                "room_code": room_code,
                "sem_code": sem_code,
            }
            self.db.create("class", new_class)
            a_success(crs_code=crs_code, prof_id=prof_id)

        elif table == "course":
            # Process course creation.
            crs_code, crs_title, crs_description, crs_credit, dept_code = a_create(table)
            new_course = {
                "crs_code": crs_code,
                "crs_title": crs_title,
                "crs_description": crs_description,
                "crs_credit": crs_credit,
                "dept_code": dept_code,
            }
            self.db.create("course", new_course)
            a_success(crs_code=crs_code, crs_title=crs_title)

        elif table == "department":
            # Process department student creation.
            dept_code, dept_name = a_create(table)
            new_dept = {
                "dept_code": dept_code,
                "dept_name": dept_name,
            }
            self.db.create("department", new_dept)
            a_success(dept_code=dept_code, dept_name=dept_name)

        elif table == "building":
            # Process building creation.
            bldg_code, bldg_name = a_create(table)
            new_building = {
                "bldg_code": bldg_code,
                "bldg_name": bldg_name
            }
            self.db.create("building", new_building)
            a_success(bldg_code=bldg_code, bldg_name=bldg_name)

        elif table == "room":
            # Process room creation.
            room_code, room_type, bldg_code = a_create(table)
            new_room = {
                "room_code": room_code,
                "room_type": room_type,
                "bldg_code": bldg_code
            }
            self.db.create("room", new_room)
            a_success(room_code=room_code, room_type=room_type)
  
        elif table == "enrollment":
            # Process enrollment creation.
            class_code, stu_id = a_create(table, self.db)
            new_enrollment = {
                "class_code": class_code,
                "stu_id": stu_id
            }
            self.db.create("enrollment", new_enrollment)
            a_success(enroll_class_code=class_code, enroll_stu_id=stu_id)
            
    def manage(self, table):
        """Delegate record updates to the view layer."""
        a_manage(self.db, table)

