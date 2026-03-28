import customtkinter as ct
from tkinter import ttk
from csv import DictWriter, DictReader


from course_view import CourseView
from student_view import StudentView 
from result_view import ResultView
from overall_report_view import ReportView

# Data Storage Handling
class CSVStorage:
    def __init__(self, filename, fieldnames):
        self.filename = filename
        self.fieldnames = fieldnames

    def load_data(self):
        data = []
        try:
            with open(self.filename, "r", newline="") as file:
                reader = DictReader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError: 
            pass
        return data
    
    def save_data(self, data_list):

        with open(self.filename, "w", newline="") as file:
            writer = DictWriter(file, fieldnames=self.fieldnames) 
            writer.writeheader() 
            writer.writerows(data_list)

# Course Manager
class CourseManager:
    def __init__(self, storage): 
        self.storage = storage

    def get_all_courses(self): 
        return self.storage.load_data()
    
    def add_course(self, course): 
        d = self.get_all_courses() 
        d.append(course.to_dict()) 
        self.storage.save_data(d)
        
    def update_course(self, index, course):
        d = self.get_all_courses()
        d[index] = course.to_dict()
        self.storage.save_data(d)
        
    def delete_course(self, index):
        d = self.get_all_courses()
        d.pop(index)
        self.storage.save_data(d)
        
    def search_courses(self, q): 
        return [c for c in self.get_all_courses() if q in c["Course Name"].lower()]

# Student Data Mangaer
class StudentManager:
    def __init__(self, storage): 
        self.storage = storage
        
    def get_all_students(self): 
        return self.storage.load_data()
        
    def add_student(self, student):
        d = self.get_all_students()
        d.append(student.to_dict())
        self.storage.save_data(d)
        
    def update_student(self, index, student):
        d = self.get_all_students()
        d[index] = student.to_dict()
        self.storage.save_data(d)
        
    def delete_student(self, index):
        d = self.get_all_students()
        d.pop(index)
        self.storage.save_data(d)
        
    def search_students(self, query): 
        return [s for s in self.get_all_students() if query in s["Roll"]]

# Result Mangaer
class ResultManager:
    def __init__(self, storage): 
        self.storage = storage
        
    def get_all_results(self): 
        return self.storage.load_data()
    
    def add_result(self, result):
        d = self.get_all_results()
        
        for r in d:
            if r["Roll"] == result.roll and r["Course"] == result.course:
                return False, "This student already has a grade for this course!"
                
        d.append(result.to_dict())
        self.storage.save_data(d)
        return True, "Success"

    def update_result(self, index, result):
        d = self.get_all_results()
        d[index] = result.to_dict()
        self.storage.save_data(d)
        
    def delete_result(self, index):
        d = self.get_all_results()
        d.pop(index)
        self.storage.save_data(d)
        
    def search_results(self, query): 
        return [r for r in self.get_all_results() if query in r["Roll"]]


# Dashboard

class StudentResultApp(ct.CTk):
    def __init__(self, c_manager, s_manager, r_manager):
        super().__init__()
        
        # Store the managers so the views can access them
        self.c_manager = c_manager
        self.s_manager = s_manager
        self.r_manager = r_manager 
        
        # Window configuration
        self.title("Student Result Manager")
        self.geometry("1500x770+0+0")
        self.configure(fg_color="white")

        # Table View
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", rowheight=50, font=("Arial", 20), bordercolor="black", borderwidth=1)
        style.configure("Treeview.Heading", font=("Arial", 20, "bold"), background="#2B2B2B", foreground="white", bordercolor="#", borderwidth=1)
        style.map("Treeview", background=[("selected", "blue")])

        # Header
        ct.CTkLabel(self, text="Student Result Manager", text_color="black", font=("Times New Roman", 42, "bold")).pack(pady=20)
        
        #  Sidebar Layout 
        self.sidebar_frame = ct.CTkFrame(self, width=260, fg_color="black", corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        ct.CTkLabel(self.sidebar_frame, text="MENU", font=("Arial", 34, "bold"), text_color="white").pack(pady=(50,10))

        #  Main Content Area 
        self.main_frame = ct.CTkFrame(self, fg_color="grey", corner_radius=0)
        self.main_frame.pack(side="left", fill="both", expand=True, padx=5, pady=(1,5))

        # Attach buttons to the sidebar
        self.add_sidebar_btn("Courses", self.show_course)
        self.add_sidebar_btn("Student", self.show_student)
        self.add_sidebar_btn("Results", self.show_result) 
        self.add_sidebar_btn("Statistics", self.show_report)
        self.add_sidebar_btn("Logout", self.logout)
        
        # Automatically load the courses view when the app first opens
        self.show_course()

    #  Navigation Functions 
    def add_sidebar_btn(self, text, cmd):
        ct.CTkButton(self.sidebar_frame, text=text, command=cmd, fg_color="transparent", hover_color="#2B2B2B", height=50, font=("Arial", 25)).pack(fill="x", padx=10, pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children(): 
            widget.destroy()

    def show_course(self):
        self.clear_frame()
        CourseView(self.main_frame, self.c_manager).pack(fill="both", expand=True)

    def show_student(self):
        self.clear_frame()
        StudentView(self.main_frame, self.s_manager).pack(fill="both", expand=True)

    def show_result(self):
        self.clear_frame()
        ResultView(self.main_frame, self.r_manager, self.s_manager, self.c_manager).pack(fill="both", expand=True)

    def show_report(self):
        self.clear_frame()
        ReportView(self.main_frame, self.c_manager, self.s_manager, self.r_manager).pack(fill="both", expand=True)

    def logout(self):

        self.destroy()       
        import main          
        main.run_app()       


if __name__ == "__main__":
    # Initialize the Storage and Managers with their specific CSV headers
    c_man = CourseManager(CSVStorage("courses.csv", ["Serial No", "Course Name", "Duration", "Description"]))
    s_man = StudentManager(CSVStorage("students.csv", ["Roll", "Name", "Phone", "Gender", "Address"]))
    r_man = ResultManager(CSVStorage("results.csv", ["Roll", "Course", "Marks", "Grade"])) 
    