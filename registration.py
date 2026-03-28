import customtkinter as ct
from tkinter import messagebox
import csv

class RegistrationWindow(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Register New Account")
        self.geometry("700x700") 
        self.configure(fg_color="white")
        self.setup_ui()

    # Setup Ui
    def setup_ui(self):        
        ct.CTkLabel(self, text="Create Account", font=("Arial", 35, "bold"), text_color="black").place(x=220, y=30)

        # Full Name Input
        ct.CTkLabel(self, text="Full Name:", font=("Arial", 25), text_color="black").place(x=150, y=100)
        self.name_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, fg_color="#F0F0F0", text_color="black", border_width=1)
        self.name_entry.place(x=150, y=140)

        # Phone Number Input
        ct.CTkLabel(self, text="Phone Number:", font=("Arial", 25), text_color="black").place(x=150, y=190)
        self.phone_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, fg_color="#F0F0F0", text_color="black", border_width=1)
        self.phone_entry.place(x=150, y=230)

        # Username Input
        ct.CTkLabel(self, text="Username:", font=("Arial", 25), text_color="black").place(x=150, y=280)
        self.user_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, fg_color="#F0F0F0", text_color="black", border_width=1)
        self.user_entry.place(x=150, y=320)

        # Password Input
        ct.CTkLabel(self, text="Password:", font=("Arial", 25), text_color="black").place(x=150, y=370)
        self.pass_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, fg_color="#F0F0F0", text_color="black", show="*", border_width=1)
        self.pass_entry.place(x=150, y=410)

        # Confirm Password Input
        ct.CTkLabel(self, text="Confirm Password:", font=("Arial", 25), text_color="black").place(x=150, y=460)
        self.confirm_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, fg_color="#F0F0F0", text_color="black", show="*", border_width=1)
        self.confirm_entry.place(x=150, y=500)

        # Buttons
        ct.CTkButton(self, text="Register", font=("Arial", 25, "bold"), width=400, height=45, command=self.register_user).place(x=150, y=570)
        ct.CTkButton(self, text="Back to Home", font=("Arial", 25), width=400, height=45, fg_color="transparent", text_color="black", hover_color="#E0E0E0", command=self.go_back).place(x=150, y=625)

    # Register User Function
    def register_user(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        confirm_password = self.confirm_entry.get().strip()

        # Empty Check
        if not name or not phone or not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return
            
        # Phone Validation
        if not phone.isdigit() and len(phone) !=11:
            messagebox.showerror("Format Error", "Phone Number must contain only numbers and has to be 11 digits only.")
            return
        
        # 3. Password Check
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if len(password) <8:
            messagebox.showerror("Error", "Passwords should be 8 characters long")
            return
        
        # Check Existing Username
        file_exists = True
        try:
            with open("users.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Username"].lower() == username.lower():
                        messagebox.showerror("Error", "Username already exists!")
                        return
        except FileNotFoundError:
            file_exists = False

        # Save new user to CSV
        with open("users.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Phone", "Username", "Password"])
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({"Name": name, "Phone": phone, "Username": username, "Password": password})

        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        self.go_back()

    # Return to Home Screen
    def go_back(self):
        self.destroy()
        import main
        main.run_app()

def run():
    app = RegistrationWindow()
    app.mainloop()