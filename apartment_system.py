from tkinter import *
import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import Label, ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector

def insert_data1(hallno, bookingid, dateofbooking, duration, flatid, time):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="sys"
        )
        cursor = connection.cursor()
        query = "INSERT INTO Halls (HallID, BookingID, DateOfBooking, Duration, FlatID, EventTime) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (hallno, bookingid, dateofbooking, duration, flatid, time)
        cursor.execute(query, data)
        connection.commit()
        messagebox.showinfo("Success", "Data inserted successfully!")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to insert data: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def insert_data2(reciptno, paymentdate, propertytype, propertyid, amount, facility):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="sys"
        )
        cursor = connection.cursor()
        query = "INSERT INTO Maintenance (Receiptno, PaymentDate, PropertyType, PropertyID, Amount, GeneratorFacility ) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (reciptno, paymentdate, propertytype, propertyid, amount, facility)
        cursor.execute(query, data)
        connection.commit()
        messagebox.showinfo("Success", "Data inserted successfully!")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to insert data: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def delete_data(booking_id):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='sys'
        )
        cursor = conn.cursor()

        # Construct the DELETE query using the provided booking ID
        delete_query = "DELETE FROM Halls WHERE BookingID = %s"
        cursor.execute(delete_query, (booking_id,))

        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully")
        clear_fields()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to delete record: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def clear_fields():
    bookid_entry.delete(0, END)

def on_delete_button_click():
    booking_id = bookid_entry.get()
    if booking_id:
        delete_data(booking_id)
    else:
        messagebox.showwarning("Warning", "Please enter a booking ID")

def clear_fields1():
    receipt_entry.delete(0, END)

def delete_data1(receipt_no):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='sys'
        )
        cursor = conn.cursor()

        # Construct the DELETE query using the provided booking ID
        delete_query = "DELETE FROM Maintenance WHERE Receiptno = %s"
        cursor.execute(delete_query, (receipt_no,))

        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully")
        clear_fields1()  # Call clear_fields() after showing success message

    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to delete record: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def on_delete_button_click1():
    receipt_no = receipt_entry.get()
    if receipt_no:
        delete_data1(receipt_no)
    else:
        messagebox.showwarning("Warning", "Please enter a booking ID")

def update_database(booking_id, hall_number, date_of_booking, duration, flat_id, time):
    try:
        # Establish a connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="sys"
        )

        if mydb.is_connected():
            # Create a cursor object to interact with the database
            mycursor = mydb.cursor()

            # Prepare the UPDATE query
            update_query = "UPDATE Halls SET "
            updates = []

            # Check for filled attributes and add them to the update list
            if hall_number:
                updates.append(f"HallID = '{hall_number}'")
            if date_of_booking:
                updates.append(f"DateOfBooking = '{date_of_booking}'")
            if duration:
                updates.append(f"Duration = '{duration}'")
            if flat_id:
                updates.append(f"FlatID = '{flat_id}'")
            if time:
                updates.append(f"EventTime = '{time}'")

            # Join the updates to form the SET part of the query
            update_query += ', '.join(updates)

            # Add the WHERE clause
            update_query += f" WHERE BookingID = '{booking_id}'"

            # Execute the query with user-provided data
            mycursor.execute(update_query)

            # Commit the changes to the database
            mydb.commit()

            # Close the cursor and database connection
            mycursor.close()
            mydb.close()

            return True  # Updated successfully
    except mysql.connector.Error as error:
        print("Error updating data:", error)
        return False  # Failed to update
    
def update_data(receipt_no, payment_date=None, property_type=None, property_id=None, amount=None , facility=None):
    try:
        # Connect to the MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="sys"
        )
        mycursor = mydb.cursor()
        # Generate the update query based on the fields filled by the user
        sql = "UPDATE Maintenance SET "
        update_values = []

        if payment_date:
            update_values.append(f"PaymentDate = '{payment_date}'")
        if property_type:
            update_values.append(f"PropertyType = '{property_type}'")
        if property_id:
            update_values.append(f"PropertyID = '{property_id}'")
        if amount:
            update_values.append(f"Amount = '{amount}'")
        if facility:
            update_values.append(f"GeneratorFacility = '{facility}'")

        # Join the update values together
        sql += ', '.join(update_values)
        sql += f" WHERE Receiptno = '{receipt_no}'"  # Assuming 'Receiptno' is the column name

        # Execute the update query
        mycursor.execute(sql)
        # Commit the transaction
        mydb.commit()
        # Close the database connection
        mydb.close()

        return True  # Return True indicating successful update
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False  # Return False indicating update failure
    
class DataTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")
        self.stored_dataframe = pd.DataFrame()

        # Configure Treeview style
        style = ttk.Style()
        style.theme_use("clam")  # Change the theme to 'clam' or any other theme available
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black")  # Set colors for Treeview

        # Style configuration for columns
        style.configure("Bold.Treeview.Heading", font=("TkDefaultFont", 9, "bold"))

    def set_datatable(self, dataframe):
        self.stored_dataframe = dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        self.delete(*self.get_children())
        columns = list(dataframe.columns)
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        for col in columns:
            self.heading(col, text=col, anchor="center")  # Apply the bold style to column headers
            self.tag_configure("Bold.Treeview.Heading", font=("TkDefaultFont", 9, "bold"))

            # Set width based on the length of the column name
            column_width = max(len(col) * 10, 10)  # Set a minimum width of 100 (adjust as needed)
            self.column(col, width=column_width, anchor="center")

        df_rows = dataframe.to_numpy().tolist()
        for row in df_rows:
            self.insert("", "end", values=row)

    def reset_table(self):
        self._draw_table(self.stored_dataframe)

    def fetch_data_from_database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345678',
                database='sys'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM Maintenance_View"
                cursor.execute(query)
                rows = cursor.fetchall()

                # Get column names
                columns = [col[0] for col in cursor.description]

                # Create DataFrame from fetched rows and columns
                dataframe = pd.DataFrame(rows, columns=columns)
                self.set_datatable(dataframe)

        except mysql.connector.Error as error:
            print("Error connecting to the database:", error)

        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

class SearchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        try:
            image_path = "C:/Users/ADIL TRADERS/Desktop/images/a2.jpg"
            image = Image.open(image_path)
            resized_image = image.resize((400, 1070))
            photo = ImageTk.PhotoImage(resized_image)

            image_label = tk.Label(parent, image=photo)
            image_label.image = photo  # Necessary to prevent the image from being garbage collected
            image_label.place(relx=0, rely=0, relwidth=0.2, relheight=1)  # Adjust placement and size

        except FileNotFoundError as e:
            print(f"File not found: {e}")

        # Treeview (DataTable)
        self.data_table = DataTable(parent)
        self.data_table.place(rely=0, relx=0.2, relwidth=0.8, relheight=1)  # Adjust the relx, relwidth, and relheight values

        self.path_map = {}
        
        # Fetch data when SearchPage initializes
        self.data_table.fetch_data_from_database()

    def search_table(self, event):
        entry = self.search_entrybox.get()
        if entry == "":
            self.data_table.reset_table()
        else:
            entry_split = entry.split(",")
            column_value_pairs = {}
            for pair in entry_split:
                pair_split = pair.split("=")
                if len(pair_split) == 2:
                    col = pair_split[0]
                    lookup_value = pair_split[1]
                    column_value_pairs[col] = lookup_value
            self.data_table.find_value(pairs=column_value_pairs)

class DataTable1(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")
        self.stored_dataframe = pd.DataFrame()

        # Configure Treeview style
        style = ttk.Style()
        style.theme_use("clam")  # Change the theme to 'clam' or any other theme available
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black")  # Set colors for Treeview

        # Style configuration for columns
        style.configure("Bold.Treeview.Heading", font=("TkDefaultFont", 9, "bold"))

    def set_datatable(self, dataframe):
        self.stored_dataframe = dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        self.delete(*self.get_children())
        columns = list(dataframe.columns)
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        for col in columns:
            self.heading(col, text=col, anchor="center")  # Apply the bold style to column headers
            self.tag_configure("Bold.Treeview.Heading", font=("TkDefaultFont", 9, "bold"))

            # Set width based on the length of the column name
            column_width = max(len(col) * 10, 20)  # Set a minimum width of 100 (adjust as needed)
            self.column(col, width=column_width, anchor="center")

        df_rows = dataframe.to_numpy().tolist()
        for row in df_rows:
            self.insert("", "end", values=row)

    def reset_table(self):
        self._draw_table(self.stored_dataframe)

    def fetch_data_from_database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345678',
                database='sys'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM Halls"
                cursor.execute(query)
                rows = cursor.fetchall()

                # Get column names
                columns = [col[0] for col in cursor.description]

                # Create DataFrame from fetched rows and columns
                dataframe = pd.DataFrame(rows, columns=columns)
                self.set_datatable(dataframe)

        except mysql.connector.Error as error:
            print("Error connecting to the database:", error)

        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

class SearchPage1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        try:
            image_path = "C:/Users/ADIL TRADERS/Desktop/images/a2.jpg"
            image = Image.open(image_path)
            resized_image = image.resize((400, 1050))
            photo = ImageTk.PhotoImage(resized_image)

            image_label = tk.Label(parent, image=photo)
            image_label.image = photo  # Necessary to prevent the image from being garbage collected
            image_label.place(relx=0, rely=0, relwidth=0.2, relheight=1)  # Adjust placement and size

        except FileNotFoundError as e:
            print(f"File not found: {e}")

        # Treeview (DataTable)
        self.data_table = DataTable1(parent)
        self.data_table.place(rely=0, relx=0.2, relwidth=0.8, relheight=1)  # Adjust the relx, relwidth, and relheight values

        self.path_map = {}
        
        # Fetch data when SearchPage initializes
        self.data_table.fetch_data_from_database()

    def search_table(self, event):
        entry = self.search_entrybox.get()
        if entry == "":
            self.data_table.reset_table()
        else:
            entry_split = entry.split(",")
            column_value_pairs = {}
            for pair in entry_split:
                pair_split = pair.split("=")
                if len(pair_split) == 2:
                    col = pair_split[0]
                    lookup_value = pair_split[1]
                    column_value_pairs[col] = lookup_value
            self.data_table.find_value(pairs=column_value_pairs)

class DataTable2(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")
        self.stored_dataframe = pd.DataFrame()

        # Configure Treeview style
        style = ttk.Style()
        style.theme_use("clam")  # Change the theme to 'clam' or any other theme available
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black")  # Set colors for Treeview

        # Style configuration for columns
        style.configure("Bold.Treeview.Heading", font=("TkDefaultFont", 9, "bold"))

    def set_datatable(self, dataframe):
        self.stored_dataframe = dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        self.delete(*self.get_children())
        columns = list(dataframe.columns)
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        for col in columns:
            self.heading(col, text=col, anchor="center")  # Apply the bold style to column headers
            self.tag_configure("Bold.Treeview.Heading", font=("TkDefaultFont", 9, "bold"))

            # Set width based on the length of the column name
            column_width = max(len(col) * 10, 20)  # Set a minimum width of 100 (adjust as needed)
            self.column(col, width=column_width, anchor="center")

        df_rows = dataframe.to_numpy().tolist()
        for row in df_rows:
            self.insert("", "end", values=row)

    def reset_table(self):
        self._draw_table(self.stored_dataframe)

    def fetch_data_from_database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345678',
                database='sys'
            )

            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM Maintenance"
                cursor.execute(query)
                rows = cursor.fetchall()

                # Get column names
                columns = [col[0] for col in cursor.description]

                # Create DataFrame from fetched rows and columns
                dataframe = pd.DataFrame(rows, columns=columns)
                self.set_datatable(dataframe)

        except mysql.connector.Error as error:
            print("Error connecting to the database:", error)

        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

class SearchPage2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        try:
            image_path = "C:/Users/ADIL TRADERS/Desktop/images/a2.jpg"
            image = Image.open(image_path)
            resized_image = image.resize((400, 1050))
            photo = ImageTk.PhotoImage(resized_image)

            image_label = tk.Label(parent, image=photo)
            image_label.image = photo  # Necessary to prevent the image from being garbage collected
            image_label.place(relx=0, rely=0, relwidth=0.2, relheight=1)  # Adjust placement and size

        except FileNotFoundError as e:
            print(f"File not found: {e}")

        # Treeview (DataTable)
        self.data_table = DataTable2(parent)
        self.data_table.place(rely=0, relx=0.2, relwidth=0.8, relheight=1)  # Adjust the relx, relwidth, and relheight values

        self.path_map = {}
        
        # Fetch data when SearchPage initializes
        self.data_table.fetch_data_from_database()

    def search_table(self, event):
        entry = self.search_entrybox.get()
        if entry == "":
            self.data_table.reset_table()
        else:
            entry_split = entry.split(",")
            column_value_pairs = {}
            for pair in entry_split:
                pair_split = pair.split("=")
                if len(pair_split) == 2:
                    col = pair_split[0]
                    lookup_value = pair_split[1]
                    column_value_pairs[col] = lookup_value
            self.data_table.find_value(pairs=column_value_pairs)

class LoginPage:
    def __init__(self, window):
        self.window = window
        self.window.geometry('1166x718')
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.title('Login Page')

        self.bg_frame_image = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        self.bg_frame_photo = ImageTk.PhotoImage(self.bg_frame_image)
        self.bg_frame_photo = None
        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=480, y=250)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ========================================================================
        # ============ Left Side Image ===========================================
        # ========================================================================
        self.side_image = Image.open('C:/Users/ADIL TRADERS/Desktop/images/vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        self.sign_in_image = Image.open('C:/Users/ADIL TRADERS/Desktop/images/hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('C:/Users/ADIL TRADERS/Desktop/images/username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ========================================================================
        # ============================password====================================
        # ========================================================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ====================================================
        self.password_icon = Image.open('C:/Users/ADIL TRADERS/Desktop/images/password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        # ========= show/hide password ===============================================
        self.show_image = ImageTk.PhotoImage \
            (file='C:/Users/ADIL TRADERS/Desktop/images/show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='C:/Users/ADIL TRADERS/Desktop/images/hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        self.lgn_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
        self.login.place(x=20, y=10)
        self.login.config(command=self.check_login)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')


    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":
            self.open_new_window()
        else:
            self.show_invalid_login()

    def open_new_window(self):
        self.window.destroy()  # Close current login window
        self.new_window = Tk()
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('APARTMENT MANAGEMENT SYSTEM')

        bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(bg_frame)
        bg_panel = Label(self.new_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')

        # Place the label for 'Login Successful!'
        self.logined = Label(self.new_window, text='Login Successfully!', font=("yu gothic ui", 20,"bold"), bg='#040405', fg='white')
        self.logined.place(x=850, y=100)

        # ====== Login Frame =========================
        self.frame = Frame(self.new_window, bg='#040405', width=500, height=600)
        self.frame.place(x=720, y=250)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt1 = "WHAT YOU WANT TO DO?"
        self.heading1 = Label(self.frame, text=self.txt1, font=('yu gothic ui', 20, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading1.place(x=80, y=30, width=350, height=50)

        # ========================================================================
        # ============================insert button===============================
        # ========================================================================
        self.ins_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/btn1.png')
        photo = ImageTk.PhotoImage(self.ins_button)
        self.ins_button_label = Label(self.frame, image=photo, bg='#040405')
        self.ins_button_label.image = photo
        self.ins_button_label.place(x=100, y=100)
        self.insert = Button(self.ins_button_label, text='INSERT', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.open_insert_window)
        self.insert.place(x=20, y=10)  # Insert button  # Insert button

        # ========================================================================
        # ============================delete button===============================
        # ========================================================================
        self.del_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/btn1.png')
        photo = ImageTk.PhotoImage(self.del_button)
        self.del_button_label = Label(self.frame, image=photo, bg='#040405')
        self.del_button_label.image = photo
        self.del_button_label.place(x=100, y=200)
        self.delete = Button(self.del_button_label, text='DELETE', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.delete_action)
        self.delete.place(x=20, y=10)
        # ========================================================================
        # ============================update button===============================
        # ========================================================================
        self.upd_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/btn1.png')
        photo = ImageTk.PhotoImage(self.upd_button)
        self.upd_button_label = Label(self.frame, image=photo, bg='#040405')
        self.upd_button_label.image = photo
        self.upd_button_label.place(x=100, y=300)
        self.update = Button(self.upd_button_label, text='UPDATE', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.update_action)
        self.update.place(x=20, y=10)
        # ========================================================================
        # ============================view button===============================
        # ========================================================================
        self.view_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/btn1.png')
        photo = ImageTk.PhotoImage(self.view_button)
        self.view_button_label = Label(self.frame, image=photo, bg='#040405')
        self.view_button_label.image = photo
        self.view_button_label.place(x=100, y=400)
        self.view = Button(self.view_button_label, text='VIEW', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.view_action)
        self.view.place(x=20, y=10)
        # ========================================================================
        # ============================report button===============================
        # ========================================================================
        self.rep_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/btn1.png')
        photo = ImageTk.PhotoImage(self.rep_button)
        self.rep_button_label = Label(self.frame, image=photo, bg='#040405')
        self.rep_button_label.image = photo
        self.rep_button_label.place(x=100, y=500)
        self.report = Button(self.rep_button_label, text='REPORT', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.report_action)
        self.report.place(x=20, y=10)

        self.new_window.mainloop()

    def back_to_previous_window(self):
        if self.new_window:
            self.new_window.destroy()
        self.new_window = self.current_window

    # ========================================================================
    # ============================insert window===============================
    # ========================================================================
    def open_insert_window(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Insert Data')

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(bg_frame)
        bg_panel = Label(self.new_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')
        # ============================ Frame ================================
        frame5 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame5.place(x=480, y=250)

        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Desktop/images/framedes.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(frame5, image=photo , bg='#040405')
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt2 = "IN WHICH TABLE YOU WANT TO INSERT?"
        self.heading2 = Label(frame5, text=self.txt2, font=('intro rust', 20, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading2.place(x=10, y=30, width=580, height=50)

        # ======================================================================
        # ============================halls button===============================
        # =======================================================================
        self.hall_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.hall_button)
        self.hall_button_label = Label(frame5, image=photo, bg='#040405')
        self.hall_button_label.image = photo
        self.hall_button_label.place(x=150, y=150)
        self.hall = Button(self.hall_button_label, text='HALLS', font=("yu gothic ui", 13, "bold"), width=15, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.hall_insert)
        self.hall.place(x=70, y=10)  # Insert button  # Insert button

        # ========================================================================
        # ============================maintenance button==========================
        # ========================================================================
        self.main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.main_button)
        self.main_button_label = Label(frame5, image=photo, bg='#040405')
        self.main_button_label.image = photo
        self.main_button_label.place(x=150, y=250)
        self.maintenance = Button(self.main_button_label, text='MAINTENANCE', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.maintenance_insert)
        self.maintenance.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame5, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=683, y=538)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    # ========================================================================
    # ============================halls window================================
    # ========================================================================
    def hall_insert(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Insert Data')

        bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(bg_frame)
        bg_panel = Label(self.new_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')

        frame5 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame5.place(x=480, y=250)

        # ========================================================================
        # ============ right Side Image ==========================================
        # ========================================================================
        side_image = Image.open('C:/Users/ADIL TRADERS/Desktop/images/anim.png')
        photo = ImageTk.PhotoImage(side_image)
        side_image_label = Label(frame5, image=photo, bg='#040405')
        side_image_label.image = photo
        side_image_label.place(x=450, y=70)

        # ================ Header Text Left ====================
        headerText_image_left = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/headerText_image.png")
        headerText_image_label1 = Label(
            frame5,
            image=headerText_image_left,
            bg="#040405"
        )
        headerText1 = Label(
            frame5,
            text="HALLS BOOKING DETAILS",
            fg="#FFFFFF",
            font=("cooper black", 40 * -1,"bold"),
            bg="#040405"
        )
        headerText1.place(x=80, y=45)

        # ================ Header Text Left ====================
        headerText_image_left = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/headerText_image.png")
        headerText_image_label1 = Label(
            frame5,
            image=headerText_image_left,
            bg="#040405"
        )
        headerText1 = Label(
            frame5,
            text="HALLS BOOKING DETAILS",
            fg="#FFFFFF",
            font=("cooper black", 40 * -1,"bold"),
            bg="#040405"
        )
        headerText1.place(x=80, y=45)

        # ================ Hall Number Section ====================
        self.hallNo_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.hallNo_image = ImageTk.PhotoImage(self.hallNo_image_pil)
        
        # Create label and place it
        self.hallNo_image_Label = Label(
            frame5,
            image=self.hallNo_image,
            bg="#040405"
        )
        self.hallNo_image_Label.place(x=80, y=150)
        
        # Create a label for text
        self.hallNo_text = Label(
            self.hallNo_image_Label,
            text="Hall Number",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.hallNo_text.place(x=25, y=0)
        
        # Create an entry field
        hallNo_entry = Entry(
            self.hallNo_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1)
        )
        hallNo_entry.place(x=25, y=17, width=140, height=27)

        # ================ Booking ID Section ====================
        self.bookingID_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.bookingID_image = ImageTk.PhotoImage(self.bookingID_image_pil)

        # Create label and place it
        self.bookingID_image_Label = Label(
            frame5,
            image=self.bookingID_image,
            bg="#040405"
        )
        self.bookingID_image_Label.place(x=293, y=150)

        # Create a label for text
        self.bookingID_text = Label(
            self.bookingID_image_Label,
            text="Booking ID",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.bookingID_text.place(x=25, y=0)

        # Create an entry field
        bookingID_entry = Entry(
            self.bookingID_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1)
        )
        bookingID_entry.place(x=25, y=17, width=140, height=27)

        # ================ Date of Booking Section ====================
        self.dateofbooking_image = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.dateofbooking_image_Label = Label(
            frame5,
            image=self.dateofbooking_image,
            bg="#040405"
        )
        self.dateofbooking_image_Label.place(x=80, y=220)

        self.dateofbooking_text = Label(
            self.dateofbooking_image_Label,
            text="Date of Booking",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13 * -1),
            bg="#3D404B"
        )
        self.dateofbooking_text.place(x=25, y=-0)

        dateofbooking_entry = Entry(
            self.dateofbooking_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1),
        )
        dateofbooking_entry.place(x=25, y=17, width=140, height=27)

        # ================ Duration Section ====================
        self.duration_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.duration_image = ImageTk.PhotoImage(self.duration_image_pil)

        # Create label and place it
        self.duration_image_Label = Label(
            frame5,
            image=self.duration_image,
            bg="#040405"
        )
        self.duration_image_Label.place(x=293, y=220)

        # Create a label for text
        self.duration_text = Label(
            self.duration_image_Label,
            text="Duration",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.duration_text.place(x=25, y=0)

        # Create an entry field
        duration_entry = Entry(
            self.duration_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1)
        )
        duration_entry.place(x=25, y=17, width=140, height=27)

        # ================ Flat ID Section ====================
        self.flatid_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.flatid_image = ImageTk.PhotoImage(self.flatid_image_pil)

        # Create label and place it
        self.flatid_image_Label = Label(
            frame5,
            image=self.flatid_image,
            bg="#040405"
        )
        self.flatid_image_Label.place(x=80, y=290)

        # Create a label for text
        self.flatid_text = Label(
            self.flatid_image_Label,
            text="Flat ID",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.flatid_text.place(x=25, y=0)

        # Create an entry field
        flatid_entry = Entry(
            self.flatid_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1)
        )
        flatid_entry.place(x=25, y=17, width=140, height=27)

        # ================ Time Section ====================
        self.time_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.time_image = ImageTk.PhotoImage(self.time_image_pil)

        # Create label and place it
        self.time_image_Label = Label(
            frame5,
            image=self.time_image,
            bg="#040405"
        )
        self.time_image_Label.place(x=80, y=360)

        # Create a label for text
        self.time_text = Label(
            self.time_image_Label,
            text="Time",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.time_text.place(x=25, y=0)

        # Create an entry field
        time_entry = Entry(
            self.time_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1)
        )
        time_entry.place(x=25, y=17, width=140, height=27)

        # =============== Submit Button (Modified) ====================
        def clear_entries():
            hallNo_entry.delete(0, END)
            bookingID_entry.delete(0, END)
            dateofbooking_entry.delete(0, END)
            duration_entry.delete(0, END)
            flatid_entry.delete(0, END)
            time_entry.delete(0, END)

        def submit_data():
            hallno = hallNo_entry.get()
            bookingid = bookingID_entry.get()
            dateofbooking = dateofbooking_entry.get()
            duration = duration_entry.get()
            flatid = flatid_entry.get()
            time = time_entry.get()

            insert_data1(hallno, bookingid, dateofbooking, duration, flatid, time)
            clear_entries()

        main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(main_button)
        main_button_label = Label(frame5, image=photo, bg='#040405')
        main_button_label.image = photo
        main_button_label.place(x=80, y=450)
        submit = Button(main_button_label, text='ADD DETAILS', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=submit_data)
        submit.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame5, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=730, y=520)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    # ========================================================================
    # ============================maintenance window==========================
    # ========================================================================
    def maintenance_insert(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Insert Data')

        bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(bg_frame)
        bg_panel = Label(self.new_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')

        frame6 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame6.place(x=480, y=250)
        
        # ========================================================================
        # ============ right Side Image ==========================================
        # ========================================================================
        side_image = Image.open('C:/Users/ADIL TRADERS/Desktop/images/anim.png')
        photo = ImageTk.PhotoImage(side_image)
        side_image_label = Label(frame6, image=photo, bg='#040405')
        side_image_label.image = photo
        side_image_label.place(x=450, y=70)

        # ================ Header Text Left ====================
        headerText_image_left = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/headerText_image.png")
        headerText_image_label1 = Label(
            frame6,
            image=headerText_image_left,
            bg="#040405"
        )
        headerText1 = Label(
            frame6,
            text="MAINTENANCE RECORD",
            fg="#FFFFFF",
            font=("cooper black", 40 * -1, "bold"),
            bg="#040405"
        )
        headerText1.place(x=80, y=45)

        # ================ Reciptno Section ====================
        self.reciptNo_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.reciptNo_image = ImageTk.PhotoImage(self.reciptNo_image_pill)

        self.reciptNo_image_Label = Label(
            frame6,
            image=self.reciptNo_image,
            bg="#040405"
        )
        self.reciptNo_image_Label.place(x=80, y=150)

        self.reciptNo_text = Label(
            self.reciptNo_image_Label,
            text="Receipt No",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.reciptNo_text.place(x=25, y=0)

        reciptNo_entry = Entry(
            self.reciptNo_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        reciptNo_entry.place(x=25, y=17, width=140, height=27)

        # ================ Payment Date Section ====================
        self.paymentDate_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.paymentDate_image = ImageTk.PhotoImage(self.paymentDate_image_pill)

        self.paymentDate_image_Label = Label(
            frame6,
            image=self.paymentDate_image,
            bg="#040405"
        )
        self.paymentDate_image_Label.place(x=293, y=150)

        self.paymentDate_text = Label(
            self.paymentDate_image_Label,
            text="Payment Date",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.paymentDate_text.place(x=25, y=0)

        paymentDate_entry = Entry(
            self.paymentDate_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        paymentDate_entry.place(x=25, y=17, width=140, height=27)

        # ================ Property Type Section ====================
        self.propertyType_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.propertyType_image = ImageTk.PhotoImage(self.propertyType_image_pill)

        self.propertyType_image_Label = Label(
            frame6,
            image=self.propertyType_image,
            bg="#040405"
        )
        self.propertyType_image_Label.place(x=80, y=220)

        self.propertyType_text = Label(
            self.propertyType_image_Label,
            text="Property Type",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.propertyType_text.place(x=25, y=0)

        propertyType_entry = Entry(
            self.propertyType_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        propertyType_entry.place(x=25, y=17, width=140, height=27)

        # ================ Property ID Section ====================
        self.propertyID_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.propertyID_image = ImageTk.PhotoImage(self.propertyID_image_pill)

        self.propertyID_image_Label = Label(
            frame6,
            image=self.propertyID_image,
            bg="#040405"
        )
        self.propertyID_image_Label.place(x=293, y=220)

        self.propertyID_text = Label(
            self.propertyID_image_Label,
            text="Property ID",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.propertyID_text.place(x=25, y=0)

        propertyID_entry = Entry(
            self.propertyID_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        propertyID_entry.place(x=25, y=17, width=140, height=27)

        # ================ Amount Section ====================
        self.amount_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.amount_image = ImageTk.PhotoImage(self.amount_image_pill)

        self.amount_image_Label = Label(
            frame6,
            image=self.amount_image,
            bg="#040405"
        )
        self.amount_image_Label.place(x=80, y=290)

        self.amount_text = Label(
            self.amount_image_Label,
            text="Amount",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.amount_text.place(x=25, y=0)

        amount_entry = Entry(
            self.amount_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        amount_entry.place(x=25, y=17, width=140, height=27)

        # ================ GENERATOR FACILITY Section ====================
        self.facility_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.facility_image = ImageTk.PhotoImage(self.facility_image_pill)

        self.facility_image_Label = Label(
            frame6,
            image=self.facility_image,
            bg="#040405"
        )
        self.facility_image_Label.place(x=80, y=360)

        self.facility_text = Label(
            self.facility_image_Label,
            text="Generator",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.facility_text.place(x=25, y=0)

        facility_entry = Entry(
            self.facility_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        facility_entry.place(x=25, y=17, width=140, height=27)

        def clear_entries():
            reciptNo_entry.delete(0, END)
            paymentDate_entry.delete(0, END)
            propertyType_entry.delete(0, END)
            propertyID_entry.delete(0, END)
            amount_entry.delete(0, END)
            facility_entry.delete(0, END)

        # =============== Submit Button (Modified) ====================
        def submit_data():
            reciptno = reciptNo_entry.get()
            paymentdate = paymentDate_entry.get()
            propertytype = propertyType_entry.get()
            propertyid = propertyID_entry.get()
            amount = amount_entry.get()
            facility = facility_entry.get()

            insert_data2(reciptno, paymentdate, propertytype, propertyid, amount, facility)
            clear_entries()
            # Do something with the collected data, like storing it or processing it

        main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(main_button)
        main_button_label = Label(frame6, image=photo, bg='#040405')
        main_button_label.image = photo
        main_button_label.place(x=80, y=450)
        
        submit = Button(main_button_label, text='ADD DETAILS', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=submit_data)
        submit.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame6, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=730, y=520)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    def delete_action(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Delete Data')

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(bg_frame)
        bg_panel = Label(self.new_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')
        # ============================ Frame ================================
        frame5 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame5.place(x=480, y=250)

        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Desktop/images/framedes.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(frame5, image=photo , bg='#040405')
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt2 = "IN WHICH TABLE YOU WANT TO DELETE?"
        self.heading2 = Label(frame5, text=self.txt2, font=('intro rust', 20, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading2.place(x=10, y=30, width=580, height=50)

        # ======================================================================
        # ============================halls button===============================
        # =======================================================================
        self.hall_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.hall_button)
        self.hall_button_label = Label(frame5, image=photo, bg='#040405')
        self.hall_button_label.image = photo
        self.hall_button_label.place(x=150, y=150)
        self.hall = Button(self.hall_button_label, text='HALLS', font=("yu gothic ui", 13, "bold"), width=15, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.hall_delete)
        self.hall.place(x=70, y=10)  # Insert button  # Insert button

        # ========================================================================
        # ============================maintenance button==========================
        # ========================================================================
        self.main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.main_button)
        self.main_button_label = Label(frame5, image=photo, bg='#040405')
        self.main_button_label.image = photo
        self.main_button_label.place(x=150, y=250)
        self.maintenance = Button(self.main_button_label, text='MAINTENANCE', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.maintenance_delete)
        self.maintenance.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame5, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=683, y=538)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55 , y=10)

    # ========================================================================
    # =============================hall delete window=========================
    # ========================================================================
    def hall_delete(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Delete Data')

        global bookid_entry  # Access the global variable bookid_entry

        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.new_window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        frame4 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame4.place(x=480, y=250)

        # ========================================================================
        # ============ right Side Image ==========================================
        # ========================================================================
        self.side_image = Image.open('C:/Users/ADIL TRADERS/Desktop/images/sideimg.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(frame4, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=380, y=70)

        # ================ Header Text Left ====================
        headerText_image_left = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/headerText_image.png")
        headerText_image_label1 = Label(
            frame4,
            image=headerText_image_left,
            bg="#040405"
        )
        headerText1 = Label(
            frame4,
            text="DELETE RECORD",
            fg="#FFFFFF",
            font=("cooper black", 40 * -1,"bold"),
            bg="#040405"
        )
        headerText1.place(x=80, y=70)

        self.bookid_image = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.bookid_image = ImageTk.PhotoImage(self.bookid_image)

        self.bookid_image_Label = Label(
            frame4,
            image=self.bookid_image,
            bg="#040405"
        )
        self.bookid_image_Label.place(x=80, y=150)

        self.bookid_text = Label(
            self.bookid_image_Label,
            text="BOOKING ID",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.bookid_text.place(x=25, y=0)

        bookid_entry = Entry(
            self.bookid_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        bookid_entry.place(x=25, y=17, width=140, height=27)

        self.main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.main_button)
        self.main_button_label = Label(frame4, image=photo, bg='#040405')
        self.main_button_label.image = photo
        self.main_button_label.place(x=80, y=400)
        # Inside create_window function, modify the submit Button command to call on_delete_button_click
        submit = Button(self.main_button_label, text='DELETE', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',
                        command=on_delete_button_click)
        submit.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame4, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=730, y=520)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55 , y=10)

    # ========================================================================
    # =======================maintenance delete window========================
    # ========================================================================
    def maintenance_delete(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Delete Data')

        global receipt_entry  # Access the global variable bookid_entry

        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.new_window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        frame4 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame4.place(x=480, y=250)

        # ========================================================================
        # ============ right Side Image ==========================================
        # ========================================================================
        self.side_image = Image.open('C:/Users/ADIL TRADERS/Desktop/images/sideimg.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(frame4, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=380, y=70)

        # ================ Header Text Left ====================
        headerText_image_left = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/headerText_image.png")
        headerText_image_label1 = Label(
            frame4,
            image=headerText_image_left,
            bg="#040405"
        )
        headerText1 = Label(
            frame4,
            text="DELETE RECORD",
            fg="#FFFFFF",
            font=("cooper black", 40 * -1,"bold"),
            bg="#040405"
        )
        headerText1.place(x=80, y=70)

        receipt_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.receipt_image = ImageTk.PhotoImage(receipt_image_pil)

        self.receipt_image_Label = Label(
            frame4,
            image=self.receipt_image,
            bg="#040405"
        )
        self.receipt_image_Label.place(x=80, y=150)

        self.receipt_text = Label(
            self.receipt_image_Label,
            text="RECEIPT NO",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.receipt_text.place(x=25, y=0)

        receipt_entry = Entry(
            self.receipt_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        receipt_entry.place(x=25, y=17, width=140, height=27)

        self.main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.main_button)
        self.main_button_label = Label(frame4, image=photo, bg='#040405')
        self.main_button_label.image = photo
        self.main_button_label.place(x=80, y=400)
        # Inside create_window function, modify the submit Button command to call on_delete_button_click
        submit = Button(self.main_button_label, text='DELETE', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',
                        command=on_delete_button_click1)
        submit.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame4, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=683, y=538)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55 , y=10)

    def update_action(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('UPDATE RECORD')

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(bg_frame)
        bg_panel = Label(self.new_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')
        # ============================ Frame ================================
        frame5 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame5.place(x=480, y=250)

        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Desktop/images/framedes.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(frame5, image=photo , bg='#040405')
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt2 = "IN WHICH TABLE YOU WANT TO UPDATE?"
        self.heading2 = Label(frame5, text=self.txt2, font=('intro rust', 20, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading2.place(x=10, y=30, width=580, height=50)

        # ======================================================================
        # ============================halls button===============================
        # =======================================================================
        self.hall_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.hall_button)
        self.hall_button_label = Label(frame5, image=photo, bg='#040405')
        self.hall_button_label.image = photo
        self.hall_button_label.place(x=150, y=150)
        self.hall = Button(self.hall_button_label, text='HALLS', font=("yu gothic ui", 13, "bold"), width=15, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.hall_update)
        self.hall.place(x=70, y=10)  # Insert button  # Insert button

        # ========================================================================
        # ============================maintenance button==========================
        # ========================================================================
        self.main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.main_button)
        self.main_button_label = Label(frame5, image=photo, bg='#040405')
        self.main_button_label.image = photo
        self.main_button_label.place(x=150, y=250)
        self.maintenance = Button(self.main_button_label, text='MAINTENANCE', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.maintenance_update)
        self.maintenance.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame5, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=683, y=538)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    # ========================================================================
    # ============================Hall Update window==========================
    # ========================================================================
    def hall_update(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('UPDATE')

        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.new_window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        frame4 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame4.place(x=480, y=250)

        # ========================================================================
        # ============ right Side Image ==========================================
        # ========================================================================
        self.side_image = Image.open('C:/Users/ADIL TRADERS/Desktop/images/anim.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(frame4, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=450, y=70)

        # ================ Header Text Left ====================
        headerText_image_left = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/headerText_image.png")
        headerText_image_label1 = Label(
            frame4,
            image=headerText_image_left,
            bg="#040405"
        )
        headerText1 = Label(
            frame4,
            text="UPDATE BOOKING DETAILS",
            fg="#FFFFFF",
            font=("cooper black", 40 * -1,"bold"),
            bg="#040405"
        )
        headerText1.place(x=80, y=45)

        # ================ Booking ID Section ====================
        self.bookingID_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.bookingID_image = ImageTk.PhotoImage(self.bookingID_image_pil)

        # Create label and place it
        self.bookingID_image_Label = Label(
            frame4,
            image=self.bookingID_image,
            bg="#040405"
        )
        self.bookingID_image_Label.place(x=293, y=150)

        # Create a label for text
        self.bookingID_text = Label(
            self.bookingID_image_Label,
            text="Booking ID",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.bookingID_text.place(x=25, y=0)

        # Create an entry field
        bookingID_entry = Entry(
            self.bookingID_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1)
        )
        bookingID_entry.place(x=25, y=17, width=140, height=27)

        # ================ Hall Number Section ====================
        self.hallNo_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.hallNo_image = ImageTk.PhotoImage(self.hallNo_image_pil)
        
        # Create label and place it
        self.hallNo_image_Label = Label(
            frame4,
            image=self.hallNo_image,
            bg="#040405"
        )
        self.hallNo_image_Label.place(x=80, y=150)
        
        # Create a label for text
        self.hallNo_text = Label(
            self.hallNo_image_Label,
            text="Hall Number",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.hallNo_text.place(x=25, y=0)
        
        # Create an entry field
        hallNo_entry = Entry(
            self.hallNo_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1)
        )
        hallNo_entry.place(x=25, y=17, width=140, height=27)

        # ================ Date of Booking Section ====================
        self.dateofbooking_image = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.dateofbooking_image_Label = Label(
            frame4,
            image=self.dateofbooking_image,
            bg="#040405"
        )
        self.dateofbooking_image_Label.place(x=80, y=220)

        self.dateofbooking_text = Label(
            self.dateofbooking_image_Label,
            text="Date of Booking",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13 * -1),
            bg="#3D404B"
        )
        self.dateofbooking_text.place(x=25, y=-0)

        dateofbooking_entry = Entry(
            self.dateofbooking_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1),
        )
        dateofbooking_entry.place(x=25, y=17, width=140, height=27)

        # ================ Duration Section ====================
        self.duration_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.duration_image = ImageTk.PhotoImage(self.duration_image_pil)

        # Create label and place it
        self.duration_image_Label = Label(
            frame4,
            image=self.duration_image,
            bg="#040405"
        )
        self.duration_image_Label.place(x=293, y=220)

        # Create a label for text
        self.duration_text = Label(
            self.duration_image_Label,
            text="Duration",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.duration_text.place(x=25, y=0)

        # Create an entry field
        duration_entry = Entry(
            self.duration_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1)
        )
        duration_entry.place(x=25, y=17, width=140, height=27)

        # ================ Flat ID Section ====================
        self.flatid_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.flatid_image = ImageTk.PhotoImage(self.flatid_image_pil)

        # Create label and place it
        self.flatid_image_Label = Label(
            frame4,
            image=self.flatid_image,
            bg="#040405"
        )
        self.flatid_image_Label.place(x=80, y=290)

        # Create a label for text
        self.flatid_text = Label(
            self.flatid_image_Label,
            text="Flat ID",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.flatid_text.place(x=25, y=0)

        # Create an entry field
        flatid_entry = Entry(
            self.flatid_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1)
        )
        flatid_entry.place(x=25, y=17, width=140, height=27)

        # ================ Time Section ====================
        self.time_image_pil = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.time_image = ImageTk.PhotoImage(self.time_image_pil)

        # Create label and place it
        self.time_image_Label = Label(
            frame4,
            image=self.time_image,
            bg="#040405"
        )
        self.time_image_Label.place(x=80, y=360)

        # Create a label for text
        self.time_text = Label(
            self.time_image_Label,
            text="Time",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.time_text.place(x=25, y=0)

        # Create an entry field
        time_entry = Entry(
            self.time_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1)
        )
        time_entry.place(x=25, y=17, width=140, height=27)

        # =============== Submit Button (Modified) ====================
        def clear_entries():
            hallNo_entry.delete(0, END)
            bookingID_entry.delete(0, END)
            dateofbooking_entry.delete(0, END)
            duration_entry.delete(0, END)
            flatid_entry.delete(0, END)
            time_entry.delete(0, END)

        def submit_data():
            bookingid = bookingID_entry.get()
            hallno = hallNo_entry.get()
            dateofbooking = dateofbooking_entry.get()
            duration = duration_entry.get()
            flatid = flatid_entry.get()
            time = time_entry.get()

            updated = update_database(bookingid, hallno, dateofbooking, duration, flatid, time)
            if updated:
                messagebox.showinfo("Success", "Data updated successfully!")
                clear_entries()
            else:
                messagebox.showerror("Error", "Failed to update data!")

        main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(main_button)
        main_button_label = Label(frame4, image=photo, bg='#040405')
        main_button_label.image = photo
        main_button_label.place(x=80, y=450)
        submit = Button(main_button_label, text='UPDATE', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=submit_data)
        submit.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame4, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=683, y=538)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)
    
    # ========================================================================
    # =======================maintenance Update window========================
    # ========================================================================
    def maintenance_update(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('UPDATE')

        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.new_window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        frame4 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame4.place(x=480, y=250)
        
        # ========================================================================
        # ============ right Side Image ==========================================
        # ========================================================================
        self.side_image = Image.open('C:/Users/ADIL TRADERS/Desktop/images/anim.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(frame4, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=450, y=70)

        # ================ Header Text Left ====================
        headerText_image_left = PhotoImage(file="C:/Users/ADIL TRADERS/Desktop/images/headerText_image.png")
        headerText_image_label1 = Label(
            frame4,
            image=headerText_image_left,
            bg="#040405"
        )
        headerText1 = Label(
            frame4,
            text="UPDATE MAINTENANCE RECORD",
            fg="#FFFFFF",
            font=("cooper black", 40 * -1, "bold"),
            bg="#040405"
        )
        headerText1.place(x=80, y=45)

        # ================ Reciptno Section ====================
        self.reciptNo_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.reciptNo_image = ImageTk.PhotoImage(self.reciptNo_image_pill)

        self.reciptNo_image_Label = Label(
            frame4,
            image=self.reciptNo_image,
            bg="#040405"
        )
        self.reciptNo_image_Label.place(x=80, y=150)

        self.reciptNo_text = Label(
            self.reciptNo_image_Label,
            text="Receipt No",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.reciptNo_text.place(x=25, y=0)

        reciptNo_entry = Entry(
            self.reciptNo_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        reciptNo_entry.place(x=25, y=17, width=140, height=27)

        # ================ Payment Date Section ====================
        self.paymentDate_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.paymentDate_image = ImageTk.PhotoImage(self.paymentDate_image_pill)

        self.paymentDate_image_Label = Label(
            frame4,
            image=self.paymentDate_image,
            bg="#040405"
        )
        self.paymentDate_image_Label.place(x=293, y=150)

        self.paymentDate_text = Label(
            self.paymentDate_image_Label,
            text="Payment Date",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.paymentDate_text.place(x=25, y=0)

        paymentDate_entry = Entry(
            self.paymentDate_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        paymentDate_entry.place(x=25, y=17, width=140, height=27)

        # ================ Property Type Section ====================
        self.propertyType_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.propertyType_image = ImageTk.PhotoImage(self.propertyType_image_pill)

        self.propertyType_image_Label = Label(
            frame4,
            image=self.propertyType_image,
            bg="#040405"
        )
        self.propertyType_image_Label.place(x=80, y=220)

        self.propertyType_text = Label(
            self.propertyType_image_Label,
            text="Property Type",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.propertyType_text.place(x=25, y=0)

        propertyType_entry = Entry(
            self.propertyType_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        propertyType_entry.place(x=25, y=17, width=140, height=27)

        # ================ Property ID Section ====================
        self.propertyID_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.propertyID_image = ImageTk.PhotoImage(self.propertyID_image_pill)

        self.propertyID_image_Label = Label(
            frame4,
            image=self.propertyID_image,
            bg="#040405"
        )
        self.propertyID_image_Label.place(x=293, y=220)

        self.propertyID_text = Label(
            self.propertyID_image_Label,
            text="Property ID",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.propertyID_text.place(x=25, y=0)

        propertyID_entry = Entry(
            self.propertyID_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        propertyID_entry.place(x=25, y=17, width=140, height=27)

        # ================ Amount Section ====================
        self.amount_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.amount_image = ImageTk.PhotoImage(self.amount_image_pill)

        self.amount_image_Label = Label(
            frame4,
            image=self.amount_image,
            bg="#040405"
        )
        self.amount_image_Label.place(x=80, y=290)

        self.amount_text = Label(
            self.amount_image_Label,
            text="Amount",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.amount_text.place(x=25, y=0)

        amount_entry = Entry(
            self.amount_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        amount_entry.place(x=25, y=17, width=140, height=27)

        # ================ GENERATOR FACILITY Section ====================
        self.facility_image_pill = Image.open("C:/Users/ADIL TRADERS/Desktop/images/input_img.png")
        self.facility_image = ImageTk.PhotoImage(self.facility_image_pill)

        self.facility_image_Label = Label(
            frame4,
            image=self.facility_image,
            bg="#040405"
        )
        self.facility_image_Label.place(x=80, y=360)

        self.facility_text = Label(
            self.facility_image_Label,
            text="Generator",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13*-1),
            bg="#3D404B"
        )
        self.facility_text.place(x=25, y=0)

        facility_entry = Entry(
            self.facility_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16*-1),
        )
        facility_entry.place(x=25, y=17, width=140, height=27)

        def clear_entries():
            reciptNo_entry.delete(0, END)
            paymentDate_entry.delete(0, END)
            propertyType_entry.delete(0, END)
            propertyID_entry.delete(0, END)
            amount_entry.delete(0, END)
            facility_entry.delete(0, END)

        # =============== Submit Button ====================
        def submit_data():
            reciptno = reciptNo_entry.get()
            paymentdate = paymentDate_entry.get()
            propertytype = propertyType_entry.get()
            propertyid = propertyID_entry.get()
            amount = amount_entry.get()
            facility = facility_entry.get()

            if reciptno and update_data(reciptno, paymentdate, propertytype, propertyid, amount, facility):
                clear_entries()
                messagebox.showinfo("Success", "Data updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update data")

        main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(main_button)
        main_button_label = Label(frame4, image=photo, bg='#040405')
        main_button_label.image = photo
        main_button_label.place(x=80, y=450)
        
        submit = Button(main_button_label, text='UPDATE', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white' , command = submit_data)
        submit.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame4, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=683, y=538)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    def view_action(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('View Data')

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        bg_frame = Image.open('C:/Users/ADIL TRADERS/Downloads/ap.png')
        photo = ImageTk.PhotoImage(bg_frame)
        bg_panel = Label(self.new_window, image=photo)
        bg_panel.image = photo
        bg_panel.pack(fill='both', expand='yes')
        # ============================ Frame ================================
        frame5 = Frame(self.new_window, bg='#040405', width=950, height=600)
        frame5.place(x=480, y=250)

        self.bg_frame = Image.open('C:/Users/ADIL TRADERS/Desktop/images/framedes.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(frame5, image=photo , bg='#040405')
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt2 = "WHICH TABLE DATA YOU WANT TO VIEW?"
        self.heading2 = Label(frame5, text=self.txt2, font=('intro rust', 20, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading2.place(x=10, y=30, width=580, height=50)

        # ======================================================================
        # ============================halls button===============================
        # =======================================================================
        self.hall_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.hall_button)
        self.hall_button_label = Label(frame5, image=photo, bg='#040405')
        self.hall_button_label.image = photo
        self.hall_button_label.place(x=150, y=150)
        self.hall = Button(self.hall_button_label, text='HALLS', font=("yu gothic ui", 13, "bold"), width=15, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.hall_view)
        self.hall.place(x=70, y=10)  # Insert button  # Insert button

        # ========================================================================
        # ============================maintenance button==========================
        # ========================================================================
        self.main_button = Image.open('C:/Users/ADIL TRADERS/Desktop/images/arbtn.png')
        photo = ImageTk.PhotoImage(self.main_button)
        self.main_button_label = Label(frame5, image=photo, bg='#040405')
        self.main_button_label.image = photo
        self.main_button_label.place(x=150, y=250)
        self.maintenance = Button(self.main_button_label, text='MAINTENANCE', font=("yu gothic ui", 13, "bold"), width=20, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.maintenance_view)
        self.maintenance.place(x=50, y=10)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(frame5, image=photo, bg='#040405')
        main_button_label1.image = photo
        main_button_label1.place(x=683, y=538)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    def hall_view(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Halls Booking Record')
        self.search_page = SearchPage1(parent=self.new_window)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(self.new_window, image=photo, bg='#4b7939')
        main_button_label1.image = photo
        main_button_label1.place(x=220, y=990)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    def maintenance_view(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Maintenance Record')
        self.search_page = SearchPage2(parent=self.new_window)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(self.new_window, image=photo, bg='#4b7939')
        main_button_label1.image = photo
        main_button_label1.place(x=220, y=990)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    def report_action(self):
        self.current_window = self.new_window
        self.new_window = Toplevel()  # Use Toplevel instead of Tk
        self.new_window.geometry('1166x718')
        self.new_window.resizable(0, 0)
        self.new_window.state('zoomed')
        self.new_window.title('Report')
        self.search_page = SearchPage(parent=self.new_window)

        #====================== Back Button ==================================
        main_button1 = Image.open('C:/Users/ADIL TRADERS/Desktop/images/backbtn.png')
        photo = ImageTk.PhotoImage(main_button1)
        main_button_label1 = Label(self.new_window, image=photo, bg='#4b7939')
        main_button_label1.image = photo
        main_button_label1.place(x=220, y=990)
        submit = Button(main_button_label1, text='BACK', font=("yu gothic ui", 13, "bold"), width=5, bd=0,
                        bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.back_to_previous_window)
        submit.place(x=55, y=10)

    def show_invalid_login(self):
        # Display an error message for invalid login
        messagebox.showerror("Invalid Login", "Invalid username or password. Please try again.")

def page():
    window = Tk()
    LoginPage(window)
    window.mainloop()

if __name__ == '__main__':
    page()