from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QStackedWidget, QMessageBox, QCalendarWidget, QListWidget, QListWidgetItem, QInputDialog, QDialog, QDialogButtonBox
)
import sys
import sqlite3

def create_database_and_tables(time_tracking_file):
    conn = sqlite3.connect(time_tracking_file)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
    )

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

    conn.close()


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.addStretch()

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.log_in)
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.show_registration)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def log_in(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_id = self.validate_login(username, password)
        if user_id:
            self.parent().login_user(user_id, username)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def validate_login(self, username, password):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        conn.close()

        return result and result[1] == password and result[0]

    def show_registration(self):
        self.parent().setCurrentWidget(self.parent().registration_page)

class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registration")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.addStretch()

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_label = QLabel("Confirm Password")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.show_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
        elif self.user_exists(username):
            QMessageBox.warning(self, "Error", "User already exists")
        else:
            self.create_user(username, password)
            QMessageBox.information(self, "Success", "User registered successfully")
            self.show_login()

    def user_exists(self, username):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()[0]

        conn.close()

        return result > 0

    def create_user(self, username, password):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

    def show_login(self):
       self.parent().setCurrentWidget(self.parent().login_page)

class TaskItem(QListWidgetItem):
    def __init__(self, task_id, task_name, total_time, task_description, parent=None):
        super().__init__(parent)

        self.task_id = task_id
        self.task_name = task_name
        self.total_time = total_time
        self.task_description = task_description

        self.task_widget = TaskWidget(self)
        self.setSizeHint(self.task_widget.sizeHint())

class TaskWidget(QWidget):
    def __init__(self, task_item, parent=None):
        super().__init__(parent)

        self.task_item = task_item

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.task_label = QLabel(task_item.task_name)
        self.time_label = QLabel(f"Total Time: {task_item.total_time} s")

        layout.addWidget(self.task_label)
        layout.addWidget(self.time_label)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_tracking)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_tracking)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_total_time)

    def start_tracking(self):
        self.timer.start(1000)

    def stop_tracking(self):
        self.timer.stop()

    def update_total_time(self):
        self.task_item.total_time += 1
        self.time_label.setText(f"Total Time: {self.task_item.total_time} s")


class TimeTrackingApp(QWidget):
    def __init__(self, user_id=None):
        super().__init__()

        self.setWindowTitle("Time Tracking Application")

        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Time Tracking Application")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        self.username_label = QLabel("Username")
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.show_settings)

        header_layout.addWidget(self.username_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.settings_button)

        # Calendar
        self.calendar = QCalendarWidget()

        # Project list
        self.project_list = QListWidget()
        self.project_list.itemDoubleClicked.connect(self.show_edit_task_dialog)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.calendar)
        main_layout.addWidget(self.project_list)

        task_management_layout = QHBoxLayout()

        self.create_task_button = QPushButton("Create Task")
        self.create_task_button.clicked.connect(self.create_task)

        self.delete_task_button = QPushButton("Delete Task")
        self.delete_task_button.clicked.connect(self.delete_task)

        self.stop_all_tasks_button = QPushButton("Stop All Tasks")
        self.stop_all_tasks_button.clicked.connect(self.stop_all_tasks)

        task_management_layout.addWidget(self.create_task_button)
        task_management_layout.addWidget(self.delete_task_button)
        task_management_layout.addWidget(self.stop_all_tasks_button)

        main_layout.addLayout(task_management_layout)

        self.setLayout(main_layout)

    def show_settings(self):
        print("Settings button clicked")

    def create_task(self):
        task_name, ok = QInputDialog.getText(self, "Create Task", "Task Name:")

        if ok and task_name:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO task_list (user_id, task_name) VALUES (?, ?)", (self.user_id, task_name))

            conn.commit()
            conn.close()

            self.update_task_list(clear_timers=False)

    def delete_task(self):
        current_task = self.project_list.currentItem()

        if isinstance(current_task, TaskItem):
            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM task_list WHERE task_id = ?", (current_task.task_id,))

            conn.commit()
            conn.close()

            self.update_task_list(clear_timers=False)

    def stop_all_tasks(self):
        for i in range(self.project_list.count()):
            task_item = self.project_list.item(i)
            if isinstance(task_item, TaskItem):
                task_item.task_widget.stop_tracking()

    def update_task_list(self, clear_timers=False):
        self.project_list.clear()

        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("SELECT task_id, task_name, total_time, task_description FROM task_list WHERE user_id = ?",
                       (self.user_id,))
        tasks = cursor.fetchall()

        conn.close()

        for task in tasks:
            task_item = TaskItem(task[0], task[1], task[2], task[3])
            self.project_list.addItem(task_item)
            self.project_list.setItemWidget(task_item, task_item.task_widget)
            if clear_timers:
                task_item.task_widget.stop_tracking()


    def show_edit_task_dialog(self):
        current_task = self.project_list.currentItem()

        if current_task and isinstance(current_task, TaskItem):
            edit_task_dialog = QDialog(self)
            edit_task_dialog.setWindowTitle("Edit Task")

            layout = QVBoxLayout()

            task_name_label = QLabel("Task Name:")
            task_name_input = QLineEdit(current_task.task_name)
            layout.addWidget(task_name_label)
            layout.addWidget(task_name_input)

            total_time_label = QLabel(f"Total Time: {current_task.total_time} seconds")
            layout.addWidget(total_time_label)

            description_label = QLabel("Description:")
            description_input = QLineEdit(current_task.task_description)
            layout.addWidget(description_label)
            layout.addWidget(description_input)

            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(edit_task_dialog.accept)
            buttons.rejected.connect(edit_task_dialog.reject)
            layout.addWidget(buttons)

            edit_task_dialog.setLayout(layout)

            result = edit_task_dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                new_task_name = task_name_input.text()
                new_task_description = description_input.text()

                conn = sqlite3.connect(database)
                cursor = conn.cursor()

                cursor.execute("UPDATE task_list SET task_name = ?, task_description = ? WHERE task_id = ?",
                               (new_task_name, new_task_description, current_task.task_id))

                conn.commit()
                conn.close()

                self.update_task_list()

class TimeTrackingApplication(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login_page = LoginPage()
        self.registration_page = RegistrationPage()
        self.main_widget = TimeTrackingApp()

        self.addWidget(self.login_page)
        self.addWidget(self.registration_page)
        self.addWidget(self.main_widget)

        self.setCurrentWidget(self.login_page)
        self.setFixedSize(500, 400)

    def login_user(self, user_id, username):
        self.main_widget.user_id = user_id
        self.main_widget.username_label.setText(username)
        self.main_widget.update_task_list()
        self.setCurrentWidget(self.main_widget)

if __name__ == "__main__":
        app = QApplication(sys.argv)
        #Simply create a folder named "db" and place its directory in here with name time_tracking.db following it as seen below
        database = r"C:\Users\ajru5\OneDrive\Documents\FloridaPoly\Spring2023\Secure Software Engineering\pythonProject\db\time_tracking.db"
        create_database_and_tables(database)
        time_tracking_application = TimeTrackingApplication()
        time_tracking_application.show()
        sys.exit(app.exec())
