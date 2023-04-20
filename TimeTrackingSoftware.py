import sys
import sqlite3
from datetime import timedelta

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QInputDialog, QListWidget, QListWidgetItem, QStackedWidget, QCalendarWidget, QDialog, QDialogButtonBox, QMessageBox, \
    QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon


def create_database_and_tables(database):
    conn = sqlite3.connect(database)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            show_calendar INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
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

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """
    )

    conn.commit()
    conn.close()


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title_label = QLabel("Login")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24))
        layout.addWidget(self.title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)

        self.create_account_button = QPushButton("Create Account")
        layout.addWidget(self.create_account_button)

        self.setLayout(layout)


class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title_label = QLabel("Registration")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24))
        layout.addWidget(self.title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register")
        layout.addWidget(self.register_button)

        self.back_to_login_button = QPushButton("Back")
        layout.addWidget(self.back_to_login_button)

        self.setLayout(layout)


class TaskWidget(QWidget):
    def __init__(self, task_id, task_name, total_time, task_description):
        super().__init__()

        self.task_id = task_id
        self.task_name = task_name
        self.total_time = total_time
        self.task_description = task_description

        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.time_label = QLabel()
        self.update_task_label()
        layout.addWidget(self.time_label)

        start_button = QPushButton("Start")
        start_button.setFixedSize(60, 20)
        start_button.clicked.connect(self.start_tracking)
        layout.addWidget(start_button)

        stop_button = QPushButton("Stop")
        stop_button.setFixedSize(60, 20)
        stop_button.clicked.connect(self.stop_tracking)
        layout.addWidget(stop_button)

        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(60, 20)
        delete_button.clicked.connect(self.delete_task)
        layout.addWidget(delete_button)

        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(60, 20)
        edit_button.clicked.connect(self.show_edit_task_dialog)
        layout.addWidget(edit_button)

        self.setLayout(layout)

    def update_task_label(self):
        self.time_label.setText(f"{self.task_name} - {(self.total_time // 3600)}:{((self.total_time % 3600) // 60)}:{(self.total_time % 60)}")

    def start_tracking(self):
        if not hasattr(self, "timer"):
            self.timer = QTimer()
            self.timer.timeout.connect(self.increment_time)
        self.timer.start(1000)

    def stop_tracking(self):
        if hasattr(self, "timer"):
            self.timer.stop()
            self.save_total_time()

    def increment_time(self):
        self.total_time += 1
        self.update_task_label()
        self.save_total_time()

    def save_total_time(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("UPDATE task_list SET total_time = ? WHERE task_id = ?", (self.total_time, self.task_id))

        conn.commit()
        conn.close()

    def delete_task(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM task_list WHERE task_id = ?", (self.task_id,))

        conn.commit()
        conn.close()

        self.setParent(None)

    def show_edit_task_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Edit Task")

        vbox = QVBoxLayout()

        task_name_label = QLabel("Task Name:")
        vbox.addWidget(task_name_label)

        task_name_edit = QLineEdit(self.task_name)
        vbox.addWidget(task_name_edit)

        task_description_label = QLabel("Task Description:")
        vbox.addWidget(task_description_label)

        task_description_edit = QTextEdit(self.task_description)
        vbox.addWidget(task_description_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        vbox.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        dialog.setLayout(vbox)

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.task_name = task_name_edit.text()
            self.task_description = task_description_edit.toPlainText()

            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE task_list SET task_name = ?, task_description = ? WHERE task_id = ?",
                (self.task_name, self.task_description, self.task_id))

            conn.commit()
            conn.close()

            self.update_task_label()


class Settings:
    def __init__(self, user_id):
        self.user_id = user_id
        self.preferences = self.load_preferences()

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



class CalendarWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
            super().__init__()

            self.setGeometry(200, 200, 700, 400)
            self.setWindowTitle("Calendar")
            self.setWindowIcon(QIcon('python.png'))

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



class TimeTrackingApp(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        self.user_settings = Settings(user_id)

        layout = QVBoxLayout()

        self.username_label = QLabel()
        self.update_username_label()
        layout.addWidget(self.username_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.calendar_button = QPushButton("View Calendar")
        self.calendar_button.clicked.connect(self.show_new_window)
        layout.addWidget(self.calendar_button, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.show_settings_dialog)
        layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        self.task_list = QListWidget()
        self.load_tasks()
        layout.addWidget(self.task_list)

        create_task_button = QPushButton("Create Task")
        create_task_button.clicked.connect(self.create_task)
        layout.addWidget(create_task_button)

        stop_all_tasks_button = QPushButton("Stop All Tasks")
        stop_all_tasks_button.clicked.connect(self.stop_all_tasks)
        layout.addWidget(stop_all_tasks_button)

        self.setLayout(layout)

    def update_username_label(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users WHERE user_id = ?", (self.user_id,))
        username = cursor.fetchone()[0]

        conn.close()

        self.username_label.setText(f"Welcome, {username}!")

    def load_tasks(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("SELECT task_id, task_name, total_time, task_description FROM task_list WHERE user_id = ?",
                       (self.user_id,))

        for task_id, task_name, total_time, task_description in cursor.fetchall():
            task_widget = TaskWidget(task_id, task_name, total_time, task_description)
            task_list_item = QListWidgetItem()
            task_list_item.setSizeHint(task_widget.sizeHint())

            self.task_list.addItem(task_list_item)
            self.task_list.setItemWidget(task_list_item, task_widget)

        conn.close()

    def create_task(self):
        task_name, ok = QInputDialog.getText(self, "Create Task", "Task Name:")

        if ok and task_name:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO task_list (user_id, task_name) VALUES (?, ?)", (self.user_id, task_name))
            conn.commit()

            task_id = cursor.lastrowid

            conn.close()

            task_widget = TaskWidget(task_id, task_name, 0, "")
            task_list_item = QListWidgetItem()
            task_list_item.setSizeHint(task_widget.sizeHint())

            self.task_list.addItem(task_list_item)
            self.task_list.setItemWidget(task_list_item, task_widget)

    def stop_all_tasks(self):
        for index in range(self.task_list.count()):
            task_widget = self.task_list.itemWidget(self.task_list.item(index))
            task_widget.stop_tracking()

    def show_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec()

    def toggle_calendar(self, state):
        self.calendar.setVisible(state)

    def apply_preferences(self):
        self.calendar.setVisible(self.user_settings.preferences["show_calendar"])

    def logout(self):
        self.parent().setCurrentIndex(0)

    def show_new_window(self, checked):
        self.w = CalendarWindow()
        self.w.show()

class TimeTrackingApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.login_page = LoginPage()
        self.registration_page = RegistrationPage()

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.registration_page)

        self.setCentralWidget(self.stacked_widget)

        self.login_page.login_button.clicked.connect(self.login)
        self.login_page.username_input.returnPressed.connect(self.login)
        self.login_page.password_input.returnPressed.connect(self.login)
        self.login_page.create_account_button.clicked.connect(self.switch_to_register)

        self.registration_page.register_button.clicked.connect(self.register)
        self.registration_page.username_input.returnPressed.connect(self.register)
        self.registration_page.password_input.returnPressed.connect(self.register)
        self.registration_page.back_to_login_button.clicked.connect(self.switch_to_login)

    def login(self):
        username = self.login_page.username_input.text()
        password = self.login_page.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        conn.close()

        if result:
            user_id, stored_password = result

            if password == stored_password:
                time_tracking_app = TimeTrackingApp(user_id)
                time_tracking_app.user_settings = Settings(user_id)
                time_tracking_app.apply_preferences()
                self.stacked_widget.addWidget(time_tracking_app)
                self.stacked_widget.setCurrentIndex(self.stacked_widget.count() - 1)
                self.setWindowTitle("Time Tracking Application")
            else:
                QMessageBox.warning(self, "Error", "Incorrect password.")
        else:
            QMessageBox.warning(self, "Error", "User not found.")

    def register(self):
        username = self.registration_page.username_input.text()
        password = self.registration_page.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

            QMessageBox.information(self, "Success", "User registered successfully.")
            self.stacked_widget.setCurrentIndex(0)
            self.login_page.username_input.clear()
            self.login_page.password_input.clear()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists.")

        conn.close()

    def switch_to_register(self):
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_login(self):
        self.stacked_widget.setCurrentIndex(0)


def main():
    create_database_and_tables(database)

    app = QApplication(sys.argv)

    main_window = TimeTrackingApplication()
    main_window.setWindowTitle("Time Tracking Application")
    main_window.setGeometry(100, 100, 600, 400)

    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    database = r"C:\\db\time_tracking.db"
    main()


