import customtkinter as ct
from tkinter import messagebox
import csv

class LoginWindow(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("System Login")
        self.geometry("700x500")
        self.configure(fg_color="white")
        self.setup_ui()

    # UI Setup
    def setup_ui(self):
        
        ct.CTkLabel(self, text="Teacher Login", font=("Arial", 35, "bold"), text_color="black").place(x=230, y=50)

        # Username Input Field
        ct.CTkLabel(self, text="Username:", font=("Arial", 25), text_color="black").place(x=150, y=130)
        self.user_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, fg_color="#F0F0F0", text_color="black", border_width=1, border_color="black")
        self.user_entry.place(x=150, y=170)

        # Password Input Field
        ct.CTkLabel(self, text="Password:", font=("Arial", 25), text_color="black").place(x=150, y=220)
        self.pass_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, fg_color="#F0F0F0", text_color="black", show="*", border_width=1, border_color="black")
        self.pass_entry.place(x=150, y=260)

        # Buttons
        ct.CTkButton(self, text="Login", font=("Arial", 25, "bold"), width=400, height=45, command=self.verify_login).place(x=150, y=340)
        ct.CTkButton(self, text="Back to Home", font=("Arial", 25), width=400, height=45, fg_color="transparent", text_color="black", hover_color="#E0E0E0", command=self.go_back).place(x=150, y=390)

    # Verify Login Credentials
    def verify_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        # Check empty fields
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return
        
        success = False

        # Read users.csv and check credentials
        try:
            with open("users.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Username"] == username and row["Password"] == password:
                        success = True
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "No accounts found. Please register first.")
            return
        
        # Login success
        if success:
            messagebox.showinfo("Welcome", f"Login successful! Welcome, {username}.")
            self.destroy() 
            self.launch_dashboard() 

        # Login failed    
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # Open Dashboard
    def launch_dashboard(self):
        from dashboard import StudentResultApp, CourseManager, StudentManager, ResultManager, CSVStorage
        
        c_man = CourseManager(CSVStorage("courses.csv", ["Serial No", "Course Name", "Duration", "Description"]))
        s_man = StudentManager(CSVStorage("students.csv", ["Roll", "Name", "Phone", "Gender", "Address"]))
        r_man = ResultManager(CSVStorage("results.csv", ["Roll", "Course", "Marks", "Grade"])) 
        
        dashboard_app = StudentResultApp(c_man, s_man, r_man)
        dashboard_app.mainloop()

    # Return to Home Screen
    def go_back(self):
        self.destroy()
        import main
        main.run_app()

# Run Login Window
def run():
    app = LoginWindow()
    app.mainloop()

