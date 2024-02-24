import unittest
from datetime import datetime as dt
from src.db1 import * # Import functions to be tested from the source code

class TestValidations(unittest.TestCase):
    def test_is_username(self):
        self.assertTrue(is_username("username123"))
        self.assertTrue(is_username("456User"))

        self.assertFalse(is_username("user name"))
        self.assertFalse(is_username("user@name"))
        self.assertFalse(is_username("user_name"))
        self.assertFalse(is_username("user-name"))
        self.assertFalse(is_username("user.name"))

    def test_is_name(self):
        self.assertTrue(is_name("John"))
        self.assertTrue(is_name("John-Doe"))
        self.assertTrue(is_name("John Doe"))

        self.assertFalse(is_name("John123"))
        self.assertFalse(is_name("John_Doe"))
        self.assertFalse(is_name("John#Doe"))
        self.assertFalse(is_name("A.Simons"))

    def test_is_password(self):
        self.assertTrue(is_password("Passw0rd!"))
        self.assertTrue(is_password("Password@1"))

        self.assertFalse(is_password("Pa1*s"))
        self.assertFalse(is_password("password"))
        self.assertFalse(is_password("passw0rd"))
        self.assertFalse(is_password("12345678"))
        self.assertFalse(is_password("abc*5678"))

    def test_is_email(self):
        self.assertTrue(is_email("user@example.com"))
        self.assertTrue(is_email("user.name@example.com"))

        self.assertFalse(is_email("user@@example.com"))
        self.assertFalse(is_email(".user@example.com"))
        self.assertFalse(is_email("user.@example.com"))
        self.assertFalse(is_email("user.@example..com"))
        self.assertFalse(is_email("user..s@example.com"))
        self.assertFalse(is_email("user#example.com"))
        self.assertFalse(is_email("user@example"))
        self.assertFalse(is_email("example.com"))
        self.assertFalse(is_email("user@.com"))
    
    def test_is_role_permission(self):
        # Same for roles and permissions
        self.assertTrue(is_role_permission("TestRole"))
        self.assertTrue(is_role_permission("Test_Role"))

        self.assertFalse(is_role_permission("Test Role"))
        self.assertFalse(is_role_permission("TestRole1"))
        self.assertFalse(is_role_permission("Test-Role"))
        self.assertFalse(is_role_permission("Test.Role"))
    
    def test_is_question_id(self):
        # Test is_question_id function with valid and invalid question IDs
        self.assertTrue(is_question_id('Q123'))
        self.assertTrue(is_question_id('Q1'))

        self.assertFalse(is_question_id('Q0'))
        self.assertFalse(is_question_id('Qabc'))
        self.assertFalse(is_question_id('Q'))
        self.assertFalse(is_question_id('1Q'))
        self.assertFalse(is_question_id('120'))

    def test_is_image_path(self):
        # Test is_image_path function with valid and invalid image paths
        self.assertTrue(is_image_path('..\images\Q123.png'))
        self.assertTrue(is_image_path('..\images\Q1.jpg'))

        self.assertFalse(is_image_path('..\images\Q0.png'))
        self.assertFalse(is_image_path('..\images\Qabc.gif'))
        self.assertFalse(is_image_path('..\images\Q123.txt'))
        self.assertFalse(is_image_path('.\images\Q123.png'))
        self.assertFalse(is_image_path('\images\Q123.png'))
        self.assertFalse(is_image_path('..\data\Q123.png'))
        self.assertFalse(is_image_path('..\images\O123.png'))

    def test_is_option_id(self):
        self.assertTrue(is_option_id('Q123O1'))
        self.assertTrue(is_option_id('Q1O1'))

        self.assertFalse(is_option_id('Q0O1'))
        self.assertFalse(is_option_id('Q123'))
        self.assertFalse(is_option_id('Q1O'))
        self.assertFalse(is_option_id('O1'))
        self.assertFalse(is_option_id('1O'))
        self.assertFalse(is_option_id('123'))
    
    def test_exam_id_format(self):
        self.assertTrue(is_exam_id('Ex123'))

        self.assertFalse(is_exam_id('Exam123'))
        self.assertFalse(is_exam_id('Ex0'))
        self.assertFalse(is_exam_id('123'))

    def test_valid_exam_date(self):
        future_date = (dt.now().date().year + 1, 1, 1)  # Date set to next year
        future_date_str = f"{future_date[0]}/{'{:02d}'.format(future_date[1])}/{'{:02d}'.format(future_date[2])}"
        self.assertTrue(is_valid_exam_date(future_date_str))
        
        past_date_str = "2020/01/01"
        self.assertFalse(is_valid_exam_date(past_date_str))

        invalid_date_str = "2022-01-01"  # Invalid format
        self.assertFalse(is_valid_exam_date(invalid_date_str))

    def test_valid_exam_time(self):
        valid_time_str = "13:30:00"
        self.assertTrue(is_valid_exam_time(valid_time_str))

        invalid_time_str = "25:30:00"  # Invalid hour
        self.assertFalse(is_valid_exam_time(invalid_time_str))

        invalid_format_str = "1:30 PM"  # Invalid format
        self.assertFalse(is_valid_exam_time(invalid_format_str))