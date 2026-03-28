import customtkinter as ct
from tkinter import ttk, messagebox

class Student:
    def __init__(self, roll, name, phone, gender, address):
        self.roll, self.name, self.phone, self.gender, self.address = roll, name, phone, gender, address

    # Dictionary so save data to the CSV     
    def to_dict(self):
        return {"Roll": self.roll, "Name": self.name, "Phone": self.phone, "Gender": self.gender, "Address": self.address}

class StudentView(ct.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent")
        self.manager, self.selected_index, self.S_Frame = manager, None, None
        self.setup_ui()
        self.show_student_table()

    # UI Setup
    def setup_ui(self):
        # Roll Number Entry
        ct.CTkLabel(self, text="Roll Number:", font=("Arial", 25), text_color="black").place(x=50, y=50)
        self.roll_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.roll_entry.place(x=50, y=90)
        
        # Full Name Entry
        ct.CTkLabel(self, text="Full Name:", font=("Arial", 25), text_color="black").place(x=50, y=140)
        self.name_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.name_entry.place(x=50, y=180)
        
        # Phone Entry
        ct.CTkLabel(self, text="Phone Number:", font=("Arial", 25), text_color="black").place(x=50, y=230)
        self.phone_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.phone_entry.place(x=50, y=270)
        
        # Gender (ComboBox) 
        ct.CTkLabel(self, text="Gender:", font=("Arial", 25), text_color="black").place(x=50, y=320)
        self.gender_combo = ct.CTkComboBox(self, values=["Male", "Female"], font=("Arial", 25), width=400, 
                                           text_color="black", fg_color="white", border_width=1, border_color="black",
                                           dropdown_fg_color="white", dropdown_text_color="black")
        self.gender_combo.place(x=50, y=360)
        
        # Address Entry
        ct.CTkLabel(self, text="Address:", font=("Arial", 25), text_color="black").place(x=50, y=410)
        self.address_entry = ct.CTkTextbox(self, font=("Arial", 25), height=100, width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.address_entry.place(x=50, y=450)

        # Buttons
        btn_frame = ct.CTkFrame(self, fg_color="transparent")
        btn_frame.place(x=50, y=570)
        ct.CTkButton(btn_frame, text="Save", width=100, font=("Arial", 25), command=self.save_student).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Update", width=100, font=("Arial", 25), fg_color="green", hover_color="dark green", command=self.update_student).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Delete", width=100, font=("Arial", 25), fg_color="red", hover_color="dark red", command=self.delete_student).pack(side="left", padx=10)

        # Search Area 
        ct.CTkLabel(self, text="Search Roll:", font=("Arial", 25), text_color="black").place(x=550, y=50)
        self.search_entry = ct.CTkEntry(self, font=("Arial", 25), width=350, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.search_entry.place(x=550, y=90)
        ct.CTkButton(self, text="Search", width=100, font=("Arial", 25), command=self.search_student).place(x=920, y=90)
        ct.CTkButton(self, text="Clear", width=100, font=("Arial", 25), command=self.clear_search_view).place(x=1040, y=90)

    # Table
    def show_student_table(self, filtered=None):
        # Deleting Old Table Frame
        if self.S_Frame: 
            self.S_Frame.destroy()
        
        # Table Frame
        self.S_Frame = ct.CTkFrame(self, fg_color="white", width=1000, height=450)
        self.S_Frame.place(x=550, y=140)
        
        # Data Source (Added true indexing logic here)
        all_students = self.manager.get_all_students()
        data = filtered if filtered is not None else all_students

        # Headings
        self.Table = ttk.Treeview(self.S_Frame, columns=("roll_number","student_name","phone","gender","address"), show="headings")
        cols = {"roll_number":"Roll", "student_name":"Name", "phone":"Phone", "gender":"Gender", "address":"Address"}
        for k, v in cols.items(): 
            self.Table.heading(k, text=v)

        # Column Width
        self.Table.column("roll_number", width=100, anchor="center")
        self.Table.column("student_name", width=250, anchor="w")
        self.Table.column("phone", width=180, anchor="center")
        self.Table.column("gender", width=120, anchor="center")
        self.Table.column("address", width=250, anchor="w")
        

        # Vertical Scrollbar
        scroll_y = ttk.Scrollbar(self.S_Frame, orient="vertical", command=self.Table.yview)
        self.Table.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.Table.pack(fill="both", expand=True)

        # Insert Data (Using true database index)
        for i, s in enumerate(data):
            true_index = all_students.index(s)
            self.Table.insert("", "end", iid=true_index, values=(s["Roll"], s["Name"], s["Phone"], s["Gender"], s["Address"]))
        self.Table.bind("<<TreeviewSelect>>", self.on_select)

    # Selecting Data
    def on_select(self, event):
        sel = self.Table.selection()
        if not sel: return
        self.selected_index = int(sel[0]) # Now properly grabs the real DB index
        s = self.manager.get_all_students()[self.selected_index]
        
        self.clear_entries()
        self.roll_entry.insert(0, s["Roll"])
        self.name_entry.insert(0, s["Name"])
        self.phone_entry.insert(0, s["Phone"])
        self.gender_combo.set(s["Gender"])
        self.address_entry.insert("1.0", s["Address"])

    # Clear Input    
    def clear_entries(self):
        self.roll_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.address_entry.delete("1.0", "end")
        self.gender_combo.set("Male")

    # Clear Search
    def clear_search_view(self):
        self.search_entry.delete(0, 'end')
        self.show_student_table()

    # Save Student
    def save_student(self):
        roll_number = self.roll_entry.get().strip()
        student_name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        gender = self.gender_combo.get()
        address = self.address_entry.get("1.0", "end-1c").strip()
        
        # Empty Fields Check
        if not roll_number or not student_name or not phone or not address: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
            
        # Roll Number Format Validation   
        if not roll_number.isdigit():
            messagebox.showerror("Format Error", "Roll Number must contain only numbers.")
            return

        # Duplicate Roll Number Validation
        for s in self.manager.get_all_students():
            if s["Roll"] == roll_number:
                messagebox.showerror("Duplicate Error", f"A student with Roll Number '{roll_number}' already exists!")
                return
        
        # Phone Validation
        if not phone.isdigit():
            messagebox.showerror("Format Error", "Phone Number must contain only numbers.")
            return
        
        if len(phone) != 11:
            messagebox.showerror("Format Error", "Phone Number must be exactly 11 digits.")
            return
 
        # Student Name Validation
        if student_name.isdigit():
            messagebox.showerror("Format Error", "Name cannot be just numbers.")
            return

        # Adding Student   
        self.manager.add_student(Student(roll_number, student_name, phone, gender, address))
        messagebox.showinfo("Success", f"Student '{student_name}' has been saved successfully.")
        self.clear_entries()
        self.show_student_table()

    # Update Student
    def update_student(self):
        if self.selected_index is None: 
            messagebox.showwarning("Selection Error", "Please click a row in the table to select it first!")
            return
            
        roll_number = self.roll_entry.get().strip()
        student_name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        gender = self.gender_combo.get()
        address = self.address_entry.get("1.0", "end-1c").strip()
        
        if not roll_number or not student_name or not phone or not address: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
            
        if not roll_number.isdigit():
            messagebox.showerror("Format Error", "Roll Number must contain only numbers.")
            return

        # Duplicate Check for UPDATES
        for i, s in enumerate(self.manager.get_all_students()):
            if i != self.selected_index and s["Roll"] == roll_number:
                messagebox.showerror("Duplicate Error", f"Another student already uses Roll Number '{roll_number}'!")
                return

        if not phone.isdigit():
            messagebox.showerror("Format Error", "Phone Number must contain only numbers.")
            return
        
        if len(phone) != 11:
            messagebox.showerror("Format Error", "Phone Number must be exactly 11 digits.")
            return

        if student_name.isdigit():
            messagebox.showerror("Format Error", "Name cannot be just numbers.")
            return
            
        self.manager.update_student(self.selected_index, Student(roll_number, student_name, phone, gender, address))
        messagebox.showinfo("Success", f"Student '{student_name}' updated successfully!")
        self.selected_index = None
        self.clear_entries()
        self.show_student_table()

    # Delete Student
    def delete_student(self):
        if self.selected_index is None: 
            messagebox.showwarning("Selection Error", "Please select a student from the table to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure? This will permanently remove this student."):
            self.manager.delete_student(self.selected_index)
            messagebox.showinfo("Deleted", "Student has been removed from the database.")
            self.selected_index = None
            self.clear_entries()
            self.show_student_table()

    # Search Student
    def search_student(self):
        query = self.search_entry.get().strip()
        if not query:
            self.show_student_table()
            return
            
        found = self.manager.search_students(query)
        if found: 
            self.show_student_table(found)
        else: 
            messagebox.showinfo("No Match", "No student found matching that Roll Number.")