import unittest
import sqlite3
import os
from datetime import datetime as dt, timedelta
from src.db1 import * # Import functions to be tested from the source code

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        # Create the User table before running any tests
        create_user_table()
        # Create the Role table before running any tests
        create_role_table()
        # Create the Permission table before running any tests
        create_permission_table()
        # Create the User_Role table before running any tests
        create_user_role_table()
        # Create the Role_Permission table before running any tests
        create_role_permission_table()
        # Create the Login table before running any tests
        create_login_table()
        # Create the Question table before running any tests
        create_question_table()
        # Create the Option table before running any tests
        create_option_table()
        # Create the Exam table before running any tests
        create_exam_table()
        # Create the Exam_Question table before running any tests
        create_exam_question_table()
        # Create the User_Exam table before running any tests
        create_user_exam_table()
        # Create the Answer table before running any tests
        create_answer_table()
        # Create the Feedback table before running any tests
        create_feedback_table()

    def tearDown(self):
        # Delete test-related data after each test
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM User WHERE user_name='TestUser1'")
        cursor.execute("DELETE FROM User WHERE user_name='TestQCreator1'")
        cursor.execute("DELETE FROM User WHERE user_name='TestECreator1'")
        cursor.execute("DELETE FROM User WHERE user_name='TestEHandler1'")
        cursor.execute("DELETE FROM User WHERE user_name='TestESupervisor1'")
        cursor.execute("DELETE FROM User WHERE user_name='TestStudent1'")
        cursor.execute("DELETE FROM User WHERE user_name='TestStudent2'")

        cursor.execute("DELETE FROM Role WHERE role_name='Test_Role'")
        cursor.execute("DELETE FROM Role WHERE role_name='TestRole'")

        cursor.execute("DELETE FROM Permission WHERE permission_name='Test_Permission'")
        cursor.execute("DELETE FROM Permission WHERE permission_name='TestPermission'")

        cursor.execute("DELETE FROM User_Role WHERE user_name='TestUser1' AND role_name='Test_Role'")
        cursor.execute("DELETE FROM User_Role WHERE user_name='TestQCreator1' AND role_name='Question_Creator'")
        cursor.execute("DELETE FROM User_Role WHERE user_name='TestECreator1' AND role_name='Exam_Creator'")
        cursor.execute("DELETE FROM User_Role WHERE user_name='TestEHandler1' AND role_name='Exam_Handler'")
        cursor.execute("DELETE FROM User_Role WHERE user_name='TestESupervisor1' AND role_name='Exam_Supervisor'")
        cursor.execute("DELETE FROM User_Role WHERE user_name='TestStudent1' AND role_name='Student'")
        cursor.execute("DELETE FROM User_Role WHERE user_name='TestStudent2' AND role_name='Student'")

        cursor.execute("DELETE FROM Role_Permission WHERE role_name='Test_Role' AND permission_name='Test_Permission'")
        
        cursor.execute("DELETE FROM Login WHERE user_name='TestUser1'")

        cursor.execute("DELETE FROM Question WHERE question_id='Q1000'")
        cursor.execute("DELETE FROM Question WHERE question_id='Q1001'")
        cursor.execute("DELETE FROM Question WHERE question_id='Q1002'")
        cursor.execute("DELETE FROM Question WHERE question_id='Q1003'")
        cursor.execute("DELETE FROM Question WHERE question_id='Q1004'")

        cursor.execute("DELETE FROM Option WHERE option_id='Q1000O1'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1000O2'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1000O3'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1000O4'")

        cursor.execute("DELETE FROM Option WHERE option_id='Q1001O1'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1001O2'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1001O3'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1001O4'")

        cursor.execute("DELETE FROM Option WHERE option_id='Q1002O1'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1002O2'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1002O3'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1002O4'")

        cursor.execute("DELETE FROM Option WHERE option_id='Q1003O1'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1003O2'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1003O3'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1003O4'")

        cursor.execute("DELETE FROM Option WHERE option_id='Q1004O1'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1004O2'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1004O3'")
        cursor.execute("DELETE FROM Option WHERE option_id='Q1004O4'")

        cursor.execute("DELETE FROM Exam WHERE exam_id='Ex100'")

        cursor.execute("DELETE FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1000'")
        cursor.execute("DELETE FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1001'")
        cursor.execute("DELETE FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1002'")
        cursor.execute("DELETE FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1003'")
        cursor.execute("DELETE FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1004'")

        cursor.execute("DELETE FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent1'")
        cursor.execute("DELETE FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent2'")

        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1000'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1001'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1002'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1003'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1004'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1000'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1001'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1002'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1003'""")
        cursor.execute("""DELETE FROM Answer
                       WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1004'""")
        
        cursor.execute("DELETE FROM Feedback WHERE exam_id='Ex100' AND user_name='TestStudent1'")
        cursor.execute("DELETE FROM Feedback WHERE exam_id='Ex100' AND user_name='TestStudent2'")

        connection.commit()
        connection.close()
    
    def test_create_user_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='User'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(User)")
        columns = cursor.fetchall()
        expected_columns = ['user_name', 'hashed_password', 'first_name', 'last_name', 'email',  \
                            'registration_date', 'registration_time']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)

    def test_insert_user(self):
        # Insert a user (valid username, password, firstname, lastname, email --> successful)
        self.assertEqual(insert_user('TestUser1', 'Test*1234', 'Test', 'User', 'test1@example.com'), "User info inserted successfully.")
        # Insert a user (invalid username--> unsuccessful)
        self.assertEqual(insert_user('Test_User2', 'Test*1234', 'Test', 'User', 'test2@example.com'), "Invalid username format.")
        # Insert a user (invalid password--> unsuccessful)
        self.assertEqual(insert_user('TestUser3', 'test1234', 'Test', 'User', 'test3@example.com'), "Invalid password format.")
        # Insert a user (invalid name--> unsuccessful)
        self.assertEqual(insert_user('TestUser4', 'Test*1234', 'Test4', 'User4', 'test4@example.com'), "Invalid name format.")
        # Insert a user (invalid email--> unsuccessful)
        self.assertEqual(insert_user('TestUser5', 'Test*1234', 'Test', 'User', 'test5@@example.com'), "Invalid email format.")
        # Insert a user (duplicate username--> unsuccessful)
        self.assertEqual(insert_user('TestUser1', 'Test*1234', 'Test', 'User', 'test5@@example.com'), "Username already exists.")

        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM User WHERE user_name='TestUser1'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM User WHERE user_name='Test_User2'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM User WHERE user_name='TestUser3'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM User WHERE user_name='TestUser4'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM User WHERE user_name='TestUser5'")
        res5 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'TestUser1')

        self.assertIsNone(res2)
        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
    
    def test_update_user(self):
        # Insert a user
        self.assertEqual(update_user('TestUser1', 'Test*1234', 'Test', 'User', 'test1@example.com'), "User info inserted successfully.")
        
        # update a user (valid inputs--> successful)
        self.assertEqual(update_user('TestUser1', 'Test*1234*5', 'Testt', 'Userr', 'test1@example.com'), "User info updated successfully.")
        # update a user (invalid username--> unsuccessful)
        self.assertEqual(update_user('Test_User1', 'Test*1234', 'Test', 'User', 'test2@example.com'), "Invalid username format.")
        # update a user (invalid password--> unsuccessful)
        self.assertEqual(update_user('TestUser1', 'test1234', 'Test', 'User', 'test3@example.com'), "Invalid password format.")
        # update a user (invalid name--> unsuccessful)
        self.assertEqual(update_user('TestUser1', 'Test*1234', 'Test4', 'User4', 'test4@example.com'), "Invalid name format.")
        # update a user (invalid email--> unsuccessful)
        self.assertEqual(update_user('TestUser1', 'Test*1234', 'Test', 'User', 'test5@@example.com'), "Invalid email format.")
        # update a user (valid but not registered username--> unsuccessful)
        self.assertEqual(update_user('TestUser1000', 'Test*1234', 'Test', 'User', 'test5@@example.com'), "User not registered.")

        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM User WHERE user_name='TestUser1'")
        res1 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'TestUser1')
        self.assertEqual(res1[2], 'Testt')
        self.assertEqual(res1[3], 'Userr')
        self.assertEqual(res1[4], 'test1@example.com')
    
    def test_delete_user(self):
        # Insert a user
        self.assertEqual(update_user('TestUser1', 'Test*1234', 'Test', 'User', 'test1@example.com'), "User info inserted successfully.")
        
        # delete a user (valid inputs--> successful)
        self.assertEqual(delete_user('TestUser1'), "User deleted successfully.")
        # delete a user (invalid username--> unsuccessful)
        self.assertEqual(delete_user('Test_User1'), "Invalid username format.")
        # delete a user (valid but not registered username--> unsuccessful)
        self.assertEqual(delete_user('TestUser1000'), "User not registered.")

        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM User WHERE user_name='TestUser1'")
        res1 = cursor.fetchone()

        connection.close()

        self.assertIsNone(res1)
    
    def test_create_role_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Role'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Role)")
        columns = cursor.fetchall()
        expected_columns = ['role_name', 'creation_date', 'creation_time']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)
    
    def test_insert_role(self):
        # Insert a role (valid rolename--> successful)
        self.assertEqual(insert_role('Test_Role'), "Role info inserted successfully.")
        # Insert a role (valid rolename--> successful)
        self.assertEqual(insert_role('TestRole'), "Role info inserted successfully.")
        # Insert a role (invalid rolename--> unsuccessful)
        self.assertEqual(insert_role('Test Role'), "Invalid role format.")
        # Insert a role (invalid rolename--> unsuccessful)
        self.assertEqual(insert_role('Test-Role'), "Invalid role format.")
        # Insert a role (invalid rolename--> unsuccessful)
        self.assertEqual(insert_role('Test.Role'), "Invalid role format.")
        # Insert a role (invalid rolename--> unsuccessful)
        self.assertEqual(insert_role('TestRole1'), "Invalid role format.")
        # Insert a role (valid but duplicate rolename--> unsuccessful)
        self.assertEqual(insert_role('TestRole'), "Role name already exists.")

        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Role WHERE role_name='Test_Role'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Role WHERE role_name='TestRole'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Role WHERE role_name='Test Role'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM Role WHERE role_name='Test-Role'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM Role WHERE role_name='Test.Role'")
        res5 = cursor.fetchone()

        cursor.execute("SELECT * FROM Role WHERE role_name='TestRole1'")
        res6 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'Test_Role')

        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], 'TestRole')

        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
        self.assertIsNone(res6)
    
    def test_create_permission_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Permission'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Permission)")
        columns = cursor.fetchall()
        expected_columns = ['permission_name', 'creation_date', 'creation_time']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)
    
    def test_insert_permission(self):
        # Insert a permission (valid permission name--> successful)
        self.assertEqual(insert_permission('Test_Permission'), "Permission info inserted successfully.")
        # Insert a permission (valid permission name--> successful)
        self.assertEqual(insert_permission('TestPermission'), "Invalid permission format.")
        # Insert a permission (invalid permission name--> unsuccessful)
        self.assertEqual(insert_permission('Test Permission'), "Invalid permission format.")
        # Insert a permission (invalid permission name--> unsuccessful)
        self.assertEqual(insert_permission('Test-Permission'), "Invalid permission format.")
        # Insert a permission (invalid permission name--> unsuccessful)
        self.assertEqual(insert_permission('Test.Permission'), "Invalid permission format.")
        # Insert a permission (invalid permission name--> unsuccessful)
        self.assertEqual(insert_permission('TestPermission1'), "Invalid permission format.")
        # Insert a permission (valid but duplicate permission name--> unsuccessful)
        self.assertEqual(insert_permission('Test_Permission'), "Permission name already exists.")

        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Permission WHERE permission_name='Test_Permission'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Permission WHERE permission_name='TestPermission'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Permission WHERE permission_name='Test Permission'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM Permission WHERE permission_name='Test-Permission'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM Permission WHERE permission_name='Test.Permission'")
        res5 = cursor.fetchone()

        cursor.execute("SELECT * FROM Permission WHERE permission_name='TestPermission1'")
        res6 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'Test_Permission')

        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], 'TestPermission')

        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
        self.assertIsNone(res6)
    
    def test_create_user_role_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='User_Role'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(User_Role)")
        columns = cursor.fetchall()
        expected_columns = ['user_name', 'role_name', 'role_assignment_date', 'role_assignment_time']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)
    
    def test_insert_user_role(self):
        # Insert a user and a role
        self.assertEqual(insert_user('TestUser1', 'Test*1234', 'Test', 'User', 'test1@example.com'), "User info inserted successfully.")
        self.assertEqual(insert_role('Test_Role'), "Role info inserted successfully.")
        self.assertEqual(insert_user("TestStudent1", "stud@Exam1", "Test", "Student", "stud1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestStudent1","Student"), "User role assigned successfully.")
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")
        
        # Insert a user role (valid username, role name--> successful)
        self.assertEqual(insert_user_role('TestUser1', 'Test_Role'), "User role assigned successfully.")
        # Insert a user role (invalid username--> unsuccessful)
        self.assertEqual(insert_user_role('Test User', 'Test_Role'), "Invalid username format.")
        # Insert a user role (invalid role name--> unsuccessful)
        self.assertEqual(insert_user_role('TestUser1', 'Test Role'), "Invalid role format.")
        # Insert a user role (valid but not registered user--> unsuccessful)
        self.assertEqual(insert_user_role('TestUser1000', 'Test_Role'), "User not registered.")
        # Insert a user role (valid but not created role--> unsuccessful)
        self.assertEqual(insert_user_role('TestUser1', 'Test_Role_New'), "Role not created.")
        # Insert a user role (duplicate user role--> unsuccessful)
        self.assertEqual(insert_user_role('TestUser1', 'Test_Role'), "User already assigned this role.")
        # Insert a user role (assigning another admin--> unsuccessful)
        self.assertEqual(insert_user_role('TestUser1', 'Administrator'), "No more admins are allowed.")
        # Insert a user role (assigning a student another role--> unsuccessful)
        self.assertEqual(insert_user_role('TestStudent1', 'Question_Creator'), "A student can't have any other roles.")
        # Insert a user role (assigning a non-student, student role--> unsuccessful)
        self.assertEqual(insert_user_role('TestQCreator1', 'Student'), "A non-student can't have the student role.")

        # Check if the user role has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM User_Role WHERE user_name='TestUser1' AND role_name='Test_Role'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Role WHERE user_name='Test User' AND role_name='Test_Role'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Role WHERE user_name='TestUser1' AND role_name='Test Role'")
        res3 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'TestUser1')
        self.assertEqual(res1[1], 'Test_Role')

        self.assertIsNone(res2)
        self.assertIsNone(res3)
    
    def test_create_role_permission_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Role_Permission'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Role_Permission)")
        columns = cursor.fetchall()
        expected_columns = ['role_name', 'permission_name', 'permission_assignment_date', 'permission_assignment_time']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)
    
    def test_insert_role_permission(self):
        # Insert a role and a permission
        self.assertEqual(insert_role('Test_Role'), "Role info inserted successfully.")
        self.assertEqual(insert_permission('Test_Permission'), "Permission info inserted successfully.")

        # Insert a role permission (valid role name, permission name--> successful)
        self.assertEqual(insert_role_permission('Test_Role', 'Test_Permission'), "Role Permission assigned successfully.")
        # Insert a role permission (invalid role name--> unsuccessful)
        self.assertEqual(insert_role_permission('Test Role', 'Test_Permission'), "Invalid role format.")
        # Insert a role permission (invalid permission name--> unsuccessful)
        self.assertEqual(insert_role_permission('Test_Role', 'Test Permission'), "Invalid permission format.")

        # Check if the user role has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Role_Permission WHERE role_name='Test_Role' AND permission_name='Test_Permission'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Role_Permission WHERE role_name='Test Role' AND permission_name='Test_Permission'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Role_Permission WHERE role_name='Test_Role' AND permission_name='Test Permission'")
        res3 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'Test_Role')
        self.assertEqual(res1[1], 'Test_Permission')

        self.assertIsNone(res2)
        self.assertIsNone(res3)
    
    def test_create_login_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Login'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Login)")
        columns = cursor.fetchall()
        expected_columns = ['user_name', 'login_date', 'login_time', 'logout_date', 'logout_time']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)
    
    def test_user_login(self):
        # Insert a user
        self.assertEqual(insert_user('TestUser1', 'Test*1234', 'Test', 'User', 'test1@example.com'), "User info inserted successfully.")

        # Attempt to login with incorrect credentials-->unsuccessful
        self.assertEqual(user_login('TestUser1', 'Test@1234'), "Incorrect password!")
        # Attempt to login with correct credentials-->successful
        self.assertEqual(user_login('TestUser1', 'Test*1234'), "User logged in successfully.")
        # Attempt to login for valid but unregistered username-->unsuccessful
        self.assertEqual(user_login('TestUser100', 'Test*1234'), "Username not registered.")
        # Attempt to login for invalid username-->unsuccessful
        self.assertEqual(user_login('Test User', 'Test*1234'), "Invalid username format.")
        # Attempt to login for invalid password-->unsuccessful
        self.assertEqual(user_login('TestUser1', 'Test 1234'), "Invalid password format.")
        # Attempt to login with correct credentials again-->unsuccessful
        self.assertEqual(user_login('TestUser1', 'Test*1234'), "User has already logged in!")

        # Check if the user login has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Login WHERE user_name='TestUser1'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Login WHERE user_name='TestUser100'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Login WHERE user_name='Test User'")
        res3 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'TestUser1')

        self.assertIsNone(res2)
        self.assertIsNone(res3)

    def test_user_logout(self):
        # Insert a user and a user login
        self.assertEqual(insert_user('TestUser1', 'Test*1234', 'Test', 'User', 'test1@example.com'), "User info inserted successfully.")
        self.assertEqual(user_login('TestUser1', 'Test*1234'), "User logged in successfully.")
        
        # Logout the user (valid registered username that already logged in--> successful)
        self.assertEqual(user_logout('TestUser1'), "User logged out successfully.")
        # Logout the user (valid unregistered username--> unsuccessful)
        self.assertEqual(user_logout('TestUser100'), "Username not registered.")
        # Logout the user (invalid username--> unsuccessful)
        self.assertEqual(user_logout('Test User'), "Invalid username format.")

        # Check if the user logout has been updated
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Login WHERE user_name='TestUser1'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Login WHERE user_name='TestUser100'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Login WHERE user_name='Test User'")
        res3 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'TestUser1')
        self.assertIsNotNone(res1[3])  # Check that logout date is not null

        self.assertIsNone(res2)
        self.assertIsNone(res3)
    
    def test_create_question_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Question'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Question)")
        columns = cursor.fetchall()
        expected_columns = ['question_id', 'topic', 'subtopic', 'text', 'image', 'difficulty', 'type', \
                            'points', 'creation_date', 'creation_time', 'creator_user_name']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)

    def test_insert_question(self):
        # Create a question creator user
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")

        # Insert a question (valid question_id,difficulty,type,points,creator_username with no image --> successful)
        self.assertEqual(insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        # Insert a question (valid question_id,difficulty,type,points,creator_username with a image --> successful)
        self.assertEqual(insert_question('Q1001', 'Math', 'Calculus', 'What is dy/dx for y=f(x) as in the image attached?', '..\images\Q1001.png', 'Hard', 'Descriptive/Practical', 5, 'TestQCreator1'), "Question info inserted successfully.")
        # Insert a question (invalid question_id--> unsuccessful)
        self.assertEqual(insert_question('1002', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Invalid question ID format.")
        # Insert a question (invalid difficulty--> unsuccessful)
        self.assertEqual(insert_question('Q1003', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Very Very Easy', 'Multiple choice', 5, 'TestQCreator1'), "Invalid difficulty level.")
        # Insert a question (invalid type--> unsuccessful)
        self.assertEqual(insert_question('Q1004', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Piece of cake', 5, 'TestQCreator1'), "Invalid question type.")
        # Insert a question (invalid points--> unsuccessful)
        self.assertEqual(insert_question('Q1005', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', -2.45, 'TestQCreator1'), "Invalid points value.")
        # Insert a question (invalid username--> unsuccessful)
        self.assertEqual(insert_question('Q1006', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'Test User'), "Invalid username format.")
        # Insert a question (valid unregistered username--> unsuccessful)
        self.assertEqual(insert_question('Q1007', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestUser100'), "User not registered.")
        # Insert a question (valid registered non-question creator username--> unsuccessful)
        self.assertEqual(insert_question('Q1008', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestUser1'), "User is not question creator.")
        # Insert a question (invalid image path--> unsuccessful)
        self.assertEqual(insert_question('Q1009', 'Math', 'Algebra', 'What is 2 + 2?', '\data\mypic.jpg', 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Invalid image path.")
        # Insert a question (no image and no text--> unsuccessful)
        self.assertEqual(insert_question('Q1010', 'Math', 'Algebra', None, None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "A Question must have at least a text or an image.")

        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1000'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1001'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='1002'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1003'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1004'")
        res5 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1005'")
        res6 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1006'")
        res7 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1007'")
        res8 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1008'")
        res9 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1009'")
        res10 = cursor.fetchone()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1010'")
        res11 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'Q1000')

        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], 'Q1001')

        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
        self.assertIsNone(res6)
        self.assertIsNone(res7)
        self.assertIsNone(res8)
        self.assertIsNone(res9)
        self.assertIsNone(res10)
        self.assertIsNone(res11)
    
    def test_update_question(self):
        # Create a question creator user and insert a question
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")
        self.assertEqual(insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        
        # update a question (valid inputs--> successful)
        self.assertEqual(update_question('Q1000', 'Math', 'Algebra', 'What is 5 - 2?', None, 'Easy', 'Multiple choice', 1), "Question info updated successfully.")
        # update a question (invalid question_id--> unsuccessful)
        self.assertEqual(update_question('Q1000-s1', 'Math', 'Algebra', 'What is 5 - 2?', None, 'Easy', 'Multiple choice', 1), "Invalid question ID format.")
        # update a question (invalid question_id--> unsuccessful)
        self.assertEqual(update_question('Q1000', 'Math', 'Algebra', 'What is 5 - 2?', "C:\Users", 'Easy', 'Multiple choice', 1), "Invalid image path.")
        # update a question (invalid difficulty level--> unsuccessful)
        self.assertEqual(update_question('Q1000', 'Math', 'Algebra', 'What is 5 - 2?', None, 'Too Easy', 'Multiple choice', 1), "Invalid difficulty level.")
        # update a question (invalid question type--> unsuccessful)
        self.assertEqual(update_question('Q1000', 'Math', 'Algebra', 'What is 5 - 2?', None, 'Easy', 'Randomly-chosed', 1), "Invalid question type.")
        # update a question (invalid points--> unsuccessful)
        self.assertEqual(update_question('Q1000', 'Math', 'Algebra', 'What is 5 - 2?', None, 'Easy', 'Multiple choice', -3.75), "Invalid points value.")
        # update a question (no image and no text--> unsuccessful)
        self.assertEqual(update_question('Q1000', 'Math', 'Algebra', None, None, 'Easy', 'Multiple choice', 1), "A Question must have at least a text or an image.")
        # update a question (question not exists--> unsuccessful)
        self.assertEqual(update_question('Q10000', 'Math', 'Algebra', 'What is 5 - 2?', None, 'Easy', 'Multiple choice', 1), "Question not exists.")

        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1000'")
        res1 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'Q1000')
        self.assertEqual(res1[1], 'Math')
        self.assertEqual(res1[2], 'Algebra')
        self.assertEqual(res1[3], 'What is 5 - 2?')
        self.assertIsNotNone(res1[4])
        self.assertEqual(res1[5], 'Easy')
        self.assertEqual(res1[6], 'Multiple choice')
        self.assertEqual(res1[7], 1)

    def test_delete_question(self):
        # Create a question creator user and insert a question
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")
        self.assertEqual(insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        
        # delete a question (valid inputs--> successful)
        self.assertEqual(delete_question('Q1000'), "Question deleted successfully.")
        # delete a question (invalid question_id--> unsuccessful)
        self.assertEqual(delete_question('Q1000/a-1'), "Invalid question ID format.")
        # delete a question (question not exists--> unsuccessful)
        self.assertEqual(delete_question('Q10000'), "Question not exists.")
        
        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Question WHERE question_id='Q1000'")
        res1 = cursor.fetchone()

        connection.close()

        self.assertIsNone(res1)
    
    def test_create_option_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Option'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Option)")
        columns = cursor.fetchall()
        expected_columns = ['option_id', 'question_id', 'text', 'image', 'is_correct_answer']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)
    
    def test_insert_question_option(self):
        # Create a question creator user and 2 questions
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")
        self.assertEqual(insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1001', 'Math', 'Calculus', 'What is dy/dx for y=f(x) as in the image attached?', '..\images\Q1001.png', 'Hard', 'Descriptive/Practical', 5, 'TestQCreator1'), "Question info inserted successfully.")

        # Insert 4 options (valid option_id,question_id, is_correct_answer with no image --> successful)
        self.assertEqual(insert_question_option("Q1000O1", "Q1000", "4", None, 1), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O2", "Q1000", "5", None, 0), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O3", "Q1000", "6", None, 0), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O4", "Q1000", "3", None, 0), "Question option info inserted successfully.")
        # Insert an option (invalid option_id--> unsuccessful)
        self.assertEqual(insert_question_option('O1001', 'Q1001', '1+x', None, 1), "Invalid option ID format.")
        # Insert an option (invalid question_id--> unsuccessful)
        self.assertEqual(insert_question_option("Q1002O1", '1002', '56', None, 0), "Invalid question ID format.")
        # Insert an option (valid option_id,question_id but no such question_id--> unsuccessful)
        self.assertEqual(insert_question_option("Q1002O2", 'Q1002', 'x=1', None, 0), "Question not exists.")
        # Insert an option (invalid is_correct_answer--> unsuccessful)
        self.assertEqual(insert_question_option("Q1000O5", 'Q1000', 'x=1', None, 5), "Invalid is_correct_answer.")
        # Insert an option (invalid image path--> unsuccessful)
        self.assertEqual(insert_question_option("Q1002O1", 'Q1000', 'x=1', "G:\Options", 1), "Invalid image path.")
        # Insert an option (no text no image--> unsuccessful)
        self.assertEqual(insert_question_option("Q1002O1", 'Q1000', None, None, 1), "An Option must have at least a text or an image.")
        # Insert an option (option duplication--> unsuccessful)
        self.assertEqual(insert_question_option("Q1000O1", "Q1000", "4", None, 1), "Option already exists.")
        
        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1000O1'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1000O2'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1000O3'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1000O4'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM Option WHERE option_id='O1001'")
        res5 = cursor.fetchone()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1002O1'")
        res6 = cursor.fetchone()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1002O2'")
        res7 = cursor.fetchone()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1000O5'")
        res8 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'Q1000O1')
        self.assertEqual(res1[1], 'Q1000')  # Check if the question_id is correct
        self.assertEqual(res1[2], '4')  # Check if the text is correct
        self.assertIsNone(res1[3])  # No image provided
        self.assertEqual(res1[4], 1)  # is_correct_answer should be 1

        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], 'Q1000O2')
        self.assertEqual(res2[1], 'Q1000')  # Check if the question_id is correct
        self.assertEqual(res2[2], '5')  # Check if the text is correct
        self.assertIsNone(res2[3])  # No image provided
        self.assertEqual(res2[4], 0)  # is_correct_answer should be 0

        self.assertIsNotNone(res3)
        self.assertEqual(res3[0], 'Q1000O3')
        self.assertEqual(res3[1], 'Q1000')  # Check if the question_id is correct
        self.assertEqual(res3[2], '6')  # Check if the text is correct
        self.assertIsNone(res3[3])  # No image provided
        self.assertEqual(res3[4], 0)  # is_correct_answer should be 0

        self.assertIsNotNone(res4)
        self.assertEqual(res4[0], 'Q1000O4')
        self.assertEqual(res4[1], 'Q1000')  # Check if the question_id is correct
        self.assertEqual(res4[2], '3')  # Check if the text is correct
        self.assertIsNone(res4[3])  # No image provided
        self.assertEqual(res4[4], 0)  # is_correct_answer should be 0

        self.assertIsNone(res5)
        self.assertIsNone(res6)
        self.assertIsNone(res7)
        self.assertIsNone(res8)
    
    def test_update_question_option(self):
        # Create a question creator user and 1 question with 4 options
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")
        self.assertEqual(insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O1", "Q1000", "4", None, 1), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O2", "Q1000", "5", None, 0), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O3", "Q1000", "6", None, 0), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O4", "Q1000", "3", None, 0), "Question option info inserted successfully.")

        # update an option (valid inputs--->successful)
        self.assertEqual(update_question_option("Q1000O1", "Q1000", "x=4", None, 1), "Question option info updated successfully.")
        # update an option (invalid option-id--->unsuccessful)
        self.assertEqual(update_question_option("Q1000/Op2", "Q1000", "x=5", None, 1), "Invalid option ID format.")
        # update an option (invalid question-id--->unsuccessful)
        self.assertEqual(update_question_option("Q1000O2", "Q-1000", "x=5", None, 1), "Invalid question ID format.")
        # update an option (invalid image path--->unsuccessful)
        self.assertEqual(update_question_option("Q1000O2", "Q1000", "x=5", "C:\NewOp", 1), "Invalid image path.")
        # update an option (invalid is_correct_answer--->unsuccessful)
        self.assertEqual(update_question_option("Q1000O2", "Q1000", "x=5", None, 5), "Invalid is_correct_answer.")
        # update an option (question not exists--->unsuccessful)
        self.assertEqual(update_question_option("Q1000O2", "Q10000", "x=5", None, 0), "Question not exists.")
        # update an option (option not exists--->unsuccessful)
        self.assertEqual(update_question_option("Q1000O5", "Q1000", "x=5", None, 0), "Option not exists.")

        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1000O1'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1000O2'")
        res2 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], 'Q1000O1')
        self.assertEqual(res1[1], 'Q1000')
        self.assertEqual(res1[2], 'x=4')
        self.assertIsNotNone(res1[3])
        self.assertEqual(res1[4], 1)

        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], 'Q1000O2')
        self.assertEqual(res2[1], 'Q1000')
        self.assertEqual(res2[2], '5')
        self.assertIsNotNone(res2[3])
        self.assertEqual(res2[4], 0)

    def test_delete_question_option(self):
        # Create a question creator user and 1 question with 4 options
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")
        self.assertEqual(insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O1", "Q1000", "4", None, 1), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O2", "Q1000", "5", None, 0), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O3", "Q1000", "6", None, 0), "Question option info inserted successfully.")
        self.assertEqual(insert_question_option("Q1000O4", "Q1000", "3", None, 0), "Question option info inserted successfully.")

        # delete an option (valid inputs--->successful)
        self.assertEqual(delete_question_option("Q1000O1"), "Question option info deleted successfully.")
        # delete an option (invalid option_id--->unsuccessful)
        self.assertEqual(delete_question_option("Q1000/O1"), "Invalid option ID format.")
        # delete an option (valid inputs--->unsuccessful)
        self.assertEqual(delete_question_option("Q1000O8"), "Option not exists.")

        # Check if the users has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Option WHERE option_id='Q1000O1'")
        res1 = cursor.fetchone()

        connection.close()

        self.assertIsNone(res1)

    def test_create_exam_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Exam'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Exam)")
        columns = cursor.fetchall()
        expected_columns = ['exam_id', 'exam_name', 'exam_date', 'start_time', 'duration', 'creation_date', \
                            'creation_time', 'has_negative_score', 'passing_score', 'handler_user_name', \
                            'supervisor_user_name', 'creator_user_name']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)

    def test_insert_exam(self):
        # Create a exam creator user
        self.assertEqual(insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestECreator1","Exam_Creator"), "User role assigned successfully.")
        # Create a exam handler user
        self.assertEqual(insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestEHandler1","Exam_Handler"), "User role assigned successfully.")
        # Create a exam supervisor user
        self.assertEqual(insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestESupervisor1","Exam_Supervisor"), "User role assigned successfully.")
        
        # Insert a exam (valid inputs --> successful)
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        self.assertEqual(insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam info inserted successfully.")
        # Insert a exam (invalid exam_id --> unsuccessful)
        self.assertEqual(insert_exam("E 101", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid exam ID format.")
        # Insert a exam (invalid exam_date --> unsuccessful)
        exam_date2 = (dt.now() - timedelta(days=2)).strftime('%Y/%m/%d')
        self.assertEqual(insert_exam("Ex102", "Test exam name", exam_date2, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid exam date format or it's not in the future.")
        # Insert a exam (invalid exam_time --> unsuccessful)
        self.assertEqual(insert_exam("Ex103", "Test exam name", exam_date1, "68:74:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid start time format.")
        # Insert a exam (invalid duration --> unsuccessful)
        self.assertEqual(insert_exam("Ex104", "Test exam name", exam_date1, "08:30:00", -45, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid duration value.")
        # Insert a exam (invalid has_negative_score --> unsuccessful)
        self.assertEqual(insert_exam("Ex105", "Test exam name", exam_date1, "08:30:00", 30, 10, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid value for has_negative_score.")
        # Insert a exam (invalid passing_score --> unsuccessful)
        self.assertEqual(insert_exam("Ex106", "Test exam name", exam_date1, "08:30:00", 30, 0, 200, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid passing score value.")
        # Insert a exam (invalid handler_user_name --> unsuccessful)
        self.assertEqual(insert_exam("Ex107", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "Test#E*Handler", "TestESupervisor1", "TestECreator1"), "Invalid username format.")
        # Insert a exam (valid but not registered handler_user_name --> unsuccessful)
        self.assertEqual(insert_exam("Ex108", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler100", "TestESupervisor1", "TestECreator1"), "Invalid exam handler username.")
        # Insert a exam (invalid supervisor_user_name --> unsuccessful)
        self.assertEqual(insert_exam("Ex109", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "Test@E=Supervisor1", "TestECreator1"), "Invalid username format.")
        # Insert a exam (valid but not registered supervisor_user_name --> unsuccessful)
        self.assertEqual(insert_exam("Ex110", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor100", "TestECreator1"), "Invalid exam supervisor username.")
        # Insert a exam (invalid handler_user_name --> unsuccessful)
        self.assertEqual(insert_exam("Ex111", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "Test$$ECreator1"), "Invalid username format.")
        # Insert a exam (valid but not registered handler_user_name --> unsuccessful)
        self.assertEqual(insert_exam("Ex112", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator100"), "Invalid exam creator username.")
        # Insert a exam (duplicate exam --> unsuccessful)
        self.assertEqual(insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam already exists.")

        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex100'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='E 101'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex102'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex103'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex104'")
        res5 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex105'")
        res6 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex106'")
        res7 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex107'")
        res8 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex108'")
        res9 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex109'")
        res10 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex110'")
        res11 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex111'")
        res12 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex112'")
        res13 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], "Ex100")
        self.assertEqual(res1[1], "Test exam name")
        self.assertEqual(res1[4], 30)
        self.assertEqual(res1[7], 0)
        self.assertEqual(res1[8], 40)
        self.assertEqual(res1[9], "TestEHandler1")
        self.assertEqual(res1[10], "TestESupervisor1")
        self.assertEqual(res1[11], "TestECreator1")

        self.assertIsNone(res2)
        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
        self.assertIsNone(res6)
        self.assertIsNone(res7)
        self.assertIsNone(res8)
        self.assertIsNone(res9)
        self.assertIsNone(res10)
        self.assertIsNone(res11)
        self.assertIsNone(res12)
        self.assertIsNone(res13)
    
    def test_update_exam(self):
        # Create a exam creator user
        self.assertEqual(insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestECreator1","Exam_Creator"), "User role assigned successfully.")
        # Create a exam handler user
        self.assertEqual(insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestEHandler1","Exam_Handler"), "User role assigned successfully.")
        # Create a exam supervisor user
        self.assertEqual(insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestESupervisor1","Exam_Supervisor"), "User role assigned successfully.")
        # Create a exam
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        self.assertEqual(insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam info inserted successfully.")
        
        # Update a exam (valid input --> successful)
        self.assertEqual(update_exam("Ex100", "Test exam new name", exam_date1, "08:45:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam info updated successfully.")
        # Update a exam (invalid exam_date --> successful)
        exam_date2 = (dt.now() - timedelta(days=2)).strftime('%Y/%m/%d')
        self.assertEqual(update_exam("Ex100", "Test exam name", exam_date2, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid exam date format or it's not in the future.")
        # Update a exam (invalid exam_time --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam new name", exam_date1, "68:74:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid start time format.")
        # Update a exam (invalid duration --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam new name", exam_date1, "08:30:00", -45.5, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid duration value.")
        # Update a exam (invalid has_negative_score --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam new name", exam_date1, "08:30:00", 30, 10, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid value for has_negative_score.")
        # Update a exam (invalid passing_score --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam new name", exam_date1, "08:30:00", 30, 0, 200, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Invalid passing score value.")
        # Update a exam (invalid handler_user_name --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "Test#E*Handler", "TestESupervisor1", "TestECreator1"), "Invalid username format.")
        # Update a exam (valid but not registered handler_user_name --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler100", "TestESupervisor1", "TestECreator1"), "Invalid exam handler username.")
        # Update a exam (invalid supervisor_user_name --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "Test@E=Supervisor1", "TestECreator1"), "Invalid username format.")
        # Update a exam (valid but not registered supervisor_user_name --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor100", "TestECreator1"), "Invalid exam supervisor username.")
        # Update a exam (invalid handler_user_name --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "Test$$ECreator1"), "Invalid username format.")
        # Update a exam (valid but not registered handler_user_name --> unsuccessful)
        self.assertEqual(update_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator100"), "Invalid exam creator username.")
        # Update a exam (exam not exists --> unsuccessful)
        self.assertEqual(update_exam("Ex1000", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam not exists.")
        
        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex100'")
        res1 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], "Ex100")
        self.assertEqual(res1[1], "Test exam new name")
        self.assertEqual(res1[3], "08:45:00")
        self.assertEqual(res1[4], 30)
        self.assertEqual(res1[7], 0)
        self.assertEqual(res1[8], 40)
        self.assertEqual(res1[9], "TestEHandler1")
        self.assertEqual(res1[10], "TestESupervisor1")
        self.assertEqual(res1[11], "TestECreator1")
    
    def test_delete_exam(self):
        # Create a exam creator user
        self.assertEqual(insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestECreator1","Exam_Creator"), "User role assigned successfully.")
        # Create a exam handler user
        self.assertEqual(insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestEHandler1","Exam_Handler"), "User role assigned successfully.")
        # Create a exam supervisor user
        self.assertEqual(insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestESupervisor1","Exam_Supervisor"), "User role assigned successfully.")
        # Create a exam
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        self.assertEqual(insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam question info inserted successfully.")
        
        # delete a exam (valid input --> successful)
        self.assertEqual(delete_exam("Ex100"), "Exam info deleted successfully.")
        # delete a exam (invalid exam_id --> successful)
        self.assertEqual(delete_exam("Ex/ 100"), "Invalid exam ID format.")
        # delete a exam (exam not exists --> unsuccessful)
        self.assertEqual(delete_exam("Ex1000"), "Exam not exists.")
        
        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Exam WHERE exam_id='Ex100'")
        res1 = cursor.fetchone()

        connection.close()

        self.assertIsNone(res1)
    
    def test_create_exam_question_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Exam_Question'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Exam_Question)")
        columns = cursor.fetchall()
        expected_columns = ['exam_id', 'question_id']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)

    def test_insert_exam_question(self):
        # Create a question creator user
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")
        # Create a exam creator user
        self.assertEqual(insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestECreator1","Exam_Creator"), "User role assigned successfully.")
        # Create a exam handler user
        self.assertEqual(insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestEHandler1","Exam_Handler"), "User role assigned successfully.")
        # Create a exam supervisor user
        self.assertEqual(insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestESupervisor1","Exam_Supervisor"), "User role assigned successfully.")
        # TestQCreator1 creates 5 questions
        self.assertEqual(insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1001', 'Math', 'Algebra', 'What is 2 - 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1002', 'Math', 'Algebra', 'What is 2 * 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1003', 'Math', 'Algebra', 'What is 2 / 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1004', 'Math', 'Algebra', 'What is 2 ^ 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        # TestECreator1 creates an exam
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        self.assertEqual(insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam info inserted successfully.")

        # Insert 5 exam question (valid inputs --> successful)
        self.assertEqual(insert_exam_question("Ex100", "Q1000"), "Exam question info inserted successfully.")
        self.assertEqual(insert_exam_question("Ex100", "Q1001"), "Exam question info inserted successfully.")
        self.assertEqual(insert_exam_question("Ex100", "Q1002"), "Exam question info inserted successfully.")
        self.assertEqual(insert_exam_question("Ex100", "Q1003"), "Exam question info inserted successfully.")
        self.assertEqual(insert_exam_question("Ex100", "Q1004"), "Exam question info inserted successfully.")
        # Insert an exam question (invalid exam_id --> unsuccessful)
        self.assertEqual(insert_exam_question("E 100", "Q1000"), "Invalid exam ID format.")
        # Insert an exam question (valid but not registered exam_id --> unsuccessful)
        self.assertEqual(insert_exam_question("Ex200", "Q1000"), "Invalid exam_id.")
        # Insert an exam question (invalid question_id --> unsuccessful)
        self.assertEqual(insert_exam_question("Ex100", "1000"), "Invalid question ID format.")
        # Insert an exam question (valid but not registered question_id --> unsuccessful)
        self.assertEqual(insert_exam_question("Ex100", "Q2000"), "Invalid question_id.")

        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1000'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='E 100' AND question_id='Q1000'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex200' AND question_id='Q1000'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='1000'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q2000'")
        res5 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], "Ex100")
        self.assertEqual(res1[1], "Q1000")

        self.assertIsNone(res2)
        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
    
    def test_delete_exam_question(self):
        # Create a question creator user
        self.assertEqual(insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestQCreator1","Question_Creator"), "User role assigned successfully.")
        # Create a exam creator user
        self.assertEqual(insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestECreator1","Exam_Creator"), "User role assigned successfully.")
        # Create a exam handler user
        self.assertEqual(insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestEHandler1","Exam_Handler"), "User role assigned successfully.")
        # Create a exam supervisor user
        self.assertEqual(insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestESupervisor1","Exam_Supervisor"), "User role assigned successfully.")
        # TestQCreator1 creates 5 questions
        self.assertEqual(insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1001', 'Math', 'Algebra', 'What is 2 - 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1002', 'Math', 'Algebra', 'What is 2 * 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1003', 'Math', 'Algebra', 'What is 2 / 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        self.assertEqual(insert_question('Q1004', 'Math', 'Algebra', 'What is 2 ^ 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1'), "Question info inserted successfully.")
        # TestECreator1 creates an exam
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        self.assertEqual(insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam info inserted successfully.")
        # Insert 5 exam question (valid inputs --> successful)
        self.assertEqual(insert_exam_question("Ex100", "Q1000"), "Exam question info inserted successfully.")
        self.assertEqual(insert_exam_question("Ex100", "Q1001"), "Exam question info inserted successfully.")
        self.assertEqual(insert_exam_question("Ex100", "Q1002"), "Exam question info inserted successfully.")
        self.assertEqual(insert_exam_question("Ex100", "Q1003"), "Exam question info inserted successfully.")
        self.assertEqual(insert_exam_question("Ex100", "Q1004"), "Exam question info inserted successfully.")
        
        # delete an exam question (valid --> successful)
        self.assertEqual(delete_exam_question("Ex100", "Q1000"), "Exam question info deleted successfully.")
        self.assertEqual(delete_exam_question("Ex100", "Q1001"), "Exam question info deleted successfully.")
        self.assertEqual(delete_exam_question("Ex100", "Q1002"), "Exam question info deleted successfully.")
        self.assertEqual(delete_exam_question("Ex100", "Q1003"), "Exam question info deleted successfully.")
        self.assertEqual(delete_exam_question("Ex100", "Q1004"), "Exam question info deleted successfully.")
        # delete an exam question (invalid exam_id --> unsuccessful)
        self.assertEqual(delete_exam_question("Ex200", "Q1000"), "Invalid exam_id.")
        # delete an exam question (valid but not registered exam_id --> unsuccessful)
        self.assertEqual(delete_exam_question("Ex200", "Q1000"), "Invalid exam_id.")
        # Insert an exam question (invalid question_id --> unsuccessful)
        self.assertEqual(delete_exam_question("Ex100", "1000"), "Invalid question ID format.")
        # Insert an exam question (valid but not registered question_id --> unsuccessful)
        self.assertEqual(delete_exam_question("Ex100", "Q2000"), "Invalid question_id.")

        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1000'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1001'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1002'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1003'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1004'")
        res5 = cursor.fetchone()

        cursor.execute("SELECT * FROM Exam_Question WHERE exam_id='Ex100' AND question_id='Q1005'")
        res6 = cursor.fetchone()

        connection.close()

        self.assertIsNone(res1)
        self.assertIsNone(res2)
        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
        self.assertIsNone(res6)
    
    def test_create_user_exam_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='User_Exam'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(User_Exam)")
        columns = cursor.fetchall()
        expected_columns = ['exam_id', 'user_name', 'score', 'total_questions', 'correct_answers', 'wrong_answers', \
                            'unanswered_questions', 'is_passed', 'is_marked']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)

    def test_insert_user_exam(self):
        # Create 2 student users
        self.assertEqual(insert_user("TestStudent1", "stud@Exam1", "Test", "Student", "stud1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestStudent1","Student"), "User role assigned successfully.")
        self.assertEqual(insert_user("TestStudent2", "stud@Exam2", "Test", "Student", "stud2@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestStudent2","Student"), "User role assigned successfully.")
        # Create a exam creator user
        self.assertEqual(insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestECreator1","Exam_Creator"), "User role assigned successfully.")
        # Create a exam handler user
        self.assertEqual(insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestEHandler1","Exam_Handler"), "User role assigned successfully.")
        # Create a exam supervisor user
        self.assertEqual(insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestESupervisor1","Exam_Supervisor"), "User role assigned successfully.")
        # TestECreator1 creates an exam
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        self.assertEqual(insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam info inserted successfully.")

        # insert 2 user exams (valid inputs --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, 5, 0, 0, 5, 0, 0), "User exam info inserted successfully.")
        self.assertEqual(insert_user_exam("Ex100", "TestStudent2", 0, 5, 0, 0, 5, 0, 0), "User exam info inserted successfully.")
        # insert an user exam (invalid exam_id --> unsuccessful)
        self.assertEqual(insert_user_exam("Ex 101", "TestStudent1", 0, 5, 0, 0, 5, 0, 0), "Invalid exam ID format.")
        # insert an user exam (valid but not registered exam_id --> unsuccessful)
        self.assertEqual(insert_user_exam("Ex101", "TestStudent1", 0, 5, 0, 0, 5, 0, 0), "Invalid exam_id.")
        # insert an user exam (invalid user_name --> unsuccessful)
        self.assertEqual(insert_user_exam("Ex100", "Test Student", 0, 5, 0, 0, 5, 0, 0), "Invalid username format.")
        # insert an user exam (valid but not registered user_name --> unsuccessful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent100", 0, 5, 0, 0, 5, 0, 0), "Invalid student username.")
        # insert an user exams (invalid score --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", "ali", 5, 0, 0, 5, 0, 0), "Invalid score.")
        # insert an user exams (invalid total questions --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, -3.5, 0, 0, 5, 0, 0), "Invalid total questions.")
        # insert an user exams (invalid correct answers --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, 5, 10, 0, 5, 0, 0), "Invalid correct answers.")
        # insert an user exams (invalid wrong answers --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, 5, 0, -5, 5, 0, 0), "Invalid wrong answers.")
        # insert an user exams (invalid unanswered questions --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, 5, 0, 0, 10, 0, 0), "Invalid unanswered questions.")
        # insert an user exams (invalid sum --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, 5, 1, 2, 5, 0, 0), "The sum of correct answers, wrong answers, and unanswered questions must be equal to total questions.")
        # insert an user exams (invalid is_passed --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, 5, 0, 0, 5, 10, 0), "Invalid value for is_passed.")
        # insert an user exams (invalid is_marked --> successful)
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, 5, 0, 0, 5, 0, 10), "Invalid value for is_marked.")

        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent1'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent2'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex 101' AND user_name='TestStudent1'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex101' AND user_name='TestStudent1'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex100' AND user_name='Test Student'")
        res5 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent100'")
        res6 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], "Ex100")
        self.assertEqual(res1[1], "TestStudent1")

        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], "Ex100")
        self.assertEqual(res2[1], "TestStudent2")

        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
        self.assertIsNone(res6)
    
    def test_delete_user_exam(self):
        # Create 2 student users
        self.assertEqual(insert_user("TestStudent1", "stud@Exam1", "Test", "Student", "stud1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestStudent1","Student"), "User role assigned successfully.")
        self.assertEqual(insert_user("TestStudent2", "stud@Exam2", "Test", "Student", "stud2@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestStudent2","Student"), "User role assigned successfully.")
        # Create a exam creator user
        self.assertEqual(insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestECreator1","Exam_Creator"), "User role assigned successfully.")
        # Create a exam handler user
        self.assertEqual(insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestEHandler1","Exam_Handler"), "User role assigned successfully.")
        # Create a exam supervisor user
        self.assertEqual(insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com"), "User info inserted successfully.")
        self.assertEqual(insert_user_role("TestESupervisor1","Exam_Supervisor"), "User role assigned successfully.")
        # TestECreator1 creates an exam
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        self.assertEqual(insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 40, "TestEHandler1", "TestESupervisor1", "TestECreator1"), "Exam info inserted successfully.")
        # insert 2 user exams
        self.assertEqual(insert_user_exam("Ex100", "TestStudent1", 0, 5, 0, 0, 5, 0, 0), "User exam info inserted successfully.")
        self.assertEqual(insert_user_exam("Ex100", "TestStudent2", 0, 5, 0, 0, 5, 0, 0), "User exam info inserted successfully.")

        # delete 2 user exams (valid inputs --> successful)
        self.assertEqual(delete_user_exam("Ex100", "TestStudent1"), "User exam info deleted successfully.")
        self.assertEqual(delete_user_exam("Ex100", "TestStudent2"), "User exam info deleted successfully.")
        
        # delete an user exam (invalid exam_id --> unsuccessful)
        self.assertEqual(delete_user_exam("Ex 101", "TestStudent1"), "Invalid exam ID format.")
        # delete an user exam (valid but not registered exam_id --> unsuccessful)
        self.assertEqual(delete_user_exam("Ex101", "TestStudent1"), "Invalid exam_id.")
        # delete an user exam (invalid user_name --> unsuccessful)
        self.assertEqual(delete_user_exam("Ex100", "Test Student"), "Invalid username format.")
        # delete an user exam (valid but not registered user_name --> unsuccessful)
        self.assertEqual(delete_user_exam("Ex100", "TestStudent100"), "Invalid student username.")

        # Check if the question has been inserted
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent1'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent2'")
        res2 = cursor.fetchone()

        connection.close()

        self.assertIsNone(res1)
        self.assertIsNone(res2)
    
    def test_create_answer_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Answer'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Answer)")
        columns = cursor.fetchall()
        expected_columns = ['exam_id', 'user_name', 'question_id', 'option_id', 'answer_text']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)

    def test_insert_answer(self):
        # Create 2 student users
        insert_user("TestStudent1", "stud@Exam1", "Test", "Student", "stud1@example.com")
        insert_user_role("TestStudent1","Student")
        insert_user("TestStudent2", "stud@Exam2", "Test", "Student", "stud2@example.com")
        insert_user_role("TestStudent2","Student")
        # Create a question creator user
        insert_user("TestQCreator1", "123*Qc#exam", "Test", "Question Creator", "qc1@example.com")
        insert_user_role("TestQCreator1","Question_Creator")
        # Create a exam creator user
        insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com")
        insert_user_role("TestECreator1","Exam_Creator")
        # Create a exam handler user
        insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com")
        insert_user_role("TestEHandler1","Exam_Handler")
        # Create a exam supervisor user
        insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com")
        insert_user_role("TestESupervisor1","Exam_Supervisor")
        # TestECreator1 creates an exam
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 15, "TestEHandler1", "TestESupervisor1", "TestECreator1")
        # insert 2 user exams
        insert_user_exam("Ex100", "TestStudent1", 0, 5, 0, 0, 5, 0, 0)
        insert_user_exam("Ex100", "TestStudent2", 0, 5, 0, 0, 5, 0, 0)
        # TestQCreator1 creates 5 questions
        insert_question('Q1000', 'Math', 'Algebra', 'What is 2 + 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1')
        insert_question('Q1001', 'Math', 'Algebra', 'What is 2 - 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1')
        insert_question('Q1002', 'Math', 'Algebra', 'What is 2 * 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1')
        insert_question('Q1003', 'Math', 'Algebra', 'What is 2 / 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1')
        insert_question('Q1004', 'Math', 'Algebra', 'What is 2 ^ 2?', None, 'Normal', 'Multiple choice', 5, 'TestQCreator1')
        # insert question options
        insert_question_option("Q1000O1", "Q1000", "4", None, 1)
        insert_question_option("Q1000O2", "Q1000", "5", None, 0)
        insert_question_option("Q1000O3", "Q1000", "6", None, 0)
        insert_question_option("Q1000O4", "Q1000", "3", None, 0)

        insert_question_option("Q1001O1", "Q1001", "1", None, 0)
        insert_question_option("Q1001O2", "Q1001", "0", None, 1)
        insert_question_option("Q1001O3", "Q1001", "2", None, 0)
        insert_question_option("Q1001O4", "Q1001", "3", None, 0)

        insert_question_option("Q1002O1", "Q1002", "5", None, 0)
        insert_question_option("Q1002O2", "Q1002", "6", None, 0)
        insert_question_option("Q1002O3", "Q1002", "4", None, 1)
        insert_question_option("Q1002O4", "Q1002", "1", None, 0)

        insert_question_option("Q1003O1", "Q1003", "4", None, 0)
        insert_question_option("Q1003O2", "Q1003", "3", None, 0)
        insert_question_option("Q1003O3", "Q1003", "2", None, 0)
        insert_question_option("Q1003O4", "Q1003", "1", None, 1)

        insert_question_option("Q1004O1", "Q1004", "4", None, 1)
        insert_question_option("Q1004O2", "Q1004", "5", None, 0)
        insert_question_option("Q1004O3", "Q1004", "6", None, 0)
        insert_question_option("Q1004O4", "Q1004", "3", None, 0)
        
        # insert some answers (valid inputs --> successful)
        insert_answer("Ex100", "TestStudent1", "Q1000", "Q1000O1", None)
        insert_answer("Ex100", "TestStudent1", "Q1001", "Q1001O2", None)
        insert_answer("Ex100", "TestStudent1", "Q1002", "Q1002O2", None)
        insert_answer("Ex100", "TestStudent1", "Q1003", "Q1003O4", None)
        insert_answer("Ex100", "TestStudent1", "Q1004", "Q1004O1", None)

        insert_answer("Ex100", "TestStudent2", "Q1000", None, None)
        insert_answer("Ex100", "TestStudent2", "Q1001", "Q1001O2", None)
        insert_answer("Ex100", "TestStudent2", "Q1002", "Q1002O3", None)
        insert_answer("Ex100", "TestStudent2", "Q1003", "Q1003O1", None)
        insert_answer("Ex100", "TestStudent2", "Q1004", "Q1004O2", None)
        # insert an answer (invalid exam_id --> unsuccessful)
        insert_answer("Ex 101", "TestStudent1", "Q1000", "Q1000O1", None)
        # insert an answer (valid but not registered exam_id --> unsuccessful)
        insert_answer("Ex101", "TestStudent1", "Q1001", "Q1001O1", None)
        # insert an answer (invalid user_name --> unsuccessful)
        insert_answer("Ex100", "Test Student", "Q1000", "Q1000O1", None)
        # insert an answer (valid but not registered user_name --> unsuccessful)
        insert_answer("Ex100", "TestStudent100", "Q1000", "Q1000O1", None)
        # insert an answer (invalid question_id --> unsuccessful)
        insert_answer("Ex100", "TestStudent1", "1000", "Q1000O1", None)
        # insert an answer (valid but not registered question_id --> unsuccessful)
        insert_answer("Ex100", "TestStudent1", "Q2000", "Q1000O1", None)
        # insert an answer (invalid option_id --> unsuccessful)
        insert_answer("Ex100", "TestStudent1", "Q1000", "O1", None)
        # insert an answer (valid but not registered option_id --> unsuccessful)
        insert_answer("Ex100", "TestStudent1", "Q1000", "Q1000O8", None)

        # update user_exams by calculate scores, correct_answers,...
        update_user_exam_multi("Ex100")

        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()
        # Checking Answer table
        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1000'""")
        res1 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1001'""")
        res2 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1002'""")
        res3 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1003'""")
        res4 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q1004'""")
        res5 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1000'""")
        res6 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1001'""")
        res7 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1002'""")
        res8 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1003'""")
        res9 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent2' AND question_id='Q1004'""")
        res10 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex 101' AND user_name='TestStudent1' AND question_id='Q1000'""")
        res11 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex101' AND user_name='TestStudent1' AND question_id='Q1001'""")
        res12 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='Test Student' AND question_id='Q1000'""")
        res13 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent100' AND question_id='Q1000'""")
        res14 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='1000'""")
        res15 = cursor.fetchone()

        cursor.execute("""SELECT * FROM Answer 
                    WHERE exam_id='Ex100' AND user_name='TestStudent1' AND question_id='Q2000'""")
        res16 = cursor.fetchone()
        # Checking User_Exam table
        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent1'")
        res17 = cursor.fetchone()

        cursor.execute("SELECT * FROM User_Exam WHERE exam_id='Ex100' AND user_name='TestStudent2'")
        res18 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], "Ex100")
        self.assertEqual(res1[1], "TestStudent1")
        self.assertEqual(res1[2], "Q1000")
        self.assertEqual(res1[3], "Q1000O1")

        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], "Ex100")
        self.assertEqual(res2[1], "TestStudent1")
        self.assertEqual(res2[2], "Q1001")
        self.assertEqual(res2[3], "Q1001O2")

        self.assertIsNotNone(res3)
        self.assertEqual(res3[0], "Ex100")
        self.assertEqual(res3[1], "TestStudent1")
        self.assertEqual(res3[2], "Q1002")
        self.assertEqual(res3[3], "Q1002O2")

        self.assertIsNotNone(res4)
        self.assertEqual(res4[0], "Ex100")
        self.assertEqual(res4[1], "TestStudent1")
        self.assertEqual(res4[2], "Q1003")
        self.assertEqual(res4[3], "Q1003O4")

        self.assertIsNotNone(res5)
        self.assertEqual(res5[0], "Ex100")
        self.assertEqual(res5[1], "TestStudent1")
        self.assertEqual(res5[2], "Q1004")
        self.assertEqual(res5[3], "Q1004O1")

        self.assertIsNotNone(res6)
        self.assertEqual(res6[0], "Ex100")
        self.assertEqual(res6[1], "TestStudent2")
        self.assertEqual(res6[2], "Q1000")
        self.assertIsNone(res6[3]) # this student didn't answer this question

        self.assertIsNotNone(res7)
        self.assertEqual(res7[0], "Ex100")
        self.assertEqual(res7[1], "TestStudent2")
        self.assertEqual(res7[2], "Q1001")
        self.assertEqual(res7[3], "Q1001O2")

        self.assertIsNotNone(res8)
        self.assertEqual(res8[0], "Ex100")
        self.assertEqual(res8[1], "TestStudent2")
        self.assertEqual(res8[2], "Q1002")
        self.assertEqual(res8[3], "Q1002O3")

        self.assertIsNotNone(res9)
        self.assertEqual(res9[0], "Ex100")
        self.assertEqual(res9[1], "TestStudent2")
        self.assertEqual(res9[2], "Q1003")
        self.assertEqual(res9[3], "Q1003O1")

        self.assertIsNotNone(res10)
        self.assertEqual(res10[0], "Ex100")
        self.assertEqual(res10[1], "TestStudent2")
        self.assertEqual(res10[2], "Q1004")
        self.assertEqual(res10[3], "Q1004O2")

        self.assertIsNone(res11)
        self.assertIsNone(res12)
        self.assertIsNone(res13)
        self.assertIsNone(res14)
        self.assertIsNone(res15)
        self.assertIsNone(res16)

        self.assertIsNotNone(res17)
        self.assertEqual(res17[0], "Ex100")
        self.assertEqual(res17[1], "TestStudent1")
        self.assertEqual(res17[2], 20) #score
        self.assertEqual(res17[3], 5) #total questions
        self.assertEqual(res17[4], 4) #correct answers
        self.assertEqual(res17[5], 1) #wrong answers
        self.assertEqual(res17[6], 0) #unanswered questions
        self.assertEqual(res17[7], 1) #is passed

        self.assertIsNotNone(res18)
        self.assertEqual(res18[0], "Ex100")
        self.assertEqual(res18[1], "TestStudent2")
        self.assertEqual(res18[2], 10) #score
        self.assertEqual(res18[3], 5) #total questions
        self.assertEqual(res18[4], 2) #correct answers
        self.assertEqual(res18[5], 2) #wrong answers
        self.assertEqual(res18[6], 1) #unanswered questions
        self.assertEqual(res18[7], 0) #is passed
    
    def test_create_feedback_table(self):
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Check if the User table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Feedback'")
        table_exists = cursor.fetchone()
        self.assertIsNotNone(table_exists)

        # Check if the columns are created correctly
        cursor.execute("PRAGMA table_info(Feedback)")
        columns = cursor.fetchall()
        expected_columns = ['exam_id', 'user_name', 'feedback_time', 'feedback_type', 'text', \
                            'question_id', 'rating', 'status', 'is_visible']
        self.assertEqual(len(columns), len(expected_columns))
        for column, expected_column in zip(columns, expected_columns):
            self.assertEqual(column[1], expected_column)

    def test_insert_feedback(self):
        # Create 2 student users
        insert_user("TestStudent1", "stud@Exam1", "Test", "Student", "stud1@example.com")
        insert_user_role("TestStudent1","Student")
        insert_user("TestStudent2", "stud@Exam2", "Test", "Student", "stud2@example.com")
        insert_user_role("TestStudent2","Student")
        # Create a exam creator user
        insert_user("TestECreator1", "123*Ec#exam", "Test", "Exam Creator", "ec1@example.com")
        insert_user_role("TestECreator1","Exam_Creator")
        # Create a exam handler user
        insert_user("TestEHandler1", "123*Eh#exam", "Test", "Exam Handler", "eh1@example.com")
        insert_user_role("TestEHandler1","Exam_Handler")
        # Create a exam supervisor user
        insert_user("TestESupervisor1", "123*Es#exam", "Test", "Exam Supervisor", "es1@example.com")
        insert_user_role("TestESupervisor1","Exam_Supervisor")
        # TestECreator1 creates an exam
        exam_date1 = (dt.now() + timedelta(weeks=1)).strftime('%Y/%m/%d')
        insert_exam("Ex100", "Test exam name", exam_date1, "08:30:00", 30, 0, 15, "TestEHandler1", "TestESupervisor1", "TestECreator1")
        
        # insert some feedbcks (valid inputs --> successful)
        insert_feedback("Ex100", "TestStudent1", "Suggestion for improvement", \
                        """Thank you for providing such a thorough assessment of the course material. The exam questions were engaging and thought-provoking, making the learning experience enjoyable.
                        Your exam application is good but could be better and here is my suggestion:
                        Diverse Question Types: Include a variety of question types (e.g., multiple-choice, short answer, essay) to assess different aspects of understanding.""" \
                            , None, 8, "Pending/Unread", 1)
        insert_feedback("Ex100", "TestStudent2", "Comment on clarity, and difficulty levels", \
                        """Why bother studying when the exam is filled with trick questions? It's like the professor enjoys watching us struggle.
                        Your exam application is not good enough and i have some comments on exam:
                        Overly Difficult: A few questions were overly difficult and seemed beyond the scope of what we learned in class. It would be beneficial to adjust the difficulty level to better match the course content.""" \
                            , None, 2, "Pending/Unread", 0)
        # insert a feedbck (invalid exam_id --> unsuccessful)
        insert_feedback("Ex 101", "TestStudent1", "Suggestion for improvement", "....feedback text...", None, 8, "Pending/Unread", 1)
        # insert a feedbck (valid but not registered exam_id --> unsuccessful)
        insert_feedback("Ex101", "TestStudent1", "Suggestion for improvement", "....feedback text...", None, 8, "Pending/Unread", 1)
        # insert a feedbck (invalid user_name --> unsuccessful)
        insert_feedback("Ex100", "Test Student", "Suggestion for improvement", "....feedback text...", None, 8, "Pending/Unread", 1)
        # insert a feedbck (valid but not registered user_name --> unsuccessful)
        insert_feedback("Ex100", "TestStudent100", "Suggestion for improvement", "....feedback text...", None, 8, "Pending/Unread", 1)
        # insert a feedbck (invalid feedback type --> unsuccessful)
        insert_feedback("Ex100", "TestStudent1", "Diss", "....feedback text...", None, 8, "Pending/Unread", 1)
        # insert a feedbck (invalid rating --> unsuccessful)
        insert_feedback("Ex100", "TestStudent1", "Suggestion for improvement", "....feedback text...", None, -6, "Pending/Unread", 1)
        # insert a feedbck (invalid status --> unsuccessful)
        insert_feedback("Ex100", "TestStudent1", "Suggestion for improvement", "....feedback text...", None, 8, "Sending", 1)
        # insert a feedbck (invalid is_visible --> unsuccessful)
        insert_feedback("Ex100", "TestStudent1", "Suggestion for improvement", "....feedback text...", None, 8, "Pending/Unread", 10)
        
        # Exam supervisor now reads the feedbacks and update their status....
        read_feedbacks("Ex100")

        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor = connection.cursor()
        # Checking Feedback table
        cursor.execute("SELECT * FROM Feedback WHERE exam_id='Ex100' AND user_name='TestStudent1'")
        res1 = cursor.fetchone()

        cursor.execute("SELECT * FROM Feedback WHERE exam_id='Ex100' AND user_name='TestStudent2'")
        res2 = cursor.fetchone()

        cursor.execute("SELECT * FROM Feedback WHERE exam_id='Ex 101' AND user_name='TestStudent1'")
        res3 = cursor.fetchone()

        cursor.execute("SELECT * FROM Feedback WHERE exam_id='Ex101' AND user_name='TestStudent1'")
        res4 = cursor.fetchone()

        cursor.execute("SELECT * FROM Feedback WHERE exam_id='Ex100' AND user_name='Test Student'")
        res5 = cursor.fetchone()

        cursor.execute("SELECT * FROM Feedback WHERE exam_id='Ex100' AND user_name='TestStudent100'")
        res6 = cursor.fetchone()

        connection.close()

        self.assertIsNotNone(res1)
        self.assertEqual(res1[0], "Ex100")
        self.assertEqual(res1[1], "TestStudent1")
        self.assertEqual(res1[3], "Suggestion for improvement")
        self.assertEqual(res1[6], 8)
        self.assertEqual(res1[7], "Analyzed/Read")
        self.assertEqual(res1[8], 1)

        self.assertIsNotNone(res2)
        self.assertEqual(res2[0], "Ex100")
        self.assertEqual(res2[1], "TestStudent2")
        self.assertEqual(res2[3], "Comment on clarity, and difficulty levels")
        self.assertEqual(res2[6], 2)
        self.assertEqual(res2[7], "Analyzed/Read")
        self.assertEqual(res2[8], 0)

        self.assertIsNone(res3)
        self.assertIsNone(res4)
        self.assertIsNone(res5)
        self.assertIsNone(res6)

if __name__ == '__main__':
    unittest.main()
