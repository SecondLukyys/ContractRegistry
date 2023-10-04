import tkinter as tk
from tkinter import ttk, IntVar, messagebox
from tkinter import Toplevel
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
from tkinter import filedialog

class ContractRegistryAppWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contract Registry")
        self.geometry("900x600")
        self.resizable(False, False)
        self.database_class_instance = databaseActions()
        self.database_class_instance.initialize_database()
        self.create_widgets()
        
        self.company_name_entry = tk.Entry(self)
        self.company_code_entry = tk.Entry(self)
        self.contract_date_calendar = Calendar(self)
        self.contacts_entry = tk.Entry(self) 
        self.var2 = IntVar(self)
        self.file_data = None

    def create_widgets(self):
        for widget in self.winfo_children():
          widget.destroy()

        center_frame = tk.Frame(self)
        center_frame.pack(expand=True, fill="both", padx=20, pady=20)  # Add padding for centering

        new_entry_button = tk.Button(center_frame, text="New Contract", command=self.open_new_entry_window)
        new_entry_button.pack(fill="x", padx=222, pady=15)

        search_button = tk.Button(center_frame, text="Search Contract", command=self.display_contract_search)
        search_button.pack(fill="x", padx=222, pady=15)

        display_button = tk.Button(center_frame, text="View All Contracts", command=self.display_all_contract_details)
        display_button.pack(fill="x", padx=222, pady=15)

        exit_button = tk.Button(center_frame, text="Exit", command=self.quit)
        exit_button.pack(fill="x", padx=222, pady=15)

    def open_new_entry_window(self):
        for widget in self.winfo_children():
          widget.destroy()

        self.company_name_label = tk.Label(self, text="Company Name:")
        self.company_name_label.pack(fill="x", padx=222, pady=1)
        self.company_name_entry = tk.Entry(self)
        self.company_name_entry.pack(fill="x", padx=222, pady=1)

        self.company_code_label = tk.Label(self, text="Company Code/Contract Id: (This input field works as Unique contract identifier)")
        self.company_code_label.pack(fill="x", padx=222, pady=1)
        self.company_code_entry = tk.Entry(self)
        self.company_code_entry.pack(fill="x", padx=222, pady=1)

        contract_date_label = tk.Label(self, text="Contract Date:")
        contract_date_label.pack(fill="x", padx=222, pady=5)
        self.contract_date_calendar = Calendar(self)
        self.contract_date_calendar.pack(fill="x", padx=222, pady=5)

        contacts_label = tk.Label(app, text="Contacts:")
        contacts_label.pack(fill="x", padx=222, pady=1)
        self.contacts_entry = tk.Entry(app)
        self.contacts_entry.pack(fill="x", padx=222, pady=1)

        file_select_button = tk.Button(self, text="Select Word or Pdf file", command=self.select_file)
        file_select_button.pack(fill="x", padx=222, pady=15)

        add_button = tk.Button(self, text="Add Contract", command=self.add_contract)
        add_button.pack(fill="x", padx=222, pady=15)

        back_button = tk.Button(self, text="Back", command=self.create_widgets)
        back_button.pack(fill="x", padx=222, pady=15)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")])
        if file_path:
            with open(file_path, "rb") as file:
                self.file_data = file.read()
            print("File selected successfully.")
            self.show_warning("File added successfully!")

    def add_contract(self):
        company_name = self.company_name_entry.get()
        company_code = self.company_code_entry.get()
        selected_date_str = self.contract_date_calendar.get_date()
        
        try:
            selected_date = datetime.strptime(selected_date_str, "%d/%m/%y")
        except ValueError:
            print("Invalid date format:", selected_date_str)
            return
        
        date_string = selected_date.strftime("%Y-%m-%d")
        contacts = self.contacts_entry.get()

        if not company_code:
            self.show_warning("Company Code cannot be empty!")
            return

        if self.file_data:
            self.insert_data(company_name, company_code, date_string, contacts, self.file_data)
        else:
            self.insert_data(company_name, company_code, date_string, contacts)
        
    def show_warning(self, message):
        popup_window = tk.Toplevel(self)
        popup_window.title("Warning")
        popup_window.geometry("400x200")

        message_label = tk.Label(popup_window, text=message)
        message_label.pack(pady=20)

        ok_button = tk.Button(popup_window, text="OK", command=popup_window.destroy)
        ok_button.pack()

    def display_contract_search(self):
        for widget in self.winfo_children():
            widget.destroy()

        search_label = tk.Label(self, text="Search contracts by Company Name:")
        search_label.pack(fill="x", padx=222, pady=1)

        search_entry = tk.Entry(self)
        search_entry.pack(fill="x", padx=222, pady=1)

        search_button = tk.Button(self, text="Search", command=lambda: self.search_contracts(search_entry.get()))
        search_button.pack(fill="x", padx=222, pady=15)

        search_button = tk.Button(self, text="Refresh data", command=lambda: self.refresh_contracts(search_entry.get()))
        search_button.pack(fill="x", padx=222, pady=15)

        # Create a listbox to display the contract data
        contract_listbox = tk.Listbox(self, selectmode="extended", height=15)
        contract_listbox.pack(fill="both", padx=10, pady=10)
        
        back_button = tk.Button(self, text="Back", command=self.create_widgets)
        back_button.pack(fill="x", padx=222, pady=15)

        # Define the columns you want to display
        columns = ("Company Code / Contract Id", "Company Name", "Contract Date", "Contacts", "Has file")

        # Fetch and display all contract data in the listbox
        self.display_all_contract_data(contract_listbox)

        # Insert headers for the listbox at the beginning
        contract_listbox.insert(0, " | ".join(columns))

    def refresh_contracts(self, search_term):
        for widget in self.winfo_children():
            widget.destroy()

        search_label = tk.Label(self, text="Search contracts by Company Name:")
        search_label.pack(fill="x", padx=222, pady=1)

        search_entry = tk.Entry(self)
        search_entry.pack(fill="x", padx=222, pady=1)

        search_button = tk.Button(self, text="Search", command=lambda: self.search_contracts(search_entry.get()))
        search_button.pack(fill="x", padx=222, pady=15)

        search_button = tk.Button(self, text="Refresh data", command=lambda: self.refresh_contracts(search_entry.get()))
        search_button.pack(fill="x", padx=222, pady=15)

        # Create a listbox to display the contract data
        contract_listbox = tk.Listbox(self, selectmode="extended", height=15)
        contract_listbox.pack(fill="both", padx=10, pady=10)

        # Define the columns you want to display
        columns = ("Company Code / Contract Id", "Company Name", "Contract Date", "Contacts", "Has file")

        # Insert headers for the listbox at the beginning
        contract_listbox.insert(0, " | ".join(columns))

        # Fetch and display all contract data in the listbox
        self.display_all_contract_data(contract_listbox)

        back_button = tk.Button(self, text="Back", command=self.create_widgets)
        back_button.pack(fill="x", padx=222, pady=15)

    def display_all_contract_data(self, contract_listbox):
        self.conn = sqlite3.connect("ContractRegistry.db")
        self.cursor = self.conn.cursor()

        # Select company_code, company_name, contract_date, contacts, and file_data from the contracts table
        self.cursor.execute("SELECT company_code, company_name, contract_date, contacts, file_data FROM contracts")
        rows = self.cursor.fetchall()

        for row in rows:
            # Extract the file_data from the row
            company_code, company_name, contract_date, contacts, file_data = row

            # Check if file_data is empty
            has_file = "Yes" if file_data else "No"

            # Create the listbox entry with "Yes" or "No" based on file_data
            entry = f"{company_code} | {company_name} | {contract_date} | {contacts} | {has_file}"

            # Insert the entry into the listbox
            contract_listbox.insert("end", entry)

        self.conn.close()

    def search_contracts(self, search_term):
        for widget in self.winfo_children():
            widget.destroy()

        search_label = tk.Label(self, text="Search contracts by Company Name:")
        search_label.pack(fill="x", padx=222, pady=1)

        search_entry = tk.Entry(self)
        search_entry.pack(fill="x", padx=222, pady=1)

        search_button = tk.Button(self, text="Search", command=lambda: self.search_contracts(search_entry.get()))
        search_button.pack(fill="x", padx=222, pady=15)

        search_button = tk.Button(self, text="Refresh data", command=lambda: self.refresh_contracts(search_entry.get()))
        search_button.pack(fill="x", padx=222, pady=15)

        # Create a listbox to display the contract data
        contract_listbox = tk.Listbox(self, selectmode="extended", height=15)
        contract_listbox.pack(fill="both", padx=10, pady=10)

        # Define the columns you want to display
        columns = ("Company Code / Contract Id", "Company Name", "Contract Date", "Contacts", "Has file")

        # Insert headers for the listbox at the beginning
        contract_listbox.insert(0, " | ".join(columns))

        # Fetch and display all contract data in the listbox
        self.display_search_results(contract_listbox, search_term)

        back_button = tk.Button(self, text="Back", command=self.create_widgets)
        back_button.pack(fill="x", padx=222, pady=15)
        

    def display_search_results(self, contract_listbox, search_term):
        self.conn = sqlite3.connect("ContractRegistry.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT company_code, company_name, contract_date, contacts FROM contracts WHERE company_name = ?", (search_term,))
        rows = self.cursor.fetchall()

        if not rows:
            self.show_warning("No matching contracts found.")
            return

        for row in rows:
            contract_listbox.insert("end", " | ".join(map(str, row)))

        self.conn.close()

    def display_all_contract_details(self):
        for widget in self.winfo_children():
            widget.destroy()

        center_frame = tk.Frame(self)
        center_frame.pack(expand=True, fill="both", padx=20, pady=20)

        header_frame = tk.Frame(center_frame)
        header_frame.pack(fill="both", padx=10, pady=10)

        contract_listbox = tk.Listbox(center_frame, selectmode="extended", height=15)
        contract_listbox.pack(fill="both", padx=10, pady=10)

        columns = ("Company Code / Contract Id", "Company Name", "Contract Date", "Contacts")

        for col in columns:
            tk.Label(header_frame, text=col, relief="solid", width=15).pack(side="left")

        self.display_contract_data(contract_listbox)

        back_button = tk.Button(self, text="Back", command=self.create_widgets)
        back_button.pack(fill="x", padx=222, pady=15)

    def display_contract_data(self, contract_listbox):
        self.conn = sqlite3.connect("ContractRegistry.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT company_code, company_name, contract_date, contacts FROM contracts")
        rows = self.cursor.fetchall()

        for row in rows:
            contract_listbox.insert("end", " | ".join(map(str, row)))

        self.conn.close()


    def insert_data(self, company_name, company_code, date_string, contacts, file_data=None):
        self.conn = sqlite3.connect("ContractRegistry.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM contracts WHERE company_code=?", (company_code,))
        existing_details = self.cursor.fetchone()


        if existing_details is not None:
            print("Company code is already in use")
            self.show_warning("Company code is already in use! Try another one")
            self.conn.close()
            return
        
        if file_data:
            self.cursor.execute('''INSERT INTO contracts (company_code, company_name, contract_date, contacts, file_data)
                            VALUES (?, ?, ?, ?, ?)''',
                            (company_code, company_name, date_string, contacts, self.file_data))
            self.show_warning("Contract added successfully with file attached!")
        else:
            self.cursor.execute('''INSERT INTO contracts (company_code, company_name, contract_date, contacts)
                            VALUES (?, ?, ?, ?)''',
                            (company_code, company_name, date_string, contacts))
            self.show_warning("Contract added successfully without file attached!")

        self.cursor.execute("SELECT * FROM contracts")

        rows = self.cursor.fetchall()

        print("Company Code / Contract Id | Company Name | Contract Date | Contacts ")

        for row in rows:
            company_code, company_name, contract_date, contacts, file_data = row
            print(f"{company_code} | {company_name} | {contract_date} | {contacts}")


        self.conn.commit()
        self.conn.close()

class databaseActions():
    def initialize_database(self):
        self.conn = sqlite3.connect("ContractRegistry.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS contracts (
                                company_code TEXT PRIMARY KEY,
                                company_name TEXT,
                                contract_date TEXT,
                                contacts TEXT,
                                file_data BLOB  -- Add a BLOB column for file data
                            )''')
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    app = ContractRegistryAppWindow()
    app.mainloop()