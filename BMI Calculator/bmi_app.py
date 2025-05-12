import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database setup
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY,
    user_name TEXT,
    height REAL,
    weight REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)''')
conn.commit()

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.current_user = tk.StringVar()

        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        # User Frame
        user_frame = tk.Frame(self.root)
        user_frame.pack(pady=10)

        tk.Label(user_frame, text="User:").pack(side=tk.LEFT)
        self.user_dropdown = ttk.Combobox(user_frame, textvariable=self.current_user)
        self.user_dropdown.pack(side=tk.LEFT, padx=5)
        
        tk.Button(user_frame, text="New User", command=self.create_user_popup).pack(side=tk.LEFT)

        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Height (m):").grid(row=0, column=0)
        self.height_entry = tk.Entry(input_frame)
        self.height_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Weight (kg):").grid(row=1, column=0)
        self.weight_entry = tk.Entry(input_frame)
        self.weight_entry.grid(row=1, column=1)

        tk.Button(input_frame, text="Calculate BMI", command=self.calculate_bmi).grid(row=2, column=0, columnspan=2, pady=5)

        # Result Frame
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

        # History Frame
        history_frame = tk.LabelFrame(self.root, text="BMI History")
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.history_tree = ttk.Treeview(history_frame, columns=("date", "height", "weight", "bmi", "category"), show="headings")
        for col in self.history_tree["columns"]:
            self.history_tree.heading(col, text=col.title())
        self.history_tree.pack(fill="both", expand=True)

        # Visualization Frame
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack(fill="both", expand=True)

    def create_user_popup(self):
        popup = tk.Toplevel()
        popup.title("Create New User")
        tk.Label(popup, text="Enter name:").pack()
        entry = tk.Entry(popup)
        entry.pack()

        def save_user():
            name = entry.get().strip()
            if not name:
                messagebox.showwarning("Input Error", "Name cannot be empty.")
                return
            try:
                cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
                conn.commit()
                self.load_users()
                self.current_user.set(name)
                popup.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("User Exists", f"User '{name}' already exists.")

        tk.Button(popup, text="Save", command=save_user).pack(pady=5)

    def load_users(self):
        cursor.execute("SELECT name FROM users")
        users = [row[0] for row in cursor.fetchall()]
        self.user_dropdown["values"] = users

    def calculate_bmi(self):
        if not self.current_user.get():
            messagebox.showwarning("No User", "Please select or create a user.")
            return

        try:
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            if height <= 0 or weight <= 0:
                raise ValueError

            bmi = round(weight / (height ** 2), 2)
            category = self.get_bmi_category(bmi)
            self.result_label.config(text=f"BMI: {bmi} ({category})")

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO bmi_records (user_name, height, weight, bmi, category, date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.current_user.get(), height, weight, bmi, category, date))
            conn.commit()

            self.update_history()
            self.display_bmi_trend()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid height and weight.")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Pre-obesity"
        elif bmi < 35:
            return "Obesity class I"
        elif bmi < 40:
            return "Obesity class II"
        else:
            return "Obesity class III"

    def update_history(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        cursor.execute('''SELECT date, height, weight, bmi, category FROM bmi_records 
                          WHERE user_name = ? ORDER BY date DESC''', (self.current_user.get(),))
        for record in cursor.fetchall():
            self.history_tree.insert("", tk.END, values=record)

    def display_bmi_trend(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        cursor.execute('''SELECT date, bmi FROM bmi_records WHERE user_name = ? ORDER BY date''', (self.current_user.get(),))
        records = cursor.fetchall()
        if not records:
            return

        dates = [record[0] for record in records]
        bmis = [record[1] for record in records]

        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, bmis, marker='o')
        ax.set_title(f"BMI Trend for {self.current_user.get()}")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.axhline(y=18.5, color='red', linestyle='--', label="Underweight/Normal")
        ax.axhline(y=25, color='yellow', linestyle='--', label="Normal/Overweight")
        ax.axhline(y=30, color='orange', linestyle='--', label="Obese")

        fig.autofmt_xdate()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()