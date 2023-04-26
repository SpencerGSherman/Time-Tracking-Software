'''
Defined library imports necessary for program functionality (primarily using the PyQt6 Gui framework utilities).
'''
import sys
import sqlite3
from datetime import timedelta

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QInputDialog, QListWidget, QListWidgetItem, QStackedWidget, QCalendarWidget, QDialog, QDialogButtonBox, QMessageBox, \
    QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon

'''
Database table configuration handles and maintains user information. Table records are initialized here
for the user, and a foreign key id will link created accounts to both the user_settings and task_list table.
The format here is using sqlite3 and a local db file which is targeted and interacted with throughout execution.
'''
def create_database_and_tables(database):
    conn = sqlite3.connect(database)

    # Using an SQL query, the code below creates a table named
    # 'user settings' with user_id as the primary key, and the foreign
    # key for the other table created named 'users'
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            show_calendar INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        """
    )

    # Using an SQL query, the code below creates a table named
    # 'task_list' and its attributes are task_id(INTEGER), user_id
    # (INTEGER), task_name(TEXT), total_time(INTEGER set to 0 by default),
    # and task_description(TEXT)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS task_list (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_name TEXT NOT NULL,
            total_time INTEGER DEFAULT 0,
            task_description TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
        """
    )

    # Using an SQL query, the code below creates a table named 'users'
    # with the attributes user_id(INTEGER), username(TEXT) and password(TEXT)
    # The user_id is a foreign key
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
    )
    #confirms changes made to the database
    conn.commit()
    conn.close()

'''
This module houses the login page widget which will provide an interface for
the user to interact with their associated username/password. There is also a
connection created to transition to the registration page.
'''
class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        #Variable to layout the elements for the LoginPage class
        layout = QVBoxLayout()

        # The code below displays 'Login' in Arial in the center of the GUI
        self.title_label = QLabel("Login")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24))
        layout.addWidget(self.title_label)

        #The code below creates an input bar to enter the username.
        #The placeholder text is labelled 'Username'
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # The code below creates an input bar to enter the password.
        # The placeholder text is labelled 'Password'
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        #Button to allow a user to login
        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)

        #Button to register and create an account
        self.create_account_button = QPushButton("Create Account")
        layout.addWidget(self.create_account_button)

        #Sets the layout of this class, LoginPage, using the layout variable
        self.setLayout(layout)

'''
This module houses the registration page widget which will provide an interface for a
user to create a new account with an associated username/password. There is also a
connection created to transition to the login page.
'''
class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()

        #variable to layout the elements in the RegistrationPage class
        layout = QVBoxLayout()

        #Creates a label named 'Registration' and sets it at the center
        #of the label in an Arial font
        self.title_label = QLabel("Registration")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24))
        layout.addWidget(self.title_label)

        #Creates an input bar to enter a username for a new account
        #The placeholder text is 'Username'
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # Creates an input bar to enter a username for a new account
        # The placeholder text is 'Password'
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        #Creates a button which allows a user to register for an account
        #which is added into the database as well
        self.register_button = QPushButton("Register")
        layout.addWidget(self.register_button)

        #Button labeled 'Back' to take user back to the log in page
        #once registered
        self.back_to_login_button = QPushButton("Back")
        layout.addWidget(self.back_to_login_button)

        #Sets the layout of the Registration page using the layout variable
        self.setLayout(layout)

'''
The task widget is created within the TimeTrackingApp class with a parent type
that is a simple list widget. This module will be unique to each user's task list and
allow for the individual creation and manipulation (start/stop/edit/delete) of individual units.
'''
class TaskWidget(QWidget):
    def __init__(self, task_id, task_name, total_time, task_description):
        super().__init__()

        #Task id attribute
        self.task_id = task_id
        #Attribute for the task name
        self.task_name = task_name
        #Attribute for the total time elapsed
        self.total_time = total_time
        #Attribute for the description of the task
        self.task_description = task_description

        #The code below creates a variable to lay out the elements in a
        #TaskWidget class and sets the size of it
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        #Creates a label to dispaly the elapsed time
        self.time_label = QLabel()
        self.update_task_label()
        layout.addWidget(self.time_label)

        #Creates a button that allows the user to
        #start and stop a task
        start_button = QPushButton("Start/Stop")
        start_button.setFixedSize(80, 25)
        start_button.clicked.connect(self.start_tracking)
        layout.addWidget(start_button)

        #Creates a button that allows the user to
        #delete a task
        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(60, 25)
        delete_button.clicked.connect(self.delete_task)
        layout.addWidget(delete_button)

        #Creates a button that displays a window
        #to edit task configurations
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(60, 25)
        edit_button.clicked.connect(self.show_edit_task_dialog)
        layout.addWidget(edit_button)

        self.setLayout(layout)

        self.is_on = True


    #Updates the time to display it in hours, minute, and seconds
    def update_task_label(self):
        self.time_label.setText(f"{self.task_name} - {(self.total_time // 3600)}:{((self.total_time % 3600) // 60)}:{(self.total_time % 60)}")

    #Function that serves as the timer for the task
    def start_tracking(self):
        if self.is_on:
            #if the program is running
            if not hasattr(self, "timer"):
                self.timer = QTimer()
                self.timer.timeout.connect(self.increment_time)
            self.timer.start(1000)
            self.is_on = False
        else:
            #if the program is not running
            if hasattr(self, "timer"):
                self.timer.stop()
                self.save_total_time()
            self.is_on = True

    #Function that stops the timer of a task
    def stop_tracking(self):
        if hasattr(self, "timer"):
            self.timer.stop()
            self.save_total_time()

    #Function that increments the total time by 1
    def increment_time(self):
        self.total_time += 1
        self.update_task_label()
        self.save_total_time()

    #Function that saves the total elapsed time and saves it
    #in the database
    def save_total_time(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        #Using an SQL query, the code below stores the elapsed time in the database given a task id
        cursor.execute("UPDATE task_list SET total_time = ? WHERE task_id = ?", (self.total_time, self.task_id))

        conn.commit()
        conn.close()


    #Function that deletes a task from the task list and deletes
    #it from the database as well
    def delete_task(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        #Using an SQL query, the code below deletes a task from the task list table
        #in the database given a task id
        cursor.execute("DELETE FROM task_list WHERE task_id = ?", (self.task_id,))

        conn.commit()
        conn.close()

        self.setParent(None)


    #Function to edit the task configurations
    def show_edit_task_dialog(self):

        #creates a window for editing the task
        dialog = QDialog()
        dialog.setWindowTitle("Edit Task")

        #variable for the layout of the window
        #for editing the task
        vbox = QVBoxLayout()

        #Creates a label for an input bar
        #named 'Task Name: '
        task_name_label = QLabel("Task Name:")
        vbox.addWidget(task_name_label)

        #Creates an input bar to enter the task name
        task_name_edit = QLineEdit(self.task_name)
        vbox.addWidget(task_name_edit)

        #Creates a label for an input bar
        #named 'Task Description: '
        task_description_label = QLabel("Task Description:")
        vbox.addWidget(task_description_label)

        #Creates an input bar to enter the task description
        task_description_edit = QTextEdit(self.task_description)
        vbox.addWidget(task_description_edit)

        #Creates a variable to store two buttons for the window which are OK and Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        vbox.addWidget(button_box)


        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        #Sets the layout for the window
        dialog.setLayout(vbox)

        #Variable that stores the status of the button
        #selection of the dialog window(editing window)
        result = dialog.exec()

        #If the OK button is selected, the task configurations are
        #saved into the database and into the task list in the application
        if result == QDialog.DialogCode.Accepted:

            #The code below updates the task name and description
            self.task_name = task_name_edit.text()
            self.task_description = task_description_edit.toPlainText()

            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            #The code below updates the task name and description in the
            #database given a task id
            cursor.execute(
                "UPDATE task_list SET task_name = ?, task_description = ? WHERE task_id = ?",
                (self.task_name, self.task_description, self.task_id))

            conn.commit()
            conn.close()

            self.update_task_label()

'''
Settings is the storehouse for all user preferences from the user_settings table,
and it will be able to save, load, and edit explicitly-defined user parameters.
'''
class Settings:
    def __init__(self, user_id):
        #The two attributes for the Settings class
        #are a user id and preferences
        self.user_id = user_id
        self.preferences = self.load_preferences()

    #This functions loads the preferences for the
    #settings for a particular user
    def load_preferences(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()


        cursor.execute("SELECT show_calendar FROM user_settings WHERE user_id = ?", (self.user_id,))
        result = cursor.fetchone()

        if result:
            show_calendar = bool(result[0])
        else:
            show_calendar = True
            cursor.execute("INSERT INTO user_settings (user_id, show_calendar) VALUES (?, ?)",
                           (self.user_id, int(show_calendar)))
            conn.commit()

        conn.close()
        return {"show_calendar": show_calendar}

    def save_preferences(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("UPDATE user_settings SET show_calendar = ? WHERE user_id = ?",
                       (int(self.preferences["show_calendar"]), self.user_id))
        conn.commit()

        conn.close()

    def toggle_calendar(self):
        self.preferences["show_calendar"] = not self.preferences["show_calendar"]
        self.save_preferences()

'''
This module is a dialog widget as a member of the TimeTrackingApp that will handle
dialog between the system and the user for updating preferences or reaching a logout state.
'''
class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Settings")

        layout = QVBoxLayout(self)

        self.calendar_checkbox = QCheckBox("Show Calendar")
        self.calendar_checkbox.stateChanged.connect(self.toggle_calendar)
        layout.addWidget(self.calendar_checkbox)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

    def toggle_calendar(self, state):
        self.parent().toggle_calendar(state)

    def logout(self):
        self.parent().logout()
        self.accept()

"""
This class represents a calendar window which
will be utilized for viewing a calendar by
pressing a button
"""
class CalendarWindow(QWidget):

    def __init__(self):
            super().__init__()

            #sets the window size, title, and icon
            self.setGeometry(200, 200, 700, 400)
            self.setWindowTitle("Calendar")
            self.setWindowIcon(QIcon('python.png'))

            #vbox is a variable for the layout of the
            #calendar window elements
            vbox = QVBoxLayout()

            self.calendar = QCalendarWidget()
            self.calendar.setGridVisible(True)
            self.calendar.selectionChanged.connect(self.calendar_date)

            self.label = QLabel("Hello")
            self.label.setFont(QFont("Sanserif", 15))
            self.label.setStyleSheet('color:green')

            vbox.addWidget(self.calendar)
            vbox.addWidget(self.label)

            self.setLayout(vbox)

    def calendar_date(self):
            dateselected = self.calendar.selectedDate()
            date_in_string = str(dateselected.toPyDate())

            self.label.setText("Date Is : " + date_in_string)


'''
The TimeTrackingApp class will control the task list creation, format its layout, handle the
link to calendar creation/viewing, as well as act like a homepage in the stacked global widget. It
must be created with an application already instilled and will be specific to each user_id. 
'''
class TimeTrackingApp(QWidget):
    def __init__(self, user_id):
        super().__init__()

        #These attributes set the user_id and settings
        #on the basis of the user_id(by creating a
        #Settings object with a user_id parameter)
        self.user_id = user_id
        self.user_settings = Settings(user_id)

        #variable that contains the layout for the TimeTrackingApp class
        layout = QVBoxLayout()

        #The code below creates a label with the username and places it at the upper
        #left section of the window
        self.username_label = QLabel()
        self.update_username_label()
        layout.addWidget(self.username_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        #The code below creates a button to view the calendar and places it at the bottom
        #right of the upper window
        self.calendar_button = QPushButton("View Calendar")
        self.calendar_button.clicked.connect(self.show_calendar_window)
        layout.addWidget(self.calendar_button, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        #The code below creates a button to view the settings and places it below the calendar button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.show_settings_dialog)
        layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)


        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        #The code below creates a list of created tasks displayed
        #in the window
        self.task_list = QListWidget()
        self.load_tasks()
        layout.addWidget(self.task_list)

        #The code below creates a button to create a task
        create_task_button = QPushButton("Create Task")
        create_task_button.clicked.connect(self.create_task)
        layout.addWidget(create_task_button)

        #The code below creates a button to stop all of the
        #tasks in the task list
        stop_all_tasks_button = QPushButton("Stop All Tasks")
        stop_all_tasks_button.clicked.connect(self.stop_all_tasks)
        layout.addWidget(stop_all_tasks_button)

        #Sets the layout of the TimeTrackingApp class with the
        #layout variable
        self.setLayout(layout)


    #the function below updates the username label displayed in
    #the upper left corner of the TimeTrackingApp class
    def update_username_label(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        #Using an SQL query, this code selects the username given a user ID and stores
        #the value in a variable named 'username'
        cursor.execute("SELECT username FROM users WHERE user_id = ?", (self.user_id,))
        username = cursor.fetchone()[0]

        conn.close()
        #sets the label text with the value of the variable username
        self.username_label.setText(f"Welcome, {username}!")



    #The function below fetches the tasks from the database
    #to be displayed in the task list
    def load_tasks(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        #Using a SQL query, the code below selects the task and its attributes
        #from the database given a user id
        cursor.execute("SELECT task_id, task_name, total_time, task_description FROM task_list WHERE user_id = ?",
                       (self.user_id,))

        #The code below adds the tasks into the task list
        for task_id, task_name, total_time, task_description in cursor.fetchall():
            task_widget = TaskWidget(task_id, task_name, total_time, task_description)
            task_list_item = QListWidgetItem()
            task_list_item.setSizeHint(task_widget.sizeHint())

            self.task_list.addItem(task_list_item)
            self.task_list.setItemWidget(task_list_item, task_widget)

        conn.close()

    #This function is used to create a task and
    #the user is asked to enter a name for the task
    def create_task(self):
        #Creates an input dialog window to get the name for the task
        task_name, ok = QInputDialog.getText(self, "Create Task", "Task Name:")

        #If the task is created by selecting the 'OK' button
        if ok and task_name:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            #Using an SQL query, the code below inserts a task into the database
            #table named 'task_list' given a user id and task name
            cursor.execute("INSERT INTO task_list (user_id, task_name) VALUES (?, ?)", (self.user_id, task_name))
            conn.commit()

            task_id = cursor.lastrowid

            conn.close()

            #the code below creates a task widget object which represents a task
            #and it is defined again as a task list item
            task_widget = TaskWidget(task_id, task_name, 0, "")
            task_list_item = QListWidgetItem()
            task_list_item.setSizeHint(task_widget.sizeHint())

            #The code below inserts a task into the task list
            self.task_list.addItem(task_list_item)
            self.task_list.setItemWidget(task_list_item, task_widget)

    #The function below stops all tasks in a task list. It iterates through
    #each task item and stops the timer for each one
    def stop_all_tasks(self):
        for index in range(self.task_list.count()):
            task_widget = self.task_list.itemWidget(self.task_list.item(index))
            task_widget.stop_tracking()

    #The function below shows the window to display
    #the settings by creating a dialog box
    def show_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()


    def toggle_calendar(self, state):
        self.calendar.setVisible(state)


    def apply_preferences(self):
        self.calendar.setVisible(self.user_settings.preferences["show_calendar"])

    #This function logs the user out of the application
    def logout(self):
        self.parent().setCurrentIndex(0)

    #The function below shows a calendar window
    #by creating a CalendarWindow object and calling
    #the show function
    def show_calendar_window(self, checked):
        self.w = CalendarWindow()
        self.w.show()

'''
This module acts as the program's main composed structure inclusive of the login, registration, and
and main window widgets (stacked format). It handles login and registration validation as well
as the link to provide user's with a path into their unique application instance.
'''
class TimeTrackingApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        #Creates a widget for layout to display elements one at a time
        self.stacked_widget = QStackedWidget()
        #Creates a LoginPage object in the login_page variable
        #to serve as a login page
        self.login_page = LoginPage()
        #Creates a RegistrationPage in the registration_page
        #variable to serve as a registration page
        self.registration_page = RegistrationPage()

        #The two lines below add the login page
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.registration_page)

        #centers the stacked_widget in the TimeTrackingApplication class
        self.setCentralWidget(self.stacked_widget)

        #The code below sets functionality for the three variables below where
        #pressing the buttons for login, username input, and password input would
        #allow a user to login
        self.login_page.login_button.clicked.connect(self.login)
        self.login_page.username_input.returnPressed.connect(self.login)
        self.login_page.password_input.returnPressed.connect(self.login)
        #If the following button to create an account is selected, the user
        #is taken to a window for registering for a new account
        self.login_page.create_account_button.clicked.connect(self.switch_to_register)

        #The code below sets functionality for three variable using the register function
        #for the register button, username input, and password input. This allows the
        #user to register for a new account
        self.registration_page.register_button.clicked.connect(self.register)
        self.registration_page.username_input.returnPressed.connect(self.register)
        self.registration_page.password_input.returnPressed.connect(self.register)
        #If the back to login button is selected, the user is taken back to the
        #login page
        self.registration_page.back_to_login_button.clicked.connect(self.switch_to_login)



    #The function below allows a user to log in to the application given that they
    #created an account and enter both the correct username and password
    def login(self):
        #The two variables below obtain the username and password inputs
        username = self.login_page.username_input.text()
        password = self.login_page.password_input.text()

        #If either a username or password is not entered, or if both are not entered,
        #a window is displayed asking the user to enter both the username and password
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        #Using an SQL query and given a username, the code below selects the user_id
        #and password and stores them into a variable named 'result'
        cursor.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        conn.close()

        #The code below stores the user_id and password from the database into two
        #variables named user_id and stored_password
        if result:
            user_id, stored_password = result

            #If the password entered matches the password from the
            #database(stored_password), the user is logged in and
            #the time tracking application is created with the user info
            #with the user_id as a parameter
            if password == stored_password:
                #creates the time tracking application by creating
                #a TimeTrackingApp object with user_id as a parameter
                time_tracking_app = TimeTrackingApp(user_id)
                time_tracking_app.user_settings = Settings(user_id)
                time_tracking_app.apply_preferences()
                #Adds the time tracking application into the stacked
                #widget and changes the index of it to display the
                #time tracking application
                self.stacked_widget.addWidget(time_tracking_app)
                self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)
                self.setWindowTitle("Time Tracking Application")

            #If the password entered does not match the password from the database
            #a window is displayed telling the error the password entered was incorrect
            else:
                QMessageBox.warning(self, "Error", "Incorrect password.")
        #If the username does not exist in the database, a window is displayed
        #telling the user that the user was not found
        else:
            QMessageBox.warning(self, "Error", "User not found.")



    #The function below allows a user to register if
    #they provide both a username and a password
    def register(self):
        #The two variables below obtain the username and password inputs
        username = self.registration_page.username_input.text()
        password = self.registration_page.password_input.text()

        #If a user did not enter either a username, a password,or both
        #a window is displayed asking the user to enter both a username
        #and a password
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        #As a constraint, if the password is less than 8 characters long, a window is
        #displayed notifying the user that the password must be at leadt 8 characters loign
        if not len(self.registration_page.password_input.text()) >= 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters long")
            return

        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        #Using an SQL query, the username and password are inserted in the username and password
        #columns into the users table in the database
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

            QMessageBox.information(self, "Success", "User registered successfully.")
            self.stacked_widget.setCurrentIndex(0)
            self.login_page.username_input.clear()
            self.login_page.password_input.clear()

        #In the case where the entered username exists in the database, a window
        #is displayed notifying the user that the username they entered already
        #exists(in the database)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists.")

        conn.close()

    #Using the stacked_widget variable, this function
    #switches the window to the register window
    def switch_to_register(self):
        self.stacked_widget.setCurrentIndex(1)

    # Using the stacked_widget variable, this function
    # switches the window to the login window
    def switch_to_login(self):
        self.stacked_widget.setCurrentIndex(0)

'''
Definition of main within the system is here and will create the application runtime from our
current system. An instantiate of the TimeTrackingApplication class is generated to present 
the user with the comprehensive stacked widget.
'''
def main():
    create_database_and_tables(database)

    app = QApplication(sys.argv)

    #creates an object named main_window as an instance
    #of the TimeTrackingApplication
    main_window = TimeTrackingApplication()
    #Sets the window title as 'TimeTrackingApplication
    main_window.setWindowTitle("Time Tracking Application")
    #Sets the window size
    main_window.setGeometry(100, 100, 600, 400)

    #Shows the time tracking software by calling the show function
    #from the main_window variable
    main_window.show()

    sys.exit(app.exec())


#Executes the function by calling main.The database is
#created in a variable called database. The value of
#database is the path of the db folder and the file
#in it named time_tracking.db
if __name__ == "__main__":
    database = r"C:\Users\dcarb\Documents\db\time_tracking.db"
    main()