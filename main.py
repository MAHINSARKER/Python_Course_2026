import customtkinter as ct
import login
import registration

class WelcomeWindow(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Result Manager")
        self.geometry("700x500")
        self.configure(fg_color="black")
        self.setup_ui()

 # UI Setup
    def setup_ui(self):
        frame = ct.CTkFrame(self, fg_color="white", corner_radius=15, width=500, height=350)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Labels
        ct.CTkLabel(frame, text="Student Result Manager", font=("Arial", 35, "bold"), text_color="black").place(x=50, y=50)
        ct.CTkLabel(frame, text="Please Login or Create an Account to continue.", font=("Arial", 18), text_color="grey").place(x=60, y=100)
        
        # Buttons
        ct.CTkButton(frame, text="Login", font=("Arial", 20, "bold"), width=300, height=50, command=self.open_login).place(x=100, y=180)
        ct.CTkButton(frame, text="Get Started (Register)", font=("Arial", 20, "bold"), width=300, height=50, fg_color="grey", hover_color="dark grey", command=self.open_registration).place(x=100, y=250)

# Login Frame
    def open_login(self):
        self.destroy()  
        login.run()     
# Registration Frame
    def open_registration(self):
        self.destroy() 
        registration.run()

def run_app():
        app = WelcomeWindow()
        app.mainloop()

if __name__ == "__main__":
        run_app()