import random
import string
import psycopg2
from datetime import datetime

def generate_login():
    unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"student_{unique_id}"

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def create_user(conn, cursor, student):
    login = student["username"]
    password = student["password"]
    
    cursor.execute(
        """
        INSERT INTO users_user (email, password, is_superuser, is_active, is_staff)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """,
        (login, password, False, True, False, )
    )
    user_id = cursor.fetchone()[0]
    conn.commit()
    return user_id

def create_student(conn, cursor, student):
    user_id = create_user(conn, cursor, student)
    
    cursor.execute(
        """
        INSERT INTO users_student (user, first_name, middle_name, last_name, date_birthday, is_learning, is_headman, guardian, group, date_input, date_output, sub_groups)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            user_id,
            student.get("first_name"),
            student.get("middle_name"),
            student.get("last_name"),
            student.get("date_birthday"),
            student.get("is_learning"),
            student.get("is_headman"),
            student.get("guardian"),
            student.get("group"),
            student.get("date_input"),
            student.get("date_output"),
            student.get("sub_groups"),
        )
    )
    conn.commit()
    return user_id
