import customtkinter as ct
from tkinter import ttk, messagebox

class Course:
    def __init__(self, serial, name, duration, description):
        self.serial = serial
        self.name = name
        self.duration = duration
        self.description = description
        
    # Dictionary so save data to the CSV    
    def to_dict(self):
        return {"Serial No": self.serial, "Course Name": self.name, "Duration": self.duration, "Description": self.description}


class CourseView(ct.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent")
        self.manager = manager               
        self.selected_index = None           
        self.C_Frame = None                  
        
        self.setup_ui()                      
        self.show_course_table()             


    # UI Setup
    def setup_ui(self):

        # Course Name Entry
        ct.CTkLabel(self, text="Course Name:", font=("Arial", 25), text_color="black").place(x=50, y=50)
        self.course_name_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white")        
        self.course_name_entry.place(x=50, y=90)

        # Course Duration Entry
        ct.CTkLabel(self, text="Duration (in months):", font=("Arial", 25), text_color="black").place(x=50, y=150)
        self.duration_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white")
        self.duration_entry.place(x=50, y=190)

        # Course Description Entry
        ct.CTkLabel(self, text="Description:", font=("Arial", 25), text_color="black").place(x=50, y=250)
        self.txt_description = ct.CTkTextbox(self, font=("Arial", 25), height=150, width=400, text_color="black", fg_color="white")
        self.txt_description.place(x=50, y=290)

        # Buttons
        btn_frame = ct.CTkFrame(self, fg_color="transparent") 
        btn_frame.place(x=50, y=470)
        ct.CTkButton(btn_frame, text="Save", width=100, font=("Arial", 25), command=self.save_course).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Update", width=100, font=("Arial", 25), fg_color="green", hover_color="dark green", command=self.update_course).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Delete", width=100, font=("Arial", 25), fg_color="red", hover_color="dark red", command=self.delete_course).pack(side="left", padx=10)

        # Course Search Field
        ct.CTkLabel(self, text="Search Course Name:", font=("Arial", 25), text_color="black").place(x=550, y=50)
        self.search_entry = ct.CTkEntry(self, font=("Arial", 25), width=350, text_color="black", fg_color="white")
        self.search_entry.place(x=550, y=90)
        ct.CTkButton(self, text="Search", width=100, font=("Arial", 25), command=self.search_course).place(x=920, y=90)
        ct.CTkButton(self, text="Clear", width=100, font=("Arial", 25), command=self.clear_search_view).place(x=1040, y=90)
    

    # Data TABLE
    def show_course_table(self, filtered=None):

        # Deleting Old Table Frame
        if self.C_Frame: 
            self.C_Frame.destroy()
        
        # Table Frame
        self.C_Frame = ct.CTkFrame(self, fg_color="white", width=900, height=500)
        self.C_Frame.place(x=550, y=140)
        
        # Data Source
        data = self.manager.get_all_courses()
        if filtered is not None:
            data = filtered
        
        self.Table = ttk.Treeview(self.C_Frame, columns=("serial_number", "course_name", "dur", "desc"), show="headings")
        
        #Table Heading
        self.Table.heading("serial_number", text="Serial No.")
        self.Table.heading("course_name", text="Course Name")
        self.Table.heading("dur", text="Duration")
        self.Table.heading("desc", text="Description", anchor="w")
        
        # Column Width
        self.Table.column("serial_number", width=200, stretch=False, anchor="center") 
        self.Table.column("course_name", width=300, stretch=False, anchor="center")
        self.Table.column("dur", width=150, stretch=False, anchor="center")
        self.Table.column("desc", width=250, stretch=False, anchor="w") 

        # Vertical Scrollbars
        scroll_y = ttk.Scrollbar(self.C_Frame, orient="vertical", command=self.Table.yview)
        scroll_y.pack(side="right", fill="y")
        self.Table.configure(yscrollcommand=scroll_y.set)

        self.Table.pack(fill="both", expand=True)

        # Insert data
        for i, c in enumerate(data): 
            serial_num = c.get("Serial No", i+1)                
            self.Table.insert("", "end", iid=i, values=(serial_num, c["Course Name"], c["Duration"], c["Description"]))            
        self.Table.bind("<<TreeviewSelect>>", self.on_select)

    # Selecting Data
    def on_select(self, event):
        sel = self.Table.selection()
        if not sel: return
        
        self.selected_index = int(sel[0])
        all_courses = self.manager.get_all_courses()
        c = all_courses[self.selected_index]
        
        self.clear_entries()
        self.course_name_entry.insert(0, c["Course Name"])
        self.duration_entry.insert(0, c["Duration"])
        self.txt_description.insert("1.0", c["Description"]) 

    # Clear Input
    def clear_entries(self):
        self.course_name_entry.delete(0, "end")
        self.duration_entry.delete(0, "end")
        self.txt_description.delete("1.0", "end")

    # Clear Search
    def clear_search_view(self):
        self.search_entry.delete(0, 'end')
        self.show_course_table()
        
    # Save Course
    def save_course(self):
        course_name = self.course_name_entry.get().strip()
        duration = self.duration_entry.get().strip()
        description = self.txt_description.get("1.0", "end-1c").strip()

        # Empty Fields Check
        if not course_name or not duration or not description: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        # Course Name Validation
        if course_name.isdigit():
            messagebox.showerror("Format Error", "Course Name cannot be a number")
            return
        
        # Duplicate check
        for c in self.manager.get_all_courses():
            if c["Course Name"].lower() == course_name.lower():
                messagebox.showerror("Duplicate Error", f"A course named '{course_name}' already exists!")
                return
        
        # Duration validation
        if not duration.isdigit(): 
            messagebox.showerror("Format Error", "Duration must be a whole number.") 
            return
        elif int(duration) > 12:
            messagebox.showerror("Limit Error", "Course duration cannot exceed 12 months.")
            return
        
        # Description Validation
        if description.isdigit():
            messagebox.showerror("Format Error", "Description cannot be a number")
            return        
        
        # Generating a permanent Serial Number based on existing data 
        existing_courses = self.manager.get_all_courses()
        if existing_courses and "Serial No" in existing_courses[-1]:
            new_serial = int(existing_courses[-1]["Serial No"]) + 1
        else:
            new_serial = len(existing_courses) + 1

        # Adding Course
        self.manager.add_course(Course(new_serial, course_name, duration, description))
        messagebox.showinfo("Success", f"Course '{course_name}' has been saved successfully.")        
        self.clear_entries()      
        self.show_course_table()  

    # Update Course
    def update_course(self):
        if self.selected_index is None: 
            messagebox.showwarning("Selection Error", "Please click a row in the table to select it first!")
            return

        course_name = self.course_name_entry.get().strip()
        duration = self.duration_entry.get().strip()
        description = self.txt_description.get("1.0", "end-1c").strip()

        if not course_name or not duration or not description: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        if course_name.isdigit():
            messagebox.showerror("Format Error", "Course Name cannot be a number")
            return

        for i, c in enumerate(self.manager.get_all_courses()):
            if i != self.selected_index and c["Course Name"].lower() == course_name.lower():
                messagebox.showerror("Duplicate Error", f"A course named '{course_name}' already exists!")
                return
        
        if not duration.isdigit(): 
            messagebox.showerror("Format Error", "Duration must be a whole number.") 
            return
        elif int(duration) > 12:
            messagebox.showerror("Limit Error", "Course duration cannot exceed 12 months.")
            return
        
        if description.isdigit():
            messagebox.showerror("Format Error", "Description cannot be a number")
            return        

        # Retrieve the original permanent serial number
        existing_courses = self.manager.get_all_courses()
        current_serial = existing_courses[self.selected_index].get("Serial No", self.selected_index + 1)

        self.manager.update_course(self.selected_index, Course(current_serial, course_name, duration, description))
        messagebox.showinfo("Success", f"Course '{course_name}' updated successfully!")        
        self.selected_index = None 
        self.clear_entries()
        self.show_course_table()

    # Delete Course
    def delete_course(self):
        if self.selected_index is None:
            messagebox.showwarning("Selection Error", "Please select a course from the table to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure? This will permanently remove this course."):
            self.manager.delete_course(self.selected_index)
            messagebox.showinfo("Deleted", "Course has been removed from the database.")
            
            self.selected_index = None
            self.clear_entries()
            self.show_course_table()

    # Search Course
    def search_course(self):
        query = self.search_entry.get().lower().strip()
        
        if not query:
            self.show_course_table() 
            return
            
        found = self.manager.search_courses(query)
        if found: 
            self.show_course_table(found) 
        else: 
            messagebox.showinfo("No Match", "No course found")