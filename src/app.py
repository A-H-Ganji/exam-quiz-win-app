import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter import messagebox, filedialog
from db1 import *
from datetime import datetime, timedelta
from csv import writer
import shutil
from tkcalendar import Calendar
import random

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")

        # Set fixed window size
        self.geometry("800x600")
        
        # Disable window resizing
        self.resizable(False, False)

        # Load the background image
        # the relative file path
        path = "..\images\login_background.jpg"
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the file from there
        image_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        self.background_image = Image.open(image_path)
        self.background_image = self.background_image.resize((800, 600), Image.BILINEAR)  # Resize the image to fit the window
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a label for the background image
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.grid(row=0, column=0, sticky="nsew")

        # Set row and column configurations to make the window expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a frame for login components
        self.login_frame = tk.Frame(self.background_label, bg='white')
        self.login_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

        # Welcome label
        self.welcome_label = tk.Label(self.login_frame, text="Welcome to Exam/Quiz Application", font=("Helvetica", 20, "bold"), bg='white', fg='black', height=2)
        self.welcome_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Create a frame for username components
        self.username_frame = tk.Frame(self.login_frame, bg='white', height=2)
        self.username_frame.grid(row=1, column=0, padx=30, sticky="w")

        # Username label
        self.username_label = tk.Label(self.username_frame, text="Username:", font=("Helvetica", 16), bg='white', fg='black', height=2)
        self.username_label.grid(row=1, column=0, padx=(10, 5), sticky="e")

        # Username entry
        self.username_entry = tk.Entry(self.username_frame, relief="groove", borderwidth=2, font=("Helvetica", 16))
        self.username_entry.grid(row=1, column=1, padx=(0, 10), sticky="w")

        # Create a frame for password-related components
        self.password_frame = tk.Frame(self.login_frame, bg='white', height=2)
        self.password_frame.grid(row=2, column=0, padx=30, sticky="w")

        # Password label
        self.password_label = tk.Label(self.password_frame, text="Password:", font=("Helvetica", 16), bg='white', fg='black', height=2)
        self.password_label.grid(row=0, column=0, padx=(10, 5), sticky="e")

        # Password entry
        self.password_entry = tk.Entry(self.password_frame, relief="groove", borderwidth=2, font=("Helvetica", 16), show="*")
        self.password_entry.grid(row=0, column=1, pady=5, sticky="w")

        # Forgot Password button
        path = "..\images\\forgot_password.png"
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the file from there
        image_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        self.forgot_password_image = Image.open(image_path)
        self.forgot_password_icon = ImageTk.PhotoImage(self.forgot_password_image)
        self.forgot_password_button = tk.Button(self.password_frame, image=self.forgot_password_icon, cursor="hand2", command=self.forgot_password, width=26, height=26)
        self.forgot_password_button.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="w")

        # Buttons frame
        self.buttons_frame = tk.Frame(self.login_frame, bg='white')
        self.buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Login button
        self.login_button = tk.Button(self.buttons_frame, text="Login", font=("Helvetica", 14), cursor="hand2", command=self.login)
        self.login_button.grid(row=0, column=0, padx=10, pady=10)

        # Clear button
        self.clear_button = tk.Button(self.buttons_frame, text="Clear", font=("Helvetica", 14), cursor="hand2", command=self.clear_fields)
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)

        # Center the frame on the window
        self.center_frame()

        # Bind the window resizing event to centering the frame
        self.bind("<Configure>", self.center_frame)

    def center_frame(self, event=None):
        # Update the grid to ensure that the frame is centered
        self.login_frame.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        frame_width = self.login_frame.winfo_width()
        frame_height = self.login_frame.winfo_height()
        x = (window_width - frame_width) // 2
        y = (window_height - frame_height) // 2
        self.login_frame.grid_configure(padx=x, pady=y)

    # Login functionality
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if both fields are filled
        if not username or not password:
            messagebox.showinfo("Incomplete Information", "Please enter both username and password.")
            return

        login_message = user_login(username, password)

        if login_message == "User logged in successfully.":
            self.withdraw()  # Hide the login page
            user_panel = UserPanel(self, username)
            user_panel.mainloop()
        else:
            messagebox.showinfo("Login Result", login_message)
    
    # Clear functionality
    def clear_fields(self):
        # Clear username and password fields
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
    
    # Forgot Password functionality
    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Contact the admin to reset your password.")

class UserPanel(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username
        # Store reference to parent (Login page)
        self.parent = parent
        self.title("User Panel")

        # Set fixed window size
        self.geometry("1200x700")
        # make the background white
        self.configure(bg='white')

        # Retrieve user information from the database
        # the relative file path
        path = '..\data\Exam_App.db'
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the file from there
        db_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection=sqlite3.connect(db_path)
        cursor=connection.cursor()

        # Query user first and last name from the database
        cursor.execute("""
        SELECT first_name, last_name 
        FROM User
        WHERE user_name = ?""", (self.username, ))
        self.first_name, self.last_name = cursor.fetchone()

        # Query user roles from the database
        cursor.execute("""
        SELECT UR.role_name 
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.user_name = ?""", (self.username, ))
        self.roles = [role[0] for role in cursor.fetchall()]

        connection.close()

        # Create the top frame for user information and logout button
        self.create_top_frame()

        # Create the notebook (tabbed window)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Add tabs based on user roles(single-role users)
        if len(self.roles) == 1 and self.roles[0] == 'Administrator':
            self.add_admin_tabs()
        elif len(self.roles) == 1 and self.roles[0] == 'Question_Creator':
            self.add_question_creator_tabs()
        elif len(self.roles) == 1 and self.roles[0] == 'Exam_Creator':
            self.add_exam_creator_tabs()
        elif len(self.roles) == 1 and self.roles[0] == 'Exam_Supervisor':
            self.add_exam_supervisor_tabs()
        elif len(self.roles) == 1 and self.roles[0] == 'Exam_Handler':
            self.add_exam_handler_tabs()
        elif len(self.roles) == 1 and self.roles[0] == 'Exam_Analyst':
            self.add_exam_analyst_tabs()
        elif len(self.roles) == 1 and self.roles[0] == 'Student':
            self.add_student_tabs()
        # ...... Managing multi-role users ......
        
    
        # Bind the event handler to the tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def create_top_frame(self):
        # Top frame to display user name, date/time, and logout button
        self.top_frame = tk.Frame(self, bg='white', bd=2, relief='solid')
        self.top_frame.pack(fill='x', side='top')

        # Display user's name
        self.name_label = tk.Label(self.top_frame, text=f"Name: {self.first_name} {self.last_name}", font=("Helvetica", 12), bg='white')
        self.name_label.pack(side='left', padx=(10, 50))

        # Logout button
        self.create_logout_button()

        # Display today's date and time
        self.date_time_label = tk.Label(self.top_frame, text="", font=("Helvetica", 12), bg='white')
        self.date_time_label.pack(side='right', padx=(50, 10))

        # Update the time periodically
        self.update_time()

    def create_logout_button(self):
        path = "..\images\logout.png"
        scriptdir = os.path.dirname(__file__)
        image_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        logout_button_image = Image.open(image_path)
        self.logout_icon = ImageTk.PhotoImage(logout_button_image)
        self.logout_button = tk.Button(self.top_frame, image=self.logout_icon, command=self.logout, width=32, height=32, bd=0, bg="orange", borderwidth=2, cursor="hand2")
        self.logout_button.pack(side='right')  

    def add_admin_tabs(self):
        # Add tabs for different functionalities
        self.admin_security_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.admin_security_tab, text='Security')
        self.create_admin_security_widgets(self.admin_security_tab)

        self.admin_reports_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.admin_reports_tab, text='Reports')
        self.create_admin_reports_widgets(self.admin_reports_tab)

        self.admin_help_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.admin_help_tab, text='Help')
        self.create_admin_help_widgets(self.admin_help_tab)

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.config(text=f"Today's Date and Time: {current_time}")
        self.after(1000, self.update_time) 

    def logout(self):
        # Call user_logout function from db1.py
        user_logout(self.username)
        # Close the user panel window
        self.destroy()
        # Show the login window
        self.parent.deiconify()
    
    def create_admin_security_widgets(self, admin_security_tab):
        # Create a frame for Users labeled frame
        self.users_frame = tk.LabelFrame(admin_security_tab, text="Users")
        self.users_frame.pack(padx=10, pady=10)

        # Add radio buttons for Insert, Update, and Delete
        self.user_opr_var = tk.StringVar()
        self.user_opr_var.set("insert_user")  # Default selection

        insert_radio = tk.Radiobutton(self.users_frame, text="Insert New User", variable=self.user_opr_var, value="insert_user", command=self.config_fields)
        insert_radio.grid(row=0, column=0)

        update_radio = tk.Radiobutton(self.users_frame, text="Update Existing User", variable=self.user_opr_var, value="update_user", command=self.config_fields)
        update_radio.grid(row=0, column=1)

        delete_radio = tk.Radiobutton(self.users_frame, text="Delete Existing User", variable=self.user_opr_var, value="delete_user", command=self.config_fields)
        delete_radio.grid(row=0, column=2)

        # Add a frame to display user fields
        self.user_fields_frame1 = tk.Frame(self.users_frame)
        self.user_fields_frame1.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Labels and entry fields for user information
        self.username_label1 = tk.Label(self.user_fields_frame1, text="Username:")
        self.username_label1.grid(row=0, column=0, padx=5)
        self.username_entry1 = tk.Entry(self.user_fields_frame1)
        self.username_entry1.grid(row=1, column=0, padx=5)

        self.password_label = tk.Label(self.user_fields_frame1, text="Password:")
        self.password_label.grid(row=0, column=1, padx=5)
        self.password_entry = tk.Entry(self.user_fields_frame1, show='*')
        self.password_entry.grid(row=1, column=1, padx=5)

        self.first_name_label = tk.Label(self.user_fields_frame1, text="First Name:")
        self.first_name_label.grid(row=0, column=2, padx=5)
        self.first_name_entry = tk.Entry(self.user_fields_frame1)
        self.first_name_entry.grid(row=1, column=2, padx=5)

        self.last_name_label = tk.Label(self.user_fields_frame1, text="Last Name:")
        self.last_name_label.grid(row=0, column=3, padx=5)
        self.last_name_entry = tk.Entry(self.user_fields_frame1)
        self.last_name_entry.grid(row=1, column=3, padx=5)

        self.email_label = tk.Label(self.user_fields_frame1, text="Email:")
        self.email_label.grid(row=0, column=4, padx=5)
        self.email_entry = tk.Entry(self.user_fields_frame1)
        self.email_entry.grid(row=1, column=4, padx=5)

        # Add a frame to display user management buttons
        self.user_buttons_frame = tk.Frame(self.users_frame)
        self.user_buttons_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # Buttons for user operations
        self.insert_user_button = tk.Button(self.user_buttons_frame, text="Insert User", cursor="hand2", command=self.gui_insert_user)
        self.insert_user_button.grid(row=0, column=0, padx=5)

        self.update_user_button = tk.Button(self.user_buttons_frame, text="Update User", cursor="hand2", command=self.gui_update_user)
        self.update_user_button.grid(row=0, column=1, padx=5)

        self.delete_user_button = tk.Button(self.user_buttons_frame, text="Delete User", cursor="hand2", command=self.gui_delete_user)
        self.delete_user_button.grid(row=0, column=2, padx=5)

        # initial config of buttons based on 'insert'
        self.delete_user_button.config(state=tk.NORMAL)
        self.update_user_button.config(state=tk.DISABLED)
        self.delete_user_button.config(state=tk.DISABLED)

        # Set focus to the username field
        self.username_entry1.focus_set()

        # Create a frame for Roles labeled frame
        self.roles_frame = tk.LabelFrame(admin_security_tab, text="Roles")
        self.roles_frame.pack(padx=10, pady=10)

        # Add a frame for username field
        self.user_fields_frame2 = tk.Frame(self.roles_frame)
        self.user_fields_frame2.grid(row=0, column=0, padx=10, pady=10)

        # Labels and entry fields for user role information
        self.username_label2 = tk.Label(self.user_fields_frame2, text="Username:")
        self.username_label2.grid(row=0, column=0, padx=5)
        self.username_entry2 = tk.Entry(self.user_fields_frame2)
        self.username_entry2.grid(row=0, column=1, padx=5)

        # Add a frame for checkboxes
        self.role_checkboxes_frame = tk.Frame(self.roles_frame)
        self.role_checkboxes_frame.grid(row=1, column=0, padx=10, pady=10)
        
        # Add checkboxes for roles
        self.exam_analyst_var = tk.BooleanVar()
        self.exam_analyst_var.set(False)
        exam_analyst_checkbox = tk.Checkbutton(self.role_checkboxes_frame, text="Exam_Analyst", variable=self.exam_analyst_var)
        exam_analyst_checkbox.grid(row=0, column=0)

        self.exam_creator_var = tk.BooleanVar()
        self.exam_creator_var.set(False)
        exam_creator_checkbox = tk.Checkbutton(self.role_checkboxes_frame, text="Exam_Creator", variable=self.exam_creator_var)
        exam_creator_checkbox.grid(row=0, column=1)

        self.exam_handler_var = tk.BooleanVar()
        self.exam_handler_var.set(False)
        exam_handler_checkbox = tk.Checkbutton(self.role_checkboxes_frame, text="Exam_Handler", variable=self.exam_handler_var)
        exam_handler_checkbox.grid(row=0, column=2)

        self.exam_supervisor_var = tk.BooleanVar()
        self.exam_supervisor_var.set(False)
        exam_supervisor_checkbox = tk.Checkbutton(self.role_checkboxes_frame, text="Exam_Supervisor", variable=self.exam_supervisor_var)
        exam_supervisor_checkbox.grid(row=0, column=3)

        self.question_creator_var = tk.BooleanVar()
        self.question_creator_var.set(False)
        question_creator_checkbox = tk.Checkbutton(self.role_checkboxes_frame, text="Question_Creator", variable=self.question_creator_var)
        question_creator_checkbox.grid(row=0, column=4)

        self.student_var = tk.BooleanVar()
        self.student_var.set(False)
        student_checkbox = tk.Checkbutton(self.role_checkboxes_frame, text="Student", variable=self.student_var)
        student_checkbox.grid(row=0, column=5)

        # Add a frame to display role management buttons
        self.role_buttons_frame = tk.Frame(self.roles_frame)
        self.role_buttons_frame.grid(row=2, column=0, padx=10, pady=10)

        # Buttons for user role assignment/revoke
        self.assign_role_button = tk.Button(self.role_buttons_frame, text="Assign User Role", cursor="hand2", command=self.assign_user_role)
        self.assign_role_button.grid(row=0, column=0, padx=5)

        self.revoke_role_button = tk.Button(self.role_buttons_frame, text="Revoke User Role", cursor="hand2", command=self.revoke_user_role)
        self.revoke_role_button.grid(row=0, column=1, padx=5)

    def config_fields(self):
        operation = self.user_opr_var.get()

        # Handle 'insert' operation
        if operation == 'insert_user':
            # Enable/disable fields
            self.username_entry1.config(state=tk.NORMAL)
            self.password_entry.config(state=tk.NORMAL)
            self.first_name_entry.config(state=tk.NORMAL)
            self.last_name_entry.config(state=tk.NORMAL)
            self.email_entry.config(state=tk.NORMAL)

            # Clear/reset fields
            self.username_entry1.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            # Enable/disable buttons
            self.insert_user_button.config(state=tk.NORMAL)
            self.update_user_button.config(state=tk.DISABLED)
            self.delete_user_button.config(state=tk.DISABLED)
            
            # Set focus to the username field
            self.username_entry1.focus_set()

        # Handle 'update' operation
        elif operation == 'update_user':
            # Clear/reset fields
            self.username_entry1.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            # Enable/disable fields
            self.username_entry1.config(state=tk.NORMAL)
            self.password_entry.config(state=tk.NORMAL)
            self.first_name_entry.config(state=tk.NORMAL)
            self.last_name_entry.config(state=tk.NORMAL)
            self.email_entry.config(state=tk.NORMAL)

            # Enable/disable buttons
            self.insert_user_button.config(state=tk.DISABLED)
            self.update_user_button.config(state=tk.NORMAL)
            self.delete_user_button.config(state=tk.DISABLED)

            # Set focus to the username field
            self.username_entry1.focus_set()

        # Handle 'delete' operation    
        elif operation == 'delete_user':
            # Clear/reset fields
            self.username_entry1.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            # Enable/disable fields
            self.username_entry1.config(state=tk.NORMAL)
            self.password_entry.config(state=tk.DISABLED)
            self.first_name_entry.config(state=tk.DISABLED)
            self.last_name_entry.config(state=tk.DISABLED)
            self.email_entry.config(state=tk.DISABLED)

            # Enable/disable buttons
            self.insert_user_button.config(state=tk.DISABLED)
            self.update_user_button.config(state=tk.DISABLED)
            self.delete_user_button.config(state=tk.NORMAL)

            # Set focus to the username field
            self.username_entry1.focus_set()

    def gui_insert_user(self):
        username = self.username_entry1.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get() if len(self.email_entry.get()) > 0 else None

        # Validate fields
        if not (username and password and first_name and last_name):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return

        # Call insert_user function from db1.py
        insert_msg = insert_user(username, password, first_name, last_name, email)
        messagebox.showinfo("User Insert", insert_msg)

    def gui_update_user(self):
        username = self.username_entry1.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get() if len(self.email_entry.get()) > 0 else None

        # Validate fields
        if not (username and password and first_name and last_name):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return

        # Call update_user function from db1.py
        update_msg = update_user(username, password, first_name, last_name, email)
        messagebox.showinfo("User Update", update_msg)

    def gui_delete_user(self):
        username = self.username_entry1.get()

        # Validate fields
        if not username:
            messagebox.showwarning("Incomplete Information", "Please insert a username to delete.")
            return

        # Call delete_user function from db1.py
        delete_msg = delete_user(username)
        messagebox.showinfo("User Delete", delete_msg)
    
    def assign_user_role(self):
        username = self.username_entry2.get()

        # Validate fields
        if not username or not any([self.exam_analyst_var.get(), self.exam_creator_var.get(), self.exam_handler_var.get(),
                                   self.exam_supervisor_var.get(), self.question_creator_var.get(), self.student_var.get()]):
            messagebox.showwarning("Incomplete Information", "Please insert a username and at least select a role.")
            return
        
        # Call insert_user_role function from db1.py for each of the check roles
        if self.exam_analyst_var.get():
            assign_user_role_msg = insert_user_role(username, "Exam_Analyst")
            messagebox.showinfo("Assign User Role", assign_user_role_msg)
        if self.exam_creator_var.get():
            assign_user_role_msg = insert_user_role(username, "Exam_Creator")
            messagebox.showinfo("Assign User Role", assign_user_role_msg)
        if self.exam_handler_var.get():
            assign_user_role_msg = insert_user_role(username, "Exam_Handler")
            messagebox.showinfo("Assign User Role", assign_user_role_msg)
        if self.exam_supervisor_var.get():
            assign_user_role_msg = insert_user_role(username, "Exam_Supervisor")
            messagebox.showinfo("Assign User Role", assign_user_role_msg)
        if self.question_creator_var.get():
            assign_user_role_msg = insert_user_role(username, "Question_Creator")
            messagebox.showinfo("Assign User Role", assign_user_role_msg)
        if self.student_var.get():
            assign_user_role_msg = insert_user_role(username, "Student")
            messagebox.showinfo("Assign User Role", assign_user_role_msg)
    
    def revoke_user_role(self):
        username = self.username_entry2.get()

        # Validate fields
        if not username or not any([self.exam_analyst_var.get(), self.exam_creator_var.get(), self.exam_handler_var.get(),
                                   self.exam_supervisor_var.get(), self.question_creator_var.get(), self.student_var.get()]):
            messagebox.showwarning("Incomplete Information", "Please insert a username and at least select a role.")
            return
        
        # Call delete_user_role function from db1.py for each of the check roles
        if self.exam_analyst_var.get():
            revoke_user_role_msg = delete_user_role(username, "Exam_Analyst")
            messagebox.showinfo("Revoke User Role", revoke_user_role_msg)
        if self.exam_creator_var.get():
            revoke_user_role_msg = delete_user_role(username, "Exam_Creator")
            messagebox.showinfo("Revoke User Role", revoke_user_role_msg)
        if self.exam_handler_var.get():
            revoke_user_role_msg = delete_user_role(username, "Exam_Handler")
            messagebox.showinfo("Revoke User Role", revoke_user_role_msg)
        if self.exam_supervisor_var.get():
            revoke_user_role_msg = delete_user_role(username, "Exam_Supervisor")
            messagebox.showinfo("Revoke User Role", revoke_user_role_msg)
        if self.question_creator_var.get():
            revoke_user_role_msg = delete_user_role(username, "Question_Creator")
            messagebox.showinfo("Revoke User Role", revoke_user_role_msg)
        if self.student_var.get():
            revoke_user_role_msg = delete_user_role(username, "Student")
            messagebox.showinfo("Revoke User Role", revoke_user_role_msg)
    
    def create_admin_reports_widgets(self, admin_reports_tab):
        # Table refresh image 
        path = "..\images\\refresh.png"
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the file from there
        image_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        self.refresh_image = Image.open(image_path)
        self.refresh_icon = ImageTk.PhotoImage(self.refresh_image)

        # Table button image 
        path = "..\images\\table.png"
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the file from there
        image_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        self.table_image = Image.open(image_path)
        self.table_icon = ImageTk.PhotoImage(self.table_image)

        # Table csv file image 
        path = "..\images\\csvfile.png"
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the file from there
        image_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        self.csvfile_image = Image.open(image_path)
        self.csvfile_icon = ImageTk.PhotoImage(self.csvfile_image)

        # Create an upper frame for stats
        self.stats_frame = tk.Label(admin_reports_tab)
        self.stats_frame.grid(row=0, column=0, sticky="nsew")

        # Button to refresh stats
        self.refresh_stats_button = tk.Button(self.stats_frame, text="Refresh Stats  ", image=self.refresh_icon, compound=tk.RIGHT, cursor="hand2", command=self.refresh_stats)
        self.refresh_stats_button.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        
        # Create a labeled frame for User stats
        self.user_stats_frame = tk.LabelFrame(self.stats_frame, text="User Stats")
        self.user_stats_frame.grid(row=1, column=0, padx=10, sticky="nsew")
        
        # Labels for different user stats
        self.total_users_label = tk.Label(self.user_stats_frame, text="Total Users:")
        self.total_users_label.grid(row=0, column=0, padx=5, sticky="w")
        self.total_users_var = tk.StringVar()
        self.total_users_var.set("")  # Default value
        self.total_users_value_label = tk.Label(self.user_stats_frame, textvariable=self.total_users_var)
        self.total_users_value_label.grid(row=0, column=1, padx=5, sticky="w")
        self.table_button1 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_users, width=20, height=20)
        self.table_button1.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button1 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.users_tocsv, width=20, height=20)
        self.tocsv_button1.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.students_label = tk.Label(self.user_stats_frame, text="Students:")
        self.students_label.grid(row=1, column=0, padx=5, sticky="w")
        self.students_var = tk.StringVar()
        self.students_var.set("")  # Default value
        self.students_value_label = tk.Label(self.user_stats_frame, textvariable=self.students_var)
        self.students_value_label.grid(row=1, column=1, padx=5, sticky="w")
        self.table_button2 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_students, width=20, height=20)
        self.table_button2.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button2 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.students_tocsv, width=20, height=20)
        self.tocsv_button2.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.exam_analysts_label = tk.Label(self.user_stats_frame, text="Exam Analysts:")
        self.exam_analysts_label.grid(row=2, column=0, padx=5, sticky="w")
        self.exam_analysts_var = tk.StringVar()
        self.exam_analysts_var.set("")  # Default value
        self.exam_analysts_value_label = tk.Label(self.user_stats_frame, textvariable=self.exam_analysts_var)
        self.exam_analysts_value_label.grid(row=2, column=1, padx=5, sticky="w")
        self.table_button3 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_exam_analysts, width=20, height=20)
        self.table_button3.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button3 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.exam_analysts_tocsv, width=20, height=20)
        self.tocsv_button3.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        self.exam_creators_label = tk.Label(self.user_stats_frame, text="Exam Creators:")
        self.exam_creators_label.grid(row=3, column=0, padx=5, sticky="w")
        self.exam_creators_var = tk.StringVar()
        self.exam_creators_var.set("")  # Default value
        self.exam_creators_value_label = tk.Label(self.user_stats_frame, textvariable=self.exam_creators_var)
        self.exam_creators_value_label.grid(row=3, column=1, padx=5, sticky="w")
        self.table_button4 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_exam_creators, width=20, height=20)
        self.table_button4.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button4 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.exam_creators_tocsv, width=20, height=20)
        self.tocsv_button4.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        self.exam_handlers_label = tk.Label(self.user_stats_frame, text="Exam Handlers:")
        self.exam_handlers_label.grid(row=4, column=0, padx=5, sticky="w")
        self.exam_handlers_var = tk.StringVar()
        self.exam_handlers_var.set("")  # Default value
        self.exam_handlers_value_label = tk.Label(self.user_stats_frame, textvariable=self.exam_handlers_var)
        self.exam_handlers_value_label.grid(row=4, column=1, padx=5, sticky="w")
        self.table_button5 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_exam_handlers, width=20, height=20)
        self.table_button5.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button5 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.exam_handlers_tocsv, width=20, height=20)
        self.tocsv_button5.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        self.exam_supervisors_label = tk.Label(self.user_stats_frame, text="Exam Supervisors:")
        self.exam_supervisors_label.grid(row=5, column=0, padx=5, sticky="w")
        self.exam_supervisors_var = tk.StringVar()
        self.exam_supervisors_var.set("")  # Default value
        self.exam_supervisors_value_label = tk.Label(self.user_stats_frame, textvariable=self.exam_supervisors_var)
        self.exam_supervisors_value_label.grid(row=5, column=1, padx=5, sticky="w")
        self.table_button6 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_exam_supervisors, width=20, height=20)
        self.table_button6.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button6 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.exam_supervisors_tocsv, width=20, height=20)
        self.tocsv_button6.grid(row=5, column=3, padx=5, pady=5, sticky="w")

        self.question_creators_label = tk.Label(self.user_stats_frame, text="Question Creators:")
        self.question_creators_label.grid(row=6, column=0, padx=5, sticky="w")
        self.question_creators_var = tk.StringVar()
        self.question_creators_var.set("")  # Default value
        self.question_creators_value_label = tk.Label(self.user_stats_frame, textvariable=self.question_creators_var)
        self.question_creators_value_label.grid(row=6, column=1, padx=5, sticky="w")
        self.table_button7 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_question_creators, width=20, height=20)
        self.table_button7.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button7 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.question_creators_tocsv, width=20, height=20)
        self.tocsv_button7.grid(row=6, column=3, padx=5, pady=5, sticky="w")
        
        self.multirole_users_label = tk.Label(self.user_stats_frame, text="Multi-role Users:")
        self.multirole_users_label.grid(row=7, column=0, padx=5, sticky="w")
        self.multirole_users_var = tk.StringVar()
        self.multirole_users_var.set("")  # Default value
        self.multirole_users_value_label = tk.Label(self.user_stats_frame, textvariable=self.multirole_users_var)
        self.multirole_users_value_label.grid(row=7, column=1, padx=5, sticky="w")
        self.table_button8 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_multirole_users, width=20, height=20)
        self.table_button8.grid(row=7, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button8 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.multirole_users_tocsv, width=20, height=20)
        self.tocsv_button8.grid(row=7, column=3, padx=5, pady=5, sticky="w")

        self.users_loggedin_label = tk.Label(self.user_stats_frame, text="User Logged in:")
        self.users_loggedin_label.grid(row=8, column=0, padx=5, sticky="w")
        self.users_loggedin_var = tk.StringVar()
        self.users_loggedin_var.set("")  # Default value
        self.users_loggedin_value_label = tk.Label(self.user_stats_frame, textvariable=self.users_loggedin_var)
        self.users_loggedin_value_label.grid(row=8, column=1, padx=5, sticky="w")
        self.table_button9 = tk.Button(self.user_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_users_loggedin, width=20, height=20)
        self.table_button9.grid(row=8, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button9 = tk.Button(self.user_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.users_loggedin_tocsv, width=20, height=20)
        self.tocsv_button9.grid(row=8, column=3, padx=5, pady=5, sticky="w")

        # Create a labeled frame for Question stats
        self.question_stats_frame = tk.LabelFrame(self.stats_frame, text="Question Stats")
        self.question_stats_frame.grid(row=1, column=1, padx=10, sticky="nsew")
        
        # Labels for different question stats
        self.total_questions_label = tk.Label(self.question_stats_frame, text="Total Questions:")
        self.total_questions_label.grid(row=0, column=0, padx=5, sticky="w")
        self.total_questions_var = tk.StringVar()
        self.total_questions_var.set("")  # Default value
        self.total_questions_value_label = tk.Label(self.question_stats_frame, textvariable=self.total_questions_var)
        self.total_questions_value_label.grid(row=0, column=1, padx=5, sticky="w")
        self.table_button10 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_questions, width=20, height=20)
        self.table_button10.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button10 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.questions_tocsv, width=20, height=20)
        self.tocsv_button10.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.total_topics_label = tk.Label(self.question_stats_frame, text="Total Topics:")
        self.total_topics_label.grid(row=1, column=0, padx=5, sticky="w")
        self.total_topics_var = tk.StringVar()
        self.total_topics_var.set("")  # Default value
        self.total_topics_value_label = tk.Label(self.question_stats_frame, textvariable=self.total_topics_var)
        self.total_topics_value_label.grid(row=1, column=1, padx=5, sticky="w")
        self.table_button11 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2",command=self.load_topics, width=20, height=20)
        self.table_button11.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button11 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.topics_tocsv, width=20, height=20)
        self.tocsv_button11.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
        self.total_subtopics_label = tk.Label(self.question_stats_frame, text="Total Subopics:")
        self.total_subtopics_label.grid(row=2, column=0, padx=5, sticky="w")
        self.total_subtopics_var = tk.StringVar()
        self.total_subtopics_var.set("")  # Default value
        self.total_subtopics_value_label = tk.Label(self.question_stats_frame, textvariable=self.total_subtopics_var)
        self.total_subtopics_value_label.grid(row=2, column=1, padx=5, sticky="w")
        self.table_button12 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_subtopics, width=20, height=20)
        self.table_button12.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button12 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.subtopics_tocsv, width=20, height=20)
        self.tocsv_button12.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        self.multiple_choice_questions_label = tk.Label(self.question_stats_frame, text="Multiple Choice Questions:")
        self.multiple_choice_questions_label.grid(row=3, column=0, padx=5, sticky="w")
        self.multiple_choice_questions_var = tk.StringVar()
        self.multiple_choice_questions_var.set("")  # Default value
        self.multiple_choice_questions_value_label = tk.Label(self.question_stats_frame, textvariable=self.multiple_choice_questions_var)
        self.multiple_choice_questions_value_label.grid(row=3, column=1, padx=5, sticky="w")
        self.table_button13 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_multiple_choice_questions, width=20, height=20)
        self.table_button13.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button13 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.multiple_choice_questions_tocsv, width=20, height=20)
        self.tocsv_button13.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        self.true_false_questions_label = tk.Label(self.question_stats_frame, text="True/False Questions:")
        self.true_false_questions_label.grid(row=4, column=0, padx=5, sticky="w")
        self.true_false_questions_var = tk.StringVar()
        self.true_false_questions_var.set("")  # Default value
        self.true_false_questions_value_label = tk.Label(self.question_stats_frame, textvariable=self.true_false_questions_var)
        self.true_false_questions_value_label.grid(row=4, column=1, padx=5, sticky="w")
        self.table_button14 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_true_false_questions, width=20, height=20)
        self.table_button14.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button14 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.true_false_questions_tocsv, width=20, height=20)
        self.tocsv_button14.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        self.descriptive_practical_questions_label = tk.Label(self.question_stats_frame, text="Descriptive/Practical Questions:")
        self.descriptive_practical_questions_label.grid(row=5, column=0, padx=5, sticky="w")
        self.descriptive_practical_questions_var = tk.StringVar()
        self.descriptive_practical_questions_var.set("")  # Default value
        self.descriptive_practical_questions_value_label = tk.Label(self.question_stats_frame, textvariable=self.descriptive_practical_questions_var)
        self.descriptive_practical_questions_value_label.grid(row=5, column=1, padx=5, sticky="w")
        self.table_button15 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_descriptive_practical_questions, width=20, height=20)
        self.table_button15.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button15 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.descriptive_practical_questions_tocsv, width=20, height=20)
        self.tocsv_button15.grid(row=5, column=3, padx=5, pady=5, sticky="w")

        self.easy_questions_label = tk.Label(self.question_stats_frame, text="Easy Questions:")
        self.easy_questions_label.grid(row=6, column=0, padx=5, sticky="w")
        self.easy_questions_var = tk.StringVar()
        self.easy_questions_var.set("")  # Default value
        self.easy_questions_value_label = tk.Label(self.question_stats_frame, textvariable=self.easy_questions_var)
        self.easy_questions_value_label.grid(row=6, column=1, padx=5, sticky="w")
        self.table_button16 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_easy_questions, width=20, height=20)
        self.table_button16.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button16 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.easy_questions_tocsv, width=20, height=20)
        self.tocsv_button16.grid(row=6, column=3, padx=5, pady=5, sticky="w")

        self.normal_questions_label = tk.Label(self.question_stats_frame, text="Normal Questions:")
        self.normal_questions_label.grid(row=7, column=0, padx=5, sticky="w")
        self.normal_questions_var = tk.StringVar()
        self.normal_questions_var.set("")  # Default value
        self.normal_questions_value_label = tk.Label(self.question_stats_frame, textvariable=self.normal_questions_var)
        self.normal_questions_value_label.grid(row=7, column=1, padx=5, sticky="w")
        self.table_button17 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_normal_questions, width=20, height=20)
        self.table_button17.grid(row=7, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button17 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.normal_questions_tocsv, width=20, height=20)
        self.tocsv_button17.grid(row=7, column=3, padx=5, pady=5, sticky="w")

        self.hard_questions_label = tk.Label(self.question_stats_frame, text="Hard Questions:")
        self.hard_questions_label.grid(row=8, column=0, padx=5, sticky="w")
        self.hard_questions_var = tk.StringVar()
        self.hard_questions_var.set("")  # Default value
        self.hard_questions_value_label = tk.Label(self.question_stats_frame, textvariable=self.hard_questions_var)
        self.hard_questions_value_label.grid(row=8, column=1, padx=5, sticky="w")
        self.table_button18 = tk.Button(self.question_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_hard_questions, width=20, height=20)
        self.table_button18.grid(row=8, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button18 = tk.Button(self.question_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.hard_questions_tocsv, width=20, height=20)
        self.tocsv_button18.grid(row=8, column=3, padx=5, pady=5, sticky="w")
    
        # Create a labeled frame for Exam stats
        self.exam_stats_frame = tk.LabelFrame(self.stats_frame, text="Exam Stats")
        self.exam_stats_frame.grid(row=1, column=2, padx=10, sticky="nsew")
        
        # Labels for different exam stats
        self.total_exams_label = tk.Label(self.exam_stats_frame, text="Total Exams:")
        self.total_exams_label.grid(row=0, column=0, padx=5, sticky="w")
        self.total_exams_var = tk.StringVar()
        self.total_exams_var.set("")  # Default value
        self.total_exams_value_label = tk.Label(self.exam_stats_frame, textvariable=self.total_exams_var)
        self.total_exams_value_label.grid(row=0, column=1, padx=5, sticky="w")
        self.table_button19 = tk.Button(self.exam_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_exams, width=20, height=20)
        self.table_button19.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button19 = tk.Button(self.exam_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.exams_tocsv, width=20, height=20)
        self.tocsv_button19.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.unstarted_exams_label = tk.Label(self.exam_stats_frame, text="Unstarted Exams:")
        self.unstarted_exams_label.grid(row=1, column=0, padx=5, sticky="w")
        self.unstarted_exams_var = tk.StringVar()
        self.unstarted_exams_var.set("")  # Default value
        self.unstarted_exams_value_label = tk.Label(self.exam_stats_frame, textvariable=self.unstarted_exams_var)
        self.unstarted_exams_value_label.grid(row=1, column=1, padx=5, sticky="w")
        self.table_button20 = tk.Button(self.exam_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_unstarted_exams, width=20, height=20)
        self.table_button20.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button20 = tk.Button(self.exam_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.unstarted_exams_tocsv, width=20, height=20)
        self.tocsv_button20.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.started_exams_label = tk.Label(self.exam_stats_frame, text="Started Exams:")
        self.started_exams_label.grid(row=2, column=0, padx=5, sticky="w")
        self.started_exams_var = tk.StringVar()
        self.started_exams_var.set("")  # Default value
        self.started_exams_value_label = tk.Label(self.exam_stats_frame, textvariable=self.started_exams_var)
        self.started_exams_value_label.grid(row=2, column=1, padx=5, sticky="w")
        self.table_button21 = tk.Button(self.exam_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_started_exams, width=20, height=20)
        self.table_button21.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button21 = tk.Button(self.exam_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.started_exams_tocsv, width=20, height=20)
        self.tocsv_button21.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        self.finished_exams_label = tk.Label(self.exam_stats_frame, text="Finished Exams:")
        self.finished_exams_label.grid(row=3, column=0, padx=5, sticky="w")
        self.finished_exams_var = tk.StringVar()
        self.finished_exams_var.set("")  # Default value
        self.finished_exams_value_label = tk.Label(self.exam_stats_frame, textvariable=self.finished_exams_var)
        self.finished_exams_value_label.grid(row=3, column=1, padx=5, sticky="w")
        self.table_button22 = tk.Button(self.exam_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_finished_exams, width=20, height=20)
        self.table_button22.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button22 = tk.Button(self.exam_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.finished_exams_tocsv, width=20, height=20)
        self.tocsv_button22.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        self.students_taking_exam_label = tk.Label(self.exam_stats_frame, text="Students Taking Exam:")
        self.students_taking_exam_label.grid(row=4, column=0, padx=5, sticky="w")
        self.students_taking_exam_var = tk.StringVar()
        self.students_taking_exam_var.set("")  # Default value
        self.students_taking_exam_value_label = tk.Label(self.exam_stats_frame, textvariable=self.students_taking_exam_var)
        self.students_taking_exam_value_label.grid(row=4, column=1, padx=5, sticky="w")
        self.table_button23 = tk.Button(self.exam_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_students_taking_exam, width=20, height=20)
        self.table_button23.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button23 = tk.Button(self.exam_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.students_taking_exam_tocsv, width=20, height=20)
        self.tocsv_button23.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        self.students_took_exam_label = tk.Label(self.exam_stats_frame, text="Students Took Exam:")
        self.students_took_exam_label.grid(row=5, column=0, padx=5, sticky="w")
        self.students_took_exam_var = tk.StringVar()
        self.students_took_exam_var.set("")  # Default value
        self.students_took_exam_value_label = tk.Label(self.exam_stats_frame, textvariable=self.students_took_exam_var)
        self.students_took_exam_value_label.grid(row=5, column=1, padx=5, sticky="w")
        self.table_button24 = tk.Button(self.exam_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_students_took_exam, width=20, height=20)
        self.table_button24.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button24 = tk.Button(self.exam_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.students_took_exam_tocsv, width=20, height=20)
        self.tocsv_button24.grid(row=5, column=3, padx=5, pady=5, sticky="w")

        # Create a labeled frame for feedback
        self.feedback_stats_frame = tk.LabelFrame(self.stats_frame, text="Feedback Stats")
        self.feedback_stats_frame.grid(row=1, column=3, padx=10, sticky="nsew")

        # Labels for different feedback stats
        self.total_feedbacks_label = tk.Label(self.feedback_stats_frame, text="Total Feedbacks:")
        self.total_feedbacks_label.grid(row=0, column=0, padx=5, sticky="w")
        self.total_feedbacks_var = tk.StringVar()
        self.total_feedbacks_var.set("")  # Default value
        self.total_feedbacks_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.total_feedbacks_var)
        self.total_feedbacks_value_label.grid(row=0, column=1, padx=5, sticky="w")
        self.table_button25 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_feedbacks, width=20, height=20)
        self.table_button25.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button25 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.feedbacks_tocsv, width=20, height=20)
        self.tocsv_button25.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.suggestions_for_improvement_label = tk.Label(self.feedback_stats_frame, text="Suggestions for improvement:")
        self.suggestions_for_improvement_label.grid(row=1, column=0, padx=5, sticky="w")
        self.suggestions_for_improvement_var = tk.StringVar()
        self.suggestions_for_improvement_var.set("")  # Default value
        self.suggestions_for_improvement_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.suggestions_for_improvement_var)
        self.suggestions_for_improvement_value_label.grid(row=1, column=1, padx=5, sticky="w")
        self.table_button26 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_suggestions_for_improvement, width=20, height=20)
        self.table_button26.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button26 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.suggestions_for_improvement_tocsv, width=20, height=20)
        self.tocsv_button26.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.comments_on_clarity_difficulty_label = tk.Label(self.feedback_stats_frame, text="Comments on clarity, and difficulty levels:")
        self.comments_on_clarity_difficulty_label.grid(row=2, column=0, padx=5, sticky="w")
        self.comments_on_clarity_difficulty_var = tk.StringVar()
        self.comments_on_clarity_difficulty_var.set("")  # Default value
        self.comments_on_clarity_difficulty_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.comments_on_clarity_difficulty_var)
        self.comments_on_clarity_difficulty_value_label.grid(row=2, column=1, padx=5, sticky="w")
        self.table_button27 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_comments_on_clarity_difficulty, width=20, height=20)
        self.table_button27.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button27 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.comments_on_clarity_difficulty_tocsv, width=20, height=20)
        self.tocsv_button27.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        self.low_ratings_label = tk.Label(self.feedback_stats_frame, text="Low Ratings(1-3):")
        self.low_ratings_label.grid(row=3, column=0, padx=5, sticky="w")
        self.low_ratings_var = tk.StringVar()
        self.low_ratings_var.set("")  # Default value
        self.low_ratings_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.low_ratings_var)
        self.low_ratings_value_label.grid(row=3, column=1, padx=5, sticky="w")
        self.table_button28 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_low_ratings, width=20, height=20)
        self.table_button28.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button28 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.low_ratings_tocsv, width=20, height=20)
        self.tocsv_button28.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        self.medium_ratings_label = tk.Label(self.feedback_stats_frame, text="Medium Ratings(4-6):")
        self.medium_ratings_label.grid(row=4, column=0, padx=5, sticky="w")
        self.medium_ratings_var = tk.StringVar()
        self.medium_ratings_var.set("")  # Default value
        self.medium_ratings_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.medium_ratings_var)
        self.medium_ratings_value_label.grid(row=4, column=1, padx=5, sticky="w")
        self.table_button29 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_medium_ratings, width=20, height=20)
        self.table_button29.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button29 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.medium_ratings_tocsv, width=20, height=20)
        self.tocsv_button29.grid(row=4, column=3, padx=5, pady=5, sticky="w")

        self.high_ratings_label = tk.Label(self.feedback_stats_frame, text="High Ratings(7-10):")
        self.high_ratings_label.grid(row=5, column=0, padx=5, sticky="w")
        self.high_ratings_var = tk.StringVar()
        self.high_ratings_var.set("")  # Default value
        self.high_ratings_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.high_ratings_var)
        self.high_ratings_value_label.grid(row=5, column=1, padx=5, sticky="w")
        self.table_button30 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_high_ratings, width=20, height=20)
        self.table_button30.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button30 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.high_ratings_tocsv, width=20, height=20)
        self.tocsv_button30.grid(row=5, column=3, padx=5, pady=5, sticky="w")

        self.pending_unread_feedbacks_label = tk.Label(self.feedback_stats_frame, text="Pending/Unread Feedbacks:")
        self.pending_unread_feedbacks_label.grid(row=6, column=0, padx=5, sticky="w")
        self.pending_unread_feedbacks_var = tk.StringVar()
        self.pending_unread_feedbacks_var.set("")  # Default value
        self.pending_unread_feedbacks_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.pending_unread_feedbacks_var)
        self.pending_unread_feedbacks_value_label.grid(row=6, column=1, padx=5, sticky="w")
        self.table_button31 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_pending_unread_feedbacks, width=20, height=20)
        self.table_button31.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button31 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.pending_unread_feedbacks_tocsv, width=20, height=20)
        self.tocsv_button31.grid(row=6, column=3, padx=5, pady=5, sticky="w")

        self.analyzed_read_feedbacks_label = tk.Label(self.feedback_stats_frame, text="Analyzed/Read Feedbacks:")
        self.analyzed_read_feedbacks_label.grid(row=7, column=0, padx=5, sticky="w")
        self.analyzed_read_feedbacks_var = tk.StringVar()
        self.analyzed_read_feedbacks_var.set("")  # Default value
        self.analyzed_read_feedbacks_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.analyzed_read_feedbacks_var)
        self.analyzed_read_feedbacks_value_label.grid(row=7, column=1, padx=5, sticky="w")
        self.table_button32 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_analyzed_read_feedbacks, width=20, height=20)
        self.table_button32.grid(row=7, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button32 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.analyzed_read_feedbacks_tocsv, width=20, height=20)
        self.tocsv_button32.grid(row=7, column=3, padx=5, pady=5, sticky="w")

        self.visible_feedbacks_label = tk.Label(self.feedback_stats_frame, text="Visible Feedbacks:")
        self.visible_feedbacks_label.grid(row=8, column=0, padx=5, sticky="w")
        self.visible_feedbacks_var = tk.StringVar()
        self.visible_feedbacks_var.set("")  # Default value
        self.visible_feedbacks_value_label = tk.Label(self.feedback_stats_frame, textvariable=self.visible_feedbacks_var)
        self.visible_feedbacks_value_label.grid(row=8, column=1, padx=5, sticky="w")
        self.table_button33 = tk.Button(self.feedback_stats_frame, image=self.table_icon, cursor="hand2", command=self.load_visible_feedbacks, width=20, height=20)
        self.table_button33.grid(row=8, column=2, padx=5, pady=5, sticky="w")
        self.tocsv_button33 = tk.Button(self.feedback_stats_frame, image=self.csvfile_icon, cursor="hand2", command=self.visible_feedbacks_tocsv, width=20, height=20)
        self.tocsv_button33.grid(row=8, column=3, padx=5, pady=5, sticky="w")

        # Create a frame for table containing data
        self.table_frame = tk.Frame(admin_reports_tab)
        self.table_frame.grid(row=2, column=0, sticky="nsew")
            
    def refresh_stats(self, event=None):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) AS user_count FROM User") 
        total_users = cursor.fetchone()
        self.total_users_var.set(total_users)

        cursor.execute("""SELECT COUNT(*) AS students_count
                       FROM User_Role
                       WHERE role_name = 'Student'""") 
        students = cursor.fetchone()
        self.students_var.set(students)

        cursor.execute("""SELECT COUNT(*) AS students_count
                       FROM User_Role
                       WHERE role_name = 'Exam_Analyst'""")
        exam_analysts = cursor.fetchone()
        self.exam_analysts_var.set(exam_analysts)
        
        cursor.execute("""SELECT COUNT(*) AS students_count
                       FROM User_Role
                       WHERE role_name = 'Exam_Creator'""")
        exam_creators = cursor.fetchone()
        self.exam_creators_var.set(exam_creators)

        cursor.execute("""SELECT COUNT(*) AS students_count
                       FROM User_Role
                       WHERE role_name = 'Exam_Handler'""")
        exam_handlers = cursor.fetchone()
        self.exam_handlers_var.set(exam_handlers)
        
        cursor.execute("""SELECT COUNT(*) AS students_count
                       FROM User_Role
                       WHERE role_name = 'Exam_Supervisor'""")
        exam_supervisors = cursor.fetchone()
        self.exam_supervisors_var.set(exam_supervisors)

        cursor.execute("""SELECT COUNT(*) AS students_count
                       FROM User_Role
                       WHERE role_name = 'Question_Creator'""")
        question_creators = cursor.fetchone()
        self.question_creators_var.set(question_creators)

        cursor.execute("""SELECT COUNT(*) AS multi_role_user_count 
                        FROM (
                            SELECT user_name 
                            FROM User_Role 
                            GROUP BY user_name 
                            HAVING COUNT(*) > 1
                        ) AS multi_role_users""")
        multirole_users = cursor.fetchone()
        self.multirole_users_var.set(multirole_users)
        
        cursor.execute("""SELECT COUNT(*) AS users_loggedin 
                       FROM Login
                       WHERE logout_date IS NULL""")
        users_loggedin = cursor.fetchone()
        self.users_loggedin_var.set(users_loggedin)
        
        cursor.execute("SELECT COUNT(*) AS total_questions FROM Question") 
        total_questions = cursor.fetchone()
        self.total_questions_var.set(total_questions)
        
        cursor.execute("SELECT COUNT(DISTINCT topic) AS distinct_topic_count FROM Question")
        total_topics = cursor.fetchone()
        self.total_topics_var.set(total_topics)

        cursor.execute("SELECT COUNT(DISTINCT subtopic) AS distinct_subtopic_count FROM Question")
        total_subtopics = cursor.fetchone()
        self.total_subtopics_var.set(total_subtopics)
        
        cursor.execute("""SELECT COUNT(*) AS multiple_choice_questions 
                       FROM Question
                       WHERE type = 'Multiple choice'""")
        multiple_choice_questions = cursor.fetchone()
        self.multiple_choice_questions_var.set(multiple_choice_questions)
        
        cursor.execute("""SELECT COUNT(*) AS true_false_questions 
                       FROM Question
                       WHERE type = 'True/False'""")
        true_false_questions = cursor.fetchone()
        self.true_false_questions_var.set(true_false_questions)
        
        cursor.execute("""SELECT COUNT(*) AS descriptive_practical_questions 
                       FROM Question
                       WHERE type = 'Descriptive/Practical'""")
        descriptive_practical_questions = cursor.fetchone()
        self.descriptive_practical_questions_var.set(descriptive_practical_questions)

        cursor.execute("""SELECT COUNT(*) AS easy_questions 
                       FROM Question
                       WHERE difficulty = 'Easy'""")
        easy_questions = cursor.fetchone()
        self.easy_questions_var.set(easy_questions)
        
        cursor.execute("""SELECT COUNT(*) AS normal_questions 
                       FROM Question
                       WHERE difficulty = 'Normal'""")
        normal_questions = cursor.fetchone()
        self.normal_questions_var.set(normal_questions)

        cursor.execute("""SELECT COUNT(*) AS hard_questions 
                       FROM Question
                       WHERE difficulty = 'Hard'""")
        hard_questions = cursor.fetchone()
        self.hard_questions_var.set(hard_questions)
        
        cursor.execute("SELECT COUNT(*) AS total_exams FROM Exam") 
        total_exams = cursor.fetchone()
        self.total_exams_var.set(total_exams)

        cursor.execute("""SELECT COUNT(*) AS unstarted_exams
                        FROM Exam
                        WHERE DATETIME('now', 'localtime') < DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time)""")
        unstarted_exams = cursor.fetchone()
        self.unstarted_exams_var.set(unstarted_exams)
        
        cursor.execute("""SELECT COUNT(*) AS started_exams
                        FROM Exam
                        WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time)
                        AND DATETIME('now', 'localtime') < DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes')""")
        started_exams = cursor.fetchone()
        self.started_exams_var.set(started_exams)

        cursor.execute("""SELECT COUNT(*) AS finished_exams
                        FROM Exam
                        WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes')""")
        finished_exams = cursor.fetchone()
        self.finished_exams_var.set(finished_exams)

        cursor.execute("""SELECT COUNT(*) AS students_taking_exam
                        FROM User_Exam
                        WHERE exam_id IN (
                            SELECT exam_id
                            FROM Exam
                            WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time)
                                AND DATETIME('now', 'localtime') <= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes'))""")
        students_taking_exam = cursor.fetchone()
        self.students_taking_exam_var.set(students_taking_exam)
        
        cursor.execute("""SELECT COUNT(DISTINCT user_name) AS students_took_exam
                        FROM User_Exam
                        WHERE exam_id IN (
                            SELECT exam_id
                            FROM Exam
                            WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes'))""")
        students_took_exam = cursor.fetchone()
        self.students_took_exam_var.set(students_took_exam)

        cursor.execute("""SELECT COUNT(*) AS total_feedbacks FROM Feedback""")
        total_feedbacks = cursor.fetchone()
        self.total_feedbacks_var.set(total_feedbacks)

        cursor.execute("""SELECT COUNT(*) AS suggestions_for_improvement
                       FROM Feedback
                       WHERE feedback_type = 'Suggestion for improvement'""")
        suggestions_for_improvement = cursor.fetchone()
        self.suggestions_for_improvement_var.set(suggestions_for_improvement)

        cursor.execute("""SELECT COUNT(*) AS comments_on_clarity_difficulty
                       FROM Feedback
                       WHERE feedback_type = 'Comment on clarity, and difficulty levels'""")
        comments_on_clarity_difficulty = cursor.fetchone()
        self.comments_on_clarity_difficulty_var.set(comments_on_clarity_difficulty)

        cursor.execute("""SELECT COUNT(*) AS low_ratings
                       FROM Feedback
                       WHERE rating BETWEEN 1 AND 3""")
        low_ratings = cursor.fetchone()
        self.low_ratings_var.set(low_ratings)

        cursor.execute("""SELECT COUNT(*) AS medium_ratings
                       FROM Feedback
                       WHERE rating BETWEEN 4 AND 6""")
        medium_ratings = cursor.fetchone()
        self.medium_ratings_var.set(medium_ratings)

        cursor.execute("""SELECT COUNT(*) AS high_ratings
                       FROM Feedback
                       WHERE rating BETWEEN 7 AND 10""")
        high_ratings = cursor.fetchone()
        self.high_ratings_var.set(high_ratings)

        cursor.execute("""SELECT COUNT(*) AS pending_unread_feedbacks
                       FROM Feedback
                       WHERE status = 'Pending/Unread'""")
        pending_unread_feedbacks = cursor.fetchone()
        self.pending_unread_feedbacks_var.set(pending_unread_feedbacks)

        cursor.execute("""SELECT COUNT(*) AS pending_unread_feedbacks
                       FROM Feedback
                       WHERE status = 'Analyzed/Read'""")
        analyzed_read_feedbacks = cursor.fetchone()
        self.analyzed_read_feedbacks_var.set(analyzed_read_feedbacks)

        cursor.execute("""SELECT COUNT(*) AS visible_feedbacks
                       FROM Feedback
                       WHERE is_visible = 1""")
        visible_feedbacks = cursor.fetchone()
        self.visible_feedbacks_var.set(visible_feedbacks)

        connection.close()

    def on_tab_changed(self, event):
        # Get the currently selected tab
        current_tab = self.notebook.tab(self.notebook.select(), "text")

        # Check if the current tab is "Reports"
        if current_tab == "Reports":
            # Call the refresh_stats function
            self.refresh_stats()
    
    def load_users(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT user_name, first_name, last_name, email, registration_date, registration_time
        FROM User""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="email", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 160, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="registration_date", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="registration_time", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_students(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Student'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="email", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 160, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="registration_date", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="registration_time", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_exam_analysts(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Exam_Analyst'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="email", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 160, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="registration_date", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="registration_time", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_exam_creators(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Exam_Creator'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="email", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 160, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="registration_date", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="registration_time", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_exam_handlers(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Exam_Handler'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="email", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 160, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="registration_date", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="registration_time", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_exam_supervisors(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Exam_Supervisor'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="email", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 160, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="registration_date", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="registration_time", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_question_creators(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Question_Creator'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="email", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 160, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="registration_date", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="registration_time", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_multirole_users(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, GROUP_CONCAT(UR.role_name, ', ') AS user_roles
        FROM User U 
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        GROUP BY UR.user_name
        HAVING COUNT(*) > 1""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "user_roles")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="user_roles", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 300, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_users_loggedin(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, L.login_date, L.login_time
        FROM User U 
        JOIN Login L
        ON U.user_name = L.user_name
        WHERE L.logout_date IS NULL""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "login_date", "login_time")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="login_date", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="login_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 115, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_questions(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, text,difficulty, type, points, creation_date, creation_time, creator_user_name
                       FROM Question""")
        data = cursor.fetchall()
        connection.close()

        columns = ("question_id", "topic", "subtopic", "text", "difficulty", "type", \
                        "points", "creation_date", "creation_time", "creator")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="question_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="topic", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="subtopic", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="difficulty", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="type", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="points",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="creation_date", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 90, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="creation_time", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 90, minwidth=50, anchor=tk.W)
        self.table.heading("#10", text="creator", anchor=tk.W)
        self.table.column("#10", stretch=tk.NO, width = 90, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_topics(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT topic FROM Question")
        data = cursor.fetchall()
        connection.close()

        columns = ("topic")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="topic", anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_subtopics(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT subtopic FROM Question")
        data = cursor.fetchall()
        connection.close()

        columns = ("subtopic")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="subtopic", anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_multiple_choice_questions(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, text,difficulty, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE type = 'Multiple choice'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("question_id", "topic", "subtopic", "text", "difficulty", \
                        "points", "creation_date", "creation_time", "creator_user_name")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="question_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="topic", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="subtopic", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="difficulty", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="points",anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_date", anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="creation_time", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="creator_user_name", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_true_false_questions(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()
        
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, text,difficulty, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE type = 'True/False'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("question_id", "topic", "subtopic", "text", "difficulty", \
                        "points", "creation_date", "creation_time", "creator_user_name")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="question_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="topic", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="subtopic", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="difficulty", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="points",anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_date", anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="creation_time", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="creator_user_name", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_descriptive_practical_questions(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()
        
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, text, difficulty, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE type = 'Descriptive/Practical'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("question_id", "topic", "subtopic", "text", "difficulty", \
                        "points", "creation_date", "creation_time", "creator_user_name")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="question_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="topic", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="subtopic", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="difficulty", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="points",anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_date", anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="creation_time", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="creator_user_name", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
    
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_easy_questions(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()
        
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, text, type, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE difficulty = 'Easy'""")
        data = cursor.fetchall()
        connection.close()
        
        columns = ("question_id", "topic", "subtopic", "text", "type", \
                            "points", "creation_date", "creation_time", "creator_user_name")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="question_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="topic", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="subtopic", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="type", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="points",anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_date", anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="creation_time", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="creator_user_name", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_normal_questions(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()
        
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, text, type, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE difficulty = 'Normal'""")
        data = cursor.fetchall()
        connection.close()
        
        columns = ("question_id", "topic", "subtopic", "text", "type", \
                            "points", "creation_date", "creation_time", "creator_user_name")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="question_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="topic", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="subtopic", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="type", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="points",anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_date", anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="creation_time", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="creator_user_name", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_hard_questions(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()
        
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, text, type, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE difficulty = 'Hard'""")
        data = cursor.fetchall()
        connection.close()
        
        columns = ("question_id", "topic", "subtopic", "text", "type", \
                            "points", "creation_date", "creation_time", "creator_user_name")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="question_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="topic", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="subtopic", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="type", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="points",anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_date", anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="creation_time", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 110, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="creator_user_name", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_exams(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name
                       FROM Exam""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time",
                                "neg_score", "pass_score", 'handler', "supervisor", "creator")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="exam_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 130, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="exam_date", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="start_time",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="duration", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="creation_date", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_time",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="neg_score", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="pass_score", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#10", text="handler", anchor=tk.W)
        self.table.column("#10", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#11", text="supervisor", anchor=tk.W)
        self.table.column("#11", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#12", text="creator", anchor=tk.W)
        self.table.column("#12", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_unstarted_exams(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name
                       FROM Exam
                       WHERE DATETIME('now', 'localtime') < DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time)""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time",
                                "neg_score", "pass_score", 'handler', "supervisor", "creator")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="exam_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 130, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="exam_date", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="start_time",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="duration", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="creation_date", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_time",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="neg_score", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="pass_score", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#10", text="handler", anchor=tk.W)
        self.table.column("#10", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#11", text="supervisor", anchor=tk.W)
        self.table.column("#11", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#12", text="creator", anchor=tk.W)
        self.table.column("#12", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_started_exams(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name
                       FROM Exam
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time)
                        AND DATETIME('now', 'localtime') < DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes')""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time",
                                "neg_score", "pass_score", 'handler', "supervisor", "creator")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="exam_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 130, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="exam_date", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="start_time",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="duration", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="creation_date", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_time",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="neg_score", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="pass_score", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#10", text="handler", anchor=tk.W)
        self.table.column("#10", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#11", text="supervisor", anchor=tk.W)
        self.table.column("#11", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#12", text="creator", anchor=tk.W)
        self.table.column("#12", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_finished_exams(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name
                       FROM Exam
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes')""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time",
                                "neg_score", "pass_score", 'handler', "supervisor", "creator")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="exam_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 130, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="exam_date", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="start_time",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="duration", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="creation_date", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="creation_time",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="neg_score", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="pass_score", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#10", text="handler", anchor=tk.W)
        self.table.column("#10", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#11", text="supervisor", anchor=tk.W)
        self.table.column("#11", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#12", text="creator", anchor=tk.W)
        self.table.column("#12", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_students_taking_exam(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT U.user_name, U.first_name, U.last_name, UE.exam_id, E.exam_name
                        FROM User_Exam UE
                        JOIN User U ON UE.user_name = U.user_name
                        JOIN Exam E ON UE.exam_id = E.exam_id
                        WHERE UE.exam_id IN (
                            SELECT E.exam_id
                            FROM Exam E
                            WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time)
                                AND DATETIME('now', 'localtime') <= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes'))""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "exam_id", "exam_name")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="exam_id", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="exam_name", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 130, minwidth=50, anchor=tk.W)
        
        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_students_took_exam(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT UE.user_name, U.first_name, U.last_name, GROUP_CONCAT(UE.exam_id, ', ') AS exam_ids
                        FROM User_Exam UE
                        JOIN User U ON UE.user_name = U.user_name
                        WHERE UE.exam_id IN (
                            SELECT E.exam_id
                            FROM Exam E
                            WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                        )
                        GROUP BY UE.user_name""")
                       
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "exam_ids")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="user_name",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="first_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="last_name", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="exam_ids", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        
        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)
    
    def load_feedbacks(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Feedback")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="feedback_type",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="text", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="question_id", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="rating",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="status", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="is_visible", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_suggestions_for_improvement(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, text, question_id, rating, status, is_visible
                       FROM Feedback
                       WHERE feedback_type = 'Suggestion for improvement'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "text", "question_id", "rating", "status", "is_visible")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="question_id", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="rating",anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="status", anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="is_visible", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_comments_on_clarity_difficulty(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, text, question_id, rating, status, is_visible
                       FROM Feedback
                       WHERE feedback_type = 'Comment on clarity, and difficulty levels'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "text", "question_id", "rating", "status", "is_visible")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="text", anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="question_id", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="rating",anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="status", anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="is_visible", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_low_ratings(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT *
                       FROM Feedback
                       WHERE rating BETWEEN 1 AND 3""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="feedback_type",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="text", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="question_id", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="rating",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="status", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="is_visible", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_medium_ratings(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT *
                       FROM Feedback
                       WHERE rating BETWEEN 4 AND 6""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="feedback_type",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="text", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="question_id", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="rating",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="status", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="is_visible", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_high_ratings(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT *
                       FROM Feedback
                       WHERE rating BETWEEN 7 AND 10""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="feedback_type",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="text", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="question_id", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="rating",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="status", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#9", text="is_visible", anchor=tk.W)
        self.table.column("#9", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_pending_unread_feedbacks(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, feedback_type, text, question_id, rating, is_visible
                       FROM Feedback
                       WHERE status = 'Pending/Unread'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "is_visible")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="feedback_type",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="text", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="question_id", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="rating",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="is_visible", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_analyzed_read_feedbacks(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, feedback_type, text, question_id, rating, is_visible
                       FROM Feedback
                       WHERE status = 'Analyzed/Read'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "is_visible")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="feedback_type",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="text", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="question_id", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="rating",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="is_visible", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)

    def load_visible_feedbacks(self):
        # Remove the entire old table if exists
        if hasattr(self, 'table'):
            self.table.grid_forget()  # Remove the grid layout manager from the table widget
            self.y_scrollbar.grid_forget()  # Remove the vertical scrollbar
            self.table.destroy()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, feedback_type, text, question_id, rating, status
                       FROM Feedback
                       WHERE is_visible = 1""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status")
        self.table = ttk.Treeview(self.table_frame, column=columns, show='headings', selectmode="browse")
        self.table.heading("#1", text="exam_id",anchor=tk.W)
        self.table.column("#1", stretch=tk.NO, width = 70, minwidth=50, anchor=tk.W)
        self.table.heading("#2", text="user_name", anchor=tk.W)
        self.table.column("#2", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#3", text="feedback_time", anchor=tk.W)
        self.table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.table.heading("#4", text="feedback_type",anchor=tk.W)
        self.table.column("#4", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#5", text="text", anchor=tk.W)
        self.table.column("#5", stretch=tk.NO, width = 200, minwidth=50, anchor=tk.W)
        self.table.heading("#6", text="question_id", anchor=tk.W)
        self.table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.table.heading("#7", text="rating",anchor=tk.W)
        self.table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.table.heading("#8", text="status", anchor=tk.W)
        self.table.column("#8", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)

        self.table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.table.insert("", "end", values=row)
    
    def users_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT user_name, first_name, last_name, email, registration_date, registration_time
        FROM User""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\users.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'users.csv' was successfully created in outputs folder.")

    def students_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Student'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\students.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'students.csv' was successfully created in outputs folder.")

    def exam_analysts_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Exam_Analyst'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\exam_analysts.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'exam_analysts.csv' was successfully created in outputs folder.")

    def exam_creators_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Exam_Creator'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\exam_creators.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'exam_creators.csv' was successfully created in outputs folder.")

    def exam_handlers_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Exam_Handler'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\exam_handlers.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'exam_handlers.csv' was successfully created in outputs folder.")

    def exam_supervisors_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Exam_Supervisor'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\exam_supervisors.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'exam_supervisors.csv' was successfully created in outputs folder.")

    def question_creators_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, U.email, U.registration_date, U.registration_time
        FROM User U
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        WHERE UR.role_name = 'Question_Creator'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "email", "registration_date", "registration_time")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\question_creators.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'question_creators.csv' was successfully created in outputs folder.")

    def multirole_users_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, U.first_name, U.last_name, GROUP_CONCAT(UR.role_name, '- ') AS user_roles
        FROM User U 
        JOIN User_Role UR
        ON U.user_name = UR.user_name
        GROUP BY UR.user_name
        HAVING COUNT(*) > 1""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "user_roles")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\multirole_users.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'multirole_users.csv' was successfully created in outputs folder.")

    def users_loggedin_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
        SELECT U.user_name, L.login_date, L.login_time
        FROM User U 
        JOIN Login L
        ON U.user_name = L.user_name
        WHERE L.logout_date IS NULL""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "login_date", "login_time")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\users_loggedin.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'users_loggedin.csv' was successfully created in outputs folder.")

    def questions_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, substr(text, 1, instr(text, '\n') - 1) as first_line,
                        difficulty, type, points, creation_date, creation_time, creator_user_name
                       FROM Question""")
        data = cursor.fetchall()
        connection.close()

        columns = ("question_id", "topic", "subtopic", "text", "difficulty", "type",
                        "points", "creation_date", "creation_time", "creator")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\questions.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'questions.csv' was successfully created in outputs folder.")

    def topics_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT topic FROM Question")
        data = cursor.fetchall()
        connection.close()

        columns = ("topic")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\topics.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'topics.csv' was successfully created in outputs folder.")

    def subtopics_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT subtopic FROM Question")
        data = cursor.fetchall()
        connection.close()

        columns = ("subtopic")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\subtopics.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'subtopics.csv' was successfully created in outputs folder.")

    def multiple_choice_questions_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, substr(text, 1, instr(text, '\n') - 1) as first_line,
                       difficulty, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE type = 'Multiple choice'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("question_id", "topic", "subtopic", "text", "difficulty",
                        "points", "creation_date", "creation_time", "creator_user_name")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\multiple_choice_questions.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'multiple_choice_questions.csv' was successfully created in outputs folder.")

    def true_false_questions_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, substr(text, 1, instr(text, '\n') - 1) as first_line,
                       difficulty, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE type = 'True/False'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("question_id", "topic", "subtopic", "text", "difficulty",
                        "points", "creation_date", "creation_time", "creator_user_name")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\true_false_questions.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'true_false_questions.csv' was successfully created in outputs folder.")

    def descriptive_practical_questions_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, substr(text, 1, instr(text, '\n') - 1) as first_line,
                       difficulty, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE type = 'Descriptive/Practical'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("question_id", "topic", "subtopic", "text", "difficulty",
                        "points", "creation_date", "creation_time", "creator_user_name")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\descriptive_practical_questions.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'descriptive_practical_questions.csv' was successfully created in outputs folder.")

    def easy_questions_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, substr(text, 1, instr(text, '\n') - 1) as first_line,
                        type, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE difficulty = 'Easy'""")
        data = cursor.fetchall()
        connection.close()
        
        columns = ("question_id", "topic", "subtopic", "text", "type",
                            "points", "creation_date", "creation_time", "creator_user_name")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\easy_questions.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'easy_questions.csv' was successfully created in outputs folder.")

    def normal_questions_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, substr(text, 1, instr(text, '\n') - 1) as first_line,
                        type, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE difficulty = 'Normal'""")
        data = cursor.fetchall()
        connection.close()
        
        columns = ("question_id", "topic", "subtopic", "text", "type",
                            "points", "creation_date", "creation_time", "creator_user_name")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\normal_questions.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'normal_questions.csv' was successfully created in outputs folder.")

    def hard_questions_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, topic, subtopic, substr(text, 1, instr(text, '\n') - 1) as first_line,
                        type, points, creation_date, creation_time, creator_user_name
                       FROM Question
                       WHERE difficulty = 'Hard'""")
        data = cursor.fetchall()
        connection.close()
        
        columns = ("question_id", "topic", "subtopic", "text", "type",
                            "points", "creation_date", "creation_time", "creator_user_name")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\hard_questions.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'hard_questions.csv' was successfully created in outputs folder.")

    def exams_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name
                       FROM Exam""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time",
                                "neg_score", "pass_score", 'handler', "supervisor", "creator")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\exams.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'exams.csv' was successfully created in outputs folder.")

    def unstarted_exams_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name
                       FROM Exam
                       WHERE DATETIME('now', 'localtime') < DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time)""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time",
                                "neg_score", "pass_score", 'handler', "supervisor", "creator")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\unstarted_exams.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'unstarted_exams.csv' was successfully created in outputs folder.")

    def started_exams_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name
                       FROM Exam
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time)
                        AND DATETIME('now', 'localtime') < DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes')""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time",
                                "neg_score", "pass_score", 'handler', "supervisor", "creator")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\started_exams.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'started_exams.csv' was successfully created in outputs folder.")

    def finished_exams_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                has_negative_score, passing_score, handler_user_name, supervisor_user_name, creator_user_name
                       FROM Exam
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes')""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time",
                                "neg_score", "pass_score", 'handler', "supervisor", "creator")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\finished_exams.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'finished_exams.csv' was successfully created in outputs folder.")

    def students_taking_exam_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT U.user_name, U.first_name, U.last_name, UE.exam_id, E.exam_name
                        FROM User_Exam UE
                        JOIN User U ON UE.user_name = U.user_name
                        JOIN Exam E ON UE.exam_id = E.exam_id
                        WHERE UE.exam_id IN (
                            SELECT E.exam_id
                            FROM Exam E
                            WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time)
                                AND DATETIME('now', 'localtime') <= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes'))""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "exam_id", "exam_name")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\students_taking_exam.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)     # Write data
        
        messagebox.showinfo("File Created", "The file 'students_taking_exam.csv' was successfully created in outputs folder.")

    def students_took_exam_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT UE.user_name, U.first_name, U.last_name, GROUP_CONCAT(UE.exam_id, ', ') AS exam_ids
                        FROM User_Exam UE
                        JOIN User U ON UE.user_name = U.user_name
                        WHERE UE.exam_id IN (
                            SELECT E.exam_id
                            FROM Exam E
                            WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                        )
                        GROUP BY UE.user_name""")
        data = cursor.fetchall()
        connection.close()

        columns = ("user_name", "first_name", "last_name", "exam_id", "exam_name")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\students_took_exam.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'students_took_exam.csv' was successfully created in outputs folder.")

    def feedbacks_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Feedback")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\feedbacks.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'feedbacks.csv' was successfully created in outputs folder.")

    def suggestions_for_improvement_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, text, question_id, rating, status, is_visible
                       FROM Feedback
                       WHERE feedback_type = 'Suggestion for improvement'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "text", "question_id", "rating", "status", "is_visible")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\suggestions_for_improvement.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'suggestions_for_improvement.csv' was successfully created in outputs folder.")

    def comments_on_clarity_difficulty_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, text, question_id, rating, status, is_visible
                       FROM Feedback
                       WHERE feedback_type = 'Comment on clarity, and difficulty levels'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "text", "question_id", "rating", "status", "is_visible")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\comments_on_clarity_difficulty.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'comments_on_clarity_difficulty.csv' was successfully created in outputs folder.")
    
    def low_ratings_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT *
                       FROM Feedback
                       WHERE rating BETWEEN 1 AND 3""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\low_ratings.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'low_ratings.csv' was successfully created in outputs folder.")

    def medium_ratings_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT *
                       FROM Feedback
                       WHERE rating BETWEEN 4 AND 6""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\medium_ratings.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'medium_ratings.csv' was successfully created in outputs folder.")

    def high_ratings_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT *
                       FROM Feedback
                       WHERE rating BETWEEN 7 AND 10""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\high_ratings.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'high_ratings.csv' was successfully created in outputs folder.")

    def pending_unread_feedbacks_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, feedback_type, text, question_id, rating, is_visible
                       FROM Feedback
                       WHERE status = 'Pending/Unread'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "is_visible")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\pending_unread_feedbacks.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'pending_unread_feedbacks.csv' was successfully created in outputs folder.")

    def analyzed_read_feedbacks_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, feedback_type, text, question_id, rating, is_visible
                       FROM Feedback
                       WHERE status = 'Analyzed/Read'""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "is_visible")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\analyzed_read_feedbacks.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'analyzed_read_feedbacks.csv' was successfully created in outputs folder.")

    def visible_feedbacks_tocsv(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT exam_id, user_name, feedback_time, feedback_type, text, question_id, rating, status
                       FROM Feedback
                       WHERE is_visible = 1""")
        data = cursor.fetchall()
        connection.close()

        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status")
        
        #open the csv file to which we want to write data
        path = '..\\outputs\\visible_feedbacks.csv'
        scriptdir = os.path.dirname(__file__)
        file_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="") as f:
            csv_writer = writer(f)
            csv_writer.writerow(columns)  # Write column names
            csv_writer.writerows(data)    # Write data
        
        messagebox.showinfo("File Created", "The file 'visible_feedbacks.csv' was successfully created in outputs folder.")
    
    def create_admin_help_widgets(self, admin_help_tab):
        # Add User Manuals and Documentation
        user_manual_label = tk.Label(admin_help_tab, text="User Manuals and Documentation", font=("Helvetica", 12, "bold"))
        user_manual_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        user_manual_info = tk.Label(admin_help_tab, text="Access user manuals and system documentation for detailed instructions.", font=("Helvetica", 12))
        user_manual_info.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Add Frequently Asked Questions (FAQs)
        faq_label = tk.Label(admin_help_tab, text="Frequently Asked Questions (FAQs)", font=("Helvetica", 12, "bold"))
        faq_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        faq_info = tk.Label(admin_help_tab, text="Find answers to common questions about system usage, troubleshooting, and more.", font=("Helvetica", 12))
        faq_info.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Add Contact Information and Support Channels
        contact_info_label = tk.Label(admin_help_tab, text="Contact Information and Support Channels", font=("Helvetica", 12, "bold"))
        contact_info_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        contact_info = tk.Label(admin_help_tab, text="Reach out to our support team via email, phone, or live chat for assistance.", font=("Helvetica", 12))
        contact_info.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # Add Video Tutorials and Demos
        video_tutorials_label = tk.Label(admin_help_tab, text="Video Tutorials and Demos", font=("Helvetica", 12, "bold"))
        video_tutorials_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        video_tutorials_info = tk.Label(admin_help_tab, text="Watch video tutorials and demos to learn how to use key features.", font=("Helvetica", 12))
        video_tutorials_info.grid(row=7, column=0, sticky="w", padx=10, pady=5)

        # Add Release Notes and Updates
        release_notes_label = tk.Label(admin_help_tab, text="Release Notes and Updates", font=("Helvetica", 12, "bold"))
        release_notes_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)

        release_notes_info = tk.Label(admin_help_tab, text="Stay updated on the latest system releases, updates, and improvements.", font=("Helvetica", 12))
        release_notes_info.grid(row=9, column=0, sticky="w", padx=10, pady=5)

        # Add Security Guidelines and Best Practices
        security_guidelines_label = tk.Label(admin_help_tab, text="Security Guidelines and Best Practices", font=("Helvetica", 12, "bold"))
        security_guidelines_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)

        security_info = tk.Label(admin_help_tab, text="Learn about security best practices and guidelines to protect your account.", font=("Helvetica", 12))
        security_info.grid(row=11, column=0, sticky="w", padx=10, pady=5)

        # Add Glossary of Terms
        glossary_label = tk.Label(admin_help_tab, text="Glossary of Terms", font=("Helvetica", 12, "bold"))
        glossary_label.grid(row=12, column=0, sticky="w", padx=10, pady=5)

        glossary_info = tk.Label(admin_help_tab, text="Explore the glossary for definitions of common terms and concepts.", font=("Helvetica", 12))
        glossary_info.grid(row=13, column=0, sticky="w", padx=10, pady=5)

        # Add Community Forums and User Groups
        community_forums_label = tk.Label(admin_help_tab, text="Community Forums and User Groups", font=("Helvetica", 12, "bold"))
        community_forums_label.grid(row=14, column=0, sticky="w", padx=10, pady=5)

        community_info = tk.Label(admin_help_tab, text="Engage with the community, ask questions, and share insights on user forums.", font=("Helvetica", 12))
        community_info.grid(row=15, column=0, sticky="w", padx=10, pady=5)
    
    def add_question_creator_tabs(self):
        # Add tabs for different functionalities
        self.question_creators_question_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.question_creators_question_tab, text='Questions & Options')
        self.create_question_creators_question_widgets(self.question_creators_question_tab)
        # Bind the load_creator_questions method to the event of opening the tab
        self.question_creators_question_tab.bind("<Visibility>", self.questions_on_tab_opened)

        self.question_creators_help_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.question_creators_help_tab, text='Help')
        self.create_question_creators_help_widgets(self.question_creators_help_tab)
    
    def create_question_creators_question_widgets(self, question_creators_question_tab):
        # Create a frame for Qustion info
        self.question_info_frame = tk.Frame(question_creators_question_tab)
        self.question_info_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)

        # Create fields and labels for question
        # Question ID

        # id generate image 
        path = "..\images\idgen.png"
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the file from there
        image_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        self.idgen_image = Image.open(image_path)
        self.idgen_icon = ImageTk.PhotoImage(self.idgen_image)

        self.question_id_label = tk.Label(self.question_info_frame, text="Question ID:")
        self.question_id_label.grid(row=0, column=0, padx=(2,0), pady=2, sticky=tk.W)
        self.question_id_var = tk.StringVar()
        self.question_id_var.set("")
        self.question_id_value_label = tk.Label(self.question_info_frame, textvariable=self.question_id_var, text="", width=10)
        self.question_id_value_label.grid(row=0, column=1, padx=2, pady=2)
        self.generate_id_button = tk.Button(self.question_info_frame, image=self.idgen_icon, cursor="hand2", command=self.generate_question_id, width=20, height=20)
        self.generate_id_button.grid(row=0, column=2, padx=2, pady=2)

        # Type
        self.type_label = tk.Label(self.question_info_frame, text="Type:")
        self.type_label.grid(row=0, column=3, padx=(20,0), pady=2, sticky=tk.W)
        self.question_type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(self.question_info_frame, values=('Multiple choice', 'True/False', 'Descriptive/Practical'), textvariable=self.question_type_var, width=20)
        self.type_combo.grid(row=0, column=4, padx=2, pady=2)
        # Bind the type selection to the options being enabled ore disabled
        self.type_combo.bind("<<ComboboxSelected>>", self.reset_options_based_on_type)

        # Difficulty
        self.difficulty_label = tk.Label(self.question_info_frame, text="Difficulty:")
        self.difficulty_label.grid(row=0, column=5, padx=(20,0), pady=2, sticky=tk.W)
        self.question_difficulty_var = tk.StringVar()
        self.difficulty_combo = ttk.Combobox(self.question_info_frame, values=('Easy', 'Normal', 'Hard'), textvariable=self.question_difficulty_var, width=10)
        self.difficulty_combo.grid(row=0, column=6, padx=2, pady=2)

        # Topic
        self.topic_label = tk.Label(self.question_info_frame, text="Topic:")
        self.topic_label.grid(row=0, column=7, padx=(20,0), pady=2, sticky=tk.W)
        self.topic_entry = tk.Entry(self.question_info_frame, width=30)
        self.topic_entry.grid(row=0, column=8, padx=2, pady=2)

        # Subtopic
        self.subtopic_label = tk.Label(self.question_info_frame, text="Subtopic:")
        self.subtopic_label.grid(row=0, column=9, padx=(20,0), pady=2, sticky=tk.W)
        self.subtopic_entry = tk.Entry(self.question_info_frame, width=30)
        self.subtopic_entry.grid(row=0, column=10, padx=2, pady=2)

        # Points
        self.points_label = tk.Label(self.question_info_frame, text="Points:")
        self.points_label.grid(row=0, column=11, padx=(20,0), pady=2, sticky=tk.W)
        self.points_entry = tk.Entry(self.question_info_frame, width=5)
        self.points_entry.grid(row=0, column=12, padx=2, pady=2)

        # Create a frame for question and options
        self.question_option_frame = tk.Frame(question_creators_question_tab)
        self.question_option_frame.grid(row=1, column=0, padx=2, pady=2, sticky=tk.NSEW)
        
        # Create a frame for Question
        self.question_frame = tk.LabelFrame(self.question_option_frame, text="Question", width=20)
        self.question_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        # Widgets for attachment image
        self.question_attachment_frame = tk.Frame(self.question_frame)
        self.question_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.question_image_browse_button = tk.Button(self.question_attachment_frame, text="Question Image", command=self.browse_question_attachment_image)
        self.question_image_browse_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.question_has_attachment_var = tk.IntVar(value=0) # Default unchecked
        self.question_has_attachment = tk.Checkbutton(self.question_attachment_frame, text="Has Attachment?", variable=self.question_has_attachment_var)
        self.question_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        self.question_attachment_image_path_var = tk.StringVar()
        self.question_attachment_image_path_var.set("")  # Default value
        self.question_image_path_label = tk.Label(self.question_attachment_frame, width=12, textvariable=self.question_attachment_image_path_var)
        self.question_image_path_label.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)
        
        # Question text area
        self.question_text_area = tk.Text(self.question_frame, width=40, height=20)
        self.question_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=2)

        # Create a frame for Options
        self.options_frame = tk.LabelFrame(self.question_option_frame, text="Options", width=20)
        self.options_frame.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        # Widgets for attachment image for option1
        self.option1_frame = tk.LabelFrame(self.options_frame, text="Option 1", width=10)
        self.option1_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        
        self.option1_attachment_frame = tk.Frame(self.option1_frame)
        self.option1_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.option1_image_browse_button = tk.Button(self.option1_attachment_frame, text="Option Image", command=self.browse_option1_attachment_image)
        self.option1_image_browse_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.option1_has_attachment_var = tk.IntVar(value=0) # Default unchecked
        self.option1_has_attachment = tk.Checkbutton(self.option1_attachment_frame, text="Has Attachment?", variable=self.option1_has_attachment_var)
        self.option1_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        self.option1_attachment_image_path_var = tk.StringVar()
        self.option1_attachment_image_path_var.set("")  # Default value
        self.option1_image_path_label = tk.Label(self.option1_attachment_frame, width=12, textvariable=self.option1_attachment_image_path_var)
        self.option1_image_path_label.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)

        self.option1_is_correct_answer_var = tk.IntVar(value=0) # Default unchecked
        self.option1_is_correct_answer = tk.Checkbutton(self.option1_attachment_frame, text="Is Correct Answer?", variable=self.option1_is_correct_answer_var)
        self.option1_is_correct_answer.grid(row=0, column=3, padx=2, pady=2, sticky=tk.W)

        # option1 text area
        self.option1_text_area = tk.Text(self.option1_frame, width=50, height=7)
        self.option1_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=3)

        # Widgets for attachment image for option2
        self.option2_frame = tk.LabelFrame(self.options_frame, text="Option 2", width=10)
        self.option2_frame.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)
        
        self.option2_attachment_frame = tk.Frame(self.option2_frame)
        self.option2_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.option2_image_browse_button = tk.Button(self.option2_attachment_frame, text="Option Image", command=self.browse_option2_attachment_image)
        self.option2_image_browse_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.option2_has_attachment_var = tk.IntVar(value=0) # Default unchecked
        self.option2_has_attachment = tk.Checkbutton(self.option2_attachment_frame, text="Has Attachment?", variable=self.option2_has_attachment_var)
        self.option2_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        self.option2_attachment_image_path_var = tk.StringVar()
        self.option2_attachment_image_path_var.set("")  # Default value
        self.option2_image_path_label = tk.Label(self.option2_attachment_frame, width=12, textvariable=self.option2_attachment_image_path_var)
        self.option2_image_path_label.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)

        self.option2_is_correct_answer_var = tk.IntVar(value=0) # Default unchecked
        self.option2_is_correct_answer = tk.Checkbutton(self.option2_attachment_frame, text="Is Correct Answer?", variable=self.option2_is_correct_answer_var)
        self.option2_is_correct_answer.grid(row=0, column=3, padx=2, pady=2, sticky=tk.W)

        # option2 text area
        self.option2_text_area = tk.Text(self.option2_frame, width=50, height=7)
        self.option2_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=3)

        # Widgets for attachment image for option
        self.option3_frame = tk.LabelFrame(self.options_frame, text="Option 3", width=10)
        self.option3_frame.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
        
        self.option3_attachment_frame = tk.Frame(self.option3_frame)
        self.option3_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.option3_image_browse_button = tk.Button(self.option3_attachment_frame, text="Option Image", command=self.browse_option3_attachment_image)
        self.option3_image_browse_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.option3_has_attachment_var = tk.IntVar(value=0) # Default unchecked
        self.option3_has_attachment = tk.Checkbutton(self.option3_attachment_frame, text="Has Attachment?", variable=self.option3_has_attachment_var)
        self.option3_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        self.option3_attachment_image_path_var = tk.StringVar()
        self.option3_attachment_image_path_var.set("")  # Default value
        self.option3_image_path_label = tk.Label(self.option3_attachment_frame, width=12, textvariable=self.option3_attachment_image_path_var)
        self.option3_image_path_label.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)

        self.option3_is_correct_answer_var = tk.IntVar(value=0) # Default unchecked
        self.option3_is_correct_answer = tk.Checkbutton(self.option3_attachment_frame, text="Is Correct Answer?", variable=self.option3_is_correct_answer_var)
        self.option3_is_correct_answer.grid(row=0, column=3, padx=2, pady=2, sticky=tk.W)

        # option3 text area
        self.option3_text_area = tk.Text(self.option3_frame, width=50, height=7)
        self.option3_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=3)

        # Widgets for attachment image for option
        self.option4_frame = tk.LabelFrame(self.options_frame, text="Option 4", width=10)
        self.option4_frame.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)
        
        self.option4_attachment_frame = tk.Frame(self.option4_frame)
        self.option4_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.option4_image_browse_button = tk.Button(self.option4_attachment_frame, text="Option Image", command=self.browse_option4_attachment_image)
        self.option4_image_browse_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.option4_has_attachment_var = tk.IntVar(value=0) # Default unchecked
        self.option4_has_attachment = tk.Checkbutton(self.option4_attachment_frame, text="Has Attachment?", variable=self.option4_has_attachment_var)
        self.option4_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

        self.option4_attachment_image_path_var = tk.StringVar()
        self.option4_attachment_image_path_var.set("")  # Default value
        self.option4_image_path_label = tk.Label(self.option4_attachment_frame, width=12, textvariable=self.option4_attachment_image_path_var)
        self.option4_image_path_label.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)

        self.option4_is_correct_answer_var = tk.IntVar(value=0) # Default unchecked
        self.option4_is_correct_answer = tk.Checkbutton(self.option4_attachment_frame, text="Is Correct Answer?", variable=self.option4_is_correct_answer_var)
        self.option4_is_correct_answer.grid(row=0, column=3, padx=2, pady=2, sticky=tk.W)

        # option4 text area
        self.option4_text_area = tk.Text(self.option4_frame, width=50, height=7)
        self.option4_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=3)

        # Create a frame for question buttons
        self.question_buttons_frame = tk.Frame(question_creators_question_tab)
        self.question_buttons_frame.grid(row=2, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Configure columns to expand equally
        self.question_buttons_frame.columnconfigure(0, weight=1)
        self.question_buttons_frame.columnconfigure(1, weight=1)
        self.question_buttons_frame.columnconfigure(2, weight=1)
        self.question_buttons_frame.columnconfigure(3, weight=1)

        self.insert_question_button = tk.Button(self.question_buttons_frame, text="Insert Question + Options", command=self.gui_insert_question)
        self.insert_question_button.grid(row=0, column=0, padx=10, pady=2, sticky=tk.E)

        self.update_question_button = tk.Button(self.question_buttons_frame, text="Update Question + Options", command=self.gui_update_question)
        self.update_question_button.grid(row=0, column=1, padx=10, pady=2)

        self.delete_question_button = tk.Button(self.question_buttons_frame, text="Delete Question + Options", command=self.gui_delete_question)
        self.delete_question_button.grid(row=0, column=2, padx=10, pady=2)

        self.reset_question_fields_button = tk.Button(self.question_buttons_frame, text="Reset Fields", command=self.reset_question_fields)
        self.reset_question_fields_button.grid(row=0, column=3, padx=10, pady=2, sticky=tk.W)

        # Create a frame for table containing data
        self.questions_table_frame = tk.Frame(question_creators_question_tab)
        self.questions_table_frame.grid(row=3, column=0, sticky=tk.NSEW)

        # Create the table containgn the questions created by this question creator
        columns = ("question_id", "topic", "subtopic", "text", "image_path", "difficulty", "type", \
                        "points", "creation_date", "creation_time")
        self.questions_table = ttk.Treeview(self.questions_table_frame, column=columns, show='headings', selectmode="browse")
        self.questions_table.heading("#1", text="question_id",anchor=tk.W)
        self.questions_table.column("#1", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#2", text="topic", anchor=tk.W)
        self.questions_table.column("#2", stretch=tk.NO, width = 150, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#3", text="subtopic", anchor=tk.W)
        self.questions_table.column("#3", stretch=tk.NO, width = 150, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#4", text="text",anchor=tk.W)
        self.questions_table.column("#4", stretch=tk.NO, width = 250, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#5", text="image_path", anchor=tk.W)
        self.questions_table.column("#5", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#6", text="difficulty", anchor=tk.W)
        self.questions_table.column("#6", stretch=tk.NO, width = 60, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#7", text="type", anchor=tk.W)
        self.questions_table.column("#7", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#8", text="points",anchor=tk.W)
        self.questions_table.column("#8", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#9", text="creation_date", anchor=tk.W)
        self.questions_table.column("#9", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.questions_table.heading("#10", text="creation_time", anchor=tk.W)
        self.questions_table.column("#10", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)

        self.questions_table.grid(row=0, column=0, sticky="nsew")

        self.questions_table_y_scrollbar = ttk.Scrollbar(self.questions_table_frame, orient="vertical", command=self.questions_table.yview)
        self.questions_table_y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.questions_table.configure(yscrollcommand=self.questions_table_y_scrollbar.set)
        # Bind the function to the Treeview's selection event
        self.questions_table.bind('<<TreeviewSelect>>', self.questions_on_treeview_select)

        s = ttk.Style(self.questions_table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

    def generate_question_id(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT question_id
                       FROM Question
                       ORDER BY creation_date DESC, creation_time DESC
                       LIMIT 1""")
        prev_last_question_id = cursor.fetchone()[0]
        connection.close()
        # Add one to the question id number and set the question_id
        new_question_id = f"Q{(int(prev_last_question_id[1:]) + 1)}"
        self.question_id_var.set(new_question_id)

    def browse_question_attachment_image(self):
        # Open file dialog to select image
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        
        if filename:
            # Extract the file extension
            _, file_extension = os.path.splitext(filename)

            # Construct the destination path
            destination_path = f"..\images\{self.question_id_var.get()}{file_extension}"
            # Update the entry with the selected file path including the original file extension
            self.question_attachment_image_path_var.set(destination_path)
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            destination_path = os.path.join(scriptdir, destination_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy the file to the images folder and rename it
            shutil.copy(filename, destination_path)

            # After attaching the file, check the checkbox
            self.question_has_attachment_var.set(1)
    
    def browse_option1_attachment_image(self):
        # Open file dialog to select image
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        
        if filename:
            # Extract the file extension
            _, file_extension = os.path.splitext(filename)

            # Construct the destination path
            destination_path = f"..\images\{self.question_id_var.get()}O1{file_extension}"
            # Update the entry with the selected file path including the original file extension
            self.option1_attachment_image_path_var.set(destination_path)
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            destination_path = os.path.join(scriptdir, destination_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy the file to the images folder and rename it
            shutil.copy(filename, destination_path)

            # After attaching the file, check the checkbox
            self.option1_has_attachment_var.set(1)
    
    def browse_option2_attachment_image(self):
        # Open file dialog to select image
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        
        if filename:
            # Extract the file extension
            _, file_extension = os.path.splitext(filename)

            # Construct the destination path
            destination_path = f"..\images\{self.question_id_var.get()}O2{file_extension}"
            # Update the entry with the selected file path including the original file extension
            self.option2_attachment_image_path_var.set(destination_path)
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            destination_path = os.path.join(scriptdir, destination_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy the file to the images folder and rename it
            shutil.copy(filename, destination_path)

            # After attaching the file, check the checkbox
            self.option2_has_attachment_var.set(1)
    
    def browse_option3_attachment_image(self):
        # Open file dialog to select image
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        
        if filename:
            # Extract the file extension
            _, file_extension = os.path.splitext(filename)

            # Construct the destination path
            destination_path = f"..\images\{self.question_id_var.get()}O3{file_extension}"
            # Update the entry with the selected file path including the original file extension
            self.option3_attachment_image_path_var.set(destination_path)
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            destination_path = os.path.join(scriptdir, destination_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy the file to the images folder and rename it
            shutil.copy(filename, destination_path)

            # After attaching the file, check the checkbox
            self.option3_has_attachment_var.set(1)
    
    def browse_option4_attachment_image(self):
        # Open file dialog to select image
        filename = filedialog.askopenfilename(initialdir="/", title="Select Image File", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        
        if filename:
            # Extract the file extension
            _, file_extension = os.path.splitext(filename)

            # Construct the destination path
            destination_path = f"..\images\{self.question_id_var.get()}O4{file_extension}"
            # Update the entry with the selected file path including the original file extension
            self.option4_attachment_image_path_var.set(destination_path)
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            destination_path = os.path.join(scriptdir, destination_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # Copy the file to the images folder and rename it
            shutil.copy(filename, destination_path)

            # After attaching the file, check the checkbox
            self.option4_has_attachment_var.set(1)
    
    def gui_insert_question(self):
        question_id = self.question_id_var.get()
        topic = self.topic_entry.get()
        subtopic = self.subtopic_entry.get() if len(self.subtopic_entry.get()) > 0 else None
        text = self.question_text_area.get("1.0", tk.END) if len(self.question_text_area.get("1.0", tk.END)) > 0 else None
        image = self.question_attachment_image_path_var.get() if self.question_attachment_image_path_var.get() else None
        difficulty = self.question_difficulty_var.get()
        type = self.question_type_var.get()
        points = int(self.points_entry.get()) if len(self.points_entry.get()) > 0 else None
        creator_user_name = self.username

        if type == "Multiple choice":
            option1_id = question_id + "O1"
            option1_text = self.option1_text_area.get("1.0", tk.END) if len(self.option1_text_area.get("1.0", tk.END)) > 0 else None
            option1_image = self.option1_attachment_image_path_var.get() if self.option1_attachment_image_path_var.get() else None
            option1_is_correct_answer = int(self.option1_is_correct_answer_var.get())
            
            option2_id = question_id + "O2"
            option2_text = self.option2_text_area.get("1.0", tk.END) if len(self.option2_text_area.get("1.0", tk.END)) > 0 else None
            option2_image = self.option2_attachment_image_path_var.get() if self.option2_attachment_image_path_var.get() else None
            option2_is_correct_answer = int(self.option2_is_correct_answer_var.get())

            option3_id = question_id + "O3"
            option3_text = self.option3_text_area.get("1.0", tk.END) if len(self.option3_text_area.get("1.0", tk.END)) > 0 else None
            option3_image = self.option3_attachment_image_path_var.get() if self.option3_attachment_image_path_var.get() else None
            option3_is_correct_answer = int(self.option3_is_correct_answer_var.get())

            option4_id = question_id + "O4"
            option4_text = self.option4_text_area.get("1.0", tk.END) if len(self.option4_text_area.get("1.0", tk.END)) > 0 else None
            option4_image = self.option4_attachment_image_path_var.get() if self.option4_attachment_image_path_var.get() else None
            option4_is_correct_answer = int(self.option4_is_correct_answer_var.get())
        elif type == "True/False":
            option1_id = question_id + "O1"
            option1_text = "True"
            option1_image = None
            option1_is_correct_answer = int(self.option1_is_correct_answer_var.get())

            option2_id = question_id + "O2"
            option2_text = "False"
            option2_image = None
            option2_is_correct_answer = int(self.option2_is_correct_answer_var.get())
        else:
            option1_id = question_id + "O1"
            option1_text = self.option1_text_area.get("1.0", tk.END) if len(self.option1_text_area.get("1.0", tk.END)) > 0 else None
            option1_image = self.option1_attachment_image_path_var.get() if self.option1_attachment_image_path_var.get() else None
            option1_is_correct_answer = 1

        # Validate fields
        if not (question_id and topic and (text or image) and difficulty and type and points):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return
        if type == "Multiple choice" and not((option1_text or option1_image) and (option2_text or option2_image) and (option3_text or option3_image) and (option4_text or option4_image) and
                sum(1 for x in (option1_is_correct_answer, option2_is_correct_answer, option3_is_correct_answer, option4_is_correct_answer) if x == 1) == 1):
            messagebox.showwarning("Invalid Options Information", "Please recheck the options info.")
            return
        elif type == "True/False" and not(option1_text == "True" and option2_text == "False" and
                ((option1_is_correct_answer and not option2_is_correct_answer) or (option2_is_correct_answer and not option1_is_correct_answer))):
            messagebox.showwarning("Invalid Options Information", "Please recheck the options info.")
            return
        elif type == "Descriptive/Practical" and not(option1_text or option1_image):
            messagebox.showwarning("Invalid Options Information", "Please recheck the options info.")
            return

        # Call insert_question function from db1.py
        question_insert_msg = insert_question(question_id, topic, subtopic, text, image, difficulty, type, points, creator_user_name)
        if type == "Multiple choice":
            option1_insert_msg = insert_question_option(option1_id, question_id, option1_text, option1_image, option1_is_correct_answer)
            option2_insert_msg = insert_question_option(option2_id, question_id, option2_text, option2_image, option2_is_correct_answer)
            option3_insert_msg = insert_question_option(option3_id, question_id, option3_text, option3_image, option3_is_correct_answer)
            option4_insert_msg = insert_question_option(option4_id, question_id, option4_text, option4_image, option4_is_correct_answer)
        elif type == "True/False":
            option1_insert_msg = insert_question_option(option1_id, question_id, option1_text, option1_image, option1_is_correct_answer)
            option2_insert_msg = insert_question_option(option2_id, question_id, option2_text, option2_image, option2_is_correct_answer)
        else:
            option1_insert_msg = insert_question_option(option1_id, question_id, option1_text, option1_image, option1_is_correct_answer)
        
        # Rollback all changes if any insert failed
        if not question_insert_msg.endswith("successfully.") or not option1_insert_msg.endswith("successfully.") or (type in ("Multiple choice", "True/False") and not option2_insert_msg.endswith("successfully.")) or \
           (type == "Multiple choice" and not option3_insert_msg.endswith("successfully.")) or (type == "Multiple choice" and not option4_insert_msg.endswith("successfully.")):
            
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
            
            sql = """ DELETE FROM Question
                    WHERE question_id = ?"""
            cursor.execute(sql, (question_id, ))
            if type == "Multiple choice":
                sql = """ DELETE FROM Option
                        WHERE option_id IN (?, ?, ?, ?)"""
                cursor.execute(sql, (option1_id, option2_id, option3_id, option4_id))
            elif type == "True/False":
                sql = """ DELETE FROM Option
                            WHERE option_id IN (?, ?)"""
                cursor.execute(sql, (option1_id, option2_id))
            else:
                sql = """ DELETE FROM Option
                            WHERE option_id = ?"""
                cursor.execute(sql, (option1_id, )) 

            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showwarning("Question + Options Insert Failed", "Insert failed and all changes rollbacked successffuly.")
            return
        else:
            messagebox.showinfo("Question + Options Insert", "Question and it's options inserted successfully.")
        
        # Reset/clear fields
        self.reset_question_fields()
        # reload the question table data
        self.load_creator_questions()

    def gui_update_question(self):
        question_id = self.question_id_var.get()
        topic = self.topic_entry.get()
        subtopic = self.subtopic_entry.get() if len(self.subtopic_entry.get()) > 0 else None
        text = self.question_text_area.get("1.0", tk.END) if len(self.question_text_area.get("1.0", tk.END)) > 0 else None
        image = self.question_attachment_image_path_var.get() if self.question_attachment_image_path_var.get() else None
        difficulty = self.question_difficulty_var.get()
        type = self.question_type_var.get()
        points = int(self.points_entry.get()) if len(self.points_entry.get()) > 0 else None

        if type == "Multiple choice":
            option1_id = question_id + "O1"
            option1_text = self.option1_text_area.get("1.0", tk.END) if len(self.option1_text_area.get("1.0", tk.END)) > 0 else None
            option1_image = self.option1_attachment_image_path_var.get() if self.option1_attachment_image_path_var.get() else None
            option1_is_correct_answer = int(self.option1_is_correct_answer_var.get())
            
            option2_id = question_id + "O2"
            option2_text = self.option2_text_area.get("1.0", tk.END) if len(self.option2_text_area.get("1.0", tk.END)) > 0 else None
            option2_image = self.option2_attachment_image_path_var.get() if self.option2_attachment_image_path_var.get() else None
            option2_is_correct_answer = int(self.option2_is_correct_answer_var.get())

            option3_id = question_id + "O3"
            option3_text = self.option3_text_area.get("1.0", tk.END) if len(self.option3_text_area.get("1.0", tk.END)) > 0 else None
            option3_image = self.option3_attachment_image_path_var.get() if self.option3_attachment_image_path_var.get() else None
            option3_is_correct_answer = int(self.option3_is_correct_answer_var.get())

            option4_id = question_id + "O4"
            option4_text = self.option4_text_area.get("1.0", tk.END) if len(self.option4_text_area.get("1.0", tk.END)) > 0 else None
            option4_image = self.option4_attachment_image_path_var.get() if self.option4_attachment_image_path_var.get() else None
            option4_is_correct_answer = int(self.option4_is_correct_answer_var.get())
        elif type == "True/False":
            option1_id = question_id + "O1"
            option1_text = "True"
            option1_image = None
            option1_is_correct_answer = int(self.option1_is_correct_answer_var.get())

            option2_id = question_id + "O2"
            option2_text = "False"
            option2_image = None
            option2_is_correct_answer = int(self.option2_is_correct_answer_var.get())
        else:
            option1_id = question_id + "O1"
            option1_text = self.option1_text_area.get("1.0", tk.END) if len(self.option1_text_area.get("1.0", tk.END)) > 0 else None
            option1_image = self.option1_attachment_image_path_var.get() if self.option1_attachment_image_path_var.get() else None
            option1_is_correct_answer = 1

        # Validate fields
        if not (question_id and topic and (text or image) and difficulty and type and points):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return
        if type == "Multiple choice" and not((option1_text or option1_image) and (option2_text or option2_image) and (option3_text or option3_image) and (option4_text or option4_image) and
                sum(1 for x in (option1_is_correct_answer, option2_is_correct_answer, option3_is_correct_answer, option4_is_correct_answer) if x == 1) == 1):
            messagebox.showwarning("Invalid Options Information", "Please recheck the options info.")
            return
        elif type == "True/False" and not(option1_text == "True" and option2_text == "False" and
                ((option1_is_correct_answer and not option2_is_correct_answer) or (option2_is_correct_answer and not option1_is_correct_answer))):
            messagebox.showwarning("Invalid Options Information", "Please recheck the options info.")
            return
        elif type == "Descriptive/Practical" and not(option1_text or option1_image):
            messagebox.showwarning("Invalid Options Information", "Please recheck the options info.")
            return

        # Take a snapshot of questiona and its options to rollback if necessary
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

        cursor.execute(""" SELECT question_id, topic, subtopic, text, image, difficulty, type, points FROM Question
                    WHERE question_id = ?""", (question_id, ))
        old_question = cursor.fetchone()[0]
         
        cursor.execute(""" SELECT option_id, text, image, is_correct_answer FROM Option
                    WHERE question_id = ?
                    ORDER BY option_id""", (question_id, ))
        old_options = cursor.fetchall()
        
        # Call update_question function from db1.py
        update_question_msg = update_question(question_id, topic, subtopic, text, image, difficulty, type, points)
        if type == "Multiple choice":
            update_option1_msg = update_question_option(option1_id, question_id, option1_text, option1_image, option1_is_correct_answer)
            update_option2_msg = update_question_option(option2_id, question_id, option2_text, option2_image, option2_is_correct_answer)
            update_option3_msg = update_question_option(option3_id, question_id, option3_text, option3_image, option3_is_correct_answer)
            update_option4_msg = update_question_option(option4_id, question_id, option4_text, option4_image, option4_is_correct_answer)
        elif type == "True/False":
            update_option1_msg = update_question_option(option1_id, question_id, option1_text, option1_image, option1_is_correct_answer)
            update_option2_msg = update_question_option(option2_id, question_id, option2_text, option2_image, option2_is_correct_answer)
        else:
            update_option1_msg = update_question_option(option1_id, question_id, option1_text, option1_image, option1_is_correct_answer)

        # Rollback all changes if any insert failed
        if not update_question_msg.endswith("successfully.") or not update_option1_msg.endswith("successfully.") or (type in ("Multiple choice", "True/False") and not update_option2_msg.endswith("successfully.")) or \
           (type == "Multiple choice" and not update_option3_msg.endswith("successfully.")) or (type == "Multiple choice" and not update_option4_msg.endswith("successfully.")):
            
            sql = """UPDATE Question
                    SET topic = ?, subtopic = ?, text = ?, image = ?, difficulty = ?, type = ?, points = ?
                    WHERE question_id = ?"""
            cursor.execute(sql, (old_question[1], old_question[2], old_question[3], old_question[4], old_question[5], old_question[6], old_question[7], question_id))
            
            if type == "Multiple choice":
                sql = """UPDATE Question
                        SET text = ?, image = ?, is_correct_answer = ?
                        WHERE option_id = ?"""
                cursor.execute(sql, (old_options[0][1], old_options[0][2], old_options[0][3], option1_id))
                cursor.execute(sql, (old_options[1][1], old_options[1][2], old_options[1][3], option2_id))
                cursor.execute(sql, (old_options[2][1], old_options[2][2], old_options[2][3], option3_id))
                cursor.execute(sql, (old_options[3][1], old_options[3][2], old_options[3][3], option4_id))

            elif type == "True/False":
                sql = """UPDATE Question
                        SET text = ?, image = ?, is_correct_answer = ?
                        WHERE option_id = ?"""
                cursor.execute(sql, (old_options[0][1], old_options[0][2], old_options[0][3], option1_id))
                cursor.execute(sql, (old_options[1][1], old_options[1][2], old_options[1][3], option2_id))
            else:
                sql = """UPDATE Question
                        SET text = ?, image = ?, is_correct_answer = ?
                        WHERE option_id = ?"""
                cursor.execute(sql, (old_options[0][1], old_options[0][2], old_options[0][3], option1_id)) 

            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showwarning("Question + Options Update Failed", "Update failed and all changes rollbacked successffuly.")
            return
        else:
            messagebox.showinfo("Question + Options Update", "Question and it's options updated successfully.")
        
        # Reset/clear fields
        self.reset_question_fields()
        # reload the question table data
        self.load_creator_questions()

    def gui_delete_question(self):
        question_id = self.question_id_var.get()

        if type == "Multiple choice":
            option1_id = question_id + "O1"
            option2_id = question_id + "O2"
            option3_id = question_id + "O3"
            option4_id = question_id + "O4"
        elif type == "True/False":
            option1_id = question_id + "O1"
            option2_id = question_id + "O2"
        else:
            option1_id = question_id + "O1"

        # Validate fields
        if not question_id:
            messagebox.showwarning("Incomplete Information", "Please insert a question ID to delete.")
            return

        # Call delete_user function from db1.py
        delete_question(question_id)
        if type == "Multiple choice":
            delete_question_option(option1_id)
            delete_question_option(option2_id)
            delete_question_option(option3_id)
            delete_question_option(option4_id)
        elif type == "True/False":
            delete_question_option(option1_id)
            delete_question_option(option2_id)
        else:
            delete_question_option(option1_id)

        # Reset/clear fields
        self.reset_question_fields()
        # reload the question table data
        self.load_creator_questions()
        messagebox.showinfo("Question Delete", "Question and it's options deleted successfully.")
        
    def load_creator_questions(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT question_id, topic, subtopic, text, image, difficulty, type, points, creation_date, creation_time
                       FROM Question
                       WHERE creator_user_name = ?""", (self.username, ))
        data = cursor.fetchall()
        connection.close()

        # Clear previous data in the table
        self.questions_table.delete(*self.questions_table.get_children())

        # Insert new data rows
        for row in data:
            self.questions_table.insert("", "end", values=row)

    def questions_on_tab_opened(self, event):
        # Load questions when the tab is opened
        self.load_creator_questions()

    def questions_on_treeview_select(self, event):
        # Reset fields
        self.reset_question_fields()
        
        # Get the selected item
        selected_item = self.questions_table.selection()
        
        if selected_item:
            # Get the values of the selected item
            values = self.questions_table.item(selected_item, 'values')

            # Replace None values with empty strings
            values = ["" if value is None else value for value in values]

            # Set the values of the question-related fields
            self.question_id_var.set(values[0])
            self.topic_entry.delete(0, tk.END)
            self.topic_entry.insert(0, values[1])
            self.subtopic_entry.delete(0, tk.END)
            self.subtopic_entry.insert(0, values[2])
            self.question_text_area.delete("1.0", tk.END)
            self.question_text_area.insert(tk.END, values[3])
            self.question_has_attachment_var.set(1) if values[4] != "None" else self.question_has_attachment_var.set(0)
            self.question_attachment_image_path_var.set(values[4]) if values[4] != "None" else ""
            self.question_difficulty_var.set(values[5])
            self.question_type_var.set(values[6])
            self.points_entry.delete(0, tk.END)
            self.points_entry.insert(0, values[7])
            
            # reset options based on the question type
            self.reset_options_based_on_type()

            # Set the values of the option-related fields
            # Fetch data by querying the database
            path = '..\data\Exam_App.db'
            scriptdir = os.path.dirname(__file__)
            db_path = os.path.join(scriptdir, path)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
    
            cursor.execute("""SELECT text, image, is_correct_answer
                        FROM Option
                        WHERE question_id = ?
                        ORDER BY option_id""", (values[0], ))
            options = cursor.fetchall()
            connection.close()

            if values[6] == "Multiple choice":
                self.option1_text_area.delete("1.0", tk.END)
                self.option1_text_area.insert(tk.END, options[0][0])
                self.option1_has_attachment_var.set(1) if options[0][1] else self.option1_has_attachment_var.set(0)
                self.option1_attachment_image_path_var.set(options[0][1]) if options[0][1] else ""
                self.option1_is_correct_answer_var.set(1) if int(options[0][2]) == 1 else self.option1_is_correct_answer_var.set(0)

                self.option2_text_area.delete("1.0", tk.END)
                self.option2_text_area.insert(tk.END, options[1][0])
                self.option2_has_attachment_var.set(1) if options[1][1] else self.option2_has_attachment_var.set(0)
                self.option2_attachment_image_path_var.set(options[1][1]) if options[1][1] else ""
                self.option2_is_correct_answer_var.set(1) if int(options[1][2]) == 1 else self.option2_is_correct_answer_var.set(0)

                self.option3_text_area.delete("1.0", tk.END)
                self.option3_text_area.insert(tk.END, options[2][0])
                self.option3_has_attachment_var.set(1) if options[2][1] else self.option3_has_attachment_var.set(0)
                self.option3_attachment_image_path_var.set(options[2][1]) if options[2][1] else ""
                self.option3_is_correct_answer_var.set(1) if int(options[2][2]) == 1 else self.option3_is_correct_answer_var.set(0)

                self.option4_text_area.delete("1.0", tk.END)
                self.option4_text_area.insert(tk.END, options[3][0])
                self.option4_has_attachment_var.set(1) if options[3][1] else self.option4_has_attachment_var.set(0)
                self.option4_attachment_image_path_var.set(options[3][1]) if options[3][1] else ""
                self.option4_is_correct_answer_var.set(1) if int(options[3][2]) == 1 else self.option4_is_correct_answer_var.set(0)
                
            elif values[6] == "True/False":
                self.option1_text_area.delete("1.0", tk.END)
                self.option1_text_area.insert(tk.END, options[0][0])
                self.option1_is_correct_answer_var.set(1) if int(options[0][2]) == 1 else self.option1_is_correct_answer_var.set(0)

                self.option2_text_area.delete("1.0", tk.END)
                self.option2_text_area.insert(tk.END, options[1][0])
                self.option2_is_correct_answer_var.set(1) if int(options[1][2]) == 1 else self.option2_is_correct_answer_var.set(0)
            else:
                self.option1_text_area.delete("1.0", tk.END)
                self.option1_text_area.insert(tk.END, options[0][0])
                self.option1_has_attachment_var.set(1) if options[0][1] else self.option1_has_attachment_var.set(0)
                self.option1_attachment_image_path_var.set(options[0][1]) if options[0][1] else ""
                self.option1_is_correct_answer_var.set(1) if int(options[0][2]) == 1 else self.option1_is_correct_answer_var.set(0)

    def reset_question_fields(self):
        # Clear Question ID field
        self.question_id_var.set("")
        # Clear Type field
        self.question_type_var.set("")
        # Clear Difficulty field
        self.question_difficulty_var.set("")
        # Clear Topic field
        self.topic_entry.delete(0, tk.END)
        # Clear Subtopic field
        self.subtopic_entry.delete(0, tk.END)
        # Clear Points field
        self.points_entry.delete(0, tk.END)
        # Clear Question Text Area
        self.question_text_area.delete("1.0", tk.END)
        # Clear Attachment Image Path
        self.question_attachment_image_path_var.set("")
        # Clear Option fields
        self.option1_attachment_image_path_var.set("")
        self.option1_text_area.delete("1.0", tk.END)
        self.option2_attachment_image_path_var.set("")
        self.option2_text_area.delete("1.0", tk.END)
        self.option3_attachment_image_path_var.set("")
        self.option3_text_area.delete("1.0", tk.END)
        self.option4_attachment_image_path_var.set("")
        self.option4_text_area.delete("1.0", tk.END)
        # Clear Correct Answer Checkbuttons
        self.option1_is_correct_answer_var.set(0)
        self.option2_is_correct_answer_var.set(0)
        self.option3_is_correct_answer_var.set(0)
        self.option4_is_correct_answer_var.set(0)
        # Clear Attachment Checkbuttons
        self.question_has_attachment_var.set(0)
        self.option1_has_attachment_var.set(0)
        self.option2_has_attachment_var.set(0)
        self.option3_has_attachment_var.set(0)
        self.option4_has_attachment_var.set(0)
    
    def reset_options_based_on_type(self, event=None):
        selected_type = self.question_type_var.get()

        if selected_type == "Multiple choice":
            # Enable all option widgets
            self.option1_text_area.config(state=tk.NORMAL)
            self.option1_has_attachment.config(state=tk.NORMAL)
            self.option1_image_browse_button.config(state=tk.NORMAL)
            self.option1_is_correct_answer.config(state=tk.NORMAL)
            self.option2_text_area.config(state=tk.NORMAL)
            self.option2_has_attachment.config(state=tk.NORMAL)
            self.option2_image_browse_button.config(state=tk.NORMAL)
            self.option2_is_correct_answer.config(state=tk.NORMAL)
            self.option3_text_area.config(state=tk.NORMAL)
            self.option3_has_attachment.config(state=tk.NORMAL)
            self.option3_image_browse_button.config(state=tk.NORMAL)
            self.option3_is_correct_answer.config(state=tk.NORMAL)
            self.option4_text_area.config(state=tk.NORMAL)
            self.option4_has_attachment.config(state=tk.NORMAL)
            self.option4_image_browse_button.config(state=tk.NORMAL)
            self.option4_is_correct_answer.config(state=tk.NORMAL)

            # Reset text for options
            self.option1_text_area.delete('1.0', tk.END)
            self.option2_text_area.delete('1.0', tk.END)
            self.option3_text_area.delete('1.0', tk.END)
            self.option4_text_area.delete('1.0', tk.END)
            # Reset is_correct_answer for options
            self.option1_is_correct_answer_var.set(0)
            self.option2_is_correct_answer_var.set(0)
            self.option3_is_correct_answer_var.set(0)
            self.option4_is_correct_answer_var.set(0)

        elif selected_type == "True/False":
            # Enable options 1,2 widgets and disable options 3,4 widgets
            self.option1_text_area.config(state=tk.NORMAL)
            self.option1_has_attachment.config(state=tk.DISABLED)
            self.option1_image_browse_button.config(state=tk.DISABLED)
            self.option1_is_correct_answer.config(state=tk.NORMAL)
            self.option2_text_area.config(state=tk.NORMAL)
            self.option2_has_attachment.config(state=tk.DISABLED)
            self.option2_image_browse_button.config(state=tk.DISABLED)
            self.option2_is_correct_answer.config(state=tk.NORMAL)
            self.option3_text_area.config(state=tk.DISABLED)
            self.option3_has_attachment.config(state=tk.DISABLED)
            self.option3_image_browse_button.config(state=tk.DISABLED)
            self.option3_is_correct_answer.config(state=tk.DISABLED)
            self.option4_text_area.config(state=tk.DISABLED)
            self.option4_has_attachment.config(state=tk.DISABLED)
            self.option4_image_browse_button.config(state=tk.DISABLED)
            self.option4_is_correct_answer.config(state=tk.DISABLED)
            
            # Set text for options 1 and 2
            self.option1_text_area.delete('1.0', tk.END)
            self.option1_text_area.insert(tk.END, "True")
            self.option2_text_area.delete('1.0', tk.END)
            self.option2_text_area.insert(tk.END, "False")
            # Reset is_correct_answer for option 1,2
            self.option1_is_correct_answer_var.set(0)
            self.option2_is_correct_answer_var.set(0)

        elif selected_type == "Descriptive/Practical":
            # Enable option 1 widgets and disable options 2,3,4 widgets
            self.option1_text_area.config(state=tk.NORMAL)
            self.option1_has_attachment.config(state=tk.NORMAL)
            self.option1_image_browse_button.config(state=tk.NORMAL)
            self.option1_is_correct_answer.config(state=tk.NORMAL)
            self.option2_text_area.config(state=tk.DISABLED)
            self.option2_has_attachment.config(state=tk.DISABLED)
            self.option2_image_browse_button.config(state=tk.DISABLED)
            self.option2_is_correct_answer.config(state=tk.DISABLED)
            self.option3_text_area.config(state=tk.DISABLED)
            self.option3_has_attachment.config(state=tk.DISABLED)
            self.option3_image_browse_button.config(state=tk.DISABLED)
            self.option3_is_correct_answer.config(state=tk.DISABLED)
            self.option4_text_area.config(state=tk.DISABLED)
            self.option4_has_attachment.config(state=tk.DISABLED)
            self.option4_image_browse_button.config(state=tk.DISABLED)
            self.option4_is_correct_answer.config(state=tk.DISABLED)
            
            # Check is_correct_answer for option 1
            self.option1_is_correct_answer_var.set(1)
            # Reset text for options
            self.option1_text_area.delete('1.0', tk.END)

    def create_question_creators_help_widgets(self, question_creators_question_tab):
        # Add User Manuals and Documentation
        user_manual_label = tk.Label(question_creators_question_tab, text="User Manuals and Documentation", font=("Helvetica", 12, "bold"))
        user_manual_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        user_manual_info = tk.Label(question_creators_question_tab, text="Access user manuals and system documentation for detailed instructions.", font=("Helvetica", 12))
        user_manual_info.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Add Frequently Asked Questions (FAQs)
        faq_label = tk.Label(question_creators_question_tab, text="Frequently Asked Questions (FAQs)", font=("Helvetica", 12, "bold"))
        faq_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        faq_info = tk.Label(question_creators_question_tab, text="Find answers to common questions about system usage, troubleshooting, and more.", font=("Helvetica", 12))
        faq_info.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Add Contact Information and Support Channels
        contact_info_label = tk.Label(question_creators_question_tab, text="Contact Information and Support Channels", font=("Helvetica", 12, "bold"))
        contact_info_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        contact_info = tk.Label(question_creators_question_tab, text="Reach out to our support team via email, phone, or live chat for assistance.", font=("Helvetica", 12))
        contact_info.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # Add Video Tutorials and Demos
        video_tutorials_label = tk.Label(question_creators_question_tab, text="Video Tutorials and Demos", font=("Helvetica", 12, "bold"))
        video_tutorials_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        video_tutorials_info = tk.Label(question_creators_question_tab, text="Watch video tutorials and demos to learn how to use key features.", font=("Helvetica", 12))
        video_tutorials_info.grid(row=7, column=0, sticky="w", padx=10, pady=5)

        # Add Release Notes and Updates
        release_notes_label = tk.Label(question_creators_question_tab, text="Release Notes and Updates", font=("Helvetica", 12, "bold"))
        release_notes_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)

        release_notes_info = tk.Label(question_creators_question_tab, text="Stay updated on the latest system releases, updates, and improvements.", font=("Helvetica", 12))
        release_notes_info.grid(row=9, column=0, sticky="w", padx=10, pady=5)

        # Add Security Guidelines and Best Practices
        security_guidelines_label = tk.Label(question_creators_question_tab, text="Security Guidelines and Best Practices", font=("Helvetica", 12, "bold"))
        security_guidelines_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)

        security_info = tk.Label(question_creators_question_tab, text="Learn about security best practices and guidelines to protect your account.", font=("Helvetica", 12))
        security_info.grid(row=11, column=0, sticky="w", padx=10, pady=5)

        # Add Glossary of Terms
        glossary_label = tk.Label(question_creators_question_tab, text="Glossary of Terms", font=("Helvetica", 12, "bold"))
        glossary_label.grid(row=12, column=0, sticky="w", padx=10, pady=5)

        glossary_info = tk.Label(question_creators_question_tab, text="Explore the glossary for definitions of common terms and concepts.", font=("Helvetica", 12))
        glossary_info.grid(row=13, column=0, sticky="w", padx=10, pady=5)

        # Add Community Forums and User Groups
        community_forums_label = tk.Label(question_creators_question_tab, text="Community Forums and User Groups", font=("Helvetica", 12, "bold"))
        community_forums_label.grid(row=14, column=0, sticky="w", padx=10, pady=5)

        community_info = tk.Label(question_creators_question_tab, text="Engage with the community, ask questions, and share insights on user forums.", font=("Helvetica", 12))
        community_info.grid(row=15, column=0, sticky="w", padx=10, pady=5)

    def add_exam_creator_tabs(self):
        # Add tabs for different functionalities
        self.exam_creators_exam_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exam_creators_exam_tab, text='Exam')
        self.create_exam_creators_exam_widgets(self.exam_creators_exam_tab)
        # Bind the load_creator_exams method to the event of opening the tab
        self.exam_creators_exam_tab.bind("<Visibility>", self.exams_on_tab_opened)

        self.exam_creators_exam_questions_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exam_creators_exam_questions_tab, text='Exam Questions')
        self.create_exam_creators_exam_questions_widgets(self.exam_creators_exam_questions_tab)
        # Bind the load_exam_question_stats method to the event of opening the tab
        self.exam_creators_exam_questions_tab.bind("<Visibility>", self.exam_question_stats_on_tab_opened)

        self.exam_creators_exam_students_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exam_creators_exam_students_tab, text='Exam Students')
        self.create_exam_creators_exam_students_widgets(self.exam_creators_exam_students_tab)
        # Bind the load_exam_student_stats method to the event of opening the tab
        self.exam_creators_exam_students_tab.bind("<Visibility>", self.exam_student_stats_on_tab_opened)

        self.exam_creators_help_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exam_creators_help_tab, text='Help')
        self.create_exam_creators_help_widgets(self.exam_creators_help_tab)
    
    def create_exam_creators_exam_widgets(self, exam_creators_exam_tab):
        # Create a frame for Exam info (upper frame)
        self.exam_info_upper_frame = tk.Frame(exam_creators_exam_tab)
        self.exam_info_upper_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Create fields and labels for question
        # Exam ID

        # id generate image 
        path = "..\images\idgen.png"
        # get the path to the directory this script is in
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the file from there
        image_path = os.path.join(scriptdir, path)
        # make sure the path exists and if not create it
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        self.idgen_image = Image.open(image_path)
        self.idgen_icon = ImageTk.PhotoImage(self.idgen_image)

        self.exam_id_label = tk.Label(self.exam_info_upper_frame, text="Exam ID:")
        self.exam_id_label.grid(row=0, column=0, padx=(2,0), pady=2, sticky=tk.W)
        self.exam_id_var = tk.StringVar()
        self.exam_id_var.set("")
        self.exam_id_value_label = tk.Label(self.exam_info_upper_frame, textvariable=self.exam_id_var, text="", width=10)
        self.exam_id_value_label.grid(row=0, column=1, padx=2, pady=2)
        self.generate_id_button = tk.Button(self.exam_info_upper_frame, image=self.idgen_icon, cursor="hand2", command=self.generate_exam_id, width=20, height=20)
        self.generate_id_button.grid(row=0, column=2, padx=2, pady=2)

        # Exam name
        self.exam_name_label = tk.Label(self.exam_info_upper_frame, text="Exam Name:")
        self.exam_name_label.grid(row=0, column=3, padx=(20,0), pady=2, sticky=tk.W)
        self.exam_name_entry = tk.Entry(self.exam_info_upper_frame, width=30)
        self.exam_name_entry.grid(row=0, column=4, padx=2, pady=2)

        # Has negative score
        self.has_negative_score_var = tk.IntVar(value=0) # Default unchecked
        self.has_negative_score = tk.Checkbutton(self.exam_info_upper_frame, text="Has Negative Score?", variable=self.has_negative_score_var)
        self.has_negative_score.grid(row=0, column=5, padx=(20,0), pady=2, sticky=tk.W)

        # passing score
        self.passing_score_label = tk.Label(self.exam_info_upper_frame, text="Passing Score:")
        self.passing_score_label.grid(row=0, column=6, padx=(20,0), pady=2, sticky=tk.W)
        self.passing_score_entry = tk.Entry(self.exam_info_upper_frame, width=10)
        self.passing_score_entry.grid(row=0, column=7, padx=2, pady=2)

        # duration
        self.duration_label = tk.Label(self.exam_info_upper_frame, text="Duration(min):")
        self.duration_label.grid(row=0, column=8, padx=(20,0), pady=2, sticky=tk.W)
        self.duration_entry = tk.Entry(self.exam_info_upper_frame, width=10)
        self.duration_entry.grid(row=0, column=9, padx=2, pady=2)

        # Create a frame for Exam info (lower frame)
        self.exam_info_lower_frame = tk.Frame(exam_creators_exam_tab)
        self.exam_info_lower_frame.grid(row=1, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Create a labeled frame for Exam date & time info
        self.exam_datetime_frame = tk.LabelFrame(self.exam_info_lower_frame, text="Exam Date & Time")
        self.exam_datetime_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)
        
        # Date
        self.exam_date_label = tk.Label(self.exam_datetime_frame, text="Exam Date:")
        self.exam_date_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.year_combo = ttk.Combobox(self.exam_datetime_frame, width=10, values=list(range(1900, 2101)))
        self.year_combo.grid(row=0, column=1, padx=2, pady=2)
        self.year_combo.set(datetime.now().year)
        self.year_combo.bind("<<ComboboxSelected>>", self.update_calendar)

        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.month_combo = ttk.Combobox(self.exam_datetime_frame, width=10, values=[f"{i} ({month_names[i-1]})" for i in range(1, 13)])
        self.month_combo.grid(row=0, column=2, padx=2, pady=2)
        self.month_combo.set(datetime.now().month)
        self.month_combo.bind("<<ComboboxSelected>>", self.update_calendar)

        self.day_combo = ttk.Combobox(self.exam_datetime_frame, width=10, values=list(range(1, 32)))
        self.day_combo.grid(row=0, column=3, padx=2, pady=2)
        self.day_combo.set(datetime.now().day)
        self.day_combo.bind("<<ComboboxSelected>>", self.update_calendar)

        # Graphical calendar
        self.cal_frame = ttk.Frame(self.exam_datetime_frame)
        self.cal_frame.grid(row=1, column=0, columnspan=4, padx=2, pady=2)

        self.cal = Calendar(self.cal_frame, selectmode='day', date_pattern='yyyy-mm-dd', cursor="hand1")
        self.cal.grid(row=0, column=0, padx=2, pady=2)
        self.cal.bind("<<CalendarSelected>>", self.update_combo_boxes)

        # Time
        self.start_time_label = tk.Label(self.exam_datetime_frame, text="Exam Time:")
        self.start_time_label.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)

        self.hour_combo = ttk.Combobox(self.exam_datetime_frame, width=10, values=list(range(24)))
        self.hour_combo.grid(row=2, column=1, padx=2, pady=2)
        self.hour_combo.set(datetime.now().hour)

        self.minute_combo = ttk.Combobox(self.exam_datetime_frame, width=10, values=list(range(60)))
        self.minute_combo.grid(row=2, column=2, padx=2, pady=2)
        self.minute_combo.set(datetime.now().minute)

        self.second_combo = ttk.Combobox(self.exam_datetime_frame, width=10, values=list(range(60)))
        self.second_combo.grid(row=2, column=3, padx=2, pady=2)
        self.second_combo.set(datetime.now().second)

        # Create a labeled frame for Exam operators info
        self.exam_operators_frame = tk.LabelFrame(self.exam_info_lower_frame, text="Exam Operators")
        self.exam_operators_frame.grid(row=0, column=1, padx=5, pady=2, sticky=tk.NSEW)

        # Fetch exam handlers and supervisors data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT UR.user_name
                        FROM User U
                        JOIN User_Role UR 
                        ON U.user_name = UR.user_name
                        WHERE role_name = 'Exam_Handler'""")
        exam_handler_users = [eh[0] for eh in cursor.fetchall()]

        cursor.execute("""SELECT UR.user_name
                        FROM User U
                        JOIN User_Role UR 
                        ON U.user_name = UR.user_name
                        WHERE role_name = 'Exam_Supervisor'""")
        exam_supervisor_users = [es[0] for es in cursor.fetchall()]
        connection.close()

        # Exam handler
        self.exam_handler_label = tk.Label(self.exam_operators_frame, text="Exam Handler User:")
        self.exam_handler_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.exam_handler_combo = ttk.Combobox(self.exam_operators_frame, width=20, values=exam_handler_users)
        self.exam_handler_combo.grid(row=0, column=1, padx=2, pady=2)
        self.exam_handler_combo.set(exam_handler_users[0])

        # Exam supervisor
        self.exam_supervisor_label = tk.Label(self.exam_operators_frame, text="Exam Supervisor User:")
        self.exam_supervisor_label.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)

        self.exam_supervisor_combo = ttk.Combobox(self.exam_operators_frame, width=20, values=exam_supervisor_users)
        self.exam_supervisor_combo.grid(row=1, column=1, padx=2, pady=2)
        self.exam_supervisor_combo.set(exam_supervisor_users[0])

        # Create a frame for exam buttons
        self.exam_buttons_frame = tk.Frame(self.exam_info_lower_frame)
        self.exam_buttons_frame.grid(row=0, column=2, padx=5, pady=2, sticky=tk.NSEW)

        # Configure columns to expand equally
        self.exam_buttons_frame.columnconfigure(0, weight=1)
        self.exam_buttons_frame.columnconfigure(1, weight=1)
        self.exam_buttons_frame.columnconfigure(2, weight=1)
        self.exam_buttons_frame.columnconfigure(3, weight=1)

        self.insert_exam_button = tk.Button(self.exam_buttons_frame, text="Insert Exam", command=self.gui_insert_exam, width=20)
        self.insert_exam_button.grid(row=0, column=0, padx=20, pady=20, sticky=tk.E)

        self.update_exam_button = tk.Button(self.exam_buttons_frame, text="Update Exam", command=self.gui_update_exam, width=20)
        self.update_exam_button.grid(row=1, column=0, padx=20, pady=20)

        self.delete_exam_button = tk.Button(self.exam_buttons_frame, text="Delete Exam", command=self.gui_delete_exam, width=20)
        self.delete_exam_button.grid(row=2, column=0, padx=20, pady=20)

        self.reset_exam_fields_button = tk.Button(self.exam_buttons_frame, text="Reset Exam", command=self.reset_exam_fields, width=20)
        self.reset_exam_fields_button.grid(row=3, column=0, padx=20, pady=20, sticky=tk.W)

        # Create a frame for table containing exam data
        self.exams_table_frame = tk.Frame(exam_creators_exam_tab)
        self.exams_table_frame.grid(row=2, column=0, sticky=tk.NSEW)

        # Create the table containing the questions created by this exam creator
        columns = ("exam_id", "exam_name", "exam_date", "start_time", "duration", "creation_date", "creation_time", "has_negative_score", \
                    "passing_score", "handler_user_name", "supervisor_user_name")
        self.exams_table = ttk.Treeview(self.exams_table_frame, column=columns, show='headings', selectmode="browse")
        self.exams_table.heading("#1", text="exam_id",anchor=tk.W)
        self.exams_table.column("#1", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#2", text="exam_name", anchor=tk.W)
        self.exams_table.column("#2", stretch=tk.NO, width = 150, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#3", text="exam_date", anchor=tk.W)
        self.exams_table.column("#3", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#4", text="start_time",anchor=tk.W)
        self.exams_table.column("#4", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#5", text="duration", anchor=tk.W)
        self.exams_table.column("#5", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#6", text="creation_date", anchor=tk.W)
        self.exams_table.column("#6", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#7", text="creation_time",anchor=tk.W)
        self.exams_table.column("#7", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#8", text="has_negative_score", anchor=tk.W)
        self.exams_table.column("#8", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#9", text="passing_score", anchor=tk.W)
        self.exams_table.column("#9", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#10", text="handler_user_name",anchor=tk.W)
        self.exams_table.column("#10", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.exams_table.heading("#11", text="supervisor_user_name", anchor=tk.W)
        self.exams_table.column("#11", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)

        self.exams_table.grid(row=0, column=0, sticky="nsew")

        self.exams_table_y_scrollbar = ttk.Scrollbar(self.exams_table_frame, orient="vertical", command=self.exams_table.yview)
        self.exams_table_y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.exams_table.configure(yscrollcommand=self.exams_table_y_scrollbar.set)
        # Bind the function to the Treeview's selection event
        self.exams_table.bind('<<TreeviewSelect>>', self.exams_on_treeview_select)

        s = ttk.Style(self.exams_table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

    def generate_exam_id(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT exam_id
                       FROM Exam
                       ORDER BY creation_date DESC, creation_time DESC
                       LIMIT 1""")
        prev_last_exam_id = cursor.fetchone()[0]
        connection.close()
        # Add one to the exam id number and set the exam_id
        new_exam_id = f"Ex{(int(prev_last_exam_id[2:]) + 1)}"
        self.exam_id_var.set(new_exam_id)

    def update_calendar(self, event=None):
        selected_date = f"{self.year_combo.get()}-{self.month_combo.get().split()[0].zfill(2)}-{self.day_combo.get().zfill(2)}"
        self.cal.selection_set(selected_date)
    
    def update_combo_boxes(self, event=None):
        selected_date = self.cal.get_date().split('-')
        self.year_combo.set(selected_date[0])
        self.month_combo.set(selected_date[1])
        self.day_combo.set(selected_date[2])

    def gui_insert_exam(self):
        exam_id = self.exam_id_var.get()
        exam_name = self.exam_name_entry.get()
        has_negative_score = int(self.has_negative_score_var.get())
        passing_score = int(self.passing_score_entry.get()) if self.passing_score_entry.get() else None
        duration = int(self.duration_entry.get()) if self.duration_entry.get() else None
        exam_date = f"{self.year_combo.get()}/{self.month_combo.get().split()[0].zfill(2)}/{self.day_combo.get().zfill(2)}"
        start_time = f"{self.hour_combo.get().zfill(2)}:{self.minute_combo.get().zfill(2)}:{self.second_combo.get().zfill(2)}"
        handler_user_name = self.exam_handler_combo.get()
        supervisor_user_name = self.exam_supervisor_combo.get()
        creator_user_name = self.username

        # Convert exam_date and start_time to datetime objects
        exam_datetime = datetime.strptime(f"{exam_date} {start_time}", "%Y/%m/%d %H:%M:%S")
        # Get tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)

        # Validate fields
        if not (exam_id and exam_name and passing_score and duration and type and exam_date and start_time and handler_user_name and supervisor_user_name):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return
        if exam_datetime < tomorrow:
            messagebox.showwarning("Invalid Exam Date & Time", "Exam datetime must be at least tomorrow.")
            return
        elif not (isinstance(duration, int) and duration > 0):
            messagebox.showwarning("Invalid Exam Duration", "Exam duration must be a positive integer.")
            return
        elif not (isinstance(passing_score, int) and 0 < passing_score < 100):
            messagebox.showwarning("Invalid Exam Passing Score", "Exam passing score must be a positive integer between 0 and 100.")
            return

        # Call insert_exam function from db1.py
        exam_insert_msg = insert_exam(exam_id, exam_name, exam_date, start_time, duration, has_negative_score, \
                                    passing_score, handler_user_name, supervisor_user_name, creator_user_name)
        messagebox.showinfo("Exam Insert", exam_insert_msg)
        
        # Reset/clear fields
        self.reset_exam_fields()
        # reload the question table data
        self.load_creator_exams()
    
    def load_creator_exams(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT exam_id, exam_name, exam_date, start_time, duration, creation_date, creation_time,
                                 has_negative_score, passing_score, handler_user_name, supervisor_user_name
                       FROM Exam
                       WHERE creator_user_name = ?""", (self.username, ))
        data = cursor.fetchall()
        connection.close()

        # Clear previous data in the table
        self.exams_table.delete(*self.exams_table.get_children())

        # Insert new data rows
        for row in data:
            self.exams_table.insert("", "end", values=row)

    def exams_on_tab_opened(self, event):
        # Load exams when the tab is opened
        self.load_creator_exams()

    def gui_update_exam(self):
        exam_id = self.exam_id_var.get()
        exam_name = self.exam_name_entry.get()
        has_negative_score = int(self.has_negative_score_var.get())
        passing_score = int(self.passing_score_entry.get()) if self.passing_score_entry.get() else None
        duration = int(self.duration_entry.get()) if self.duration_entry.get() else None
        exam_date = f"{self.year_combo.get()}/{self.month_combo.get().split()[0].zfill(2)}/{self.day_combo.get().zfill(2)}"
        start_time = f"{self.hour_combo.get().zfill(2)}:{self.minute_combo.get().zfill(2)}:{self.second_combo.get().zfill(2)}"
        handler_user_name = self.exam_handler_combo.get()
        supervisor_user_name = self.exam_supervisor_combo.get()

        # Convert exam_date and start_time to datetime objects
        exam_datetime = datetime.strptime(f"{exam_date} {start_time}", "%Y/%m/%d %H:%M:%S")
        # Get tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)

        # Validate fields
        if not (exam_id and exam_name and passing_score and duration and type and exam_date and start_time and handler_user_name and supervisor_user_name):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return
        if exam_datetime < tomorrow:
            messagebox.showwarning("Invalid Exam Date & Time", "Exam datetime must be at least tomorrow.")
            return
        elif not (isinstance(duration, int) and duration > 0):
            messagebox.showwarning("Invalid Exam Duration", "Exam duration must be a positive integer.")
            return
        elif not (isinstance(passing_score, int) and 0 < passing_score < 100):
            messagebox.showwarning("Invalid Exam Passing Score", "Exam passing score must be a positive integer between 0 and 100.")
            return

        # Call update_exam function from db1.py
        exam_update_msg = update_exam(exam_id, exam_name, exam_date, start_time, duration, has_negative_score, \
                                    passing_score, handler_user_name, supervisor_user_name)
        messagebox.showinfo("Exam Update", exam_update_msg)

        # Reset/clear fields
        self.reset_exam_fields()
        # reload the question table data
        self.load_creator_exams()

    def gui_delete_exam(self):
        exam_id = self.exam_id_var.get()

        # Validate fields
        if not exam_id:
            messagebox.showwarning("Incomplete Information", "Please fill exam_id to delete.")
            return

        # Call delete_exam function from db1.py
        exam_delete_msg = delete_exam(exam_id)
        messagebox.showinfo("Exam Delete", exam_delete_msg)

        # Reset/clear fields
        self.reset_exam_fields()
        # reload the question table data
        self.load_creator_exams()

    def exams_on_treeview_select(self, event):
        # Reset fields
        self.reset_exam_fields()
        
        # Get the selected item
        selected_item = self.exams_table.selection()
        
        if selected_item:
            # Get the values of the selected item
            values = self.exams_table.item(selected_item, 'values')

            # Replace None values with empty strings
            values = ["" if value is None else value for value in values]

            # Set the values of the exam-related fields
            self.exam_id_var.set(values[0])
            self.exam_name_entry.delete(0, tk.END)
            self.exam_name_entry.insert(0, values[1])
            self.year_combo.set(values[2].split("/")[0])
            self.month_combo.set(values[2].split("/")[1])
            self.day_combo.set(values[2].split("/")[2])
            self.hour_combo.set(values[3].split(":")[0])
            self.minute_combo.set(values[3].split(":")[1])
            self.second_combo.set(values[3].split(":")[2])
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, values[4])
            self.has_negative_score_var.set(1) if values[7] == "1" else self.has_negative_score_var.set(0)
            self.passing_score_entry.delete(0, tk.END)
            self.passing_score_entry.insert(0, values[8])
            self.exam_handler_combo.set(values[9])
            self.exam_supervisor_combo.set(values[10])
            # Update calendar
            selected_date = f"{values[2].split('/')[0]}-{values[2].split('/')[1].split()[0].zfill(2)}-{values[2].split('/')[2].zfill(2)}"
            self.cal.selection_set(selected_date)

    def reset_exam_fields(self):
        # Clear Question ID field
        self.exam_id_var.set("")
        # Clear exam name field
        self.exam_name_entry.delete(0, tk.END)
        # Clear has negative score checkbuttons
        self.has_negative_score_var.set(0)
        # Clear passing score field
        self.passing_score_entry.delete(0, tk.END)
        # Clear duration field
        self.duration_entry.delete(0, tk.END)
        # Reset time comboboxes
        self.hour_combo.set(datetime.now().hour)
        self.minute_combo.set(datetime.now().minute)
        self.second_combo.set(datetime.now().second)
        # Reset date comboboxes
        self.year_combo.set(datetime.now().year)
        self.month_combo.set(datetime.now().month)
        self.day_combo.set(datetime.now().day)

    def create_exam_creators_exam_questions_widgets(self, exam_creators_exam_questions_tab):
        # Create a left fram for Exam-questions info
        self.exam_question_left_frame = tk.Frame(exam_creators_exam_questions_tab)
        self.exam_question_left_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)
        
        # Create a frame for Exam info
        self.exam_question_frame1 = tk.Frame(self.exam_question_left_frame)
        self.exam_question_frame1.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Fetch exam handlers and supervisors data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT exam_id
                        FROM Exam
                        WHERE creator_user_name = ?
                        ORDER BY exam_id""", (self.username, ))
        exam_ids = [e[0] for e in cursor.fetchall()]

        cursor.execute("""SELECT DISTINCT topic FROM Question WHERE topic IS NOT NULL""")
        topics = [t[0] for t in cursor.fetchall()]

        cursor.execute("""SELECT DISTINCT subtopic FROM Question WHERE subtopic IS NOT NULL""")
        subtopics = [st[0] for st in cursor.fetchall()]

        connection.close()

        # Exam ID
        self.exam_id_label = tk.Label(self.exam_question_frame1, text="Exam ID:")
        self.exam_id_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.exam_id_combo = ttk.Combobox(self.exam_question_frame1, width=10, values=exam_ids)
        self.exam_id_combo.grid(row=0, column=1, padx=2, pady=2)
        self.exam_id_combo.set(exam_ids[-1])
        self.exam_id_combo.bind("<<ComboboxSelected>>", self.update_exam_question_stats)

        # Total Questions
        self.exam_total_questions_label = tk.Label(self.exam_question_frame1, text="Total Questions:")
        self.exam_total_questions_label.grid(row=0, column=2, padx=(20,0), pady=2, sticky=tk.W)
        
        self.exam_total_questions_var = tk.StringVar()
        self.exam_total_questions_var.set("0")
        self.exam_total_questions_value_label = tk.Label(self.exam_question_frame1, textvariable=self.exam_total_questions_var)
        self.exam_total_questions_value_label.grid(row=0, column=3, padx=2, pady=2, sticky=tk.W)

        # Total Points
        self.exam_total_points_label = tk.Label(self.exam_question_frame1, text="Total Points:")
        self.exam_total_points_label.grid(row=0, column=3, padx=(20,0), pady=2, sticky=tk.W)

        self.exam_total_points_var = tk.StringVar()
        self.exam_total_points_var.set("0")
        self.exam_total_points_value_label = tk.Label(self.exam_question_frame1, textvariable=self.exam_total_points_var)
        self.exam_total_points_value_label.grid(row=0, column=4, padx=2, pady=2, sticky=tk.W)

        # Create a labeled frame for Exam questions type stats
        self.exam_question_frame2 = tk.LabelFrame(self.exam_question_left_frame, text="Exam Questions Type Stats")
        self.exam_question_frame2.grid(row=1, column=0, padx=5, pady=2, sticky=tk.NSEW)

        self.multiple_choice_count_var = tk.StringVar()
        self.multiple_choice_count_var.set("0")
        self.multiple_choice_pct_var = tk.StringVar()
        self.multiple_choice_pct_var.set("0%")
        self.multiple_choice_label = tk.Label(self.exam_question_frame2, text="Multiple choice:")
        self.multiple_choice_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        self.multiple_choice_count_label = tk.Label(self.exam_question_frame2, textvariable=self.multiple_choice_count_var)
        self.multiple_choice_count_label.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)
        self.multiple_choice_pct_label = tk.Label(self.exam_question_frame2, textvariable=self.multiple_choice_pct_var)
        self.multiple_choice_pct_label.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)

        self.true_false_count_var = tk.StringVar()
        self.true_false_count_var.set("0")
        self.true_false_pct_var = tk.StringVar()
        self.true_false_pct_var.set("0%")
        self.true_false_label = tk.Label(self.exam_question_frame2, text="True/False:")
        self.true_false_label.grid(row=0, column=3, padx=(20, 0), pady=2, sticky=tk.W)
        self.true_false_count_label = tk.Label(self.exam_question_frame2, textvariable=self.true_false_count_var)
        self.true_false_count_label.grid(row=0, column=4, padx=2, pady=2, sticky=tk.W)
        self.true_false_pct_label = tk.Label(self.exam_question_frame2, textvariable=self.true_false_pct_var)
        self.true_false_pct_label.grid(row=0, column=5, padx=2, pady=2, sticky=tk.W)

        self.descriptive_practical_count_var = tk.StringVar()
        self.descriptive_practical_count_var.set("0")
        self.descriptive_practical_pct_var = tk.StringVar()
        self.descriptive_practical_pct_var.set("0%")
        self.descriptive_practical_label = tk.Label(self.exam_question_frame2, text="Descriptive/Practical:")
        self.descriptive_practical_label.grid(row=0, column=6, padx=(20, 0), pady=2, sticky=tk.W)
        self.descriptive_practical_count_label = tk.Label(self.exam_question_frame2, textvariable=self.descriptive_practical_count_var)
        self.descriptive_practical_count_label.grid(row=0, column=7, padx=2, pady=2, sticky=tk.W)
        self.descriptive_practical_pct_label = tk.Label(self.exam_question_frame2, textvariable=self.descriptive_practical_pct_var)
        self.descriptive_practical_pct_label.grid(row=0, column=8, padx=2, pady=2, sticky=tk.W)

        # Create a labeled frame for Exam questions difficulty stats
        self.exam_question_frame3 = tk.LabelFrame(self.exam_question_left_frame, text="Exam Questions Type Stats")
        self.exam_question_frame3.grid(row=2, column=0, padx=5, pady=2, sticky=tk.NSEW)

        self.easy_count_var = tk.StringVar()
        self.easy_count_var.set("0")
        self.easy_pct_var = tk.StringVar()
        self.easy_pct_var.set("0%")
        self.easy_label = tk.Label(self.exam_question_frame3, text="Easy:")
        self.easy_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        self.easy_count_label = tk.Label(self.exam_question_frame3, textvariable=self.easy_count_var)
        self.easy_count_label.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)
        self.easy_pct_label = tk.Label(self.exam_question_frame3, textvariable=self.easy_pct_var)
        self.easy_pct_label.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)

        self.normal_count_var = tk.StringVar()
        self.normal_count_var.set("0")
        self.normal_pct_var = tk.StringVar()
        self.normal_pct_var.set("0%")
        self.normal_label = tk.Label(self.exam_question_frame3, text="Normal:")
        self.normal_label.grid(row=0, column=3, padx=(20, 0), pady=2, sticky=tk.W)
        self.normal_count_label = tk.Label(self.exam_question_frame3, textvariable=self.normal_count_var)
        self.normal_count_label.grid(row=0, column=4, padx=2, pady=2, sticky=tk.W)
        self.normal_pct_label = tk.Label(self.exam_question_frame3, textvariable=self.normal_pct_var)
        self.normal_pct_label.grid(row=0, column=5, padx=2, pady=2, sticky=tk.W)

        self.hard_count_var = tk.StringVar()
        self.hard_count_var.set("0")
        self.hard_pct_var = tk.StringVar()
        self.hard_pct_var.set("0%")
        self.hard_label = tk.Label(self.exam_question_frame3, text="Hard:")
        self.hard_label.grid(row=0, column=6, padx=(20, 0), pady=2, sticky=tk.W)
        self.hard_count_label = tk.Label(self.exam_question_frame3, textvariable=self.hard_count_var)
        self.hard_count_label.grid(row=0, column=7, padx=2, pady=2, sticky=tk.W)
        self.hard_pct_label = tk.Label(self.exam_question_frame3, textvariable=self.hard_pct_var)
        self.hard_pct_label.grid(row=0, column=8, padx=2, pady=2, sticky=tk.W)

        # Create a labeled frame for Exam questions filtering and selection
        self.exam_question_frame4 = tk.LabelFrame(self.exam_question_left_frame, text="Exam Questions Selection by Filtering")
        self.exam_question_frame4.grid(row=3, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Type
        self.type_label = tk.Label(self.exam_question_frame4, text="Type:")
        self.type_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        self.type_combo = ttk.Combobox(self.exam_question_frame4, values=('Multiple choice', 'True/False', 'Descriptive/Practical'), width=30)
        self.type_combo.grid(row=0, column=1, padx=2, pady=2)

        # Difficulty
        self.difficulty_label = tk.Label(self.exam_question_frame4, text="Difficulty:")
        self.difficulty_label.grid(row=0, column=2, padx=(20,0), pady=2, sticky=tk.W)
        self.difficulty_combo = ttk.Combobox(self.exam_question_frame4, values=('Easy', 'Normal', 'Hard'), width=30)
        self.difficulty_combo.grid(row=0, column=3, padx=2, pady=2)

        # How Many
        self.how_many_label = tk.Label(self.exam_question_frame4, text="How Many?:")
        self.how_many_label.grid(row=0, column=4, padx=(20,0), pady=2, sticky=tk.W)
        self.how_many_entry = tk.Entry(self.exam_question_frame4, width=10)
        self.how_many_entry.grid(row=0, column=5, padx=2, pady=2)

        # Topic
        self.topic_label = tk.Label(self.exam_question_frame4, text="Topic:")
        self.topic_label.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
        self.topic_combo = ttk.Combobox(self.exam_question_frame4, values=topics, width=30)
        self.topic_combo.grid(row=1, column=1, padx=2, pady=2)

        # Subtopic
        self.subtopic_label = tk.Label(self.exam_question_frame4, text="Subtopic:")
        self.subtopic_label.grid(row=1, column=2, padx=(20,0), pady=2, sticky=tk.W)
        self.subtopic_combo = ttk.Combobox(self.exam_question_frame4, values=subtopics, width=30)
        self.subtopic_combo.grid(row=1, column=3, padx=2, pady=2)

        # Pick random questions button
        self.pick_random_questions_button = tk.Button(self.exam_question_frame4, text="Pick Random Questions", cursor="hand2", command=self.pick_random_questions, width=30)
        self.pick_random_questions_button.grid(row=1, column=4, padx=20, columnspan=3, pady=2)

        # Create a frame for table containing data
        self.random_questions_table_frame = tk.Frame(self.exam_question_frame4)
        self.random_questions_table_frame.grid(row=2, column=0, columnspan=6, sticky=tk.NSEW)

        # Create the table containing the randomly picked questions
        columns = ("question_id", "topic", "subtopic", "text","difficulty", "type", "points")
        self.random_questions_table = ttk.Treeview(self.random_questions_table_frame, column=columns, show='headings', selectmode="browse")
        self.random_questions_table.heading("#1", text="question_id",anchor=tk.W)
        self.random_questions_table.column("#1", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.random_questions_table.heading("#2", text="topic", anchor=tk.W)
        self.random_questions_table.column("#2", stretch=tk.NO, width = 150, minwidth=50, anchor=tk.W)
        self.random_questions_table.heading("#3", text="subtopic", anchor=tk.W)
        self.random_questions_table.column("#3", stretch=tk.NO, width = 150, minwidth=50, anchor=tk.W)
        self.random_questions_table.heading("#4", text="text",anchor=tk.W)
        self.random_questions_table.column("#4", stretch=tk.NO, width = 250, minwidth=50, anchor=tk.W)
        self.random_questions_table.heading("#5", text="difficulty", anchor=tk.W)
        self.random_questions_table.column("#5", stretch=tk.NO, width = 60, minwidth=50, anchor=tk.W)
        self.random_questions_table.heading("#6", text="type", anchor=tk.W)
        self.random_questions_table.column("#6", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.random_questions_table.heading("#7", text="points",anchor=tk.W)
        self.random_questions_table.column("#7", stretch=tk.NO, width = 50, minwidth=50, anchor=tk.W)

        self.random_questions_table.grid(row=0, column=0, sticky="nsew")

        self.random_questions_table_y_scrollbar = ttk.Scrollbar(self.random_questions_table_frame, orient="vertical", command=self.random_questions_table.yview)
        self.random_questions_table_y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.random_questions_table.configure(yscrollcommand=self.random_questions_table_y_scrollbar.set)

        s = ttk.Style(self.random_questions_table_frame)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Create a frame for adding the questions to exam
        self.add_exam_questions_frame = tk.Frame(self.exam_question_frame4)
        self.add_exam_questions_frame.grid(row=3, column=0, columnspan=6, sticky=tk.NSEW)

        self.add_exam_questions_button = tk.Button(self.add_exam_questions_frame, text="Add Exam Questions", cursor="hand2", command=self.add_exam_questions)
        self.add_exam_questions_button.grid(row=0, column=0, padx=100, pady=2)

        self.reset_question_selection_button = tk.Button(self.add_exam_questions_frame, text="Reset Question Selection", cursor="hand2", command=self.reset_question_selection)
        self.reset_question_selection_button.grid(row=0, column=1, padx=100, pady=2)

        # Create a right frame for exam question ids info
        self.exam_question_right_frame = tk.LabelFrame(exam_creators_exam_questions_tab, text="Exam Questions")
        self.exam_question_right_frame.grid(row=0, column=1, padx=5, pady=2, sticky=tk.NSEW)

        # Create the table containing the exam question ids
        columns = ("question_id")
        self.exam_questions_table = ttk.Treeview(self.exam_question_right_frame, column=columns, show='headings', selectmode="browse", height=20)
        self.exam_questions_table.heading("#1", text="question_id",anchor=tk.W)
        self.exam_questions_table.column("#1", stretch=tk.NO, width = 120, minwidth=80, anchor=tk.W)

        self.exam_questions_table.grid(row=0, column=0, sticky="nsew")

        self.exam_questions_table_y_scrollbar = ttk.Scrollbar(self.exam_question_right_frame, orient="vertical", command=self.exam_questions_table.yview)
        self.exam_questions_table_y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.exam_questions_table.configure(yscrollcommand=self.exam_questions_table_y_scrollbar.set)

        s = ttk.Style(self.exam_questions_table)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Delete exam question button
        self.delete_exam_question_button = tk.Button(self.exam_question_right_frame, text="Delete Exam Question", cursor="hand2", command=self.delete_exam_question)
        self.delete_exam_question_button.grid(row=1, column=0, padx=2, pady=2)

    def pick_random_questions(self):
        exam_id = self.exam_id_combo.get()
        type = self.type_combo.get()
        difficulty = self.difficulty_combo.get()
        how_many = int(self.how_many_entry.get())
        topic = self.topic_combo.get()
        subtopic = self.subtopic_combo.get() if self.subtopic_combo.get() != "None" and self.subtopic_combo.get() else None

        # Validate fields
        if not (exam_id and type and difficulty and how_many and topic):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return
        elif not (isinstance(how_many, int) and how_many > 0):
            messagebox.showwarning("Invalid How Many", "How many must be a positive integer.")
            return
        
        # Pick how_many random and not repeatetive questions
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
        if subtopic:
            cursor.execute("""
            SELECT question_id
            FROM Question
            WHERE type = ? AND difficulty = ? AND topic = ? AND subtopic = ?""", (type, difficulty, topic, subtopic))
        else:
            cursor.execute("""
            SELECT question_id
            FROM Question
            WHERE type = ? AND difficulty = ? AND topic = ? """, (type, difficulty, topic))

        matched_questions = [q[0] for q in cursor.fetchall()]

        cursor.execute("""
        SELECT question_id
        FROM Exam_Question
        WHERE exam_id = ?""", (exam_id, ))
        
        exam_questions = [q[0] for q in cursor.fetchall()]

        possible_questions = set(matched_questions) | set(exam_questions)

        if how_many > len(possible_questions):
            messagebox.showwarning("Sampling Impossible", "Not enough possible questions with these settings to sample.")
            return
        
        random_questions = random.sample(matched_questions, k=how_many)

        # load random questions in the table
        # Build the IN clause with f-string and Construct the SQL query using f-string
        cursor.execute(f"""SELECT question_id, topic, subtopic, text, difficulty, type, points
                       FROM Question
                       WHERE question_id IN ({', '.join('?' * len(random_questions))})""", random_questions)
        data = cursor.fetchall()
        connection.close()

        # Clear previous data in the table
        self.random_questions_table.delete(*self.random_questions_table.get_children())

        # Insert new data rows
        for row in data:
            self.random_questions_table.insert("", "end", values=row)

    def add_exam_questions(self):
        exam_id = self.exam_id_combo.get()
        # Iterate through all items in the random questions table
        for item in self.random_questions_table.get_children():
            values = self.random_questions_table.item(item, 'values')
            if len(values) == 0:
                messagebox.showwarning("No Question Selected", "Please select some random questions to add to the exam.")
                return
            question_id = values[0] 
            # Call insert_exam_question function from db1.py
            insert_exam_question(exam_id, question_id)
        
        messagebox.showinfo("Exam Questions Insert", "Exam Questions inserted successfully.")
    
        # reset question selection
        self.reset_question_selection()
        # Update exam question stats when the tab is opened
        self.update_exam_question_stats()
        #load the exam questions
        self.load_exam_questions()

    def reset_question_selection(self):
        # Clear how many field
        self.how_many_entry.delete(0, tk.END)
        # Clear treeview (random_questions_table) data
        self.random_questions_table.delete(*self.random_questions_table.get_children())
    
    def load_exam_questions(self):
        exam_id = self.exam_id_combo.get()
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id
                       FROM Exam_Question
                       WHERE exam_id = ?""", (exam_id, ))
        
        data = cursor.fetchall()
        connection.close()

        # Clear treeview (exam_questions_table) data
        self.exam_questions_table.delete(*self.exam_questions_table.get_children())
        # Insert data rows
        for row in data:
            self.exam_questions_table.insert("", "end", values=row)

    def update_exam_question_stats(self , event=None):
        exam_id = self.exam_id_combo.get()
        # Fetch exam handlers and supervisors data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT COUNT(*) AS total_questions, SUM(Q.points) AS total_points
                        FROM Exam_Question EQ
                        JOIN Question Q ON Q.question_id = EQ.question_id
                        WHERE EQ.exam_id = ?""", (exam_id, ))
        data = cursor.fetchone()
        total_questions = data[0]
        total_points = data[1]

        cursor.execute("""SELECT COUNT(*) AS multiple_choice_questions
                        FROM Exam_Question EQ
                        JOIN Question Q ON Q.question_id = EQ.question_id
                        WHERE EQ.exam_id = ? AND Q.type = 'Multiple choice'""", (exam_id, ))
        multiple_choice_questions_count = cursor.fetchone()[0]
        multiple_choice_questions_pct = int(100 * multiple_choice_questions_count / total_questions) if int(total_questions) else 0

        cursor.execute("""SELECT COUNT(*) AS true_false_questions
                        FROM Exam_Question EQ
                        JOIN Question Q ON Q.question_id = EQ.question_id
                        WHERE EQ.exam_id = ? AND Q.type = 'True/False'""", (exam_id, ))
        true_false_questions_count = cursor.fetchone()[0]
        true_false_questions_pct = int(100 * true_false_questions_count / total_questions) if int(total_questions) else 0

        cursor.execute("""SELECT COUNT(*) AS descriptive_practical_questions
                        FROM Exam_Question EQ
                        JOIN Question Q ON Q.question_id = EQ.question_id
                        WHERE EQ.exam_id = ? AND Q.type = 'Descriptive/Practical'""", (exam_id, ))
        descriptive_practical_questions_count = cursor.fetchone()[0]
        descriptive_practical_questions_pct = int(100 * descriptive_practical_questions_count / total_questions) if int(total_questions) else 0

        cursor.execute("""SELECT COUNT(*) AS easy_questions
                        FROM Exam_Question EQ
                        JOIN Question Q ON Q.question_id = EQ.question_id
                        WHERE EQ.exam_id = ? AND Q.difficulty = 'Easy'""", (exam_id, ))
        easy_questions_count = cursor.fetchone()[0]
        easy_questions_pct = int(100 * easy_questions_count / total_questions) if int(total_questions) else 0

        cursor.execute("""SELECT COUNT(*) AS normal_questions
                        FROM Exam_Question EQ
                        JOIN Question Q ON Q.question_id = EQ.question_id
                        WHERE EQ.exam_id = ? AND Q.difficulty = 'Normal'""", (exam_id, ))
        normal_questions_count = cursor.fetchone()[0]
        normal_questions_pct = int(100 * normal_questions_count / total_questions) if int(total_questions) else 0

        cursor.execute("""SELECT COUNT(*) AS hard_questions
                        FROM Exam_Question EQ
                        JOIN Question Q ON Q.question_id = EQ.question_id
                        WHERE EQ.exam_id = ? AND Q.difficulty = 'Hard'""", (exam_id, ))
        hard_questions_count = cursor.fetchone()[0]
        hard_questions_pct = int(100 * hard_questions_count / total_questions) if int(total_questions) else 0
        connection.close()

        # Setting the calculated stats to the labels
        self.exam_total_questions_var.set(total_questions)
        self.exam_total_points_var.set(total_points)

        self.multiple_choice_count_var.set(multiple_choice_questions_count)
        self.multiple_choice_pct_var.set(f"{multiple_choice_questions_pct}%")
        self.true_false_count_var.set(true_false_questions_count)
        self.true_false_pct_var.set(f"{true_false_questions_pct}%")
        self.descriptive_practical_count_var.set(descriptive_practical_questions_count)
        self.descriptive_practical_pct_var.set(f"{descriptive_practical_questions_pct}%")

        self.easy_count_var.set(easy_questions_count)
        self.easy_pct_var.set(f"{easy_questions_pct}%")
        self.normal_count_var.set(normal_questions_count)
        self.normal_pct_var.set(f"{normal_questions_pct}%")
        self.hard_count_var.set(hard_questions_count)
        self.hard_pct_var.set(f"{hard_questions_pct}%")

    def exam_question_stats_on_tab_opened(self, event):
        # Update exam question stats when the tab is opened
        self.update_exam_question_stats()
        #load the exam questions
        self.load_exam_questions()
    
    def delete_exam_question(self):
        exam_id = self.exam_id_combo.get()
        # Get the selected item
        selected_item = self.exam_questions_table.selection()
        
        if selected_item:
            # Get the values of the selected item
            values = self.exam_questions_table.item(selected_item, 'values')
            question_id = values[0] 

        # Call delete_exam_question function from db1.py
        delete_exam_question_msg = delete_exam_question(exam_id, question_id)
        messagebox.showinfo("Exam Questions Insert", delete_exam_question_msg)
    
        # reset question selection
        self.reset_question_selection()
        # Update exam question stats when the tab is opened
        self.update_exam_question_stats()
        #load the exam questions
        self.load_exam_questions()
    
    def create_exam_creators_exam_students_widgets(self, exam_creators_question_tab):
        # Create a top frame
        self.exam_student_top_frame = tk.Frame(exam_creators_question_tab)
        self.exam_student_top_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Fetch exam handlers and supervisors data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT exam_id
                        FROM Exam
                        WHERE creator_user_name = ?
                        ORDER BY exam_id""", (self.username, ))
        exam_ids = [e[0] for e in cursor.fetchall()]

        cursor.execute("""SELECT U.user_name, U.first_name, U.last_name
                        FROM User U
                        JOIN User_Role UR
                        ON U.user_name = UR.user_name
                        WHERE role_name = 'Student'""")
        students_info = [t[0] for t in cursor.fetchall()]
        student_values = [f"{si[1]} {si[2]} ({si[0]})" for si in students_info]
        connection.close()

        # Exam ID
        self.exam_id_label = tk.Label(self.exam_student_top_frame, text="Exam ID:")
        self.exam_id_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.exam_id_combo = ttk.Combobox(self.exam_student_top_frame, width=10, values=exam_ids)
        self.exam_id_combo.grid(row=0, column=1, padx=2, pady=2)
        self.exam_id_combo.set(exam_ids[-1])
        self.exam_id_combo.bind("<<ComboboxSelected>>", self.update_exam_student_stats)

        # Total exam students
        self.exam_total_students_label = tk.Label(self.exam_student_top_frame, text="Total Students:")
        self.exam_total_students_label.grid(row=0, column=2, padx=(20,0), pady=2, sticky=tk.W)
        
        self.exam_total_students_var = tk.StringVar()
        self.exam_total_students_var.set("0")
        self.exam_total_students_value_label = tk.Label(self.exam_student_top_frame, textvariable=self.exam_total_students_var)
        self.exam_total_students_value_label.grid(row=0, column=3, padx=2, pady=2, sticky=tk.W)

        # Create a bottom frame for treeviews
        self.exam_student_bottom_frame = tk.Frame(exam_creators_question_tab)
        self.exam_student_bottom_frame.grid(row=1, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Create a left frame for exam student ids info
        self.exam_student_left_frame = tk.LabelFrame(self.exam_student_bottom_frame, text="Students")
        self.exam_student_left_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Create the table containing the exam student ids
        columns = ("user_name", "first_name", "last_name")
        self.students_table = ttk.Treeview(self.exam_student_left_frame, column=columns, show='headings', selectmode="browse", height=20)
        self.students_table.heading("#1", text="user_name",anchor=tk.W)
        self.students_table.column("#1", stretch=tk.NO, width = 100, minwidth=80, anchor=tk.W)
        self.students_table.heading("#2", text="first_name",anchor=tk.W)
        self.students_table.column("#2", stretch=tk.NO, width = 100, minwidth=80, anchor=tk.W)
        self.students_table.heading("#3", text="last_name",anchor=tk.W)
        self.students_table.column("#3", stretch=tk.NO, width = 100, minwidth=80, anchor=tk.W)

        self.students_table.grid(row=0, column=0, sticky="nsew")

        self.students_table_table_y_scrollbar = ttk.Scrollbar(self.exam_student_left_frame, orient="vertical", command=self.students_table.yview)
        self.students_table_table_y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.students_table.configure(yscrollcommand=self.students_table_table_y_scrollbar.set)

        s = ttk.Style(self.students_table)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Delete exam student button
        self.add_exam_student_button = tk.Button(self.exam_student_left_frame, text="Add Exam Student", cursor="hand2", command=self.add_exam_student)
        self.add_exam_student_button.grid(row=1, column=0, padx=2, pady=2)
        
        # Create a right frame for exam student ids info
        self.exam_student_right_frame = tk.LabelFrame(self.exam_student_bottom_frame, text="Exam Students")
        self.exam_student_right_frame.grid(row=0, column=1, padx=5, pady=2, sticky=tk.NSEW)

        # Create the table containing the exam student ids
        columns = ("user_name", "first_name", "last_name")
        self.exam_students_table = ttk.Treeview(self.exam_student_right_frame, column=columns, show='headings', selectmode="browse", height=20)
        self.exam_students_table.heading("#1", text="student_id",anchor=tk.W)
        self.exam_students_table.column("#1", stretch=tk.NO, width = 100, minwidth=80, anchor=tk.W)
        self.exam_students_table.heading("#2", text="first_name",anchor=tk.W)
        self.exam_students_table.column("#2", stretch=tk.NO, width = 100, minwidth=80, anchor=tk.W)
        self.exam_students_table.heading("#3", text="last_name",anchor=tk.W)
        self.exam_students_table.column("#3", stretch=tk.NO, width = 100, minwidth=80, anchor=tk.W)

        self.exam_students_table.grid(row=0, column=0, sticky="nsew")

        self.exam_students_table_y_scrollbar = ttk.Scrollbar(self.exam_student_right_frame, orient="vertical", command=self.exam_students_table.yview)
        self.exam_students_table_y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.exam_students_table.configure(yscrollcommand=self.exam_students_table_y_scrollbar.set)

        s = ttk.Style(self.exam_students_table)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Delete exam student button
        self.delete_exam_student_button = tk.Button(self.exam_student_right_frame, text="Delete Exam Student", cursor="hand2", command=self.delete_exam_student)
        self.delete_exam_student_button.grid(row=1, column=0, padx=2, pady=2)

    def add_exam_student(self):
        exam_id = self.exam_id_combo.get()

        # Fetch exam handlers and supervisors data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT COUNT(*) AS exam_questions_count
                        FROM Exam_Question
                        WHERE exam_id = ?""", (exam_id, ))
        exam_questions_count = int(cursor.fetchone()[0])
        connection.close()

        # Get the selected item
        selected_item = self.students_table.selection()
        
        if selected_item:
            # Get the values of the selected item
            values = self.students_table.item(selected_item, 'values')

            # Set the values of the question-related fields
            user_name = values[0] 

        # Call insert_user_exam function from db1.py
        add_exam_student_msg = insert_user_exam(exam_id, user_name, 0, exam_questions_count, 0, 0, exam_questions_count, 0, 0)
        messagebox.showinfo("Add Exam Student", add_exam_student_msg)
    
        # Update exam student stats when the tab is opened
        self.update_exam_student_stats()
        #load the exam students
        self.load_exam_students()
        #load the available students
        self.load_students_available()

    def delete_exam_student(self):
        exam_id = self.exam_id_combo.get()
        # Get the selected item
        selected_item = self.exam_students_table.selection()
        
        if selected_item:
            # Get the values of the selected item
            values = self.exam_students_table.item(selected_item, 'values')
            user_name = values[0] 

        # Call delete_user_exam function from db1.py
        delete_exam_student_msg = delete_user_exam(exam_id, user_name)
        messagebox.showinfo("Exam Student Delete", delete_exam_student_msg)
    
        # Update exam student stats when the tab is opened
        self.update_exam_student_stats()
        #load the exam students
        self.load_exam_students()
        #load the available students
        self.load_students_available()

    def update_exam_student_stats(self, event=None):
        exam_id = self.exam_id_combo.get()
        # Fetch exam handlers and supervisors data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT COUNT(*) AS exam_students_count
                        FROM User_Exam
                        WHERE exam_id = ?""", (exam_id, ))
        exam_students_count = cursor.fetchall()[0]

        # Setting the calculated stats to the labels
        self.exam_total_students_var.set(exam_students_count)

    def load_students_available(self):
        exam_id = self.exam_id_combo.get()
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT U.user_name, U.first_name, U.last_name
                       FROM User U
                       JOIN User_Role UR ON UR.user_name = U.user_name
                       WHERE UR.role_name = 'Student' AND
                       U.user_name NOT IN (
                            SELECT UE.user_name
                            FROM User_Exam UE
                            WHERE exam_id = ?)""", (exam_id, ))
        data = cursor.fetchall()
        connection.close()

        # Clear treeview (students_table) data
        self.students_table.delete(*self.students_table.get_children())
        # Insert data rows
        for row in data:
            self.students_table.insert("", "end", values=row)
    
    def load_exam_students(self):
        exam_id = self.exam_id_combo.get()
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT U.user_name, U.first_name, U.last_name
                       FROM User U
                       JOIN User_Exam UE ON U.user_name = UE.user_name
                       WHERE UE.exam_id = ?""", (exam_id, ))
        data = cursor.fetchall()
        connection.close()

        # Clear treeview (exam_questions_table) data
        self.exam_students_table.delete(*self.exam_students_table.get_children())
        # Insert data rows
        for row in data:
            self.exam_students_table.insert("", "end", values=row)

    def exam_student_stats_on_tab_opened(self, event):
        # Update exam student stats when the tab is opened
        self.update_exam_student_stats()
        #load the exam students
        self.load_exam_students()
        #load the available students
        self.load_students_available()

    def create_exam_creators_help_widgets(self, exam_creators_help_tab):
        # Add User Manuals and Documentation
        user_manual_label = tk.Label(exam_creators_help_tab, text="User Manuals and Documentation", font=("Helvetica", 12, "bold"))
        user_manual_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        user_manual_info = tk.Label(exam_creators_help_tab, text="Access user manuals and system documentation for detailed instructions.", font=("Helvetica", 12))
        user_manual_info.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Add Frequently Asked Questions (FAQs)
        faq_label = tk.Label(exam_creators_help_tab, text="Frequently Asked Questions (FAQs)", font=("Helvetica", 12, "bold"))
        faq_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        faq_info = tk.Label(exam_creators_help_tab, text="Find answers to common questions about system usage, troubleshooting, and more.", font=("Helvetica", 12))
        faq_info.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Add Contact Information and Support Channels
        contact_info_label = tk.Label(exam_creators_help_tab, text="Contact Information and Support Channels", font=("Helvetica", 12, "bold"))
        contact_info_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        contact_info = tk.Label(exam_creators_help_tab, text="Reach out to our support team via email, phone, or live chat for assistance.", font=("Helvetica", 12))
        contact_info.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # Add Video Tutorials and Demos
        video_tutorials_label = tk.Label(exam_creators_help_tab, text="Video Tutorials and Demos", font=("Helvetica", 12, "bold"))
        video_tutorials_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        video_tutorials_info = tk.Label(exam_creators_help_tab, text="Watch video tutorials and demos to learn how to use key features.", font=("Helvetica", 12))
        video_tutorials_info.grid(row=7, column=0, sticky="w", padx=10, pady=5)

        # Add Release Notes and Updates
        release_notes_label = tk.Label(exam_creators_help_tab, text="Release Notes and Updates", font=("Helvetica", 12, "bold"))
        release_notes_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)

        release_notes_info = tk.Label(exam_creators_help_tab, text="Stay updated on the latest system releases, updates, and improvements.", font=("Helvetica", 12))
        release_notes_info.grid(row=9, column=0, sticky="w", padx=10, pady=5)

        # Add Security Guidelines and Best Practices
        security_guidelines_label = tk.Label(exam_creators_help_tab, text="Security Guidelines and Best Practices", font=("Helvetica", 12, "bold"))
        security_guidelines_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)

        security_info = tk.Label(exam_creators_help_tab, text="Learn about security best practices and guidelines to protect your account.", font=("Helvetica", 12))
        security_info.grid(row=11, column=0, sticky="w", padx=10, pady=5)

        # Add Glossary of Terms
        glossary_label = tk.Label(exam_creators_help_tab, text="Glossary of Terms", font=("Helvetica", 12, "bold"))
        glossary_label.grid(row=12, column=0, sticky="w", padx=10, pady=5)

        glossary_info = tk.Label(exam_creators_help_tab, text="Explore the glossary for definitions of common terms and concepts.", font=("Helvetica", 12))
        glossary_info.grid(row=13, column=0, sticky="w", padx=10, pady=5)

        # Add Community Forums and User Groups
        community_forums_label = tk.Label(exam_creators_help_tab, text="Community Forums and User Groups", font=("Helvetica", 12, "bold"))
        community_forums_label.grid(row=14, column=0, sticky="w", padx=10, pady=5)

        community_info = tk.Label(exam_creators_help_tab, text="Engage with the community, ask questions, and share insights on user forums.", font=("Helvetica", 12))
        community_info.grid(row=15, column=0, sticky="w", padx=10, pady=5)
    
    def add_student_tabs(self):
        # Add tabs for different functionalities
        self.students_exam_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.students_exam_tab, text='Exam')
        self.create_students_exam_widgets(self.students_exam_tab)

        self.students_feedback_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.students_feedback_tab, text='Feedback')
        self.create_students_feedback_widgets(self.students_feedback_tab)
        # Bind the load_exam_feedbacks method to the event of opening the tab
        self.students_feedback_tab.bind("<Visibility>", self.exam_feedbacks_on_tab_opened)

        self.students_exam_result_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.students_exam_result_tab, text='Exam Result')
        self.create_students_exam_result_widgets(self.students_exam_result_tab)

        self.students_help_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.students_help_tab, text='Help')
        self.create_students_help_widgets(self.students_help_tab)
    
    def create_students_exam_widgets(self, students_exam_tab):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT UE.user_name, UE.exam_id
                       FROM User_Exam UE
                       JOIN Exam E ON UE.exam_id = E.exam_id
                       WHERE DATETIME('now', 'localtime') < DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time)""")
        unstarted_user_exams = cursor.fetchall()
        unstarted_exam_students = [uue[0] for uue in unstarted_user_exams]

        cursor.execute("""SELECT UE.user_name, UE.exam_id
                       FROM User_Exam UE
                       JOIN Exam E ON UE.exam_id = E.exam_id
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time)
                        AND DATETIME('now', 'localtime') < DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')""")
        started_user_exams = cursor.fetchall()
        started_exam_students = [sue[0] for sue in started_user_exams]

        cursor.execute("""SELECT E.exam_id, E.exam_name, E.has_negative_score
                       FROM User_Exam UE
                       JOIN Exam E ON UE.exam_id = E.exam_id
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time)
                            AND DATETIME('now', 'localtime') < DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                            AND UE.user_name = ?""", (self.username, ))
        student_exam_data = cursor.fetchone()

        if self.username in unstarted_exam_students:
            cursor.execute("""SELECT E.exam_date, E.start_time, E.duration
                       FROM User_Exam UE
                       JOIN Exam E ON UE.exam_id = E.exam_id
                       WHERE DATETIME('now', 'localtime') < DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time)
                       AND UE.user_name = ?""", (self.username, ))
            exam_date, start_time, duration = cursor.fetchone()

            # Combine date and time strings into a single string
            combined_datetime_str = exam_date.replace('/', '-') + ' ' + start_time
            # Convert the combined string into a datetime object
            exam_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%d %H:%M:%S')
            # Calculate exam finish datetime by adding duration minutes to exam datetime
            exam_finish_datetime = exam_datetime + timedelta(minutes=duration)

        elif self.username in started_exam_students:
            cursor.execute("""SELECT E.exam_date, E.start_time, E.duration
                       FROM User_Exam UE
                       JOIN Exam E ON UE.exam_id = E.exam_id
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time)
                            AND DATETIME('now', 'localtime') < DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                            AND UE.user_name = ?""", (self.username, ))
            exam_date, start_time, duration = cursor.fetchone()

            cursor.execute("""SELECT Q.question_id, Q.text, Q.image, Q.points
                       FROM User_Exam UE
                       JOIN Exam E ON UE.exam_id = E.exam_id
                       JOIN Exam_Question EQ ON EQ.exam_id = E.exam_id
                       JOIN Question Q ON EQ.question_id = Q.question_id
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time)
                            AND DATETIME('now', 'localtime') < DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                            AND UE.user_name = ?""", (self.username, ))
            self.student_exam_questions_data = cursor.fetchall()

            # Combine date and time strings into a single string
            combined_datetime_str = exam_date.replace('/', '-') + ' ' + start_time
            # Convert the combined string into a datetime object
            exam_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%d %H:%M:%S')
            # Calculate exam finish datetime by adding duration minutes to exam datetime
            exam_finish_datetime = exam_datetime + timedelta(minutes=duration)

        connection.close()

        # initialize some vars
        self.to_exam_time_var = tk.StringVar(value="")
        self.remaining_exam_time_var = tk.StringVar(value="")

        if self.username in unstarted_exam_students:
            self.not_started_active_exam_label = tk.Label(students_exam_tab, text=f"You have an active/pending exam that starts on {combined_datetime_str}", font=("Helvetica", 18, "bold"))
            self.not_started_active_exam_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)

            # to exam label
            self.to_exam_time_label = tk.Label(students_exam_tab, textvariable=self.to_exam_time_var, font=("Helvetica", 18, "bold"))
            self.to_exam_time_label.grid(row=1, column=0, sticky="w", padx=5, pady=10)
            # Update the countdown every second
            self.update_to_exam_time_countdown(exam_datetime)

            # note label
            self.note_label = tk.Label(students_exam_tab, text=f"Note: When it's time to take exam once logout and login again.", fg="red", font=("Helvetica", 18, "bold"))
            self.note_label.grid(row=2, column=0, sticky="w", padx=5, pady=10)
        
        elif self.username in started_exam_students:
            # student has an active exam that is already startted so can take the exam and submit answers
            student_exam_id = student_exam_data[0] if student_exam_data else None
            student_exam_name = student_exam_data[1] if student_exam_data else None
            student_exam_has_negative_score = student_exam_data[2] if student_exam_data else None

            # Create a frame for exam overall info
            self.exam_overall_info_frame = tk.Frame(students_exam_tab)
            self.exam_overall_info_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)

            # Student exam ID label
            self.student_exam_id_var = tk.StringVar()
            self.student_exam_id_var.set(f"Student Exam ID:  {student_exam_id}")
            self.student_exam_id_label = tk.Label(self.exam_overall_info_frame, textvariable=self.student_exam_id_var, font=("Helvetica", 12))
            self.student_exam_id_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)

            # Student exam name label
            self.student_exam_name_label = tk.Label(self.exam_overall_info_frame, text=f"Student Exam Name:  {student_exam_name}", font=("Helvetica", 12))
            self.student_exam_name_label.grid(row=0, column=1, sticky="w", padx=(20,0), pady=2)

            # Student exam has_negative_score label
            self.student_exam_has_negative_score_var = tk.IntVar(value=1) if student_exam_has_negative_score == 1 else tk.IntVar(value=0)
            self.student_exam_has_negative_score_label = tk.Checkbutton(self.exam_overall_info_frame, text="Has Negative Score?", variable=self.student_exam_has_negative_score_var, font=("Helvetica", 12))
            self.student_exam_has_negative_score_label.grid(row=0, column=2, sticky="w", padx=(20,0), pady=2)

            # remaining exam time label
            self.remaining_exam_time_label = tk.Label(self.exam_overall_info_frame, textvariable=self.remaining_exam_time_var, font=("Helvetica", 12, "bold"))
            self.remaining_exam_time_label.grid(row=0, column=3, sticky="w", padx=(20,0), pady=2)
            # Update the countdown every second
            self.update_remaining_exam_time_countdown(exam_finish_datetime)

            # Create a frame for Qustion info
            self.question_info_frame = tk.Frame(students_exam_tab)
            self.question_info_frame.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)

            # Create fields and labels for question
            
            # first button image 
            path = "..\images\\first.png"
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            self.first_image = Image.open(image_path)
            self.first_icon = ImageTk.PhotoImage(self.first_image)

            # last button image 
            path = "..\images\last.png"
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            self.last_image = Image.open(image_path)
            self.last_icon = ImageTk.PhotoImage(self.last_image)

            # previous button image 
            path = "..\images\previous.png"
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            self.previous_image = Image.open(image_path)
            self.previous_icon = ImageTk.PhotoImage(self.previous_image)

            # next button image 
            path = "..\images\\next.png"
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            self.next_image = Image.open(image_path)
            self.next_icon = ImageTk.PhotoImage(self.next_image)

            # Question No
            self.question_no_label = tk.Label(self.question_info_frame, text="Question No:")
            self.question_no_label.grid(row=0, column=0, padx=(2,0), pady=2, sticky=tk.W)
            self.question_no_var = tk.StringVar()
            self.question_no_var.set("1")
            self.question_no_value_label = tk.Label(self.question_info_frame, textvariable=self.question_no_var, width=5, font=("Helvetica", 12, "bold"))
            self.question_no_value_label.grid(row=0, column=1, padx=2, pady=2)

            # Question ID
            self.question_id_label = tk.Label(self.question_info_frame, text="Question ID:")
            self.question_id_label.grid(row=0, column=2, padx=(20,0), pady=2, sticky=tk.W)
            self.question_id_var = tk.StringVar()
            self.question_id_var.set(str(self.student_exam_questions_data[0][0]))
            self.question_id_value_label = tk.Label(self.question_info_frame, textvariable=self.question_id_var, width=5, font=("Helvetica", 12, "bold"))
            self.question_id_value_label.grid(row=0, column=3, padx=2, pady=2)

            # Points
            self.points_label = tk.Label(self.question_info_frame, text="Points:")
            self.points_label.grid(row=0, column=4, padx=(20,0), pady=2, sticky=tk.W)
            self.points_var = tk.StringVar()
            self.points_var.set(str(self.student_exam_questions_data[0][3]))
            self.points_value_label = tk.Label(self.question_info_frame, width=5, font=("Helvetica", 12, "bold"))
            self.points_value_label.grid(row=0, column=5, padx=2, pady=2)

            # Navigation buttons (first, previous, next, last)
            self.first_button = tk.Button(self.question_info_frame, image=self.first_icon, cursor="hand2", command=self.nav_first, width=20, height=20)
            self.first_button.grid(row=0, column=6, padx=(20,0), pady=2)

            self.previous_button = tk.Button(self.question_info_frame, image=self.previous_icon, cursor="hand2", command=self.nav_previous, width=20, height=20)
            self.previous_button.grid(row=0, column=7, padx=2, pady=2)

            self.next_button = tk.Button(self.question_info_frame, image=self.next_icon, cursor="hand2", command=self.nav_next, width=20, height=20)
            self.next_button.grid(row=0, column=8, padx=2, pady=2)

            self.last_button = tk.Button(self.question_info_frame, image=self.last_icon, cursor="hand2", command=self.nav_last, width=20, height=20)
            self.last_button.grid(row=0, column=9, padx=2, pady=2)

            self.first_button.config(state=tk.DISABLED)
            self.previous_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL)
            self.last_button.config(state=tk.NORMAL)

            # Create a frame for question and options
            self.question_option_frame = tk.Frame(students_exam_tab)
            self.question_option_frame.grid(row=2, column=0, padx=2, pady=2, sticky=tk.NSEW)
            
            # Create a frame for Question
            self.question_frame = tk.LabelFrame(self.question_option_frame, text="Question", width=20)
            self.question_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            # Widgets for attachment image
            self.question_attachment_frame = tk.Frame(self.question_frame)
            self.question_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.question_image_open_button = tk.Button(self.question_attachment_frame, text="Question Image", command=lambda: self.open_question_attachment_image(self.image_path_for_question(self.question_id_var.get())))
            self.question_image_open_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
            
            self.question_has_attachment_var = tk.IntVar(value=0)
            self.question_has_attachment = tk.Checkbutton(self.question_attachment_frame, text="Has Attachment?", variable=self.question_has_attachment_var)
            self.question_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)
            self.question_has_attachment.config(state=tk.DISABLED)
            self.question_has_attachment_var.set(1 if self.student_exam_questions_data[0][2] else 0)
            
            # configure question image button
            if not self.question_has_attachment_var.get():
                self.question_image_open_button.config(state=tk.DISABLED)
            else:
                # enable the question image button
                self.question_image_open_button.config(state=tk.NORMAL)
                # set image path that open_question_attachment_image can access it
                self.question_attachment_image_path = self.student_exam_questions_data[0][2]

            # Question text area
            self.question_text_area = tk.Text(self.question_frame, width=40, height=20)
            self.question_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=2)
            self.question_text_area.delete('1.0', tk.END)
            self.question_text_area.insert(tk.END, self.student_exam_questions_data[0][1])
            self.question_text_area.config(state=tk.DISABLED)

            # Create a frame for Options
            self.options_frame = tk.LabelFrame(self.question_option_frame, text="Options", width=20)
            self.options_frame.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

            # Widgets for attachment image for option1
            self.option1_frame = tk.LabelFrame(self.options_frame, text="Option 1", width=10)
            self.option1_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
            
            self.option1_attachment_frame = tk.Frame(self.option1_frame)
            self.option1_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.option1_image_open_button = tk.Button(self.option1_attachment_frame, text="Option Image", command=lambda: self.open_option1_attachment_image(self.image_path_for_option(self.question_id_var.get(), 1)))
            self.option1_image_open_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.option1_has_attachment_var = tk.IntVar(value=0) # Default unchecked
            self.option1_has_attachment = tk.Checkbutton(self.option1_attachment_frame, text="Has Attachment?", variable=self.option1_has_attachment_var)
            self.option1_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

            self.option1_is_checked_var = tk.IntVar(value=0) # Default unchecked
            self.option1_is_checked = tk.Checkbutton(self.option1_attachment_frame, variable=self.option1_is_checked_var)
            self.option1_is_checked.grid(row=0, column=2, padx=(170,0), pady=2, sticky=tk.W)

            # option1 text area
            self.option1_text_area = tk.Text(self.option1_frame, width=50, height=7)
            self.option1_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=3)

            # Widgets for attachment image for option2
            self.option2_frame = tk.LabelFrame(self.options_frame, text="Option 2", width=10)
            self.option2_frame.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)
            
            self.option2_attachment_frame = tk.Frame(self.option2_frame)
            self.option2_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.option2_image_open_button = tk.Button(self.option2_attachment_frame, text="Option Image", command=lambda: self.open_option2_attachment_image(self.image_path_for_option(self.question_id_var.get(), 2)))
            self.option2_image_open_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.option2_has_attachment_var = tk.IntVar(value=0) # Default unchecked
            self.option2_has_attachment = tk.Checkbutton(self.option2_attachment_frame, text="Has Attachment?", variable=self.option2_has_attachment_var)
            self.option2_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

            self.option2_is_checked_var = tk.IntVar(value=0) # Default unchecked
            self.option2_is_checked = tk.Checkbutton(self.option2_attachment_frame, variable=self.option2_is_checked_var)
            self.option2_is_checked.grid(row=0, column=2, padx=(170,0), pady=2, sticky=tk.W)

            # option2 text area
            self.option2_text_area = tk.Text(self.option2_frame, width=50, height=7)
            self.option2_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=3)

            # Widgets for attachment image for option
            self.option3_frame = tk.LabelFrame(self.options_frame, text="Option 3", width=10)
            self.option3_frame.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
            
            self.option3_attachment_frame = tk.Frame(self.option3_frame)
            self.option3_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.option3_image_open_button = tk.Button(self.option3_attachment_frame, text="Option Image", command=lambda: self.open_option3_attachment_image(self.image_path_for_option(self.question_id_var.get(), 3)))
            self.option3_image_open_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.option3_has_attachment_var = tk.IntVar(value=0) # Default unchecked
            self.option3_has_attachment = tk.Checkbutton(self.option3_attachment_frame, text="Has Attachment?", variable=self.option3_has_attachment_var)
            self.option3_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

            self.option3_is_checked_var = tk.IntVar(value=0) # Default unchecked
            self.option3_is_checked = tk.Checkbutton(self.option3_attachment_frame, variable=self.option3_is_checked_var)
            self.option3_is_checked.grid(row=0, column=2, padx=(170,0), pady=2, sticky=tk.W)

            # option3 text area
            self.option3_text_area = tk.Text(self.option3_frame, width=50, height=7)
            self.option3_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=3)

            # Widgets for attachment image for option
            self.option4_frame = tk.LabelFrame(self.options_frame, text="Option 4", width=10)
            self.option4_frame.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)
            
            self.option4_attachment_frame = tk.Frame(self.option4_frame)
            self.option4_attachment_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.option4_image_open_button = tk.Button(self.option4_attachment_frame, text="Option Image", command=lambda: self.open_option4_attachment_image(self.image_path_for_option(self.question_id_var.get(), 4)))
            self.option4_image_open_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.option4_has_attachment_var = tk.IntVar(value=0) # Default unchecked
            self.option4_has_attachment = tk.Checkbutton(self.option4_attachment_frame, text="Has Attachment?", variable=self.option4_has_attachment_var)
            self.option4_has_attachment.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

            self.option4_is_checked_var = tk.IntVar(value=0) # Default unchecked
            self.option4_is_checked = tk.Checkbutton(self.option4_attachment_frame, variable=self.option4_is_checked_var)
            self.option4_is_checked.grid(row=0, column=2, padx=(170,0), pady=2, sticky=tk.W)

            # option4 text area
            self.option4_text_area = tk.Text(self.option4_frame, width=50, height=7)
            self.option4_text_area.grid(row=1, column=0, padx=2, pady=2, columnspan=3)

            # Create a frame for answer buttons
            self.question_buttons_frame = tk.Frame(students_exam_tab)
            self.question_buttons_frame.grid(row=3, column=0, padx=5, pady=2, sticky=tk.NSEW)

            # load exam_question_options
            self.load_exam_question_options(self.student_exam_questions_data[0][0])

            # Configure columns to expand equally
            self.question_buttons_frame.columnconfigure(0, weight=1)
            self.question_buttons_frame.columnconfigure(1, weight=1)

            self.submit_answer_button = tk.Button(self.question_buttons_frame, text="Submit Answer", command=self.submit_answer)
            self.submit_answer_button.grid(row=0, column=0, padx=10, pady=2, sticky=tk.E)

            self.reset_answer_button = tk.Button(self.question_buttons_frame, text="Reset Answer", command=self.reset_answer)
            self.reset_answer_button.grid(row=0, column=1, padx=10, pady=2, sticky=tk.W)

            # Create a frame for answer stats
            self.answer_stats_frame = tk.Frame(students_exam_tab)
            self.answer_stats_frame.grid(row=4, column=0, padx=5, pady=2, sticky=tk.NSEW)

            # Answered and Unanswered questions
            self.answered_questions_label = tk.Label(self.answer_stats_frame, text="Answered Questions:")
            self.answered_questions_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
            self.answered_questions_var = tk.StringVar()
            self.answered_questions_var.set("0")
            self.answered_questions_value_label = tk.Label(self.answer_stats_frame, textvariable=self.answered_questions_var, width=5, font=("Helvetica", 12, "bold"))
            self.answered_questions_value_label.grid(row=0, column=1, padx=2, pady=2)

            self.unanswered_questions_label = tk.Label(self.answer_stats_frame, text="Unanswered Questions:")
            self.unanswered_questions_label.grid(row=0, column=2, padx=(10,0), pady=2, sticky=tk.W)
            self.unanswered_questions_var = tk.StringVar()
            self.unanswered_questions_var.set("0")
            self.unanswered_questions_value_label = tk.Label(self.answer_stats_frame, textvariable=self.unanswered_questions_var, width=5, font=("Helvetica", 12, "bold"))
            self.unanswered_questions_value_label.grid(row=0, column=3, padx=2, pady=2)

            # update answer stats
            self.update_answer_stats()

        else:
            # Student has no active exam so in this tab just sees a label informing this case
            self.no_active_exam_label = tk.Label(students_exam_tab, text="You have no active/pending exam.", font=("Helvetica", 18, "bold"))
            self.no_active_exam_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def update_to_exam_time_countdown(self, exam_datetime):
        # Calculate the time difference
        current_time = datetime.now()
        time_difference = exam_datetime - current_time

        # Calculate days, hours, minutes, and seconds
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Construct countdown text based on remaining time
        if days > 0:
            countdown_text = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds until exam starts..."
        elif hours > 0:
            countdown_text = f"{hours} hours, {minutes} minutes, {seconds} seconds until exam starts..."
        elif minutes > 0:
            countdown_text = f"{minutes} minutes, {seconds} seconds until exam starts..."
        else:
            countdown_text = f"{seconds} seconds until exam starts..."

        # Update the label with the countdown
        self.to_exam_time_var.set(countdown_text)

        # Schedule the update every second
        self.after(1000, self.update_to_exam_time_countdown, exam_datetime)

    def update_remaining_exam_time_countdown(self, exam_finish_datetime):
        # Calculate the time difference
        current_time = datetime.now()
        time_difference = exam_finish_datetime - current_time

        # Calculate hours, minutes, and seconds
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Construct countdown text based on remaining time
        if hours > 0:
            countdown_text = f"{hours} hours, {minutes} minutes, {seconds} seconds remaining from exam time"
        elif minutes > 0:
            countdown_text = f"{minutes} minutes, {seconds} seconds remaining from exam time"
        else:
            countdown_text = f"{seconds} seconds remaining from exam time"

        # Update the label with the countdown
        self.remaining_exam_time_var.set(countdown_text)

        # Schedule the update every second
        self.after(1000, self.update_remaining_exam_time_countdown, exam_finish_datetime)

    def nav_first(self):
        # Activate fields to set values
        self.question_has_attachment.config(state=tk.NORMAL)
        self.question_text_area.config(state=tk.NORMAL)
        # set values
        self.question_no_var.set("1")
        self.question_id_var.set(str(self.student_exam_questions_data[0][0]))
        self.points_var.set(str(self.student_exam_questions_data[0][3]))
        self.question_has_attachment_var.set(1 if self.student_exam_questions_data[0][2] else 0)
        
        if not self.question_has_attachment_var.get():
                self.question_image_open_button.config(state=tk.DISABLED)
        else:
            # enable the question image button
            self.question_image_open_button.config(state=tk.NORMAL)
            # set image path that open_question_attachment_image can access it
            self.question_attachment_image_path = self.student_exam_questions_data[0][2]

        self.question_text_area.delete('1.0', tk.END)
        self.question_text_area.insert(tk.END, self.student_exam_questions_data[0][1])
        # disable fields
        self.question_has_attachment.config(state=tk.DISABLED)
        self.question_text_area.config(state=tk.DISABLED)
        # disable previous and first buttons but make sure next and last buttons are normal
        self.first_button.config(state=tk.DISABLED)
        self.previous_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)
        self.last_button.config(state=tk.NORMAL)

        # load exam_question_options
        self.load_exam_question_options(self.student_exam_questions_data[0][0])

    def nav_previous(self):    
        # Activate fields to set values
        self.question_has_attachment.config(state=tk.NORMAL)
        self.question_text_area.config(state=tk.NORMAL)
        # set values
        self.question_no_var.set(str(int(self.question_no_var.get()) - 1))
        x = int(self.question_no_var.get())
        self.question_id_var.set(str(self.student_exam_questions_data[x-1][0]))
        self.points_var.set(str(self.student_exam_questions_data[x-1][3]))
        self.question_has_attachment_var.set(1 if self.student_exam_questions_data[x-1][2] else 0)
        
        if not self.question_has_attachment_var.get():
                self.question_image_open_button.config(state=tk.DISABLED)
        else:
            # enable the question image button
            self.question_image_open_button.config(state=tk.NORMAL)
            # set image path that open_question_attachment_image can access it
            self.question_attachment_image_path = self.student_exam_questions_data[x-1][2]
                
        self.question_text_area.delete('1.0', tk.END)
        self.question_text_area.insert(tk.END, self.student_exam_questions_data[x-1][1])
        # disable fields
        self.question_has_attachment.config(state=tk.DISABLED)
        self.question_text_area.config(state=tk.DISABLED)
        
        # after navigation, check question index and enable/disable nav buttons if necessary
        if x == 1:
            # we're gonna be in the first question
            self.first_button.config(state=tk.DISABLED)
            self.previous_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL)
            self.last_button.config(state=tk.NORMAL)
        else:
            # make sure all of the nav buttons are enabled
            self.first_button.config(state=tk.NORMAL)
            self.previous_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
            self.last_button.config(state=tk.NORMAL)
        
        # load exam_question_options
        self.load_exam_question_options(self.student_exam_questions_data[x-1][0])

    def nav_next(self):
        # Activate fields to set values
        self.question_has_attachment.config(state=tk.NORMAL)
        self.question_text_area.config(state=tk.NORMAL)
        # set values
        self.question_no_var.set(str(int(self.question_no_var.get()) + 1))
        x = int(self.question_no_var.get())
        self.question_id_var.set(str(self.student_exam_questions_data[x-1][0]))
        self.points_var.set(str(self.student_exam_questions_data[x-1][3]))
        self.question_has_attachment_var.set(1 if self.student_exam_questions_data[x-1][2] else 0)
        
        if not self.question_has_attachment_var.get():
                self.question_image_open_button.config(state=tk.DISABLED)
        else:
            # enable the question image button
            self.question_image_open_button.config(state=tk.NORMAL)
            # set image path that open_question_attachment_image can access it
            self.question_attachment_image_path = self.student_exam_questions_data[x-1][2]
                
        self.question_text_area.delete('1.0', tk.END)
        self.question_text_area.insert(tk.END, self.student_exam_questions_data[x-1][1])
        # disable fields
        self.question_has_attachment.config(state=tk.DISABLED)
        self.question_text_area.config(state=tk.DISABLED)
        
        # after navigation, check question index and enable/disable nav buttons if necessary
        if x == len(self.student_exam_questions_data):
            # we're gonna be in the last question
            self.first_button.config(state=tk.NORMAL)
            self.previous_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
            self.last_button.config(state=tk.DISABLED)
        else:
            # make sure all of the nav buttons are enabled
            self.first_button.config(state=tk.NORMAL)
            self.previous_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
            self.last_button.config(state=tk.NORMAL)
        
        # load exam_question_options
        self.load_exam_question_options(self.student_exam_questions_data[x-1][0])
        
    def nav_last(self):
        # Activate fields to set values
        self.question_has_attachment.config(state=tk.NORMAL)
        self.question_text_area.config(state=tk.NORMAL)
        # set values
        self.question_no_var.set(str(len(self.student_exam_questions_data)))
        self.question_id_var.set(str(self.student_exam_questions_data[-1][0]))
        self.points_var.set(str(self.student_exam_questions_data[-1][3]))
        self.question_has_attachment_var.set(1 if self.student_exam_questions_data[-1][2] else 0)
        
        if not self.question_has_attachment_var.get():
                self.question_image_open_button.config(state=tk.DISABLED)
        else:
            # enable the question image button
            self.question_image_open_button.config(state=tk.NORMAL)
            # set image path that open_question_attachment_image can access it
            self.question_attachment_image_path = self.student_exam_questions_data[-1][2]

        self.question_text_area.delete('1.0', tk.END)
        self.question_text_area.insert(tk.END, self.student_exam_questions_data[-1][1])
        # disable fields
        self.question_has_attachment.config(state=tk.DISABLED)
        self.question_text_area.config(state=tk.DISABLED)
        # disable next and last buttons but make sure previous and first buttons are normal
        self.first_button.config(state=tk.NORMAL)
        self.previous_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)
        self.last_button.config(state=tk.DISABLED)

        # load exam_question_options
        self.load_exam_question_options(self.student_exam_questions_data[-1][0])
    
    def load_exam_question_options(self, exam_question_id):
        exam_id = self.student_exam_id_var.get().split(" ")[-1] #text variable is like Student Exam ID:  XXXX
        user_name = self.username

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT option_id, question_id, text, image, is_correct_answer
                       FROM Option
                       WHERE question_id = ?
                       ORDER BY option_id""", (exam_question_id, ))
        exam_question_options_data = cursor.fetchall()

        cursor.execute("""SELECT type, text, image
                       FROM Question
                       WHERE question_id = ?""", (exam_question_id, ))
        exam_question_data = cursor.fetchone()

        cursor.execute("""SELECT question_id, option_id, answer_text
                       FROM Answer
                       WHERE exam_id = ? AND user_name = ? AND question_id = ?""", (exam_id, user_name, exam_question_id))
        
        student_question_answers_data = cursor.fetchone()

        connection.close()

        question_answered = False
        # find the option that the student chosen if any
        if student_question_answers_data:
            # student has answered the question
            question_answered = True
            chosen_option_number = student_question_answers_data[1][-1] #last character of the optionid id the option number
        
        # Set options based on the question type
        if exam_question_data[0] == "Multiple choice":
            # activate some fields and widgets to set the
            self.option1_text_area.config(state=tk.NORMAL)
            self.option1_has_attachment.config(state=tk.NORMAL)
            self.option1_image_open_button.config(state=tk.NORMAL)
            self.option1_is_checked.config(state=tk.NORMAL)

            self.option2_text_area.config(state=tk.NORMAL)
            self.option2_has_attachment.config(state=tk.NORMAL)
            self.option2_image_open_button.config(state=tk.NORMAL)
            self.option2_is_checked.config(state=tk.NORMAL)

            self.option3_text_area.config(state=tk.NORMAL)
            self.option3_has_attachment.config(state=tk.NORMAL)
            self.option3_image_open_button.config(state=tk.NORMAL)
            self.option3_is_checked.config(state=tk.NORMAL)

            self.option4_text_area.config(state=tk.NORMAL)
            self.option4_has_attachment.config(state=tk.NORMAL)
            self.option4_image_open_button.config(state=tk.NORMAL)
            self.option4_is_checked.config(state=tk.NORMAL)
            
            # set fields
            self.option1_text_area.delete("1.0", tk.END)
            self.option1_text_area.insert(tk.END, exam_question_options_data[0][2])
            self.option1_has_attachment_var.set(1 if exam_question_options_data[0][3] else 0)
            self.option1_is_checked_var.set(1 if (question_answered and chosen_option_number == "1") else 0)

            self.option2_text_area.delete("1.0", tk.END)
            self.option2_text_area.insert(tk.END, exam_question_options_data[1][2])
            self.option2_has_attachment_var.set(1 if exam_question_options_data[1][3] else 0)
            self.option2_is_checked_var.set(1 if (question_answered and chosen_option_number == "2") else 0)

            self.option3_text_area.delete("1.0", tk.END)
            self.option3_text_area.insert(tk.END, exam_question_options_data[2][2])
            self.option3_has_attachment_var.set(1 if exam_question_options_data[2][3] else 0)
            self.option3_is_checked_var.set(1 if (question_answered and chosen_option_number == "3") else 0)

            self.option4_text_area.delete("1.0", tk.END)
            self.option4_text_area.insert(tk.END, exam_question_options_data[3][2])
            self.option4_has_attachment_var.set(1 if exam_question_options_data[3][3] else 0)
            self.option4_is_checked_var.set(1 if (question_answered and chosen_option_number == "4") else 0)
            
            # disable some fields and widgets again
            self.option1_text_area.config(state=tk.DISABLED)
            if not self.option1_has_attachment_var.get():
                self.option1_image_open_button.config(state=tk.DISABLED)
            else:
                # enable the option1 image button
                self.option1_image_open_button.config(state=tk.NORMAL)
                # set image path that open_option1_attachment_image can access it
                self.option1_attachment_image_path = exam_question_options_data[0][3]
            self.option1_has_attachment.config(state=tk.DISABLED)

            self.option2_text_area.config(state=tk.DISABLED)
            if not self.option2_has_attachment_var.get():
                self.option2_image_open_button.config(state=tk.DISABLED)
            else:
                # enable the option2 image button
                self.option2_image_open_button.config(state=tk.NORMAL)
                # set image path that open_option2_attachment_image can access it
                self.option2_attachment_image_path = exam_question_options_data[1][3]
            self.option2_has_attachment.config(state=tk.DISABLED)

            self.option3_text_area.config(state=tk.DISABLED)
            if not self.option3_has_attachment_var.get():
                self.option3_image_open_button.config(state=tk.DISABLED)
            else:
                # enable the option3 image button
                self.option3_image_open_button.config(state=tk.NORMAL)
                # set image path that open_option3_attachment_image can access it
                self.option3_attachment_image_path = exam_question_options_data[2][3]
            self.option3_has_attachment.config(state=tk.DISABLED)

            self.option4_text_area.config(state=tk.DISABLED)
            if not self.option4_has_attachment_var.get():
                self.option4_image_open_button.config(state=tk.DISABLED)
            else:
                # enable the option4 image button
                self.option4_image_open_button.config(state=tk.NORMAL)
                # set image path that open_option4_attachment_image can access it
                self.option4_attachment_image_path = exam_question_options_data[3][3]
            self.option4_has_attachment.config(state=tk.DISABLED)
        
        elif exam_question_data[0] == "True/False":
            # activate some fields and widgets to set the
            self.option1_text_area.config(state=tk.NORMAL)
            self.option1_has_attachment.config(state=tk.NORMAL)
            self.option1_image_open_button.config(state=tk.NORMAL)
            self.option1_is_checked.config(state=tk.NORMAL)

            self.option2_text_area.config(state=tk.NORMAL)
            self.option2_has_attachment.config(state=tk.NORMAL)
            self.option2_image_open_button.config(state=tk.NORMAL)
            self.option2_is_checked.config(state=tk.NORMAL)

            self.option3_text_area.config(state=tk.NORMAL)
            self.option3_has_attachment.config(state=tk.NORMAL)
            self.option3_image_open_button.config(state=tk.NORMAL)
            self.option3_is_checked.config(state=tk.NORMAL)

            self.option4_text_area.config(state=tk.NORMAL)
            self.option4_has_attachment.config(state=tk.NORMAL)
            self.option4_image_open_button.config(state=tk.NORMAL)
            self.option4_is_checked.config(state=tk.NORMAL)
            
            # set fields
            self.option1_text_area.delete("1.0", tk.END)
            self.option1_text_area.insert(tk.END, exam_question_options_data[0][2])
            self.option1_has_attachment_var.set(1 if exam_question_options_data[0][3] else 0)
            self.option1_is_checked_var.set(1 if (question_answered and chosen_option_number == "1") else 0)

            self.option2_text_area.delete("1.0", tk.END)
            self.option2_text_area.insert(tk.END, exam_question_options_data[1][2])
            self.option2_has_attachment_var.set(1 if exam_question_options_data[1][3] else 0)
            self.option2_is_checked_var.set(1 if (question_answered and chosen_option_number == "2") else 0)

            self.option3_text_area.delete("1.0", tk.END)
            self.option3_has_attachment_var.set(0)
            self.option3_is_checked_var.set(0)

            self.option4_text_area.delete("1.0", tk.END)
            self.option4_has_attachment_var.set(0)
            self.option4_is_checked_var.set(0)
            
            # disable some fields and widgets again
            self.option1_text_area.config(state=tk.DISABLED)
            if not self.option1_has_attachment_var.get():
                self.option1_image_open_button.config(state=tk.DISABLED)
            else:
                # enable the option1 image button
                self.option1_image_open_button.config(state=tk.NORMAL)
                # set image path that open_option1_attachment_image can access it
                self.option1_attachment_image_path = exam_question_options_data[0][3]
            self.option1_has_attachment.config(state=tk.DISABLED)

            self.option2_text_area.config(state=tk.DISABLED)
            if not self.option2_has_attachment_var.get():
                self.option2_image_open_button.config(state=tk.DISABLED)
            else:
                # enable the option2 image button
                self.option2_image_open_button.config(state=tk.NORMAL)
                # set image path that open_option2_attachment_image can access it
                self.option2_attachment_image_path = exam_question_options_data[1][3]
            self.option2_has_attachment.config(state=tk.DISABLED)

            self.option3_text_area.config(state=tk.DISABLED)
            self.option3_image_open_button.config(state=tk.DISABLED)
            self.option3_has_attachment.config(state=tk.DISABLED)
            self.option3_is_checked.config(state=tk.DISABLED)

            self.option4_text_area.config(state=tk.DISABLED)
            self.option4_image_open_button.config(state=tk.DISABLED)
            self.option4_has_attachment.config(state=tk.DISABLED)
            self.option4_is_checked.config(state=tk.DISABLED)
        
        elif exam_question_data[0] == "Descriptive/Practical":
            # activate some fields and widgets to set the
            self.option1_text_area.config(state=tk.NORMAL)
            self.option1_has_attachment.config(state=tk.NORMAL)
            self.option1_image_open_button.config(state=tk.NORMAL)
            self.option1_is_checked.config(state=tk.NORMAL)

            self.option2_text_area.config(state=tk.NORMAL)
            self.option2_has_attachment.config(state=tk.NORMAL)
            self.option2_image_open_button.config(state=tk.NORMAL)
            self.option2_is_checked.config(state=tk.NORMAL)

            self.option3_text_area.config(state=tk.NORMAL)
            self.option3_has_attachment.config(state=tk.NORMAL)
            self.option3_image_open_button.config(state=tk.NORMAL)
            self.option3_is_checked.config(state=tk.NORMAL)

            self.option4_text_area.config(state=tk.NORMAL)
            self.option4_has_attachment.config(state=tk.NORMAL)
            self.option4_image_open_button.config(state=tk.NORMAL)
            self.option4_is_checked.config(state=tk.NORMAL)
            
            # set fields
            self.option1_text_area.delete("1.0", tk.END)
            if question_answered:
                self.option1_text_area.insert(tk.END, student_question_answers_data[2])
            self.option1_has_attachment_var.set(0)
            self.option1_is_checked_var.set(0)

            self.option2_text_area.delete("1.0", tk.END)
            self.option2_has_attachment_var.set(0)
            self.option2_is_checked_var.set(0)

            self.option3_text_area.delete("1.0", tk.END)
            self.option3_has_attachment_var.set(0)
            self.option3_is_checked_var.set(0)

            self.option4_text_area.delete("1.0", tk.END)
            self.option4_has_attachment_var.set(0)
            self.option4_is_checked_var.set(0)
            
            # disable some fields and widgets again
            self.option1_image_open_button.config(state=tk.DISABLED)
            self.option1_has_attachment.config(state=tk.DISABLED)
            self.option1_is_checked.config(state=tk.DISABLED)

            self.option2_text_area.config(state=tk.DISABLED)
            self.option2_image_open_button.config(state=tk.DISABLED)
            self.option2_has_attachment.config(state=tk.DISABLED)
            self.option2_is_checked.config(state=tk.DISABLED)

            self.option3_text_area.config(state=tk.DISABLED)
            self.option3_image_open_button.config(state=tk.DISABLED)
            self.option3_has_attachment.config(state=tk.DISABLED)
            self.option3_is_checked.config(state=tk.DISABLED)

            self.option4_text_area.config(state=tk.DISABLED)
            self.option4_image_open_button.config(state=tk.DISABLED)
            self.option4_has_attachment.config(state=tk.DISABLED)
            self.option4_is_checked.config(state=tk.DISABLED)
        
    def open_question_attachment_image(self, question_image_path): 
        try:
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, question_image_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Open the image file
            image = Image.open(image_path)
            # Show the image
            image.show()
        except FileNotFoundError:
            messagebox.showwarning("File not found", "Please check the path and try again.")
        except Exception as e:
            messagebox.showwarning("Error", f"An error occurred: {e}")

    def open_option1_attachment_image(self, option1_image_path):
        try:
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, option1_image_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Open the image file
            image = Image.open(image_path)
            # Show the image
            image.show()
        except FileNotFoundError:
            messagebox.showwarning("File not found", "Please check the path and try again.")
        except Exception as e:
            messagebox.showwarning("Error", f"An error occurred: {e}")

    def open_option2_attachment_image(self, option2_image_path):
        try:
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, option2_image_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Open the image file
            image = Image.open(image_path)
            # Show the image
            image.show()
        except FileNotFoundError:
            messagebox.showwarning("File not found", "Please check the path and try again.")
        except Exception as e:
            messagebox.showwarning("Error", f"An error occurred: {e}")

    def open_option3_attachment_image(self, option3_image_path):
        try:
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, option3_image_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Open the image file
            image = Image.open(image_path)
            # Show the image
            image.show()
        except FileNotFoundError:
            messagebox.showwarning("File not found", "Please check the path and try again.")
        except Exception as e:
            messagebox.showwarning("Error", f"An error occurred: {e}")

    def open_option4_attachment_image(self, option4_image_path):
        try:
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, option4_image_path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Open the image file
            image = Image.open(image_path)
            # Show the image
            image.show()
        except FileNotFoundError:
            messagebox.showwarning("File not found", "Please check the path and try again.")
        except Exception as e:
            messagebox.showwarning("Error", f"An error occurred: {e}")
    
    def image_path_for_question(self, question_id):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT image
                       FROM Question
                       WHERE question_id = ?""", (question_id, ))
        question_image_path = cursor.fetchone()[0]

        connection.close()

        return question_image_path
    
    def image_path_for_option(self, question_id, option_number):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT image
                       FROM Option
                       WHERE question_id = ?
                       ORDER BY option_id""", (question_id, ))
        question_options_images = cursor.fetchall()

        connection.close()

        return question_options_images[option_number-1][0]

    def submit_answer(self):  
        exam_id = self.student_exam_id_var.get().split(" ")[-1] #text variable is like Student Exam ID:  XXXX
        question_id = self.question_id_var.get()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT option_id, question_id, text, image, is_correct_answer
                       FROM Option
                       WHERE question_id = ?
                       ORDER BY option_id""", (question_id, ))
        exam_question_options_data = cursor.fetchall()

        cursor.execute("""SELECT type, text, image
                       FROM Question
                       WHERE question_id = ?""", (question_id, ))
        exam_question_data = cursor.fetchone()

        cursor.execute("""SELECT exam_id, user_name, question_id
                     FROM Answer""")
        answers = cursor.fetchall()

        connection.close()
        
        user_name = self.username
        
        answer_text = self.option1_text_area.get("1.0", tk.END).strip() if self.option1_text_area.get("1.0", tk.END) else None
        
        # Validate fields
        conditions = [
            self.option1_is_checked_var.get() == 1,
            self.option2_is_checked_var.get() == 1,
            self.option3_is_checked_var.get() == 1,
            self.option4_is_checked_var.get() == 1
        ]
        # Count the number of True values in the conditions list
        count_true = sum(1 for condition in conditions if condition)

        if not (exam_id and question_id):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return
        elif (exam_question_data[0] == "Multiple choice" and count_true == 0) or (exam_question_data[0] == "True/False" and count_true == 0):
            messagebox.showwarning("No Option Selected", "You must select one option to submit, otherwise don't need to submit.")
            return
        elif (exam_question_data[0] == "Multiple choice" and 1 < count_true) or (exam_question_data[0] == "True/False" and 1 < count_true):
            messagebox.showwarning("Multiple Options Selected", "You must select only one option to submit.")
            return
        elif exam_question_data[0] == "Descriptive/Practical" and not answer_text:
            messagebox.showwarning("No Answer Text", "You must type some text in option1 textarea to submit, otherwise don't need to submit.")
            return
        
        if exam_question_data[0] == "Multiple choice":
            if self.option1_is_checked_var.get() == 1:
                option_id = exam_question_options_data[0][0]
            elif self.option2_is_checked_var.get() == 1:
                option_id = exam_question_options_data[1][0]
            elif self.option3_is_checked_var.get() == 1:
                option_id = exam_question_options_data[2][0]
            else:
                option_id = exam_question_options_data[3][0]
        elif exam_question_data[0] == "True/False":
            if self.option1_is_checked_var.get() == 1:
                option_id = exam_question_options_data[0][0]
            elif self.option2_is_checked_var.get() == 1:
                option_id = exam_question_options_data[1][0]
        else:
            option_id = exam_question_options_data[0][0]

        if (exam_id, user_name, question_id) in answers:
            # student already answered this question in this exam, just update the answer
            answer_update_msg = update_answer(exam_id, user_name, question_id, option_id, answer_text)
            messagebox.showinfo("Answer Update", answer_update_msg)
            return

        # Call insert_answer function from db1.py
        answer_sumbit_msg = insert_answer(exam_id, user_name, question_id, option_id, answer_text)
        messagebox.showinfo("Answer Submit", answer_sumbit_msg)

        # update answer stats
        self.update_answer_stats()

    def reset_answer(self):
        question_id = self.question_id_var.get()

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT type, text, image
                       FROM Question
                       WHERE question_id = ?""", (question_id, ))
        exam_question_data = cursor.fetchone()

        connection.close()
        
        if exam_question_data[0] == "Multiple choice":
            self.option1_is_checked_var.set(0)
            self.option2_is_checked_var.set(0)
            self.option3_is_checked_var.set(0)
            self.option4_is_checked_var.set(0)
        elif exam_question_data[0] == "True/False":
            self.option1_is_checked_var.set(0)
            self.option2_is_checked_var.set(0)
        else:
            self.option1_text_area.delete("1.0", tk.END)
        
        # update answer stats
        self.update_answer_stats()
    
    def update_answer_stats(self):
        exam_id = self.student_exam_id_var.get().split(" ")[-1] #text variable is like Student Exam ID:  XXXX
        user_name = self.username

        # Fetch answers data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
 
        cursor.execute("""SELECT COUNT(*) AS answered_questions_count
                        FROM Answer
                        WHERE exam_id = ? AND user_name = ?""", (exam_id, user_name))
        answered_questions_count = cursor.fetchone()[0]

        cursor.execute("""SELECT COUNT(*) AS exam_questions_count
                        FROM Exam_Question
                        WHERE exam_id = ?""", (exam_id, ))
        exam_questions_count = int(cursor.fetchone()[0])

        connection.close()

        # Setting the calculated stats to the labels
        self.answered_questions_var.set(answered_questions_count)
        self.unanswered_questions_var.set(int(exam_questions_count) - int(answered_questions_count))

    def create_students_feedback_widgets(self, students_feedback_tab):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT E.exam_id
                       FROM Exam E
                       JOIN User_Exam UE ON UE.exam_id = E.exam_id
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                            AND UE.user_name = ?
                       ORDER BY E.exam_id""", (self.username, ))
        student_finished_exam_ids = cursor.fetchall()

        connection.close()

        # Create an upper frame for feedback info
        self.upper_feedback_frame = tk.Frame(students_feedback_tab)
        self.upper_feedback_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Exam ID
        self.exam_id_label = tk.Label(self.upper_feedback_frame, text="Exam ID:")
        self.exam_id_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        self.exam_id_combo = ttk.Combobox(self.upper_feedback_frame, width=5, values=student_finished_exam_ids)
        self.exam_id_combo.grid(row=0, column=1, padx=2, pady=2)
        self.exam_id_combo.set(student_finished_exam_ids[-1])

        # feedback type
        self.feedback_type_label = tk.Label(self.upper_feedback_frame, text="Feedback Type:")
        self.feedback_type_label.grid(row=0, column=2, padx=(20,0), pady=2, sticky=tk.W)
        self.feedback_type_combo = ttk.Combobox(self.upper_feedback_frame, values=('Suggestion for improvement', 'Comment on clarity, and difficulty levels'), width=35)
        self.feedback_type_combo.grid(row=0, column=3, padx=2, pady=2)

        # Question ID
        self.question_id_label = tk.Label(self.upper_feedback_frame, text="Question ID:")
        self.question_id_label.grid(row=0, column=4, padx=(20,0), pady=2, sticky=tk.W)
        self.question_id_entry = tk.Entry(self.upper_feedback_frame, width=5)
        self.question_id_entry.grid(row=0, column=5, padx=2, pady=2)

        # rating
        self.feedback_rating_label = tk.Label(self.upper_feedback_frame, text="Rating:")
        self.feedback_rating_label.grid(row=0, column=6, padx=(20,0), pady=2, sticky=tk.W)
        self.feedback_rating_combo = ttk.Combobox(self.upper_feedback_frame, values=list(range(1,11)), width=10)
        self.feedback_rating_combo.grid(row=0, column=7, padx=2, pady=2)

        # Add radio buttons for feedback visibility
        self.feedback_visibility_var = tk.StringVar()
        self.feedback_visibility_var.set("Visible")  # Default selection

        self.visible_radio = tk.Radiobutton(self.upper_feedback_frame, text="Visible", variable=self.feedback_visibility_var, value="Visible")
        self.visible_radio.grid(row=0, column=8, padx=(20,0), pady=2)

        self.invisible_radio = tk.Radiobutton(self.upper_feedback_frame, text="Invisible", variable=self.feedback_visibility_var, value="Invisible")
        self.invisible_radio.grid(row=0, column=9, padx=2, pady=2)

        # Create a lower frame for feedback info
        self.lower_feedback_frame = tk.Frame(students_feedback_tab)
        self.lower_feedback_frame.grid(row=1, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Create a left frame for feedback info (textarea)
        self.left_feedback_frame = tk.Frame(self.lower_feedback_frame)
        self.left_feedback_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # feedback text area
        self.feedback_text_area = tk.Text(self.left_feedback_frame, width=100, height=20)
        self.feedback_text_area.grid(row=0, column=0, padx=2, pady=2)

        # Create a right frame for feedback info (notes)
        self.right_feedback_frame = tk.Frame(self.lower_feedback_frame)
        self.right_feedback_frame.grid(row=0, column=1, padx=5, pady=2, sticky=tk.NSEW)

        # Note1
        self.note1_label = tk.Label(self.right_feedback_frame, text="Note1: Be careful when submitting feedbacks, because you can't edit them later.", fg="red", font=("Helvetica", 12, "bold"), wraplength=350, justify="left")
        self.note1_label.grid(row=0, column=0, padx=2, pady=2, columnspan=2, sticky=tk.W)

        # Note2
        self.note2_label = tk.Label(self.right_feedback_frame, text='Note2: If you set the feedback visibility on "Visible", everybody can read it.', fg="red", font=("Helvetica", 12, "bold"), wraplength=350, justify="left")
        self.note2_label.grid(row=1, column=0, padx=2, pady=10, columnspan=2, sticky=tk.W)

        # Note3
        self.note3_label = tk.Label(self.right_feedback_frame, text="Note3: Feedbacks are very important for us, they are analyzed and will be considered in exam app improvement. Thanks for sharing your experiences, comments, and suggestions.", font=("Helvetica", 12, "bold"), wraplength=350, justify="left")
        self.note3_label.grid(row=2, column=0, padx=2, pady=10, columnspan=2, sticky=tk.W)

        # Create a feedback buttons frame
        self.feedback_buttons_frame = tk.Frame(self.right_feedback_frame)
        self.feedback_buttons_frame.grid(row=3, column=1, padx=5, pady=2, sticky=tk.NSEW)
        
        # Submit feedback button
        self.submit_feedback_button = tk.Button(self.feedback_buttons_frame, text="Submit Feedback", cursor="hand2", command=self.submit_feedback)
        self.submit_feedback_button.grid(row=0, column=0, padx=10, pady=10)

        # Reset feedback button
        self.reset_feedback_button = tk.Button(self.feedback_buttons_frame, text="Reset Feedback", cursor="hand2", command=self.reset_feedback)
        self.reset_feedback_button.grid(row=0, column=1, padx=10, pady=10)

        # Create a frame for feedbacks table
        self.feedbacks_table_frame = tk.Frame(students_feedback_tab)
        self.feedbacks_table_frame.grid(row=2, column=0, padx=5, pady=2, sticky=tk.NSEW)

        # Create the table containing the visible feedbacks on the student finished exams 
        columns = ("exam_id", "user_name", "feedback_time", "feedback_type", "text", "question_id", "rating", "status")
        self.feedbacks_table = ttk.Treeview(self.feedbacks_table_frame, column=columns, show='headings', selectmode="browse", height=20)
        self.feedbacks_table.heading("#1", text="exam_id",anchor=tk.W)
        self.feedbacks_table.column("#1", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.feedbacks_table.heading("#2", text="user_name",anchor=tk.W)
        self.feedbacks_table.column("#2", stretch=tk.NO, width = 110, minwidth=100, anchor=tk.W)
        self.feedbacks_table.heading("#3", text="feedback_time",anchor=tk.W)
        self.feedbacks_table.column("#3", stretch=tk.NO, width = 110, minwidth=100, anchor=tk.W)
        self.feedbacks_table.heading("#4", text="feedback_type",anchor=tk.W)
        self.feedbacks_table.column("#4", stretch=tk.NO, width = 200, minwidth=100, anchor=tk.W)
        self.feedbacks_table.heading("#5", text="text",anchor=tk.W)
        self.feedbacks_table.column("#5", stretch=tk.NO, width = 400, minwidth=200, anchor=tk.W)
        self.feedbacks_table.heading("#6", text="question_id",anchor=tk.W)
        self.feedbacks_table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.feedbacks_table.heading("#7", text="rating",anchor=tk.W)
        self.feedbacks_table.column("#7", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.feedbacks_table.heading("#8", text="status",anchor=tk.W)
        self.feedbacks_table.column("#8", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        
        self.feedbacks_table.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

        self.feedbacks_table_y_scrollbar = ttk.Scrollbar(self.feedbacks_table_frame, orient="vertical", command=self.feedbacks_table.yview)
        self.feedbacks_table_y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.feedbacks_table.configure(yscrollcommand=self.feedbacks_table_y_scrollbar.set)

        # Bind the function to the Treeview's selection event
        self.feedbacks_table.bind('<<TreeviewSelect>>', self.feedbacks_on_treeview_select)

        s = ttk.Style(self.feedbacks_table)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # load the exam feedbacks table data
        self.load_student_exam_feedbacks()
    
    def submit_feedback(self):
        exam_id = self.exam_id_combo.get()
        user_name = self.username
        feedback_type = self.feedback_type_combo.get()
        text = self.feedback_text_area.get("1.0", tk.END)
        question_id = self.question_id_entry.get()
        rating = int(self.feedback_rating_combo.get())
        status = "Pending/Unread"
        is_visible = 1 if self.feedback_visibility_var.get() == "Visible" else 0

        # Validate fields
        if not (exam_id and feedback_type and rating and status):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return

        # Call insert_feedback function from db1.py
        feedback_submit_msg = insert_feedback(exam_id, user_name, feedback_type, text, question_id, rating, status, is_visible)
        messagebox.showinfo("Feedback Submit", feedback_submit_msg)
        
        # Reset/clear fields
        self.reset_feedback()
        # reload the exam feedbacks table data
        self.load_student_exam_feedbacks()

    def load_student_exam_feedbacks(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # retrieve all of the feedbacks on the finished exams that this username was in
        # (only visible feedbacks from other users but all the feedbacks from this user)
        cursor.execute("""SELECT F.exam_id, F.user_name, F.feedback_time, F.feedback_type, F.text, F.question_id, F.rating, F.status
                       FROM Feedback F
                       JOIN Exam E ON F.exam_id = E.exam_id
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                            AND (F.is_visible = 1 OR (F.is_visible = 0 AND F.user_name = ?))
                            AND E.exam_id IN (
                                SELECT UE.exam_id
                                FROM User_Exam UE
                                WHERE UE.user_name = ?
                            )
                        ORDER BY F.feedback_time DESC""", (self.username, self.username))
        data = cursor.fetchall()
        connection.close()

        # Clear treeview (feedbacks_table) data
        self.feedbacks_table.delete(*self.feedbacks_table.get_children())
        # Insert data rows
        for row in data:
            self.feedbacks_table.insert("", "end", values=row)
    
    def exam_feedbacks_on_tab_opened(self, event):
        #load the exam feedbacks
        self.load_student_exam_feedbacks()
    
    def reset_feedback(self):
        # activate fields to set their values
        self.exam_id_combo.config(state=tk.NORMAL)
        self.feedback_type_combo.config(state=tk.NORMAL)
        self.question_id_entry.config(state=tk.NORMAL)
        self.feedback_rating_combo.config(state=tk.NORMAL)
        self.visible_radio.config(state=tk.NORMAL)
        self.visible_radio.config(state=tk.NORMAL)
        self.feedback_text_area.config(state=tk.NORMAL)
        self.submit_feedback_button.config(state=tk.NORMAL)

        # Clear Question ID field
        self.question_id_entry.delete(0, tk.END)
        # Reset feedback visibility
        self.feedback_visibility_var.set("Visible")
        # Clear feedback Text Area
        self.feedback_text_area.delete("1.0", tk.END)
    
    def feedbacks_on_treeview_select(self, event):
        # Reset fields
        self.reset_feedback()
        
        # Get the selected item
        selected_item = self.feedbacks_table.selection()
        
        if selected_item:
            # Get the values of the selected item
            values = self.feedbacks_table.item(selected_item, 'values')

            # Replace None values with empty strings
            values = ["" if value is None else value for value in values]

            # activate fields to set their values
            self.exam_id_combo.config(state=tk.NORMAL)
            self.feedback_type_combo.config(state=tk.NORMAL)
            self.question_id_entry.config(state=tk.NORMAL)
            self.feedback_rating_combo.config(state=tk.NORMAL)
            self.visible_radio.config(state=tk.NORMAL)
            self.invisible_radio.config(state=tk.NORMAL)
            self.feedback_text_area.config(state=tk.NORMAL)

            # Set the values of the feedback-related fields
            self.exam_id_combo.set(values[0])
            self.feedback_type_combo.set(values[3])
            self.feedback_text_area.delete("1.0", tk.END)
            self.feedback_text_area.insert(tk.END, values[4])
            self.question_id_entry.delete(0, tk.END)
            self.question_id_entry.insert(tk.END, values[5])
            self.feedback_rating_combo.set(int(values[6]))
            self.feedback_visibility_var.set("Visible")
            
            # disable fields
            self.exam_id_combo.config(state=tk.DISABLED)
            self.feedback_type_combo.config(state=tk.DISABLED)
            self.question_id_entry.config(state=tk.DISABLED)
            self.feedback_rating_combo.config(state=tk.DISABLED)
            self.visible_radio.config(state=tk.DISABLED)
            self.invisible_radio.config(state=tk.DISABLED)
            self.feedback_text_area.config(state=tk.DISABLED)
            self.submit_feedback_button.config(state=tk.DISABLED)

    def create_students_exam_result_widgets(self, students_exam_result_tab):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT UE.exam_id, UE.score, UE.total_questions, UE.correct_answers,
                                UE.wrong_answers, UE.unanswered_questions, UE.is_passed, UE.is_marked
                       FROM User_Exam UE
                       JOIN Exam E ON UE.exam_id = E.exam_id
                       WHERE DATETIME('now', 'localtime') >= DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                            AND UE.user_name = ?""", (self.username, ))
        data = cursor.fetchall()
        connection.close()

        # load this student exams results

        # Create a frame for student exam results table
        self.student_exam_results_table_frame = tk.Frame(students_exam_result_tab)
        self.student_exam_results_table_frame.grid(row=2, column=0, padx=5, pady=2, sticky=tk.NSEW)

        columns = ("exam_id", "score", "total_questions", "correct_answers", "wrong_answers", "unanswered_questions", "is_passed", "is_marked")

        self.student_exam_results_table = ttk.Treeview(self.student_exam_results_table_frame, column=columns, show='headings', selectmode="browse")
        self.student_exam_results_table.heading("#1", text="exam_id",anchor=tk.W)
        self.student_exam_results_table.column("#1", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.student_exam_results_table.heading("#2", text="score", anchor=tk.W)
        self.student_exam_results_table.column("#2", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
        self.student_exam_results_table.heading("#3", text="total_questions", anchor=tk.W)
        self.student_exam_results_table.column("#3", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.student_exam_results_table.heading("#4", text="correct_answers", anchor=tk.W)
        self.student_exam_results_table.column("#4", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.student_exam_results_table.heading("#5", text="wrong_answers", anchor=tk.W)
        self.student_exam_results_table.column("#5", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.student_exam_results_table.heading("#6", text="unanswered_questions", anchor=tk.W)
        self.student_exam_results_table.column("#6", stretch=tk.NO, width = 120, minwidth=50, anchor=tk.W)
        self.student_exam_results_table.heading("#7", text="is_passed", anchor=tk.W)
        self.student_exam_results_table.column("#7", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)
        self.student_exam_results_table.heading("#8", text="is_marked", anchor=tk.W)
        self.student_exam_results_table.column("#8", stretch=tk.NO, width = 100, minwidth=50, anchor=tk.W)

        self.student_exam_results_table.grid(row=0, column=0, sticky="nsew")

        self.y_scrollbar = ttk.Scrollbar(self.student_exam_results_table_frame, orient="vertical", command=self.student_exam_results_table.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.student_exam_results_table.configure(yscrollcommand=self.y_scrollbar.set)

        s = ttk.Style(self.student_exam_results_table)
        s.theme_use("winnative")
        s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Insert data rows
        for row in data:
            self.student_exam_results_table.insert("", "end", values=row)

    def create_students_help_widgets(self, students_help_tab):
        # Add User Manuals and Documentation
        user_manual_label = tk.Label(students_help_tab, text="User Manuals and Documentation", font=("Helvetica", 12, "bold"))
        user_manual_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        user_manual_info = tk.Label(students_help_tab, text="Access user manuals and system documentation for detailed instructions.", font=("Helvetica", 12))
        user_manual_info.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Add Frequently Asked Questions (FAQs)
        faq_label = tk.Label(students_help_tab, text="Frequently Asked Questions (FAQs)", font=("Helvetica", 12, "bold"))
        faq_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        faq_info = tk.Label(students_help_tab, text="Find answers to common questions about system usage, troubleshooting, and more.", font=("Helvetica", 12))
        faq_info.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Add Contact Information and Support Channels
        contact_info_label = tk.Label(students_help_tab, text="Contact Information and Support Channels", font=("Helvetica", 12, "bold"))
        contact_info_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        contact_info = tk.Label(students_help_tab, text="Reach out to our support team via email, phone, or live chat for assistance.", font=("Helvetica", 12))
        contact_info.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # Add Video Tutorials and Demos
        video_tutorials_label = tk.Label(students_help_tab, text="Video Tutorials and Demos", font=("Helvetica", 12, "bold"))
        video_tutorials_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        video_tutorials_info = tk.Label(students_help_tab, text="Watch video tutorials and demos to learn how to use key features.", font=("Helvetica", 12))
        video_tutorials_info.grid(row=7, column=0, sticky="w", padx=10, pady=5)

        # Add Release Notes and Updates
        release_notes_label = tk.Label(students_help_tab, text="Release Notes and Updates", font=("Helvetica", 12, "bold"))
        release_notes_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)

        release_notes_info = tk.Label(students_help_tab, text="Stay updated on the latest system releases, updates, and improvements.", font=("Helvetica", 12))
        release_notes_info.grid(row=9, column=0, sticky="w", padx=10, pady=5)

        # Add Security Guidelines and Best Practices
        security_guidelines_label = tk.Label(students_help_tab, text="Security Guidelines and Best Practices", font=("Helvetica", 12, "bold"))
        security_guidelines_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)

        security_info = tk.Label(students_help_tab, text="Learn about security best practices and guidelines to protect your account.", font=("Helvetica", 12))
        security_info.grid(row=11, column=0, sticky="w", padx=10, pady=5)

        # Add Glossary of Terms
        glossary_label = tk.Label(students_help_tab, text="Glossary of Terms", font=("Helvetica", 12, "bold"))
        glossary_label.grid(row=12, column=0, sticky="w", padx=10, pady=5)

        glossary_info = tk.Label(students_help_tab, text="Explore the glossary for definitions of common terms and concepts.", font=("Helvetica", 12))
        glossary_info.grid(row=13, column=0, sticky="w", padx=10, pady=5)

        # Add Community Forums and User Groups
        community_forums_label = tk.Label(students_help_tab, text="Community Forums and User Groups", font=("Helvetica", 12, "bold"))
        community_forums_label.grid(row=14, column=0, sticky="w", padx=10, pady=5)

        community_info = tk.Label(students_help_tab, text="Engage with the community, ask questions, and share insights on user forums.", font=("Helvetica", 12))
        community_info.grid(row=15, column=0, sticky="w", padx=10, pady=5)
    
    def add_exam_handler_tabs(self):
        # Add tabs for different functionalities
        self.exam_handlers_mark_exam_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exam_handlers_mark_exam_tab, text='Mark Exam')
        self.create_exam_handlers_mark_exam_widgets(self.exam_handlers_mark_exam_tab)

        self.exam_handlers_help_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exam_handlers_help_tab, text='Help')
        self.create_exam_handlers_help_widgets(self.exam_handlers_help_tab)
    
    def create_exam_handlers_mark_exam_widgets(self, exam_handlers_exam_tab):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        # exam handlers that have a finished exam that at least has one unmarked user exam
        cursor.execute("""SELECT DISTINCT handler_user_name
                        FROM Exam E
                        JOIN User_Exam UE ON E.exam_id = UE.exam_id
                        WHERE DATETIME('now', 'localtime') > DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')
                            AND E.exam_id IN (SELECT DISTINCT UE.exam_id
                                              FROM User_Exam UE
                                              WHERE UE.is_marked = 0)""")
        has_unmarked_exam_handlers = [x[0] for x in cursor.fetchall()]

        connection.close()

        if self.username not in has_unmarked_exam_handlers:
            self.no_unmarked_exam_handlers_label = tk.Label(exam_handlers_exam_tab, text="You have no unmarked exams", font=("Helvetica", 18, "bold"))
            self.no_unmarked_exam_handlers_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        else:
            # exam handler has a finnished but unmarked exam
            # Fetch data by querying the database
            path = '..\data\Exam_App.db'
            scriptdir = os.path.dirname(__file__)
            db_path = os.path.join(scriptdir, path)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            cursor.execute("""SELECT DISTINCT UE.exam_id
                        FROM User_Exam UE
                        JOIN Exam E ON E.exam_id = UE.exam_id
                        WHERE UE.is_marked = 0 AND E.handler_user_name = ? AND
                            DATETIME('now', 'localtime') > DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes') 
                        """, (self.username, ))
            handler_finished_umarked_exam_ids = [x[0] for x in cursor.fetchall()]

            cursor.execute("""SELECT DISTINCT UE.user_name
                            FROM User_Exam UE
                            JOIN Exam E ON E.exam_id = UE.exam_id
                            WHERE UE.is_marked = 0 AND E.handler_user_name = ? AND
                                DATETIME('now', 'localtime') > DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes') 
                            """, (self.username, ))
            handler_finished_umarked_exam_students = [x[0] for x in cursor.fetchall()]

            connection.close()

            # Create an upper frame for exam and student selection to mark
            self.exam_student_selection_frame = tk.LabelFrame(exam_handlers_exam_tab)
            self.exam_student_selection_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.NSEW)

            # Exam ID
            self.exam_id_label = tk.Label(self.exam_student_selection_frame, text="Exam ID:")
            self.exam_id_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

            self.exam_id_combo = ttk.Combobox(self.exam_student_selection_frame, width=5, values=handler_finished_umarked_exam_ids)
            self.exam_id_combo.grid(row=0, column=1, padx=2, pady=2)
            self.exam_id_combo.set(handler_finished_umarked_exam_ids[-1])

            # Exam student
            self.unmarked_exam_students_label = tk.Label(self.exam_student_selection_frame, text="Unmarked Exam Students:")
            self.unmarked_exam_students_label.grid(row=0, column=2, padx=(20, 0), pady=2, sticky=tk.W)

            self.unmarked_exam_students_combo = ttk.Combobox(self.exam_student_selection_frame, width=15, values=handler_finished_umarked_exam_students)
            self.unmarked_exam_students_combo.grid(row=0, column=3, padx=2, pady=2)
            self.unmarked_exam_students_combo.set(handler_finished_umarked_exam_students[0])

            # Create a frame for student exam mark stats
            self.student_exam_mark_stats_frame = tk.LabelFrame(exam_handlers_exam_tab, text="Student Exam Mark Stats")
            self.student_exam_mark_stats_frame.grid(row=1, column=0, padx=2, pady=2, sticky=tk.NSEW)

            # Labels and entry fields for mark student exam stats
            self.total_exam_questions_label = tk.Label(self.student_exam_mark_stats_frame, text="Total Exam Questions:", width=20, anchor=tk.W)
            self.total_exam_questions_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
            self.total_exam_questions_var = tk.StringVar(value="")
            self.total_exam_questions_value_label = tk.Label(self.student_exam_mark_stats_frame, textvariable=self.total_exam_questions_var, width=5, anchor=tk.W)
            self.total_exam_questions_value_label.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)

            self.total_marked_questions_label = tk.Label(self.student_exam_mark_stats_frame, text="Total Marked Questions:", width=20, anchor=tk.W)
            self.total_marked_questions_label.grid(row=0, column=2, padx=(20, 0), pady=2, sticky=tk.W)
            self.total_marked_questions_var = tk.StringVar(value="")
            self.total_marked_questions_value_label = tk.Label(self.student_exam_mark_stats_frame, textvariable=self.total_marked_questions_var, width=5, anchor=tk.W)
            self.total_marked_questions_value_label.grid(row=0, column=3, padx=2, pady=2, sticky=tk.W)

            self.score_label = tk.Label(self.student_exam_mark_stats_frame, text="Score:", width=20, anchor=tk.W)
            self.score_label.grid(row=0, column=4, padx=(20, 0), pady=2, sticky=tk.W)
            self.score_var = tk.StringVar(value="")
            self.score_value_label = tk.Label(self.student_exam_mark_stats_frame, textvariable=self.score_var, width=5, anchor=tk.W)
            self.score_value_label.grid(row=0, column=5, padx=2, pady=2, sticky=tk.W)

            self.correct_answers_label = tk.Label(self.student_exam_mark_stats_frame, text="Correct Answers:", width=20, anchor=tk.W)
            self.correct_answers_label.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
            self.correct_answers_var = tk.StringVar(value="")
            self.correct_answers_value_label = tk.Label(self.student_exam_mark_stats_frame, textvariable=self.correct_answers_var, width=5, anchor=tk.W)
            self.correct_answers_value_label.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)

            self.wrong_answers_label = tk.Label(self.student_exam_mark_stats_frame, text="Wrong Answers:", width=20, anchor=tk.W)
            self.wrong_answers_label.grid(row=1, column=2, padx=(20, 0), pady=2, sticky=tk.W)
            self.wrong_answers_var = tk.StringVar(value="")
            self.wrong_answers_value_label = tk.Label(self.student_exam_mark_stats_frame, textvariable=self.wrong_answers_var, width=5, anchor=tk.W)
            self.wrong_answers_value_label.grid(row=1, column=3, padx=2, pady=2, sticky=tk.W)

            self.unanswered_questions_label = tk.Label(self.student_exam_mark_stats_frame, text="Unanswered Questions:", width=20, anchor=tk.W)
            self.unanswered_questions_label.grid(row=1, column=4, padx=(20, 0), pady=2, sticky=tk.W)
            self.unanswered_questions_var = tk.StringVar(value="")
            self.unanswered_questions_value_label = tk.Label(self.student_exam_mark_stats_frame, textvariable=self.unanswered_questions_var, width=5, anchor=tk.W)
            self.unanswered_questions_value_label.grid(row=1, column=5, padx=2, pady=2, sticky=tk.W)

            self.is_passed_label = tk.Label(self.student_exam_mark_stats_frame, text="Is Passed:", width=20, anchor=tk.W)
            self.is_passed_label.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)
            self.is_passed_var = tk.StringVar(value="")
            self.is_passed_value_label = tk.Label(self.student_exam_mark_stats_frame, textvariable=self.is_passed_var, width=10, font=("Helvetica", 12, "bold"), anchor=tk.W)
            self.is_passed_value_label.grid(row=2, column=1, padx=(20, 0), pady=2, sticky=tk.W)

            # mark next button image 
            path = "..\images\\next.png"
            # get the path to the directory this script is in
            scriptdir = os.path.dirname(__file__)
            # add the relative path to the file from there
            image_path = os.path.join(scriptdir, path)
            # make sure the path exists and if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            self.mark_next_image = Image.open(image_path)
            self.mark_next_icon = ImageTk.PhotoImage(self.mark_next_image)

            self.start_mark_exam_button = tk.Button(self.student_exam_mark_stats_frame, text="Start Mark Exam", cursor="hand2", command=self.start_mark_exam)
            self.start_mark_exam_button.grid(row=2, column=2, padx=(20, 0), pady=2, sticky=tk.NSEW)
            
            self.mark_next_button = tk.Button(self.student_exam_mark_stats_frame, image=self.mark_next_icon, cursor="hand2", command=self.mark_next, width=20, height=20, anchor=tk.W)
            self.mark_next_button.grid(row=2, column=3, padx=2, pady=2, sticky=tk.W)
            self.mark_next_button.config(state=tk.DISABLED)

            self.submit_exam_mark_button = tk.Button(self.student_exam_mark_stats_frame, text="Submit Exam Mark", cursor="hand2", command=self.submit_exam_mark)
            self.submit_exam_mark_button.grid(row=2, column=4, padx=(20, 0), pady=2, sticky=tk.NSEW)
            self.submit_exam_mark_button.config(state=tk.DISABLED)

            # Create a frame for marking the discriptive/practical questions
            self.marking_frame = tk.LabelFrame(exam_handlers_exam_tab, text="Mark Questions")
            self.marking_frame.grid(row=2, column=0, padx=2, pady=2, sticky=tk.NSEW)

            self.marking_message_var = tk.StringVar(value="Start the exam marking process!")
            self.marking_message_label = tk.Label(self.marking_frame, textvariable=self.marking_message_var, fg="red", font=("Helvetica", 12, "bold"), anchor=tk.W)
            self.marking_message_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W, columnspan=3)

            # Create a frame for discriptive/practical question 
            self.question_frame = tk.LabelFrame(self.marking_frame, text="Question")
            self.question_frame.grid(row=1, column=0, padx=2, pady=2, sticky=tk.NSEW)

            # Question text area
            self.question_text_area = tk.Text(self.question_frame, width=40, height=20)
            self.question_text_area.grid(row=0, column=0, padx=2, pady=2, columnspan=4)
            self.question_text_area.config(state=tk.DISABLED)

            self.question_points_label = tk.Label(self.question_frame, text="Question Points:", anchor=tk.W)
            self.question_points_label.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
            self.question_points_var = tk.StringVar(value="")
            self.question_points_value_label = tk.Label(self.question_frame, textvariable=self.question_points_var, width=5, anchor=tk.W)
            self.question_points_value_label.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)

            # Create a frame for question answer 
            self.question_answer_frame = tk.LabelFrame(self.marking_frame, text="Question Answer")
            self.question_answer_frame.grid(row=1, column=1, padx=2, pady=2, sticky=tk.NSEW)

            # Question Answer text area
            self.question_answer_text_area = tk.Text(self.question_answer_frame, width=40, height=20)
            self.question_answer_text_area.grid(row=0, column=0, padx=2, pady=2)
            self.question_answer_text_area.config(state=tk.DISABLED)

            # Create a frame for student answer 
            self.student_answer_frame = tk.LabelFrame(self.marking_frame, text="Student Answer")
            self.student_answer_frame.grid(row=1, column=2, padx=2, pady=2, sticky=tk.NSEW)

            # Student Answer text area
            self.student_answer_text_area = tk.Text(self.student_answer_frame, width=40, height=20)
            self.student_answer_text_area.grid(row=0, column=0, padx=2, pady=2, columnspan=4)
            self.student_answer_text_area.config(state=tk.DISABLED)

            self.points_given_label = tk.Label(self.student_answer_frame, text="Points Given:", anchor=tk.W)
            self.points_given_label.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
            self.points_given_entry = tk.Entry(self.student_answer_frame, width=5)
            self.points_given_entry.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)
            self.points_given_entry.config(state=tk.DISABLED)
            
    def start_mark_exam(self):
        # disable the start_mark_exam button
        self.start_mark_exam_button.config(state=tk.DISABLED)

        # Validate fields
        exam_id = self.exam_id_combo.get()
        student_user_name = self.unmarked_exam_students_combo.get()
        
        if not (exam_id and student_user_name):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return

        # update exam marking message
        self.marking_message_var.set("Exam marking process started...")

        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT Q.question_id, Q.text, Q.type, Q.points
                    FROM Question Q
                    JOIN Exam_Question EQ ON EQ.question_id = Q.question_id 
                    JOIN Exam E ON E.exam_id = EQ.exam_id 
                    WHERE Q.type IN ('Multiple choice', 'True/False') AND E.exam_id = ?""", (exam_id, ))
        nondescriptive_question_data = cursor.fetchall()

        cursor.execute("""SELECT Q.question_id, Q.text, Q.type, Q.points
                    FROM Question Q
                    JOIN Exam_Question EQ ON EQ.question_id = Q.question_id 
                    JOIN Exam E ON E.exam_id = EQ.exam_id    
                    WHERE Q.type = 'Descriptive/Practical' AND E.exam_id = ?""", (exam_id, ))
        descriptive_question_data = cursor.fetchall()

        cursor.execute("""SELECT has_negative_score
                    FROM Exam  
                    WHERE exam_id = ?""", (exam_id, ))
        has_negative_score = int(cursor.fetchone()[0])

        cursor.execute("""SELECT passing_score
                    FROM Exam  
                    WHERE exam_id = ?""", (exam_id, ))
        passing_score = int(cursor.fetchone()[0])

        connection.close()

        # Initially set the exam mark stats
        self.total_exam_questions_var.set(str(len(nondescriptive_question_data) + len(descriptive_question_data)))
        self.total_marked_questions_var.set("0")
        self.score_var.set("0")
        self.correct_answers_var.set("0")
        self.wrong_answers_var.set("0")
        self.unanswered_questions_var.set("0")

        # Loop through all of the exam nondescriptive questions
        for idx, question in enumerate(nondescriptive_question_data, 1):
            # update exam marking message
            self.marking_message_var.set(f"Automarking nondescriptive questions [{idx}/{len(nondescriptive_question_data) + 1}]...")

            # disable the mark_next button
            self.mark_next_button.config(state=tk.DISABLED)
            # disable descriptive/practical question & answer related fields
            self.question_text_area.config(state=tk.DISABLED)
            self.question_answer_text_area.config(state=tk.DISABLED)
            self.student_answer_text_area.config(state=tk.DISABLED)
            self.question_points_var.set("")
            self.points_given_entry.delete(0, tk.END)
            self.points_given_entry.config(state=tk.DISABLED)

            # just mark it by comparing the option_id in the answer and is_correct answer
            # Fetch data by querying the database
            path = '..\data\Exam_App.db'
            scriptdir = os.path.dirname(__file__)
            db_path = os.path.join(scriptdir, path)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            cursor.execute("""SELECT option_id
                        FROM Answer   
                        WHERE exam_id = ? AND user_name = ? AND question_id = ?""", (exam_id, student_user_name, question[0]))
            student_answer_option_id = cursor.fetchone()

            cursor.execute("""SELECT option_id
                        FROM Option   
                        WHERE question_id = ? AND is_correct_answer = 1""", (question[0], ))
            question_answer_option_id = cursor.fetchone()

            connection.close()
            # mark exam question
            if student_answer_option_id == question_answer_option_id:
                # the answer is correct so give its points and include it in correct answers
                self.total_marked_questions_var.set(str(int(self.total_marked_questions_var.get()) + 1))
                self.score_var.set(str(int(self.score_var.get()) + question[3]))
                self.correct_answers_var.set(str(int(self.correct_answers_var.get()) + 1))
            elif not student_answer_option_id:
                # the answer is none (the student did't answered this question)
                self.total_marked_questions_var.set(str(int(self.total_marked_questions_var.get()) + 1))
                self.unanswered_questions_var.set(str(int(self.unanswered_questions_var.get()) + 1))
            else:
                # the answer is wrong so give its points and include it in wrong answers
                self.total_marked_questions_var.set(str(int(self.total_marked_questions_var.get()) + 1))
                self.wrong_answers_var.set(str(int(self.wrong_answers_var.get()) + 1))
                if has_negative_score == 1:
                    # if the exam has negative score the wrong answer descreses 1/3 of the point of the question
                    self.score_var.set(str(int(self.score_var.get()) - int(question[3]/3)))
            # loops until all of the nondescriptive questions are marked....
            # update exam marking message and is_passed
            self.is_passed_var.set("Passed" if int(self.score_var.get()) >= passing_score else "Failed")
            self.marking_message_var.set(f"Automarking nondescriptive questions finished successfully.")
            
            # if there is a descriptive question in the exam
            if descriptive_question_data:
                # update exam marking message
                if len(descriptive_question_data) == 1:
                    self.marking_message_var.set(f"Manual marking descriptive question...")
                else:
                    self.marking_message_var.set(f"Manual marking descriptive questions [1/{len(descriptive_question_data) + 1}]...")

                # define a variable to keep track of the descriptive being marked
                self.current_descriptive_question = 0 # initialize with first descriptive question

                # enable the mark_next button
                self.mark_next_button.config(state=tk.NORMAL)

                # Fetch data by querying the database
                path = '..\data\Exam_App.db'
                scriptdir = os.path.dirname(__file__)
                db_path = os.path.join(scriptdir, path)
                os.makedirs(os.path.dirname(db_path), exist_ok=True)

                connection = sqlite3.connect(db_path)
                cursor = connection.cursor()

                cursor.execute("""SELECT answer_text
                            FROM Answer   
                            WHERE exam_id = ? AND user_name = ? AND question_id = ?""", (exam_id, student_user_name, descriptive_question_data[0][0]))
                student_answer_text = cursor.fetchone()

                cursor.execute("""SELECT text
                            FROM Option   
                            WHERE question_id = ? AND is_correct_answer = 1""", (descriptive_question_data[0][0], ))
                question_answer_text = cursor.fetchone()

                connection.close()
                # enable descriptive/practical question & answer related fields
                self.question_text_area.config(state=tk.NORMAL)
                self.question_answer_text_area.config(state=tk.NORMAL)
                self.student_answer_text_area.config(state=tk.NORMAL)
                self.points_given_entry.delete(0, tk.END)
                self.points_given_entry.config(state=tk.NORMAL)

                # then load the question and its correct answer and the student answer
                self.question_text_area.delete("1.0", tk.END)
                self.question_text_area.insert(tk.END, descriptive_question_data[0][1])
                self.question_text_area.config(state=tk.DISABLED)
                                               
                self.question_answer_text_area.delete("1.0", tk.END)
                self.question_answer_text_area.insert(tk.END, question_answer_text)
                self.question_answer_text_area.config(state=tk.DISABLED)                            

                self.student_answer_text_area.delete("1.0", tk.END)
                self.student_answer_text_area.insert(tk.END, student_answer_text)
                self.student_answer_text_area.config(state=tk.DISABLED) 

                # set the points given to 0 if the student answer is empty/none
                if not self.student_answer_text_area.get("1.0", tk.END).strip():
                    self.points_given_entry.delete(0, tk.END)
                    self.points_given_entry.insert(tk.END, "0")
                
                # load the question points
                self.question_points_var.set(str(descriptive_question_data[0][3]))                          
                # ... then the handler give some points to this question and clicks mark next...
            else:
                # there is no descriptive questions so the marking process is finished and only need to be submitted
                # update exam marking message
                self.marking_message_var.set(f"Exam mark stats are ready to be submitted...")
                #enable submit exam mark button
                self.submit_exam_mark_button.config(state=tk.NORMAL)
        
    def mark_next(self):
        exam_id = self.exam_id_combo.get()
        student_user_name = self.unmarked_exam_students_combo.get()

        # validate fields
        if not (exam_id and student_user_name and self.points_given_entry.get()):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT passing_score
                    FROM Exam  
                    WHERE exam_id = ?""", (exam_id, ))
        passing_score = int(cursor.fetchone()[0])

        cursor.execute("""SELECT Q.question_id, Q.text, Q.type, Q.points
                    FROM Question Q
                    JOIN Exam_Question EQ ON EQ.question_id = Q.question_id 
                    JOIN Exam E ON E.exam_id = EQ.exam_id    
                    WHERE Q.type = 'Descriptive/Practical' AND E.exam_id = ?""", (exam_id, ))
        descriptive_question_data = cursor.fetchall()

        connection.close()
        
        student_answer = self.student_answer_text_area.get("1.0", tk.END).strip()
        
        # apply the previous marked question to exam mark stats
        if student_answer:
            # the student answered the question
            self.total_marked_questions_var.set(str(int(self.total_marked_questions_var.get()) + 1))
            self.score_var.set(str(int(self.score_var.get()) + int(self.points_given_entry.get())))
            
            if int(self.points_given_entry.get()) >= 0.5 * int(self.question_points_var.get()):
                # the student earned >= 50% of the question points so include it in correct answers
                self.correct_answers_var.set(str(int(self.correct_answers_var.get()) + 1))
            else:
                # the student earned < 50% of the question points so include it in wrong answers
                self.wrong_answers_var.set(str(int(self.wrong_answers_var.get()) + 1))
        else:
            # the answer is none (the student did't answered this question)
            self.total_marked_questions_var.set(str(int(self.total_marked_questions_var.get()) + 1))
            self.unanswered_questions_var.set(str(int(self.unanswered_questions_var.get()) + 1))
        
        # is_passed
        self.is_passed_var.set("Passed" if int(self.score_var.get()) >= passing_score else "Failed")

        # iterate current_descriptive_question
        self.current_descriptive_question += 1

        # check if there is any other descriptive question
        if self.current_descriptive_question <= len(descriptive_question_data) - 1:
            # there still exists some more descriptive questions to mark
            # update exam marking message
            self.marking_message_var.set(f"Manual marking descriptive questions [{self.current_descriptive_question + 1}/{len(descriptive_question_data) + 1}]...")
            # load the next question to mark

            # enable the mark_next button
            self.mark_next_button.config(state=tk.NORMAL)

            # Fetch data by querying the database
            path = '..\data\Exam_App.db'
            scriptdir = os.path.dirname(__file__)
            db_path = os.path.join(scriptdir, path)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            cursor.execute("""SELECT answer_text
                        FROM Answer   
                        WHERE exam_id = ? AND user_name = ? AND question_id = ?""", (exam_id, student_user_name, descriptive_question_data[self.current_descriptive_question][0]))
            student_answer_text = cursor.fetchone()

            cursor.execute("""SELECT text
                        FROM Option   
                        WHERE question_id = ? AND is_correct_answer = 1""", (descriptive_question_data[self.current_descriptive_question][0], ))
            question_answer_text = cursor.fetchone()

            connection.close()
            # enable descriptive/practical question & answer related fields
            self.question_text_area.config(state=tk.NORMAL)
            self.question_answer_text_area.config(state=tk.NORMAL)
            self.student_answer_text_area.config(state=tk.NORMAL)
            self.points_given_entry.config(state=tk.NORMAL)
            self.points_given_entry.delete(0, tk.END)

            # then load the question and its correct answer and the student answer
            self.question_text_area.delete("1.0", tk.END)
            self.question_text_area.insert(tk.END, descriptive_question_data[self.current_descriptive_question][1])
            self.question_text_area.config(state=tk.DISABLED)
                                            
            self.question_answer_text_area.delete("1.0", tk.END)
            self.question_answer_text_area.insert(tk.END, question_answer_text)
            self.question_answer_text_area.config(state=tk.DISABLED)                            

            self.student_answer_text_area.delete("1.0", tk.END)
            self.student_answer_text_area.insert(tk.END, student_answer_text)
            self.student_answer_text_area.config(state=tk.DISABLED) 

            # set the points given to 0 if the student answer is empty/none
            if not self.student_answer_text_area.get("1.0", tk.END).strip():
                self.points_given_entry.delete(0, tk.END)
                self.points_given_entry.insert(tk.END, "0")
            
            # load the question points
            self.question_points_var.set(str(descriptive_question_data[self.current_descriptive_question][3]))                          
            # ... then the handler give some points to this question and clicks mark next...
        else:
            # all of the descriptive questions were marked and we're ready to submit exam stats
            # update exam marking message
            self.marking_message_var.set(f"Exam mark stats are ready to be submitted...")
            #enable submit exam mark button
            self.submit_exam_mark_button.config(state=tk.NORMAL)
            #disable mark_next button
            self.mark_next_button.config(state=tk.DISABLED)

    def submit_exam_mark(self):
        exam_id = self.exam_id_combo.get()
        student_user_name = self.unmarked_exam_students_combo.get()
        score = int(self.score_var.get()) if self.score_var.get() else None
        total_questions = int(self.total_exam_questions_var.get()) if self.total_exam_questions_var.get() else None
        correct_answers = int(self.correct_answers_var.get()) if self.correct_answers_var.get() else None
        wrong_answers = int(self.wrong_answers_var.get()) if self.wrong_answers_var.get() else None
        unanswered_questions = int(self.unanswered_questions_var.get()) if self.unanswered_questions_var.get() else None
        is_passed = 1 if self.is_passed_var.get().strip() == "Passed" else 0
        is_marked = 1

        # validate fields
        if not (exam_id != None and student_user_name != None and score != None and total_questions != None 
                and correct_answers != None and wrong_answers != None and unanswered_questions != None and is_passed != None):
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return
        
        # Call insert_feedback function from db1.py
        exam_mark_submit_msg = update_user_exam(exam_id, student_user_name, score, total_questions, correct_answers, \
                                                wrong_answers, unanswered_questions, is_passed, is_marked)
        messagebox.showinfo("Exam Mark Submit", exam_mark_submit_msg)

        # reset exam mark stats, question and answer fields
        self.reset_exam_mark()

        # update students combolist values (remove this student)
        self.update_unmarked_students()

    def reset_exam_mark(self):
        # reset exam mark stats values
        self.total_exam_questions_var.set("")
        self.total_marked_questions_var.set("")
        self.score_var.set("")
        self.correct_answers_var.set("")
        self.wrong_answers_var.set("")
        self.unanswered_questions_var.set("")
        self.is_passed_var.set("")

        # disable/enable widgets and clear them
        self.start_mark_exam_button.config(state=tk.NORMAL)
        self.mark_next_button.config(state=tk.DISABLED)
        self.submit_exam_mark_button.config(state=tk.DISABLED)

        self.question_text_area.config(state=tk.NORMAL)
        self.question_answer_text_area.config(state=tk.NORMAL)
        self.student_answer_text_area.config(state=tk.NORMAL)
        self.points_given_entry.config(state=tk.NORMAL)
        self.points_given_entry.delete(0, tk.END)
        self.points_given_entry.config(state=tk.DISABLED)

        self.question_text_area.delete("1.0", tk.END)
        self.question_answer_text_area.delete("1.0", tk.END)
        self.student_answer_text_area.delete("1.0", tk.END)
        self.question_text_area.config(state=tk.DISABLED)
        self.question_answer_text_area.config(state=tk.DISABLED)
        self.student_answer_text_area.config(state=tk.DISABLED)
        self.question_points_var.set("") 
        
    def update_unmarked_students(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""SELECT DISTINCT UE.user_name
                            FROM User_Exam UE
                            JOIN Exam E ON E.exam_id = UE.exam_id
                            WHERE UE.is_marked = 0 AND E.handler_user_name = ? AND
                                DATETIME('now', 'localtime') > DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes') 
                            """, (self.username, ))
        handler_finished_umarked_exam_students = [x[0] for x in cursor.fetchall()]

        connection.close()

        # update combolist values
        self.unmarked_exam_students_combo['values'] = handler_finished_umarked_exam_students
        self.unmarked_exam_students_combo.set(handler_finished_umarked_exam_students[0])

        # if all of the students aexams are marked(no students left) message handler
        if not handler_finished_umarked_exam_students:
            messagebox.showinfo("Exam Mark Finish", "Exam marked completely and successfully. Nice job!")

    def create_exam_handlers_help_widgets(self, exam_handlers_help_tab):
        # Add User Manuals and Documentation
        user_manual_label = tk.Label(exam_handlers_help_tab, text="User Manuals and Documentation", font=("Helvetica", 12, "bold"))
        user_manual_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        user_manual_info = tk.Label(exam_handlers_help_tab, text="Access user manuals and system documentation for detailed instructions.", font=("Helvetica", 12))
        user_manual_info.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Add Frequently Asked Questions (FAQs)
        faq_label = tk.Label(exam_handlers_help_tab, text="Frequently Asked Questions (FAQs)", font=("Helvetica", 12, "bold"))
        faq_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        faq_info = tk.Label(exam_handlers_help_tab, text="Find answers to common questions about system usage, troubleshooting, and more.", font=("Helvetica", 12))
        faq_info.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Add Contact Information and Support Channels
        contact_info_label = tk.Label(exam_handlers_help_tab, text="Contact Information and Support Channels", font=("Helvetica", 12, "bold"))
        contact_info_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        contact_info = tk.Label(exam_handlers_help_tab, text="Reach out to our support team via email, phone, or live chat for assistance.", font=("Helvetica", 12))
        contact_info.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # Add Video Tutorials and Demos
        video_tutorials_label = tk.Label(exam_handlers_help_tab, text="Video Tutorials and Demos", font=("Helvetica", 12, "bold"))
        video_tutorials_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        video_tutorials_info = tk.Label(exam_handlers_help_tab, text="Watch video tutorials and demos to learn how to use key features.", font=("Helvetica", 12))
        video_tutorials_info.grid(row=7, column=0, sticky="w", padx=10, pady=5)

        # Add Release Notes and Updates
        release_notes_label = tk.Label(exam_handlers_help_tab, text="Release Notes and Updates", font=("Helvetica", 12, "bold"))
        release_notes_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)

        release_notes_info = tk.Label(exam_handlers_help_tab, text="Stay updated on the latest system releases, updates, and improvements.", font=("Helvetica", 12))
        release_notes_info.grid(row=9, column=0, sticky="w", padx=10, pady=5)

        # Add Security Guidelines and Best Practices
        security_guidelines_label = tk.Label(exam_handlers_help_tab, text="Security Guidelines and Best Practices", font=("Helvetica", 12, "bold"))
        security_guidelines_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)

        security_info = tk.Label(exam_handlers_help_tab, text="Learn about security best practices and guidelines to protect your account.", font=("Helvetica", 12))
        security_info.grid(row=11, column=0, sticky="w", padx=10, pady=5)

        # Add Glossary of Terms
        glossary_label = tk.Label(exam_handlers_help_tab, text="Glossary of Terms", font=("Helvetica", 12, "bold"))
        glossary_label.grid(row=12, column=0, sticky="w", padx=10, pady=5)

        glossary_info = tk.Label(exam_handlers_help_tab, text="Explore the glossary for definitions of common terms and concepts.", font=("Helvetica", 12))
        glossary_info.grid(row=13, column=0, sticky="w", padx=10, pady=5)

        # Add Community Forums and User Groups
        community_forums_label = tk.Label(exam_handlers_help_tab, text="Community Forums and User Groups", font=("Helvetica", 12, "bold"))
        community_forums_label.grid(row=14, column=0, sticky="w", padx=10, pady=5)

        community_info = tk.Label(exam_handlers_help_tab, text="Engage with the community, ask questions, and share insights on user forums.", font=("Helvetica", 12))
        community_info.grid(row=15, column=0, sticky="w", padx=10, pady=5)

    def add_exam_supervisor_tabs(self):
        # Add tabs for different functionalities
        self.exam_supervisor_feedbacks_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exam_supervisor_feedbacks_tab, text='Feedbacks')
        self.create_exam_supervisor_feedbacks_widgets(self.exam_supervisor_feedbacks_tab)
        # Bind the load_supervisor_exams_feedbacks method to the event of opening the tab
        self.exam_supervisor_feedbacks_tab.bind("<Visibility>", self.supervisor_exams_feedbacks_on_tab_opened)

        self.exam_supervisor_help_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.exam_supervisor_help_tab, text='Help')
        self.create_exam_supervisor_help_widgets(self.exam_supervisor_help_tab)

    def create_exam_supervisor_feedbacks_widgets(self, exam_supervisor_feedbacks_tab):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        # exam supervisors that have a finished exam
        cursor.execute("""SELECT DISTINCT supervisor_user_name
                        FROM Exam
                        WHERE DATETIME('now', 'localtime') > DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes')""")
        finished_exam_supervisors = [x[0] for x in cursor.fetchall()]

        connection.close()

        if self.username not in finished_exam_supervisors:
            self.no_finished_exam_supervisors_label = tk.Label(exam_supervisor_feedbacks_tab, text="You have no finished exams", font=("Helvetica", 18, "bold"))
            self.no_finished_exam_supervisors_label.grid(row=0, column=0, sticky="w", padx=5, pady=10)
        
        else:
            # exam supervisor has a finnished
            # Fetch data by querying the database
            path = '..\data\Exam_App.db'
            scriptdir = os.path.dirname(__file__)
            db_path = os.path.join(scriptdir, path)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()

            cursor.execute("""SELECT exam_id
                        FROM Exam
                        WHERE DATETIME('now', 'localtime') > DATETIME(REPLACE(exam_date, '/', '-') || ' ' || start_time, '+' || duration || ' minutes')
                             AND supervisor_user_name = ?""", (self.username, ))
            supervisor_finished_exam_ids = [x[0] for x in cursor.fetchall()]

            connection.close()

            # Create an upper frame for feedback info
            self.upper_feedback_frame = tk.Frame(exam_supervisor_feedbacks_tab)
            self.upper_feedback_frame.grid(row=0, column=0, padx=5, pady=2, sticky=tk.NSEW)

            # Exam ID
            self.exam_id_label = tk.Label(self.upper_feedback_frame, text="Exam ID:")
            self.exam_id_label.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
            self.exam_id_combo = ttk.Combobox(self.upper_feedback_frame, width=5, values=supervisor_finished_exam_ids)
            self.exam_id_combo.grid(row=0, column=1, padx=2, pady=2)
            self.exam_id_combo.set(supervisor_finished_exam_ids[-1])

            # User name
            self.user_name_label = tk.Label(self.upper_feedback_frame, text="User Name:")
            self.user_name_label.grid(row=0, column=2, padx=(20,0), pady=2, sticky=tk.W)
            self.user_name_entry = tk.Entry(self.upper_feedback_frame, width=10)
            self.user_name_entry.grid(row=0, column=3, padx=2, pady=2)
            self.user_name_entry.config(state=tk.DISABLED)

            # feedback type
            self.feedback_type_label = tk.Label(self.upper_feedback_frame, text="Feedback Type:")
            self.feedback_type_label.grid(row=0, column=4, padx=(20,0), pady=2, sticky=tk.W)
            self.feedback_type_combo = ttk.Combobox(self.upper_feedback_frame, values=('Suggestion for improvement', 'Comment on clarity, and difficulty levels'), width=35)
            self.feedback_type_combo.grid(row=0, column=5, padx=2, pady=2)
            self.feedback_type_combo.config(state=tk.DISABLED)

            # Question ID
            self.question_id_label = tk.Label(self.upper_feedback_frame, text="Question ID:")
            self.question_id_label.grid(row=0, column=6, padx=(20,0), pady=2, sticky=tk.W)
            self.question_id_entry = tk.Entry(self.upper_feedback_frame, width=5)
            self.question_id_entry.grid(row=0, column=7, padx=2, pady=2)
            self.question_id_entry.config(state=tk.DISABLED)

            # rating
            self.feedback_rating_label = tk.Label(self.upper_feedback_frame, text="Rating:")
            self.feedback_rating_label.grid(row=0, column=8, padx=(20,0), pady=2, sticky=tk.W)
            self.feedback_rating_combo = ttk.Combobox(self.upper_feedback_frame, values=list(range(1,11)), width=10)
            self.feedback_rating_combo.grid(row=0, column=9, padx=2, pady=2)
            self.feedback_rating_combo.config(state=tk.DISABLED)

            # Add radio buttons for feedback visibility
            self.feedback_visibility_var = tk.StringVar()
            self.feedback_visibility_var.set("Visible")  # Default selection

            self.visible_radio = tk.Radiobutton(self.upper_feedback_frame, text="Visible", variable=self.feedback_visibility_var, value="Visible")
            self.visible_radio.grid(row=0, column=10, padx=(20,0), pady=2)
            self.visible_radio.config(state=tk.DISABLED)

            self.invisible_radio = tk.Radiobutton(self.upper_feedback_frame, text="Invisible", variable=self.feedback_visibility_var, value="Invisible")
            self.invisible_radio.grid(row=0, column=11, padx=2, pady=2)
            self.visible_radio.config(state=tk.DISABLED)

            # Update feedback button
            self.read_feedback_button = tk.Button(self.upper_feedback_frame, text="Read Feedback", cursor="hand2", command=self.read_feedback)
            self.read_feedback_button.grid(row=0, column=12, padx=(20,0), pady=2)

            # Create a lower frame for feedback info
            self.lower_feedback_frame = tk.Frame(exam_supervisor_feedbacks_tab)
            self.lower_feedback_frame.grid(row=1, column=0, padx=5, pady=2, sticky=tk.NSEW)

            # feedback text area
            self.feedback_text_area = tk.Text(self.lower_feedback_frame, width=200, height=20)
            self.feedback_text_area.grid(row=0, column=0, padx=2, pady=2)
            self.feedback_text_area.config(state=tk.DISABLED)

            # supervisor exams feedbacks table frame
            self.supervisor_exams_feedbacks_table_frame = tk.Label(exam_supervisor_feedbacks_tab)
            self.supervisor_exams_feedbacks_table_frame.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

            # Create the table containing the supervisor exams feedbacks
            columns = ("exam_id", "user_name", "feedback_type", "text", "question_id", "rating", "status", "is_visible")
            self.supervisor_exams_feedbacks_table = ttk.Treeview(self.supervisor_exams_feedbacks_table_frame, column=columns, show='headings', selectmode="browse", height=20)
            self.supervisor_exams_feedbacks_table.heading("#1", text="exam_id",anchor=tk.W)
            self.supervisor_exams_feedbacks_table.column("#1", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
            self.supervisor_exams_feedbacks_table.heading("#2", text="user_name",anchor=tk.W)
            self.supervisor_exams_feedbacks_table.column("#2", stretch=tk.NO, width = 110, minwidth=100, anchor=tk.W)
            self.supervisor_exams_feedbacks_table.heading("#3", text="feedback_type",anchor=tk.W)
            self.supervisor_exams_feedbacks_table.column("#3", stretch=tk.NO, width = 200, minwidth=100, anchor=tk.W)
            self.supervisor_exams_feedbacks_table.heading("#4", text="text",anchor=tk.W)
            self.supervisor_exams_feedbacks_table.column("#4", stretch=tk.NO, width = 400, minwidth=200, anchor=tk.W)
            self.supervisor_exams_feedbacks_table.heading("#5", text="question_id",anchor=tk.W)
            self.supervisor_exams_feedbacks_table.column("#5", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
            self.supervisor_exams_feedbacks_table.heading("#6", text="rating",anchor=tk.W)
            self.supervisor_exams_feedbacks_table.column("#6", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
            self.supervisor_exams_feedbacks_table.heading("#7", text="status",anchor=tk.W)
            self.supervisor_exams_feedbacks_table.column("#7", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
            self.supervisor_exams_feedbacks_table.heading("#8", text="is_visible",anchor=tk.W)
            self.supervisor_exams_feedbacks_table.column("#8", stretch=tk.NO, width = 80, minwidth=50, anchor=tk.W)
            
            self.supervisor_exams_feedbacks_table.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

            self.supervisor_exams_feedbacks_table_y_scrollbar = ttk.Scrollbar(self.supervisor_exams_feedbacks_table_frame, orient="vertical", command=self.supervisor_exams_feedbacks_table.yview)
            self.supervisor_exams_feedbacks_table_y_scrollbar.grid(row=0, column=1, sticky="ns")
            
            self.supervisor_exams_feedbacks_table.configure(yscrollcommand=self.supervisor_exams_feedbacks_table_y_scrollbar.set)

            # Bind the function to the Treeview's selection event
            self.supervisor_exams_feedbacks_table.bind('<<TreeviewSelect>>', self.supervisor_exams_feedbacks_on_treeview_select)

            s = ttk.Style(self.supervisor_exams_feedbacks_table)
            s.theme_use("winnative")
            s.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

            # load the supervisor exams feedbacks table data
            self.load_supervisor_exams_feedbacks()

    def read_feedback(self):
        exam_id = self.exam_id_combo.get()
        user_name = self.user_name_entry.get()

        # Validate fields
        if not exam_id:
            messagebox.showwarning("Incomplete Information", "Please fill all required fields.")
            return

        # Call read_feedback function from db1.py
        feedback_read_msg = read_feedbacks(exam_id, user_name)
        messagebox.showinfo("Feedback Read", feedback_read_msg)
        
        # Reset/clear fields
        self.reset_supervisor_exams_feedback()
        # reload the upervisor exams feedbacks table data
        self.load_supervisor_exams_feedbacks()

    def load_supervisor_exams_feedbacks(self):
        # Fetch data by querying the database
        path = '..\data\Exam_App.db'
        scriptdir = os.path.dirname(__file__)
        db_path = os.path.join(scriptdir, path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # retrieve all of the feedbacks on the finished exams that this username was in
        # (only visible feedbacks from other users but all the feedbacks from this user)
        cursor.execute("""SELECT F.exam_id, F.user_name, F.feedback_type, F.text, F.question_id, F.rating, F.status, F.is_visible
                        FROM Feedback F
                        JOIN Exam E ON E.exam_id = F.exam_id
                        WHERE E.supervisor_user_name = ? AND
                            DATETIME('now', 'localtime') > DATETIME(REPLACE(E.exam_date, '/', '-') || ' ' || E.start_time, '+' || E.duration || ' minutes')""", (self.username, ))
        data = cursor.fetchall()

        connection.close()

        # Clear treeview (feedbacks_table) data
        self.supervisor_exams_feedbacks_table.delete(*self.supervisor_exams_feedbacks_table.get_children())
        # Insert data rows
        for row in data:
            self.supervisor_exams_feedbacks_table.insert("", "end", values=row)
    
    def supervisor_exams_feedbacks_on_tab_opened(self, event):
        #load the supervisor exam feedbacks
        self.load_supervisor_exams_feedbacks()
    
    def reset_supervisor_exams_feedback(self):
        # activate fields to set their values
        self.exam_id_combo.config(state=tk.NORMAL)
        self.user_name_entry.config(state=tk.NORMAL)
        self.feedback_type_combo.config(state=tk.NORMAL)
        self.question_id_entry.config(state=tk.NORMAL)
        self.feedback_rating_combo.config(state=tk.NORMAL)
        self.visible_radio.config(state=tk.NORMAL)
        self.visible_radio.config(state=tk.NORMAL)
        self.feedback_text_area.config(state=tk.NORMAL)
        self.read_feedback_button.config(state=tk.NORMAL)

        # Clear user name field
        self.user_name_entry.delete(0, tk.END)
        # Clear Question ID field
        self.question_id_entry.delete(0, tk.END)
        # Reset feedback visibility
        self.feedback_visibility_var.set("Visible")
        # Clear feedback Text Area
        self.feedback_text_area.delete("1.0", tk.END)
    
    def supervisor_exams_feedbacks_on_treeview_select(self, event):
        # Reset fields
        self.reset_supervisor_exams_feedback()
        
        # Get the selected item
        selected_item = self.supervisor_exams_feedbacks_table.selection()
        
        if selected_item:
            # Get the values of the selected item
            values = self.supervisor_exams_feedbacks_table.item(selected_item, 'values')

            # Replace None values with empty strings
            values = ["" if value is None else value for value in values]

            # activate fields to set their values
            self.exam_id_combo.config(state=tk.NORMAL)
            self.user_name_entry.config(state=tk.NORMAL)
            self.feedback_type_combo.config(state=tk.NORMAL)
            self.question_id_entry.config(state=tk.NORMAL)
            self.feedback_rating_combo.config(state=tk.NORMAL)
            self.visible_radio.config(state=tk.NORMAL)
            self.invisible_radio.config(state=tk.NORMAL)
            self.feedback_text_area.config(state=tk.NORMAL)

            # Set the values of the feedback-related fields
            self.exam_id_combo.set(values[0])
            self.user_name_entry.delete(0, tk.END)
            self.user_name_entry.insert(tk.END, values[1])
            self.feedback_type_combo.set(values[2])
            self.feedback_text_area.delete("1.0", tk.END)
            self.feedback_text_area.insert(tk.END, values[3])
            self.question_id_entry.delete(0, tk.END)
            self.question_id_entry.insert(tk.END, values[4])
            self.feedback_rating_combo.set(int(values[5]))
            self.feedback_visibility_var.set("Visible" if int(values[7]) == 1 else "Invisible")
            
            # disable fields
            self.exam_id_combo.config(state=tk.DISABLED)
            self.user_name_entry.config(state=tk.DISABLED)
            self.feedback_type_combo.config(state=tk.DISABLED)
            self.question_id_entry.config(state=tk.DISABLED)
            self.feedback_rating_combo.config(state=tk.DISABLED)
            self.visible_radio.config(state=tk.DISABLED)
            self.invisible_radio.config(state=tk.DISABLED)
            self.feedback_text_area.config(state=tk.DISABLED)

    def create_exam_supervisor_help_widgets(self, exam_supervisor_help_tab):
        # Add User Manuals and Documentation
        user_manual_label = tk.Label(exam_supervisor_help_tab, text="User Manuals and Documentation", font=("Helvetica", 12, "bold"))
        user_manual_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        user_manual_info = tk.Label(exam_supervisor_help_tab, text="Access user manuals and system documentation for detailed instructions.", font=("Helvetica", 12))
        user_manual_info.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Add Frequently Asked Questions (FAQs)
        faq_label = tk.Label(exam_supervisor_help_tab, text="Frequently Asked Questions (FAQs)", font=("Helvetica", 12, "bold"))
        faq_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        faq_info = tk.Label(exam_supervisor_help_tab, text="Find answers to common questions about system usage, troubleshooting, and more.", font=("Helvetica", 12))
        faq_info.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Add Contact Information and Support Channels
        contact_info_label = tk.Label(exam_supervisor_help_tab, text="Contact Information and Support Channels", font=("Helvetica", 12, "bold"))
        contact_info_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        contact_info = tk.Label(exam_supervisor_help_tab, text="Reach out to our support team via email, phone, or live chat for assistance.", font=("Helvetica", 12))
        contact_info.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # Add Video Tutorials and Demos
        video_tutorials_label = tk.Label(exam_supervisor_help_tab, text="Video Tutorials and Demos", font=("Helvetica", 12, "bold"))
        video_tutorials_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

        video_tutorials_info = tk.Label(exam_supervisor_help_tab, text="Watch video tutorials and demos to learn how to use key features.", font=("Helvetica", 12))
        video_tutorials_info.grid(row=7, column=0, sticky="w", padx=10, pady=5)

        # Add Release Notes and Updates
        release_notes_label = tk.Label(exam_supervisor_help_tab, text="Release Notes and Updates", font=("Helvetica", 12, "bold"))
        release_notes_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)

        release_notes_info = tk.Label(exam_supervisor_help_tab, text="Stay updated on the latest system releases, updates, and improvements.", font=("Helvetica", 12))
        release_notes_info.grid(row=9, column=0, sticky="w", padx=10, pady=5)

        # Add Security Guidelines and Best Practices
        security_guidelines_label = tk.Label(exam_supervisor_help_tab, text="Security Guidelines and Best Practices", font=("Helvetica", 12, "bold"))
        security_guidelines_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)

        security_info = tk.Label(exam_supervisor_help_tab, text="Learn about security best practices and guidelines to protect your account.", font=("Helvetica", 12))
        security_info.grid(row=11, column=0, sticky="w", padx=10, pady=5)

        # Add Glossary of Terms
        glossary_label = tk.Label(exam_supervisor_help_tab, text="Glossary of Terms", font=("Helvetica", 12, "bold"))
        glossary_label.grid(row=12, column=0, sticky="w", padx=10, pady=5)

        glossary_info = tk.Label(exam_supervisor_help_tab, text="Explore the glossary for definitions of common terms and concepts.", font=("Helvetica", 12))
        glossary_info.grid(row=13, column=0, sticky="w", padx=10, pady=5)

        # Add Community Forums and User Groups
        community_forums_label = tk.Label(exam_supervisor_help_tab, text="Community Forums and User Groups", font=("Helvetica", 12, "bold"))
        community_forums_label.grid(row=14, column=0, sticky="w", padx=10, pady=5)

        community_info = tk.Label(exam_supervisor_help_tab, text="Engage with the community, ask questions, and share insights on user forums.", font=("Helvetica", 12))
        community_info.grid(row=15, column=0, sticky="w", padx=10, pady=5)










# Main loop
if __name__ == "__main__":
    admin_session = LoginPage()
    admin_session.mainloop()

    # student_session = LoginPage()
    # student_session.mainloop()