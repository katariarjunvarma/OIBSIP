import tkinter as tk
from tkinter import ttk, messagebox
import secrets, string, math

class CharacterPool:
    def __init__(self):
        self.sets = {
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'digits': string.digits,
            'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>? ',
        }
        self.exclusions = set()

    def build(self, selected_sets):
        pool = ''.join(self.sets[cat] for cat in selected_sets)
        return ''.join(c for c in pool if c not in self.exclusions)

class Validator:
    @staticmethod
    def validate_length(length_str):
        try:
            length = int(length_str)
            if 4 <= length <= 16:
                return True, length
            return False, "Password length must be 4–16"
        except:
            return False, "Invalid number format"

    @staticmethod
    def validate_sets(selected):
        return (True, "") if selected else (False, "Select at least one character set")

def calculate_entropy(password):
    unique = len(set(password))
    return len(password) * math.log2(unique) if unique else 0

def get_strength(entropy):
    return "Weak" if entropy < 50 else "Moderate" if entropy < 80 else "Strong"

class PasswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Advanced Password Generator")
        self.geometry("500x400")
        self.pool = CharacterPool()
        self.init_ui()

    def init_ui(self):
        ttk.Label(self, text="Password Length (4–16):").pack(pady=(10, 0))
        self.len_var = tk.StringVar(value="12")
        ttk.Spinbox(self, from_=4, to=16, textvariable=self.len_var).pack()

        self.char_options = {
            'lower': tk.BooleanVar(value=True),
            'upper': tk.BooleanVar(value=True),
            'digits': tk.BooleanVar(value=True),
            'symbols': tk.BooleanVar(value=False),
        }

        frame = ttk.LabelFrame(self, text="Character Types")
        frame.pack(padx=10, pady=10, fill="x")
        for key, var in self.char_options.items():
            ttk.Checkbutton(frame, text=key.capitalize(), variable=var).pack(anchor='w')

        ttk.Label(self, text="Exclude Characters (e.g. 1lO0):").pack()
        self.exclude_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.exclude_var).pack(fill='x', padx=10)

        ttk.Button(self, text="Generate Password", command=self.generate).pack(pady=10)
        self.output_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.output_var, state='readonly', font=('Consolas', 12)).pack(fill='x', padx=10)

        self.strength_label = ttk.Label(self, text="")
        self.strength_label.pack()
        ttk.Button(self, text="Copy to Clipboard", command=self.copy_clipboard).pack(pady=5)

    def generate(self):
        valid_len, length = Validator.validate_length(self.len_var.get())
        if not valid_len:
            messagebox.showerror("Error", length)
            return

        selected = [key for key, val in self.char_options.items() if val.get()]
        valid_sets, msg = Validator.validate_sets(selected)
        if not valid_sets:
            messagebox.showerror("Error", msg)
            return

        self.pool.exclusions = set(self.exclude_var.get())
        pool = self.pool.build(selected)
        if not pool:
            messagebox.showerror("Error", "All characters excluded.")
            return

        password = ''.join(secrets.choice(pool) for _ in range(length))
        entropy = calculate_entropy(password)
        self.output_var.set(password)
        self.strength_label.config(text=f"Strength: {get_strength(entropy)} (Entropy: {int(entropy)} bits)")

    def copy_clipboard(self):
        pw = self.output_var.get()
        if pw:
            self.clipboard_clear()
            self.clipboard_append(pw)
            messagebox.showinfo("Clipboard", "Password copied!\nIt will be cleared in 30 seconds.")
            self.after(30000, self.clipboard_clear)

if __name__ == "__main__":
    PasswordApp().mainloop()