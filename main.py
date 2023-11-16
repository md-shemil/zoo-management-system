import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

class ZooManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoo Animal Manager")
        
        # Create a database connection
        self.conn = sqlite3.connect('zoo.db')
        self.create_table()
        
        # Create GUI
        self.create_gui()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dob TEXT,
                weight REAL,
                height REAL,
                medical_condition TEXT
            )
        ''')
        self.conn.commit()

    def create_gui(self):
        # Labels
        tk.Label(self.root, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.root, text="DOB (DD-MM-YYYY)").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Weight (kg)").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Height (m)").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(self.root, text="Medical Condition").grid(row=4, column=0, padx=5, pady=5)

        # Entry widgets
        self.name_entry = tk.Entry(self.root)
        self.dob_entry = tk.Entry(self.root)
        self.weight_entry = tk.Entry(self.root)
        self.height_entry = tk.Entry(self.root)
        self.medical_condition_entry = tk.Entry(self.root)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.dob_entry.grid(row=1, column=1, padx=5, pady=5)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)
        self.height_entry.grid(row=3, column=1, padx=5, pady=5)
        self.medical_condition_entry.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(self.root, text="Add Animal", command=self.add_animal).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Delete Animal", command=self.delete_animal).grid(row=6, column=0, columnspan=2, pady=10)

        # Treeview to display animals
        columns = ("ID", "Name", "DOB", "Weight", "Height", "Medical Condition")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=7, column=0, columnspan=2)

        # Populate treeview with existing data
        self.display_animals()

        # Bind treeview selection
        self.tree.bind("<ButtonRelease-1>", self.load_animal_data)

    def add_animal(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()
        medical_condition = self.medical_condition_entry.get()

        if name and dob and weight and height:
            try:
                dob = datetime.strptime(dob, "%d-%m-%Y").date()
                weight = float(weight)
                height = float(height)

                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO animals (name, dob, weight, height, medical_condition)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, dob, weight, height, medical_condition))
                self.conn.commit()

                self.clear_entries()
                self.display_animals()

            except ValueError:
                tk.messagebox.showerror("Error", "Invalid input. Please check your data.")
        else:
            tk.messagebox.showerror("Error", "All fields must be filled.")

    def delete_animal(self):
        selected_item = self.tree.selection()

        if not selected_item:
            tk.messagebox.showerror("Error", "Please select an animal to delete.")
            return

        animal_id = self.tree.item(selected_item, 'values')[0]
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM animals WHERE id = ?', (animal_id,))
        self.conn.commit()

        self.display_animals()
        self.clear_entries()

    def display_animals(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM animals')
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def load_animal_data(self, event):
        selected_item = self.tree.selection()

        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.name_entry.delete(0, tk.END)
            self.dob_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
            self.height_entry.delete(0, tk.END)
            self.medical_condition_entry.delete(0, tk.END)

            self.name_entry.insert(tk.END, values[1])
            self.dob_entry.insert(tk.END, values[2])
            self.weight_entry.insert(tk.END, values[3])
            self.height_entry.insert(tk.END, values[4])
            self.medical_condition_entry.insert(tk.END, values[5])

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.medical_condition_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ZooManager(root)
    root.mainloop()
