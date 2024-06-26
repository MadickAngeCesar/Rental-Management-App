import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
import mysql.connector
from Login import Ui_Dialog
from rms import Ui_MainWindow

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # Connect buttons to methods
        self.ui.pushButton_2.clicked.connect(self.login)
        self.ui.pushButton_3.clicked.connect(self.signup)
        
        # Setup MySQL connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="rms"
        )
        self.cursor = self.db_connection.cursor()
    
    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        
        if username and password:
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            
            if result:
                self.accept()  # Close the login dialog and proceed to the main window
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password")
    
    def signup(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        
        if username and password:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            try:
                self.cursor.execute(query, (username, password))
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Account created successfully!")
            except mysql.connector.Error as err:
                QMessageBox.warning(self, "Error", f"Error: {err}")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password")

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup MySQL connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="rms"
        )
        self.cursor = self.db_connection.cursor()

        # Hide the tab bar
        self.ui.tabWidget.tabBar().hide()
        self.see_bills()
        self.see_states()
        self.see_teenants()
        self.see_maintenants()

        self.ui.pushButton_3.clicked.connect(self.switchTab1)
        self.ui.pushButton_4.clicked.connect(self.switchTab2)
        self.ui.pushButton_5.clicked.connect(self.switchTab3)
        self.ui.pushButton_6.clicked.connect(self.switchTab4)
        self.ui.pushButton_7.clicked.connect(self.switchTab5)

        self.ui.pushButton_13.clicked.connect(self.set_bill)
        self.ui.pushButton_9.clicked.connect(self.set_state)
        self.ui.pushButton_10.clicked.connect(self.set_teenant)
        self.ui.pushButton_11.clicked.connect(self.set_maintenant)

        self.ui.pushButton_8.clicked.connect(self.search_bills)

        self.ui.pushButton_12.clicked.connect(self.delete_maintenant)

    def switchTab1(self):
        # Switch to the second tab (index 1)
        self.ui.tabWidget.setCurrentIndex(0)

    def switchTab2(self):
        self.ui.tabWidget.setCurrentIndex(1) 
        self.see_bills()

    def switchTab3(self):
        self.ui.tabWidget.setCurrentIndex(2) 
        self.see_states()

    def switchTab4(self):
        self.ui.tabWidget.setCurrentIndex(3) 
        self.see_teenants()

    def switchTab5(self):
        self.ui.tabWidget.setCurrentIndex(4) 
        self.see_maintenants()               
    
    def set_bill(self):
        room_num = self.ui.spinBox.value()
        teenant = self.ui.lineEdit_9.text()
        electric_bill = self.ui.lineEdit_10.text()
        water_bill = self.ui.lineEdit_11.text()
        rental_bill = self.ui.lineEdit_12.text()
        contact = self.ui.lineEdit_13.text()
        due_date = self.ui.dateEdit.text()

        try:
            if room_num and teenant and electric_bill and water_bill and rental_bill and contact and due_date:
                query = "INSERT INTO bills (room_num, teenant, electric_bill, water_bill, rental_bill, contact, due_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (room_num, teenant, electric_bill, water_bill, rental_bill, contact, due_date)
                self.cursor.execute(query, values)
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Record created successfully!")
                self.see_bills()
            else:
                QMessageBox.warning(self, "Input Error", "Please fill all fields")
        except Exception as e:
                QMessageBox.warning(self, "Error", f"Error: {e}")              

    def set_state(self):
        room_num = self.ui.spinBox_2.value()
        room_state = self.ui.lineEdit_2.text()
        description = self.ui.desc.text()

        try:
            if room_num and description and room_state:
                query = "INSERT INTO states (room_num, room_state, description) VALUES (%s, %s, %s)"
                values = (room_num, room_state, description)
                self.cursor.execute(query, values)
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Record created successfully!")
                self.see_states()
            else:
                QMessageBox.warning(self, "Input Error", "Please fill all fields")
        except Exception as e:
                QMessageBox.warning(self, "Error", f"Error: {e}")  

    def set_teenant(self):
        room_num = self.ui.spinBox_3.value()
        teenant = self.ui.lineEdit_4.text()
        contact = self.ui.lineEdit_8.text()

        try:
            if room_num and contact and teenant:
                query = "INSERT INTO teenants (room_num, teenant, contact) VALUES (%s, %s, %s)"
                values = (room_num, teenant, contact)
                self.cursor.execute(query, values)
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Record created successfully!")
                self.see_teenants()
            else:
                QMessageBox.warning(self, "Input Error", "Please fill all fields")
        except Exception as e:
                QMessageBox.warning(self, "Error", f"Error: {e}") 

    def set_maintenant(self):
        service = self.ui.lineEdit_5.text()
        agent = self.ui.lineEdit_6.text()
        contact = self.ui.lineEdit_7.text()

        try:
            if service and contact and agent:
                query = "INSERT INTO maintenants (service, agent, contact) VALUES (%s, %s, %s)"
                values = (service, agent, contact)
                self.cursor.execute(query, values)
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Record created successfully!")
                self.see_maintenants()
            else:
                QMessageBox.warning(self, "Input Error", "Please fill all fields")
        except Exception as e:
                QMessageBox.warning(self, "Error", f"Error: {e}")    

    def display_on_table(self):
        results = self.cursor.fetchall()

        self.ui.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.ui.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data))) 

    def search_bills(self):
        search_name = self.ui.lineEdit.text()

        if search_name:
            query = "SELECT * FROM bills WHERE teenant LIKE %s" 
            value = ("%" + search_name + "%",)
            self.cursor.execute(query, value)
            self.display_on_table()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a name to search")                                                  

    def see_bills(self):
        query = "SELECT room_num, teenant, electric_bill, water_bill, rental_bill, contact, due_date FROM bills"
        self.cursor.execute(query)
        self.display_on_table()

    def see_states(self):
        query = "SELECT room_num, room_state, description FROM states"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        self.ui.tableWidget_2.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.ui.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.tableWidget_2.setItem(row_number, column_number, QTableWidgetItem(str(data))) 


    def see_teenants(self):
        query = "SELECT room_num, teenant, contact FROM teenants"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        self.ui.tableWidget_3.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.ui.tableWidget_3.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.tableWidget_3.setItem(row_number, column_number, QTableWidgetItem(str(data))) 

    
    def see_maintenants(self):
        query = "SELECT service, agent, contact FROM maintenants"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        self.ui.tableWidget_4.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.ui.tableWidget_4.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.tableWidget_4.setItem(row_number, column_number, QTableWidgetItem(str(data))) 

    def delete_maintenant(self):
        agent = self.ui.lineEdit_6.text()

        if agent:
            query = "DELETE FROM maintenants WHERE agent=%s"
            values = (agent,)
            self.cursor.execute(query, values)
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Record deleted successfully!")
            self.see_maintenants()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter an agent")              


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and display the login dialog
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        # If login is successful, open the main application window
        main_window = MainApp()
        main_window.show()
        sys.exit(app.exec_())
