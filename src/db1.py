import sqlite3
import bcrypt
from datetime import datetime as dt
import re
import os
#************************* I.Designing database schema and stablishing constraints ****************************# 
#------------------------------------------- I-1- User table --------------------------------------------------#
# 1-1- user_name must be consisting of only english alphabets and numbers but no space or other special/printed characters
# 1-2- password must be a valid password (at least 8 characters, at least one digit, at least one lower letter, at least one upper letter and at least one special character)
# 1-3- first_name must be consisting of only english alphabets and dash(-) and space but no digits or other special/printed characters
# 1-4- last_name must be consisting of only english alphabets and dash(-) and space but no digits or other special/printed characters
# 1-5- email must be a valid email (no consecutive dots, not more than one @,...)

# Validate username
def is_username(text):
    match = re.search(r"^[a-zA-Z0-9]+$", text)
    if match:
        return True
    return False

# Validate names
def is_name(text):
    match = re.search(r"^[a-zA-Z\- ]+$", text)
    if match:
        return True
    return False

# Validate password
def is_password(text):  
    match = re.search(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*.!@\$%#\^&\(\)\{\}\[\]:;\<\>,.\?\/~_+=\|\-]).{8,}$", text)
    if match:
        return True
    return False
    
# Validate email
def is_email(text):  
    pattern_match = re.search(r"^([a-z0-9\._+&%#-]+)@([0-9a-z\.-]+)\.([a-z]{2,6})$", text, re.IGNORECASE)
    consec_dots_match = re.search(r"^([a-z0-9\._+@&%#-]*)(\.{2})([a-z0-9\._+@&%#-]*)$", text, re.IGNORECASE)
    init_dot_match = re.search(r"^\.([a-z0-9\._+@&%#-]*)$", text, re.IGNORECASE)
    mid_dot_left_match = re.search(r"^([a-z0-9\._+&%#-]+)\.@([a-z0-9\.-]+)$", text, re.IGNORECASE)
    mid_dot_right_match = re.search(r"^([a-z0-9\._+&%#-]+)@\.([a-z0-9\.-]+)$", text, re.IGNORECASE)
    if pattern_match and not consec_dots_match and not init_dot_match  \
                    and not mid_dot_left_match and not mid_dot_right_match:
        return True
    return False

def create_user_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_name TEXT PRIMARY KEY NOT NULL CHECK (user_name REGEXP '^[a-zA-Z0-9]+$'),
        hashed_password TEXT NOT NULL,
        first_name TEXT NOT NULL CHECK (first_name REGEXP '^[a-zA-Z\- ]+$'),
        last_name TEXT NOT NULL CHECK (last_name REGEXP '^[a-zA-Z\- ]+$'),
        email TEXT CHECK (email IS NULL OR email REGEXP '^([a-z0-9\._+&%#-]+)@([0-9a-z\.-]+)\.([a-z]{2,6})$'),           
        registration_date TEXT NOT NULL,
        registration_time TEXT NOT NULL       
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    return "User table created successfully."

def insert_user(user_name, password, first_name, last_name, email=None):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate user inputs
    if not is_username(user_name):
        return "Invalid username format."
        
    if not is_password(password):
        return "Invalid password format."
        
    if not is_name(first_name) or not is_name(last_name):
        return "Invalid name format."
        
    if email and not is_email(email):
        return "Invalid email format."
    
    # Prevent unique user_name violation
    users = [u[0] for u in cursor.execute("SELECT user_name FROM User").fetchall()]
    if user_name in users:
        cursor.close()
        connection.close()
        return "Username already exists."
        
    # generate a random salt for hashing password
    salt=bcrypt.gensalt(rounds=12)
    # hash password
    hashed_password = bcrypt.hashpw(bytes(password,encoding='utf-8'), salt)
    # get registeration date and time in ISO format
    registration_date, registration_time = dt.now().isoformat().split("T")

    sql = """ INSERT INTO User (user_name, hashed_password, first_name, last_name, email,
                        registration_date, registration_time) VALUES 
                        (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(sql, (user_name, hashed_password, first_name, last_name, email, registration_date, registration_time))

    connection.commit()
    cursor.close()
    connection.close()
    return "User info inserted successfully."

def fetch_usernames():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Query user first and last name from the database
    cursor.execute("SELECT user_name FROM User")
    usernames = [x[0] for x in cursor.fetchall()]

    connection.close()
    return usernames

def update_user(user_name, password, first_name, last_name, email=None):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate user inputs
    if not is_username(user_name):
        return "Invalid username format."
        
    if not is_password(password):
        return "Invalid password format."
        
    if not is_name(first_name) or not is_name(last_name):
        return "Invalid name format."
        
    if email and not is_email(email):
        return "Invalid email format."
    
    # Validate user existence
    users = [u[0] for u in cursor.execute("SELECT user_name FROM User").fetchall()]
    if user_name not in users:
        cursor.close()
        connection.close()
        return "User not registered."
        
    # generate a random salt for hashing password
    salt=bcrypt.gensalt(rounds=12)
    # hash password
    hashed_password = bcrypt.hashpw(bytes(password,encoding='utf-8'), salt)

    sql = """ UPDATE User
              SET hashed_password = ?, first_name = ?, last_name = ?, email =?
              WHERE user_name = ?"""
    cursor.execute(sql, (hashed_password, first_name, last_name, email, user_name))

    connection.commit()
    cursor.close()
    connection.close()
    return "User info updated successfully."

def delete_user(user_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate user inputs
    if not is_username(user_name):
        return "Invalid username format."
    
    # Validate user existence
    users = [u[0] for u in cursor.execute("SELECT user_name FROM User").fetchall()]
    if user_name not in users:
        cursor.close()
        connection.close()
        return "User not registered."

    sql = "DELETE FROM User WHERE user_name = ?"
    cursor.execute(sql, (user_name, ))

    connection.commit()
    cursor.close()
    connection.close()
    return "User deleted successfully."
#------------------------------------------- I-2- Role table --------------------------------------------------#
# role_name must be consisting of only english alphabets and underscore(_) but no digits, spaces or other special/printed characters

# Validate role/permission
def is_role_permission(text):  
    match = re.search(r"^[a-zA-Z_]+$", text)
    if match:
        return True
    return False

def create_role_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Role (
        role_name TEXT PRIMARY KEY NOT NULL CHECK (role_name REGEXP '^[a-zA-Z_]+$'),
        creation_date TEXT NOT NULL,
        creation_time TEXT NOT NULL                      
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    return "Role table created successfully."

def insert_role(role_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate role inputs
    if not is_role_permission(role_name):
        return "Invalid role format."
    
    # Prevent unique role_name violation
    roles = [r[0] for r in cursor.execute("SELECT role_name FROM Role").fetchall()]
    if role_name in roles:
        cursor.close()
        connection.close()
        return "Role name already exists."

    # get creation date and time in ISO format
    creation_date, creation_time = dt.now().isoformat().split("T")

    sql = """ INSERT INTO Role (role_name, creation_date, creation_time) VALUES 
                    (?, ?, ?)"""
    cursor.execute(sql, (role_name, creation_date, creation_time))

    connection.commit()
    cursor.close()
    connection.close()
    return "Role info inserted successfully."
#------------------------------------------- I-3- Permission table --------------------------------------------------#
# permission_name must be consisting of only english alphabets and underscore(_) but no digits, spaces or other special/printed characters

def create_permission_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Permission (
        permission_name TEXT PRIMARY KEY NOT NULL CHECK (permission_name REGEXP '^[a-zA-Z_]+$'),
        creation_date TEXT,
        creation_time TEXT                      
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    return "Permission table created successfully."

def insert_permission(permission_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate permission inputs
    if not is_role_permission(permission_name):
        return "Invalid permission format."
        
    # Prevent unique role_name violation
    permissions = [p[0] for p in cursor.execute("SELECT permission_name FROM Permission").fetchall()]
    if permission_name in permissions:
        cursor.close()
        connection.close()
        return "Permission name already exists."

    # get creation date and time in ISO format
    creation_date, creation_time = dt.now().isoformat().split("T")

    sql = """ INSERT INTO Permission (permission_name, creation_date, creation_time) VALUES 
                    (?, ?, ?)"""
    cursor.execute(sql, (permission_name, creation_date, creation_time))

    connection.commit()
    cursor.close()
    connection.close()
    return "Permission info inserted successfully."
#------------------------------------------- I-4- User_Role table --------------------------------------------------#
#4-1- is_role and is_username constrints
#4-2- username exists in User table
#4-3- role exists in Role table
    
def create_user_role_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User_Role (
        user_name TEXT NOT NULL CHECK (user_name REGEXP '^[a-zA-Z0-9]+$'
                AND user_name IN (SELECT user_name FROM User)),
        role_name TEXT NOT NULL CHECK (role_name REGEXP '^[a-zA-Z_]+$'
                AND role_name IN (SELECT role_name FROM Role)),
        role_assignment_date TEXT NOT NULL,
        role_assignment_time TEXT NOT NULL,
        PRIMARY KEY (user_name, role_name),
        FOREIGN KEY(user_name) REFERENCES User(user_name) ON UPDATE CASCADE ON DELETE CASCADE, 
        FOREIGN KEY(role_name) REFERENCES Role(role_name) ON UPDATE CASCADE ON DELETE CASCADE                    
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    return "User_Role table created successfully."

def insert_user_role(user_name,role_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate user role inputs
    if not is_username(user_name):
        return "Invalid username format."
        
    if not is_role_permission(role_name):
        return "Invalid role format."
    
    # Validate user existence
    users = [u[0] for u in cursor.execute("SELECT user_name FROM User").fetchall()]
    if user_name not in users:
        cursor.close()
        connection.close()
        return "User not registered."
    
    # Validate role existence
    roles = [r[0] for r in cursor.execute("SELECT role_name FROM Role").fetchall()]
    if role_name not in roles:
        cursor.close()
        connection.close()
        return "Role not created."
    
    # Validate no duplication in roles assigned to an user
    user_roles = [ur[0] for ur in 
                cursor.execute("""SELECT UR.role_name
                                  FROM User U
                                  JOIN User_Role UR
                                  ON U.user_name = UR.user_name
                                  WHERE UR.user_name = ?""", (user_name, )).fetchall()]
    if role_name in user_roles:
        cursor.close()
        connection.close()
        return "User already assigned this role."
    
    # Validate only one admin: no more admins are allowed
    admin = cursor.execute("""SELECT UR.user_name
                           FROM User U
                           JOIN User_Role UR
                           ON U.user_name = UR.user_name
                           WHERE UR.role_name = 'Administrator'""").fetchone()[0]
    if role_name == "Administrator" and admin:
        cursor.close()
        connection.close()
        return "No more admins are allowed."
    
    # Validate that students can't have any other role
    students = [s[0] for s in 
                cursor.execute("""SELECT UR.user_name
                                  FROM User U
                                  JOIN User_Role UR
                                  ON U.user_name = UR.user_name
                                  WHERE UR.role_name = 'Student'""").fetchall()]
    if user_name in students:
        cursor.close()
        connection.close()
        return "A student can't have any other roles."
    
    # Validate that users other than students can't have student role
    nonstudents = [ns[0] for ns in 
                cursor.execute("""SELECT UR.user_name
                                  FROM User U
                                  JOIN User_Role UR
                                  ON U.user_name = UR.user_name
                                  WHERE UR.role_name <> 'Student'""").fetchall()]
    if user_name in nonstudents and role_name == "Student":
        cursor.close()
        connection.close()
        return "A non-student can't have the student role."
    
    # get assignment date and time in ISO format
    role_assignment_date, role_assignment_time = dt.now().isoformat().split("T")

    sql = """ INSERT INTO User_Role (user_name, role_name, role_assignment_date, role_assignment_time) VALUES 
                    (?, ?, ?, ?)"""
    cursor.execute(sql, (user_name, role_name, role_assignment_date, role_assignment_time))

    connection.commit()
    cursor.close()
    connection.close()
    return "User role assigned successfully."

def delete_user_role(user_name,role_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate user role inputs
    if not is_username(user_name):
        return "Invalid username format."
    if not is_role_permission(role_name):
        return "Invalid role format."
    
    # Validate user existence
    users = [u[0] for u in cursor.execute("SELECT user_name FROM User").fetchall()]
    if user_name not in users:
        cursor.close()
        connection.close()
        return "User not registered."
    
    # Validate role existence
    roles = [r[0] for r in cursor.execute("SELECT role_name FROM Role").fetchall()]
    if role_name not in roles:
        cursor.close()
        connection.close()
        return "Role not created."

    # Validate role be already assign to the user
    user_roles = [ur[0] for ur in 
                cursor.execute("""SELECT UR.role_name
                                  FROM User U
                                  JOIN User_Role UR
                                  ON U.user_name = UR.user_name
                                  WHERE UR.user_name = ?""", (user_name, )).fetchall()]
    if role_name not in user_roles:
        cursor.close()
        connection.close()
        return "User hasn't assigned this role."

    sql = "DELETE FROM User_Role WHERE user_name = ? AND role_name = ?"
    cursor.execute(sql, (user_name, role_name))

    connection.commit()
    cursor.close()
    connection.close()
    return "User role revoked successfully."
#------------------------------------------- I-5- Role_Permission table --------------------------------------------------#
#5-1- is_role and is_permission constrints
#5-2- permission exists in Permission table
#5-3- role exists in Role table
    
def create_role_permission_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Role_Permission (
        role_name TEXT NOT NULL CHECK (role_name REGEXP '^[a-zA-Z_]+$'
                AND role_name IN (SELECT role_name FROM Role)),
        permission_name TEXT NOT NULL CHECK (permission_name REGEXP '^[a-zA-Z_]+$'
                AND permission_name IN (SELECT permission_name FROM Permission)),
        permission_assignment_date TEXT NOT NULL,
        permission_assignment_time TEXT NOT NULL,
        PRIMARY KEY (role_name, permission_name),
        FOREIGN KEY(role_name) REFERENCES Role(role_name) ON UPDATE CASCADE ON DELETE CASCADE,  
        FOREIGN KEY(permission_name) REFERENCES Permission(permission_name) ON UPDATE CASCADE ON DELETE CASCADE                   
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    return "Role_Permission table created successfully."

def insert_role_permission(role_name,permission_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate role permission inputs
    if not is_role_permission(role_name):
        return "Invalid role format."
    if not is_role_permission(permission_name):
        return "Invalid permission format."

    # get assignment date and time in ISO format
    permission_assignment_date, permission_assignment_time = dt.now().isoformat().split("T")

    sql = """ INSERT INTO Role_Permission (role_name, permission_name, permission_assignment_date, permission_assignment_time) VALUES 
                    (?, ?, ?, ?)"""
    cursor.execute(sql, (role_name, permission_name, permission_assignment_date, permission_assignment_time))

    connection.commit()
    cursor.close()
    connection.close()
    return "Role Permission assigned successfully."
#------------------------------------------- I-6- Login table -----------------------------------------------#
#6-1- is_user_name and is_password constrints
#6-2- user must exist(be registered) in User table in order to login
#6-3- password must be correct according to User table in order to login
#6-4- if the user has already logged in can't log in again
#6-5- only users that already logged in can logout
    
def create_login_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Login (
        user_name TEXT NOT NULL CHECK (user_name REGEXP '^[a-zA-Z0-9]+$'
                AND user_name IN (SELECT user_name FROM User)),
        login_date TEXT NOT NULL,
        login_time TEXT NOT NULL,
        logout_date TEXT,
        logout_time TEXT,
        PRIMARY KEY (user_name, login_date, login_time),
        FOREIGN KEY(user_name) REFERENCES User(user_name) ON UPDATE CASCADE ON DELETE CASCADE                     
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    return "Login table created successfully."

def user_login(user_name, password):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate user login inputs  
    if not is_username(user_name):
        return "Invalid username format."
    if not is_password(password):
        return "Invalid password format."
     
    cursor.execute("""
    SELECT user_name, hashed_password 
    FROM User""")
    users_data=cursor.fetchall()
    cursor.execute("""
    SELECT user_name, login_date, login_time, logout_date, logout_time 
    FROM Login""")
    user_logins=cursor.fetchall()

    #check if user is already logged in
    for user_login in user_logins:
        if user_login[0] == user_name and user_login[3] == None:
            cursor.close()
            connection.close()
            return "User has already logged in!"

    #check if user is registered
    for user in users_data:
        if user[0] == user_name:
            if bcrypt.checkpw(bytes(password,encoding='utf-8'), user[1]):
                # get login date and time in ISO format
                login_date, login_time = dt.now().isoformat().split("T")

                sql = """ INSERT INTO Login (user_name, login_date, login_time) VALUES 
                                (?, ?, ?)"""
                cursor.execute(sql, (user_name, login_date, login_time))

                connection.commit()
                cursor.close()
                connection.close()

                return "User logged in successfully."
            else:
                cursor.close()
                connection.close()
                return "Incorrect password!"
    cursor.close()
    connection.close()
    return "Username not registered."

def user_logout(user_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate user logout inputs
    users = [u[0] for u in cursor.execute("""SELECT user_name FROM User""").fetchall()]
    if not is_username(user_name):
        cursor.close()
        connection.close()
        return "Invalid username format."
    if user_name not in users:
        cursor.close()
        connection.close()
        return "Username not registered."
    # get logout date and time in ISO format
    logout_date, logout_time = dt.now().isoformat().split("T")

    sql = """ UPDATE Login
              SET logout_date = ? , logout_time = ?
              WHERE user_name = ? AND logout_date IS NULL """
    cursor.execute(sql, (logout_date, logout_time, user_name))

    connection.commit()
    cursor.close()
    connection.close()
    return "User logged out successfully."    
#------------------------------------------- I-7- Question table ---------------------------------------------#
# 7-1- question_id must be like Q + positive integer
# 7-2- image must be a valid path and the file extension be an image(jpg, png ,...)
# 7-3- difficulty be in Easy, Normal, Hard
# 7-4- type be in Multiple choice, True/False, Descriptive/Practical
# 7-5- points must be a positive integer
# 7-6- creator_user_name must meet is_username rules and be in users that have Question_Creator role

# Validate question_id
def is_question_id(text):
    match = re.search(r"^Q[1-9]\d*$", text)
    if match:
        return True
    return False

# Validate image path
def is_image_path(path):
    # ..\images\Q integer.(png, jpg, ...)
    match = re.search(r"^\.\.\\images\\Q[1-9]\d*(O[1-9])?\.(png|jpg|jpeg|gif|bmp|tif|tiff)$", path)
    if match:
        return True
    return False

def create_question_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Question (
        question_id TEXT PRIMARY KEY NOT NULL CHECK (question_id REGEXP '^Q[1-9]\d*$'),
        topic TEXT NOT NULL,
        subtopic TEXT,           
        text TEXT,
        image TEXT CHECK (image IS NULL OR image REGEXP '^\.\.\\images\\Q[1-9]\d*(O[1-9])?\.(png|jpg|jpeg|gif|bmp|tif|tiff)$'),
        difficulty TEXT DEFAULT 'Normal' NOT NULL CHECK (difficulty IN ('Easy', 'Normal', 'Hard')),
        type TEXT DEFAULT 'Multiple choice' NOT NULL CHECK (type IN ('Multiple choice', 'True/False', 'Descriptive/Practical')),
        points INTEGER DEFAULT 1 NOT NULL CHECK (points > 0),
        creation_date TEXT NOT NULL,
        creation_time TEXT NOT NULL,
        creator_user_name TEXT NOT NULL CHECK (creator_user_name REGEXP '^[a-zA-Z0-9]+$' 
            AND creator_user_name IN (
                SELECT UR.user_name
                FROM User U
                JOIN User_Role UR 
                ON U.user_name = UR.user_name
                WHERE role_name = 'Question_Creator'
            )
        )
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    print("Question table created successfully.")

def insert_question(question_id, topic, subtopic, text, image, difficulty, type, points, creator_user_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_question_id(question_id):
        return "Invalid question ID format."
        
    if image and not is_image_path(image):
        return "Invalid image path."
        
    if difficulty not in ['Easy', 'Normal', 'Hard']:
        return "Invalid difficulty level."
        
    if type not in ['Multiple choice', 'True/False', 'Descriptive/Practical']:
        return "Invalid question type."
        
    if not (isinstance(points, int) and points > 0):
        return "Invalid points value."
    
    if not (text or image):
        return "A Question must have at least a text or an image."
    
    if not is_username(creator_user_name):
        return "Invalid username format."
    
    # Validate user existence
    users = [u[0] for u in cursor.execute("SELECT user_name FROM User").fetchall()]
    if creator_user_name not in users:
        cursor.close()
        connection.close()
        return "User not registered."
        
    # check if the username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Question_Creator'""")

    question_creator_users = [user[0] for user in cursor.fetchall()]
    if creator_user_name not in question_creator_users:
        return "User is not question creator."

    # Validate question duplication
    questions = [q[0] for q in cursor.execute("SELECT question_id FROM Question").fetchall()]
    if question_id in questions:
        cursor.close()
        connection.close()
        return "Question already exists."
        
    # get creation date and time in ISO format
    creation_date, creation_time = dt.now().isoformat().split("T")

    sql = """ INSERT INTO Question (question_id, topic, subtopic, text, image, difficulty, type, points, creation_date,
                        creation_time, creator_user_name) VALUES 
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(sql, (question_id, topic, subtopic, text, image, difficulty, type, points, creation_date, \
                        creation_time, creator_user_name))

    connection.commit()
    cursor.close()
    connection.close()
    return "Question info inserted successfully."

def update_question(question_id, topic, subtopic, text, image, difficulty, type, points):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_question_id(question_id):
        return "Invalid question ID format."
        
    if image and not is_image_path(image):
        return "Invalid image path."
        
    if difficulty not in ['Easy', 'Normal', 'Hard']:
        return "Invalid difficulty level."
        
    if type not in ['Multiple choice', 'True/False', 'Descriptive/Practical']:
        return "Invalid question type."
        
    if not (isinstance(points, int) and points > 0):
        return "Invalid points value."
    
    if not (text or image):
        return "A Question must have at least a text or an image."
    
    # Validate question existence
    questions = [q[0] for q in cursor.execute("SELECT question_id FROM Question").fetchall()]
    if question_id not in questions:
        cursor.close()
        connection.close()
        return "Question not exists."

    sql = """ UPDATE Question
              SET topic = ?, subtopic = ?, text = ?, image = ?, difficulty = ?, type = ?, points = ?
              WHERE question_id = ?"""
    cursor.execute(sql, (topic, subtopic, text, image, difficulty, type, points, question_id))

    connection.commit()
    cursor.close()
    connection.close()
    return "Question info updated successfully."

def delete_question(question_id):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Validate user inputs
    if not is_question_id(question_id):
        return "Invalid question ID format."
    
    # Validate question existence
    questions = [q[0] for q in cursor.execute("SELECT question_id FROM Question").fetchall()]
    if question_id not in questions:
        cursor.close()
        connection.close()
        return "Question not exists."

    sql = "DELETE FROM Question WHERE question_id = ?"
    cursor.execute(sql, (question_id, ))

    connection.commit()
    cursor.close()
    connection.close()
    return "Question deleted successfully."
#------------------------------------------- I-8- Option table ---------------------------------------------#
# 8-1- option_id must be like Q + positive integer + O + positive integer
# 8-2- question_id must meet is_question_id rules and already exists in Question table
# 8-3- image must meet is_image_path rules
# 8-4- is_correct_answer must be either 0 or 1 with default 0

# Validate option_id
def is_option_id(text):
    match = re.search(r"^Q[1-9]\d*O[1-9]$", text)
    if match:
        return True
    return False

def create_option_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Option (
        option_id TEXT PRIMARY KEY NOT NULL CHECK (option_id REGEXP '^Q[1-9]\d*O[1-9]$'),
        question_id TEXT NOT NULL CHECK (question_id REGEXP '^Q[1-9]\d*$'
                AND question_id IN (SELECT question_id FROM Question)),
        text TEXT,
        image TEXT CHECK (image IS NULL OR image REGEXP '^\.\.\\images\\Q[1-9]\d*(O[1-9])?\.(png|jpg|jpeg|gif|bmp|tif|tiff)$'),
        is_correct_answer INTEGER DEFAULT 0 NOT NULL CHECK (is_correct_answer IN (0, 1)),
        FOREIGN KEY(question_id) REFERENCES Question(question_id) ON UPDATE CASCADE ON DELETE CASCADE
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    print("Option table created successfully.")

def insert_question_option(option_id, question_id, text, image, is_correct_answer):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_option_id(option_id):
        return "Invalid option ID format."
        
    if not is_question_id(question_id):
        return "Invalid question ID format."
        
    if image and not is_image_path(image):
        return "Invalid image path."
        
    if is_correct_answer not in [0, 1]:
        return "Invalid is_correct_answer."
    
    if not (text or image):
        return "An Option must have at least a text or an image."
        
    # check if the question_id exists in the question table
    cursor.execute("""SELECT question_id FROM Question""")
    questions = [question[0] for question in cursor.fetchall()]
    if question_id not in questions:
        return "Question not exists."
    
    # check if the option_id duplication
    cursor.execute("""SELECT option_id FROM Option""")
    options = [o[0] for o in cursor.fetchall()]
    if option_id in options:
        return "Option already exists."
        
    sql = """ INSERT INTO Option (option_id, question_id, text, image, is_correct_answer) VALUES 
                        (?, ?, ?, ?, ?)"""
    cursor.execute(sql, (option_id, question_id, text, image, is_correct_answer))

    connection.commit()
    cursor.close()
    connection.close()
    return "Question option info inserted successfully."

def update_question_option(option_id, question_id, text, image, is_correct_answer):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_option_id(option_id):
        return "Invalid option ID format."
        
    if not is_question_id(question_id):
        return "Invalid question ID format."
        
    if image and not is_image_path(image):
        return "Invalid image path."
        
    if is_correct_answer not in [0, 1]:
        return "Invalid is_correct_answer."
    
    if not (text or image):
        return "An Option must have at least a text or an image."
        
    # check if the question_id exists in the question table
    cursor.execute("""SELECT question_id FROM Question""")
    questions = [question[0] for question in cursor.fetchall()]
    if question_id not in questions:
        return "Question not exists."
    
    # check option_id existence
    cursor.execute("""SELECT option_id FROM Option""")
    options = [o[0] for o in cursor.fetchall()]
    if option_id not in options:
        return "Option not exists."
        
    sql = """ UPDATE Option
              SET text = ?, image = ?, is_correct_answer = ?
              WHERE option_id = ?"""
    cursor.execute(sql, (text, image, is_correct_answer, option_id))

    connection.commit()
    cursor.close()
    connection.close()
    return "Question option info updated successfully."

def delete_question_option(option_id):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_option_id(option_id):
        return "Invalid option ID format."
        
    # check option_id existence
    cursor.execute("""SELECT option_id FROM Option""")
    options = [o[0] for o in cursor.fetchall()]
    if option_id not in options:
        return "Option not exists."
        
    sql = """ DELETE FROM Option
              WHERE option_id = ?"""
    cursor.execute(sql, (option_id, ))

    connection.commit()
    cursor.close()
    connection.close()
    return "Question option info deleted successfully."
#------------------------------------------- I-9- Exam table ---------------------------------------------#
# 9-1- exam_id must be like Ex + positive integer
# 9-2- exam_date must be in format yyyy/mm/dd and be after today
# 9-3- start_time must be in format hh:mm:ss and be in 24-hour time system
# 9-4- duration must be a positive integer
# 9-5- has_negative_score must be either 0 or 1
# 9-6- passing_score must be a positive integer less than 100 with default value 51
# 9-7- handler_user_name must meet is_username rules and be in users that have Exam_Handler role
# 9-8- supervisor_user_name must meet is_username rules and be in users that have Exam_Supervisor role
# 9-9- creator_user_name must meet is_username rules and be in users that have Exam_Creator role

# Validate exam_id
def is_exam_id(text):
    match = re.search(r"^Ex[1-9]\d*$", text)
    if match:
        return True
    return False

# Validate exam_date
def is_valid_exam_date(date):
    try:
        exam_date = dt.strptime(date, '%Y/%m/%d')
        return exam_date > dt.now()
    except ValueError:
        return False

# Validate start_time
def is_valid_exam_time(time):
    try:
        exam_time = dt.strptime(time, '%H:%M:%S')
        return True
    except ValueError:
        return False

def create_exam_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Exam (
        exam_id TEXT PRIMARY KEY NOT NULL CHECK (exam_id REGEXP '^Ex[1-9][0-9]*$'),
        exam_name TEXT NOT NULL,
        exam_date TEXT NOT NULL CHECK (exam_date REGEXP '^([1-9][0-9]{3})/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])$'),
        start_time TEXT NOT NULL CHECK (start_time REGEXP '^(0[1-9]|1[0-9]|2[0-3]):(0[1-9]|[1-5][0-9]):(0[1-9]|[1-5][0-9])$'),
        duration INTEGER NOT NULL CHECK (duration > 0),
        creation_date TEXT NOT NULL,
        creation_time TEXT NOT NULL,
        has_negative_score INTEGER DEFAULT 0 NOT NULL CHECK (has_negative_score IN (0, 1)),
        passing_score INTEGER DEFAULT 51 NOT NULL CHECK (passing_score > 0 AND passing_score < 100),
        handler_user_name TEXT NOT NULL CHECK (handler_user_name REGEXP '^[a-zA-Z0-9]+$' 
            AND handler_user_name IN (
                SELECT UR.user_name
                FROM User U
                JOIN User_Role UR 
                ON U.user_name = UR.user_name
                WHERE role_name = 'Exam_Handler'
            )),
        supervisor_user_name TEXT NOT NULL CHECK (supervisor_user_name REGEXP '^[a-zA-Z0-9]+$'
            AND supervisor_user_name IN (
                SELECT UR.user_name
                FROM User U
                JOIN User_Role UR 
                ON U.user_name = UR.user_name
                WHERE role_name = 'Exam_Supervisor'
            )),
        creator_user_name TEXT NOT NULL CHECK (creator_user_name REGEXP '^[a-zA-Z0-9]+$'
            AND creator_user_name IN (
                SELECT UR.user_name
                FROM User U
                JOIN User_Role UR 
                ON U.user_name = UR.user_name
                WHERE role_name = 'Exam_Creator'
            ))
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    print("Exam table created successfully.")

def insert_exam(exam_id, exam_name, exam_date, start_time, duration, has_negative_score, \
                passing_score, handler_user_name, supervisor_user_name, creator_user_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_valid_exam_date(exam_date):
        return "Invalid exam date format or it's not in the future."
        
    if not is_valid_exam_time(start_time):
        return "Invalid start time format."
        
    if not (isinstance(duration, int) and duration > 0):
        return "Invalid duration value."
        
    if has_negative_score not in [0, 1]:
        return "Invalid value for has_negative_score."
        
    if not (isinstance(passing_score, int) and 0 < passing_score < 100):
        return "Invalid passing score value."
    
    if not is_username(handler_user_name) or not is_username(supervisor_user_name) or not is_username(creator_user_name):
        return "Invalid username format."
        
    # check if the handler username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Exam_Handler'""")

    exam_handler_users = [user[0] for user in cursor.fetchall()]
    if handler_user_name not in exam_handler_users:
        return "Invalid exam handler username."
        
    # check if the supervisor username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Exam_Supervisor'""")

    exam_supervisor_users = [user[0] for user in cursor.fetchall()]
    if supervisor_user_name not in exam_supervisor_users:
        return "Invalid exam supervisor username."
    
    # check if the exam creator username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Exam_Creator'""")

    exam_creator_users = [user[0] for user in cursor.fetchall()]
    if creator_user_name not in exam_creator_users:
        return "Invalid exam creator username."
    
    # check the exam_id duplication
    cursor.execute("""SELECT exam_id FROM Exam""")
    exams = [e[0] for e in cursor.fetchall()]
    if exam_id in exams:
        return "Exam already exists."
    
    # get creation date and time in ISO format
    creation_date, creation_time = dt.now().isoformat().split("T")

    sql = """ INSERT INTO Exam (exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
        has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name) VALUES 
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(sql, (exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time, \
            has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name))

    connection.commit()
    cursor.close()
    connection.close()
    return "Exam info inserted successfully."

def update_exam(exam_id, exam_name, exam_date, start_time, duration, has_negative_score, \
                passing_score, handler_user_name, supervisor_user_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_valid_exam_date(exam_date):
        return "Invalid exam date format or it's not in the future."
        
    if not is_valid_exam_time(start_time):
        return "Invalid start time format."
        
    if not (isinstance(duration, int) and duration > 0):
        return "Invalid duration value."
        
    if has_negative_score not in [0, 1]:
        return "Invalid value for has_negative_score."
        
    if not (isinstance(passing_score, int) and 0 < passing_score < 100):
        return "Invalid passing score value."
        
    # check if the handler username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Exam_Handler'""")

    exam_handler_users = [user[0] for user in cursor.fetchall()]
    if handler_user_name not in exam_handler_users:
        return "Invalid exam handler username."
        
    # check if the supervisor username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Exam_Supervisor'""")

    exam_supervisor_users = [user[0] for user in cursor.fetchall()]
    if supervisor_user_name not in exam_supervisor_users:
        return "Invalid exam supervisor username."
    
    # check the exam_id exitence
    cursor.execute("""SELECT exam_id FROM Exam""")
    exams = [e[0] for e in cursor.fetchall()]
    if exam_id not in exams:
        return "Exam not exists."

    sql = """ UPDATE Exam
              SET exam_name = ?, exam_date = ?, start_time = ?, duration = ?,
                  has_negative_score = ?, passing_score = ?, handler_user_name = ?, supervisor_user_name = ?
              WHERE exam_id = ?"""
    cursor.execute(sql, (exam_name, exam_date, start_time, duration, has_negative_score, \
                         passing_score, handler_user_name, supervisor_user_name, exam_id))

    connection.commit()
    cursor.close()
    connection.close()
    return "Exam info updated successfully."

def delete_exam(exam_id):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
    
    # check the exam_id exitence
    cursor.execute("""SELECT exam_id FROM Exam""")
    exams = [e[0] for e in cursor.fetchall()]
    if exam_id not in exams:
        return "Exam not exists."

    sql = """ DELETE FROM Exam
              WHERE exam_id = ?"""
    cursor.execute(sql, (exam_id, ))

    connection.commit()
    cursor.close()
    connection.close()
    return "Exam info deleted successfully."
#------------------------------------------- I-10- Exam_Question table ---------------------------------------------#
# 10-1- exam_id must meet is_exam_id rules and already exists in Exam table
# 10-2- question_id must meet is_question_id rules and already exists in Question table
    
def create_exam_question_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Exam_Question (
        exam_id TEXT NOT NULL CHECK (exam_id REGEXP '^Ex[1-9][0-9]*$'
                AND exam_id IN (SELECT exam_id FROM Exam)),
        question_id TEXT NOT NULL CHECK (question_id REGEXP '^Q[1-9]\d*$'
                AND question_id IN (SELECT question_id FROM Question)),
        PRIMARY KEY (exam_id, question_id),           
        FOREIGN KEY(exam_id) REFERENCES Exam(exam_id) ON UPDATE CASCADE ON DELETE CASCADE
        FOREIGN KEY(question_id) REFERENCES Question(question_id) ON UPDATE CASCADE ON DELETE CASCADE
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    print("Exam_Question table created successfully.")

def insert_exam_question(exam_id, question_id):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_question_id(question_id):
        return "Invalid question ID format."
        
    # check if the exam_id is registered in the exam table
    cursor.execute("""SELECT exam_id FROM Exam""")

    exams = [exam[0] for exam in cursor.fetchall()]
    if exam_id not in exams:
        return "Invalid exam_id."
        
    # check if the question_id is registered in the question table
    cursor.execute("""SELECT question_id FROM Question""")

    questions = [question[0] for question in cursor.fetchall()]
    if question_id not in questions:
        return "Invalid question_id."
        

    sql = """ INSERT INTO Exam_Question (exam_id, question_id) VALUES (?, ?)"""
    cursor.execute(sql, (exam_id, question_id))

    connection.commit()
    cursor.close()
    connection.close()
    return "Exam question info inserted successfully."

def delete_exam_question(exam_id, question_id):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_question_id(question_id):
        return "Invalid question ID format."
        
    # check if the exam_id is registered in the exam table
    cursor.execute("""SELECT exam_id FROM Exam""")

    exams = [exam[0] for exam in cursor.fetchall()]
    if exam_id not in exams:
        return "Invalid exam_id."
        
    # check if the question_id is registered in the question table
    cursor.execute("""SELECT question_id FROM Question""")

    questions = [question[0] for question in cursor.fetchall()]
    if question_id not in questions:
        return "Invalid question_id."
    
    sql = """DELETE FROM Exam_Question
             WHERE exam_id = ? AND question_id = ?"""
    cursor.execute(sql, (exam_id, question_id))

    connection.commit()
    cursor.close()
    connection.close()
    return "Exam question info deleted successfully."
#------------------------------------------- I-11- User_Exam table ---------------------------------------------#
# 11-1- exam_id must meet is_exam_id rules and already exists in Exam table
# 11-2- user_name must meet is_user_name rules and already exists in User table and have Student Role
# 11-3- score must be an integer with default value 0
# 11-4- total_questions must be a non-negative integer with default value 0
# 11-5- correct_answers must be a non-negative integer with default value 0 and must be less than or equal total_questions
# 11-6- wrong_answers must be a non-negative integer with default value 0 and must be less than or equal total_questions
# 11-7- unanswered_questions must be a non-negative integer with default value 0 and must be less than or equal total_questions
# 11-8- (correct_answers + wrong_answers + unanswered_questions) = total_questions
# 11-9- is_passed mut be either 0 or 1 with default 0
# 11-9- is_marked mut be either 0 or 1 with default 0
    
def create_user_exam_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User_Exam (
        exam_id TEXT NOT NULL CHECK (exam_id REGEXP '^Ex[1-9][0-9]*$'
                AND exam_id IN (SELECT exam_id FROM Exam)),
        user_name TEXT NOT NULL CHECK (user_name REGEXP '^[a-zA-Z0-9]+$'
                AND user_name IN (
                SELECT UR.user_name
                FROM User U
                JOIN User_Role UR 
                ON U.user_name = UR.user_name
                WHERE role_name = 'Student'
            )),
        score INTEGER DEFAULT 0 NOT NULL,
        total_questions INTEGER DEFAULT 0 NOT NULL CHECK (total_questions >= 0),
        correct_answers INTEGER DEFAULT 0 NOT NULL CHECK (correct_answers >= 0 AND correct_answers <= total_questions),
        wrong_answers INTEGER DEFAULT 0 NOT NULL CHECK (wrong_answers >= 0 AND wrong_answers <= total_questions),
        unanswered_questions INTEGER DEFAULT 0 NOT NULL CHECK (unanswered_questions >= 0 AND unanswered_questions <= total_questions),
        is_passed INTEGER DEFAULT 0 NOT NULL CHECK (is_passed IN (0, 1)),
        is_marked INTEGER DEFAULT 0 NOT NULL CHECK (is_marked IN (0, 1)),
        PRIMARY KEY (exam_id, user_name),    
        FOREIGN KEY(exam_id) REFERENCES Exam(exam_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY(user_name) REFERENCES User(user_name) ON UPDATE CASCADE ON DELETE CASCADE
    ) WITHOUT ROWID""")

    # Drop the trigger if it already exists
    cursor.execute("DROP TRIGGER IF EXISTS check_questions_total")
    # Create Trigger to enforce (correct_answers + wrong_answers + unanswered_questions) = total_questions
    cursor.execute("""
    CREATE TRIGGER check_questions_total
    BEFORE INSERT ON User_Exam
    FOR EACH ROW
    WHEN (NEW.correct_answers + NEW.wrong_answers + NEW.unanswered_questions != NEW.total_questions)
    BEGIN
        SELECT RAISE(ABORT, 'The sum of correct answers, wrong answers, and unanswered questions must be equal to total questions.');
    END""")

    connection.commit()
    cursor.close()
    connection.close()
    print("User_Exam table created successfully.")

def insert_user_exam(exam_id, user_name, score, total_questions, correct_answers, \
                    wrong_answers, unanswered_questions, is_passed, is_marked):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_username(user_name):
        return "Invalid username format."
        
    if not isinstance(score, int):
        return "Invalid score."
        
    if not (isinstance(total_questions, int) and total_questions >= 0):
        return "Invalid total questions."
        
    if not (isinstance(correct_answers, int) and 0 <= correct_answers <= total_questions):
        return "Invalid correct answers."
        
    if not (isinstance(wrong_answers, int) and 0 <= wrong_answers <= total_questions):
        return "Invalid wrong answers."
        
    if not (isinstance(unanswered_questions, int) and 0 <= unanswered_questions <= total_questions):
        return "Invalid unanswered questions."
        
    if correct_answers + wrong_answers + unanswered_questions != total_questions:
        return "The sum of correct answers, wrong answers, and unanswered questions must be equal to total questions."
        
    if is_passed not in [0, 1]:
        return "Invalid value for is_passed."
    
    if is_marked not in [0, 1]:
        return "Invalid value for is_marked."
        
    # check if the exam_id is registered in the exam table
    cursor.execute("""SELECT exam_id FROM Exam""")

    exams = [exam[0] for exam in cursor.fetchall()]
    if exam_id not in exams:
        return "Invalid exam_id."
        
    # check if the exam student username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Student'""")

    students = [student[0] for student in cursor.fetchall()]
    if user_name not in students:
        return "Invalid student username."
        
    sql = """ INSERT INTO User_Exam (exam_id, user_name, score, total_questions, correct_answers,
                    wrong_answers, unanswered_questions, is_passed, is_marked) VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(sql, (exam_id, user_name, score, total_questions, correct_answers, \
                    wrong_answers, unanswered_questions, is_passed, is_marked))

    connection.commit()
    cursor.close()
    connection.close()
    return "User exam info inserted successfully."

def update_user_exam(exam_id, user_name, score, total_questions, correct_answers, \
                    wrong_answers, unanswered_questions, is_passed, is_marked):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_username(user_name):
        return "Invalid username format."
        
    if not isinstance(score, int):
        return "Invalid score."
        
    if not (isinstance(total_questions, int) and total_questions >= 0):
        return "Invalid total questions."
        
    if not (isinstance(correct_answers, int) and 0 <= correct_answers <= total_questions):
        return "Invalid correct answers."
        
    if not (isinstance(wrong_answers, int) and 0 <= wrong_answers <= total_questions):
        return "Invalid wrong answers."
        
    if not (isinstance(unanswered_questions, int) and 0 <= unanswered_questions <= total_questions):
        return "Invalid unanswered questions."
        
    if correct_answers + wrong_answers + unanswered_questions != total_questions:
        return "The sum of correct answers, wrong answers, and unanswered questions must be equal to total questions."
        
    if is_passed not in [0, 1]:
        return "Invalid value for is_passed."
    
    if is_marked not in [0, 1]:
        return "Invalid value for is_marked."
        
    # check if the exam_id is registered in the exam table
    cursor.execute("""SELECT exam_id FROM Exam""")

    exams = [exam[0] for exam in cursor.fetchall()]
    if exam_id not in exams:
        return "Invalid exam_id."
        
    # check if the exam student username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Student'""")

    students = [student[0] for student in cursor.fetchall()]
    if user_name not in students:
        return "Invalid student username."
        
    sql = """UPDATE User_Exam
             SET score = ?, total_questions = ?, correct_answers = ?,
                 wrong_answers = ?, unanswered_questions = ?, is_passed = ?, is_marked = ?
             WHERE exam_id = ? AND user_name = ?"""
    cursor.execute(sql, (score, total_questions, correct_answers, wrong_answers, \
                         unanswered_questions, is_passed, is_marked, exam_id, user_name))

    connection.commit()
    cursor.close()
    connection.close()
    return "User exam info updated successfully."

def delete_user_exam(exam_id, user_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_username(user_name):
        return "Invalid username format."
        
    # check if the exam_id is registered in the exam table
    cursor.execute("""SELECT exam_id FROM Exam""")

    exams = [exam[0] for exam in cursor.fetchall()]
    if exam_id not in exams:
        return f"Invalid exam_id."
        
    # check if the exam student username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Student'""")

    students = [student[0] for student in cursor.fetchall()]
    if user_name not in students:
        return "Invalid student username."
        
    sql = """ DELETE FROM User_Exam
              WHERE exam_id = ? AND user_name = ?"""
    cursor.execute(sql, (exam_id, user_name))

    connection.commit()
    cursor.close()
    connection.close()
    return "User exam info deleted successfully."
#------------------------------------------- I-12- Answer table ---------------------------------------------#
# 12-1- exam_id must meet is_exam_id rules and already exists in Exam table
# 12-2- user_name must meet is_user_name rules and already exists in User table
# 12-3- question_id must meet is_question_id rules and already exists in Question table
# 12-4- option_id must meet is_option_id rules and already exists in Option table
    
def create_answer_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Answer (
        exam_id TEXT NOT NULL CHECK (exam_id REGEXP '^Ex[1-9][0-9]*$'
                AND exam_id IN (SELECT exam_id FROM Exam)),
        user_name TEXT NOT NULL CHECK (user_name REGEXP '^[a-zA-Z0-9]+$'
                AND user_name IN (SELECT user_name FROM User)),
        question_id TEXT NOT NULL CHECK (question_id REGEXP '^Q[1-9]\d*$'
                AND question_id IN (SELECT question_id FROM Question)),
        option_id TEXT CHECK (option_id IS NULL OR (option_id REGEXP '^Q[1-9]\d*O[1-9]$'
                AND option_id IN (SELECT option_id FROM Option))),
        answer_text TEXT,
        PRIMARY KEY (exam_id, user_name, question_id),    
        FOREIGN KEY(exam_id) REFERENCES Exam(exam_id) ON UPDATE CASCADE ON DELETE CASCADE       
        FOREIGN KEY(user_name) REFERENCES User(user_name) ON UPDATE CASCADE ON DELETE CASCADE
        FOREIGN KEY(question_id) REFERENCES Question(question_id) ON UPDATE CASCADE ON DELETE CASCADE           
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    print("Answer table created successfully.")

def insert_answer(exam_id, user_name, question_id, option_id, answer_text):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_username(user_name):
        return "Invalid username format."
        
    if not is_question_id(question_id):
        return "Invalid question ID format."
        
    if option_id and not is_option_id(option_id):
        return "Invalid option ID format."
        
    # check if the exam_id is registered in the exam table
    cursor.execute("""SELECT exam_id FROM Exam""")

    exams = [exam[0] for exam in cursor.fetchall()]
    if exam_id not in exams:
        return "Invalid exam_id."
        
    # check if the exam student username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Student'""")

    students = [student[0] for student in cursor.fetchall()]
    if user_name not in students:
        return "Invalid student username."
        
    # check if the question_id is registered in the question table
    cursor.execute("""SELECT question_id FROM Question""")

    questions = [question[0] for question in cursor.fetchall()]
    if question_id not in questions:
        return "Invalid question_id."
        
    # check if the option_id is registered in the option table
    cursor.execute("""SELECT option_id FROM Option""")

    options = [option[0] for option in cursor.fetchall()]
    if option_id and option_id not in options:
        return "Invalid option_id."
    
    # check the answer duplication
    cursor.execute("""SELECT exam_id, user_name, question_id
                     FROM Answer""")
    answers = cursor.fetchall()
    if (exam_id, user_name, question_id) in exams:
        return "Answer already exists."
        
    sql = """ INSERT INTO Answer (exam_id, user_name, question_id, option_id, answer_text) VALUES 
                    (?, ?, ?, ?, ?)"""
    cursor.execute(sql, (exam_id, user_name, question_id, option_id, answer_text))

    connection.commit()
    cursor.close()
    connection.close()
    return "Answer info inserted successfully."

def update_answer(exam_id, user_name, question_id, option_id, answer_text):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_username(user_name):
        return "Invalid username format."
        
    if not is_question_id(question_id):
        return "Invalid question ID format."
        
    if option_id and not is_option_id(option_id):
        return "Invalid option ID format."
        
    # check if the exam_id is registered in the exam table
    cursor.execute("""SELECT exam_id FROM Exam""")

    exams = [exam[0] for exam in cursor.fetchall()]
    if exam_id not in exams:
        return "Invalid exam_id."
        
    # check if the exam student username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Student'""")

    students = [student[0] for student in cursor.fetchall()]
    if user_name not in students:
        return "Invalid student username."
        
    # check if the question_id is registered in the question table
    cursor.execute("""SELECT question_id FROM Question""")

    questions = [question[0] for question in cursor.fetchall()]
    if question_id not in questions:
        return "Invalid question_id."
        
    # check if the option_id is registered in the option table
    cursor.execute("""SELECT option_id FROM Option""")

    options = [option[0] for option in cursor.fetchall()]
    if option_id and option_id not in options:
        return "Invalid option_id."
    
    # check the answer existence
    cursor.execute("""SELECT exam_id, user_name, question_id
                     FROM Answer""")
    answers = cursor.fetchall()
    if (exam_id, user_name, question_id) not in answers:
        return "Answer not exists."
        
    sql = """UPDATE Answer
             SET option_id = ?, answer_text = ?
             WHERE exam_id = ? AND user_name = ? AND question_id = ?"""
    cursor.execute(sql, (option_id, answer_text, exam_id, user_name, question_id))

    connection.commit()
    cursor.close()
    connection.close()
    return "Answer info updated successfully."
#------------------------------------------- I-13- Feedback table ---------------------------------------------#
# 13-1- exam_id must meet is_exam_id rules and already exists in Exam table
# 13-2- user_name must meet is_user_name rules and already exists in User table
# 13-3- feedback_type must be either 'Suggestion for improvement' or 'Comment on clarity, and difficulty levels'
# 13-4- question_id must meet is_question_id rules and already exists in Question table
# 13-5- rating must be an integer in 1 to 10 (inclusively)
# 13-6- status must be either 'Pending/Unread' or 'Analyzed/Read' defualt is Pending/Unread
# 13-6- is_visible must be either 0 or 1 default is 1

def create_feedback_table():
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Feedback (
        exam_id TEXT NOT NULL CHECK (exam_id REGEXP '^Ex[1-9][0-9]*$'
                AND exam_id IN (SELECT exam_id FROM Exam)),
        user_name TEXT NOT NULL CHECK (user_name REGEXP '^[a-zA-Z0-9]+$'
                AND user_name IN (SELECT user_name FROM User)),
        feedback_time TEXT NOT NULL,
        feedback_type TEXT NOT NULL CHECK (feedback_type IN ('Suggestion for improvement', 'Comment on clarity, and difficulty levels')),
        text TEXT,
        question_id TEXT CHECK (question_id IS NULL OR (question_id REGEXP '^Q[1-9][0-9]*$'
                AND question_id IN (SELECT question_id FROM Question))),
        rating INTEGER CHECK (rating IS NULL OR rating BETWEEN 1 AND 10),
        status TEXT DEFAULT 'Pending/Unread' NOT NULL CHECK (status IN ('Pending/Unread', 'Analyzed/Read')),
        is_visible INTEGER DEFAULT 1 NOT NULL CHECK (is_visible IN (0, 1)),          
        PRIMARY KEY (exam_id, user_name, feedback_time),    
        FOREIGN KEY(exam_id) REFERENCES Exam(exam_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY(user_name) REFERENCES User(user_name) ON UPDATE CASCADE ON DELETE CASCADE           
    ) WITHOUT ROWID""")

    connection.commit()
    cursor.close()
    connection.close()
    print("Feedback table created successfully.")

def insert_feedback(exam_id, user_name, feedback_type, text, question_id, rating, status, is_visible):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    # Perform data validation
    if not is_exam_id(exam_id):
        return "Invalid exam ID format."
        
    if not is_username(user_name):
        return "Invalid username format."
        
    if feedback_type not in ['Suggestion for improvement', 'Comment on clarity, and difficulty levels']:
        return "Invalid feedback type."
        
    if question_id and not is_question_id(question_id):
        return "Invalid question ID format."
        
    if not (isinstance(rating, int) and 1 <= rating <= 10):
        return "Invalid rating."
        
    if status not in ['Pending/Unread', 'Analyzed/Read']:
        return "Invalid status."
        
    if is_visible not in [0, 1]:
        return "Invalid value for is_visible."
        
    # check if the exam_id is registered in the exam table
    cursor.execute("""SELECT exam_id FROM Exam""")

    exams = [exam[0] for exam in cursor.fetchall()]
    if exam_id not in exams:
        return "Invalid exam_id."
        
    
    # check if the exam student username is registered in the user table
    cursor.execute("""
    SELECT UR.user_name
    FROM User U
    JOIN User_Role UR
    ON U.user_name = UR.user_name
    Where role_name = 'Student'""")

    students = [student[0] for student in cursor.fetchall()]
    if user_name not in students:
        return "Invalid student username."
        
    # get feedback time in ISO format
    feedback_date, feedback_time = dt.now().isoformat().split("T")

    sql = """ INSERT INTO Feedback (exam_id, user_name, feedback_time, feedback_type, text, question_id, rating, status, is_visible) VALUES 
                    (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(sql, (exam_id, user_name, feedback_time, feedback_type, text, question_id, rating, status, is_visible))

    connection.commit()
    cursor.close()
    connection.close()
    return "Feedback info inserted successfully."

# Exam supervisor now reads the feedbacks and update their status....
def read_feedbacks(exam_id, user_name):
    # the relative file path
    path = '..\data\Exam_App.db'
    # get the path to the directory this script is in
    scriptdir = os.path.dirname(__file__)
    # add the relative path to the database file from there
    db_path = os.path.join(scriptdir, path)
    # make sure the path exists and if not create it
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    connection=sqlite3.connect(db_path)
    cursor=connection.cursor()

    cursor.execute("""
    UPDATE Feedback
    SET status = 'Analyzed/Read' 
    WHERE exam_id = ? AND user_name = ?""", (exam_id, user_name))

    connection.commit()
    cursor.close()
    connection.close()

    return "Exam feedbacks analyzed/read successfully."
#----------------Utilizing the defined functions to define the database schema/structure-----------------------#
if __name__ == '__main__':
    create_user_table()
    create_role_table()
    create_permission_table()
    create_user_role_table()
    create_role_permission_table()
    create_login_table()
    create_question_table()
    create_option_table()
    create_exam_table()
    create_exam_question_table()
    create_user_exam_table()
    create_answer_table()
    create_feedback_table()
