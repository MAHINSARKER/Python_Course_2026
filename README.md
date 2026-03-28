# Python Course 2026 — Student Result Manager

A Python GUI application called **Student Result Manager** built with **CustomTkinter**.  
It provides a simple interface to **register/login** and then view/manage student/course/result data stored in CSV files.

## Features
- Modern desktop GUI using **customtkinter**
- Welcome screen with **Login** and **Register**
- Uses CSV files for data storage:
  - `users.csv`
  - `students.csv`
  - `courses.csv`
  - `results.csv`
- Multiple views/modules (examples):
  - `login.py`, `registration.py`
  - `dashboard.py`
  - `student_view.py`, `course_view.py`, `result_view.py`
  - `overall_report_view.py`

## Project Structure (high level)
- `main.py` — application entry point (launches the welcome window)
- `requirements.txt` — Python dependencies
- `*.csv` — data files used by the application
- `Project Report.pdf` — project documentation/report

## Requirements
- Python **3.9+** (recommended)
- pip (Python package manager)

## Installation (Step-by-step)

### 1) Clone the repository
```bash
git clone https://github.com/MAHINSARKER/Python_Course_2026.git
cd Python_Course_2026
```

### 2) Create and activate a virtual environment (recommended)

**Windows (PowerShell):**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```


## Run the Application
From the project root directory:

```bash
python main.py
```

## Notes / Troubleshooting
- If `pip` installs packages but the app won’t run, confirm you activated the virtual environment before running `python main.py`.
- If you are on Linux and Tkinter is missing, you may need to install Tkinter from your OS package manager (Tk is required for Tkinter-based GUIs).
- Keep the CSV files in the same directory as the `.py` files.
