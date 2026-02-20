"""
Simple SQLite Database Viewer
Run this to see your data in a simple GUI
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Database Viewer")
        self.root.geometry("900x600")
        
        # Database connection
        self.conn = None
        self.cursor = None
        
        # Create GUI
        self.create_widgets()
        
        # Auto-load your database
        self.load_database(r"C:\Users\mulla\OneDrive\Desktop\ai-support-system\backend\tickets.db")
    
    def create_widgets(self):
        # Top frame for buttons
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(top_frame, text="Open Database", command=self.open_file).pack(side=tk.LEFT, padx=2)
        
        # Main paned window
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left frame for tables list
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="Tables", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.tree_tables = ttk.Treeview(left_frame, show='tree', height=20)
        self.tree_tables.pack(fill=tk.BOTH, expand=True)
        self.tree_tables.bind('<<TreeviewSelect>>', self.on_table_select)
        
        # Right frame for data display
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)
        
        ttk.Label(right_frame, text="Table Data", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Create treeview for data
        self.data_tree = ttk.Treeview(right_frame, show='headings', height=20)
        self.data_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.data_tree.configure(yscrollcommand=v_scroll.set)
        
        h_scroll = ttk.Scrollbar(right_frame, orient=tk.HORIZONTAL, command=self.data_tree.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.data_tree.configure(xscrollcommand=h_scroll.set)
        
        # Status bar
        self.status = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Select SQLite Database",
            filetypes=[("SQLite files", "*.db *.sqlite *.sqlite3"), ("All files", "*.*")]
        )
        if filename:
            self.load_database(filename)
    
    def load_database(self, filename):
        try:
            self.conn = sqlite3.connect(filename)
            self.cursor = self.conn.cursor()
            
            # Get all tables
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            
            # Clear existing items
            for item in self.tree_tables.get_children():
                self.tree_tables.delete(item)
            
            # Add tables to tree
            for table in tables:
                if not table[0].startswith('sqlite_'):
                    self.tree_tables.insert('', 'end', text=table[0], values=(table[0],))
            
            self.status.config(text=f"Connected to: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load database: {e}")
    
    def on_table_select(self, event):
        selection = self.tree_tables.selection()
        if not selection:
            return
        
        table_name = self.tree_tables.item(selection[0], 'text')
        
        try:
            # Get column names
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in self.cursor.fetchall()]
            
            # Get data
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
            data = self.cursor.fetchall()
            
            # Clear existing data
            self.data_tree.delete(*self.data_tree.get_children())
            
            # Configure columns
            self.data_tree['columns'] = columns
            self.data_tree['show'] = 'headings'
            
            for col in columns:
                self.data_tree.heading(col, text=col)
                self.data_tree.column(col, width=100, minwidth=50)
            
            # Insert data
            for row in data:
                self.data_tree.insert('', 'end', values=row)
            
            self.status.config(text=f"Table: {table_name} - {len(data)} rows")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load table: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseViewer(root)
    root.mainloop()