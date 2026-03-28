import customtkinter as ct
from tkinter import ttk, messagebox

class ReportView(ct.CTkFrame):
    def __init__(self, parent, c_manager, s_manager, r_manager):
        super().__init__(parent, fg_color="transparent")
        self.c_manager = c_manager
        self.s_manager = s_manager
        self.r_manager = r_manager
        
        # pass/fail status for the table
        self.overall_data = [] 
        self.T_Frame = None
        
        self.setup_ui()

   # Setup UI
    def setup_ui(self):
        ct.CTkLabel(self, text="Class Statistics & Reports", font=("Arial", 35, "bold"), text_color="black").pack(pady=(30, 10))

        stats_frame = ct.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(pady=20) 

        # Fetch Data
        students = self.s_manager.get_all_students()
        results = self.r_manager.get_all_results()
        
        # A dictionary to quickly look up student names by Roll
        student_dict = {s["Roll"]: s["Name"] for s in students}

        total_students = len(students)

        # Roll Number Having at least 1 result
        evaluated_rolls = set(r["Roll"] for r in results)
        unique_evaluated = len(evaluated_rolls)

        passed_students = 0
        failed_students = 0
        
        # Clear previous data
        self.overall_data = []

        for roll in evaluated_rolls:
            student_grades = [r["Grade"] for r in results if r["Roll"] == roll]
            student_name = student_dict.get(roll, "Unknown Student")
            
            if "F" in student_grades:
                failed_students += 1
                status = "FAILED"
            else:
                passed_students += 1
                status = "PASSED"
                
            # Save the student's final status for the table
            self.overall_data.append({"Roll": roll, "Name": student_name, "Status": status})

        # Display slots
        self.create_stat_slot(stats_frame, "Reg. Students", str(total_students), 0)
        self.create_stat_slot(stats_frame, "Evaluated", str(unique_evaluated), 1) 
        self.create_stat_slot(stats_frame, "Students Passed", str(passed_students), 2)
        self.create_stat_slot(stats_frame, "Students Failed", str(failed_students), 3)

        # Search Bar
        search_frame = ct.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=(10, 10))
        
        ct.CTkLabel(search_frame, text="Search Roll:", font=("Arial", 25), text_color="black").pack(side="left", padx=10)
        self.search_entry = ct.CTkEntry(search_frame, font=("Arial", 25), width=300, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.search_entry.pack(side="left", padx=10)
        
        ct.CTkButton(search_frame, text="Search", width=100, font=("Arial", 25), command=self.search_status).pack(side="left", padx=10)
        ct.CTkButton(search_frame, text="Clear", width=100, font=("Arial", 25), command=self.clear_search).pack(side="left", padx=10)

        self.show_status_table()

    # Status Slot
    def create_stat_slot(self, parent, title, value, col):
        card = ct.CTkFrame(parent, fg_color="#2B2B2B", corner_radius=10)
        card.grid(row=0, column=col, padx=15, pady=10, sticky="nsew")
        ct.CTkLabel(card, text=title, font=("Arial", 20), text_color="white").pack(pady=(20, 5), padx=20)
        ct.CTkLabel(card, text=value, font=("Arial", 40, "bold"), text_color="#1F6AA5").pack(pady=(5, 20), padx=20)

    # Table Functions 
    def show_status_table(self, filtered=None):
        if self.T_Frame:
            self.T_Frame.destroy()

        self.T_Frame = ct.CTkFrame(self, fg_color="white", width=1100, height=350)
        self.T_Frame.pack(pady=10, fill="both", expand=True, padx=50)

        # Data Sourse
        if filtered is not None:
            data_to_show = filtered
        else:
            data_to_show = self.overall_data

        # Table Format
        self.Table = ttk.Treeview(self.T_Frame, columns=("roll", "name", "status"), show="headings")
        
        self.Table.heading("roll", text="Roll Number")
        self.Table.heading("name", text="Student Name")
        self.Table.heading("status", text="Overall Status")

        self.Table.column("roll", width=150, anchor="center")
        self.Table.column("name", width=400, anchor="center")
        self.Table.column("status", width=200, anchor="center")

        # Color-code rows based on Pass/Fail status
        self.Table.tag_configure('PASSED', background="#D4EDDA", foreground="black") 
        self.Table.tag_configure('FAILED', background="#F8D7DA", foreground="black") 

        # Vertical Scrollbar
        scroll_y = ttk.Scrollbar(self.T_Frame, orient="vertical", command=self.Table.yview)
        self.Table.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.Table.pack(fill="both", expand=True)

        for i, item in enumerate(data_to_show):
            self.Table.insert("", "end", iid=i, values=(item["Roll"], item["Name"], item["Status"]), tags=(item["Status"],))

    #  Search Functions 
    def search_status(self):
        query = self.search_entry.get().strip()
        if not query:
            self.show_status_table()
            return
            
        # Find any students whose Roll Number matches the search query
        found = [item for item in self.overall_data if query in item["Roll"]]
        
        if found:
            self.show_status_table(found)
        else:
            messagebox.showinfo("No Match", "No student found matching that Roll Number.")

    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.show_status_table()