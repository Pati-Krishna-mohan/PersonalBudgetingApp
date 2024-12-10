import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import pandas as pd  
from tkinter import ttk, filedialog
from reportlab.pdfgen import canvas
import os
import ctypes

class PersonalBudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Budgeting App")
        window_width = 1600
        window_height = 900
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.primary_color = "#1a73e8"    # Blue
        self.secondary_color = "#ffffff"   # White
        self.text_color = "#202124"       # Dark gray
        self.accent_color = "#1557b0"     # Darker blue  
        self.users = {}
        self.current_user = None
        self.expense_entries = []
        self.categories = {}
        self.original_allocations = {}
        self.expense_entries = []  # List to store the expense entries
        self.filter_values = {}  # Store the applied filter values
        self.filtered_entries = []  # Store the filtered entries
        self.new_categories = []
        self.days_left = tk.IntVar()
        self.load_data()
        self.show_login_page()

    def load_data(self):
        if os.path.exists("budget_data.json"):
            with open("budget_data.json", "r") as file:
                self.users = json.load(file)

    def save_data(self):
        """Save user data to a JSON file."""
        with open("budget_data.json", "w") as file:
            json.dump(self.users, file)

    
    def show_login_page(self):
        """Display the enhanced login page."""
        self.clear_window()
        # Create main container with padding
        main_container = tk.Frame(self.root, bg=self.secondary_color)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Center frame for login elements
        login_frame = tk.Frame(
            main_container,
            bg=self.secondary_color,
            padx=40,
            pady=40
        )
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # App title
        title_frame = tk.Frame(login_frame, bg=self.secondary_color)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        app_title = tk.Label(
            title_frame,
            text="Personal Budget",
            font=("Helvetica", 24, "bold"),
            fg=self.primary_color,
            bg=self.secondary_color
        )
        app_title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Manage your finances with ease",
            font=("Helvetica", 12),
            fg=self.text_color,
            bg=self.secondary_color
        )
        subtitle.pack()
        
        # Username entry
        username_frame = tk.Frame(login_frame, bg=self.secondary_color)
        username_frame.pack(fill=tk.X, pady=10)
        
        username_label = tk.Label(
            username_frame,
            text="Username",
            font=("Helvetica", 10, "bold"),
            fg=self.text_color,
            bg=self.secondary_color,
            anchor="w"
        )
        username_label.pack(fill=tk.X)
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Helvetica", 12),
            bd=0,
            relief=tk.FLAT
        )
        self.username_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Add an underline
        tk.Frame(
            username_frame,
            height=2,
            bg=self.primary_color
        ).pack(fill=tk.X, pady=(0, 5))
        
        # Password entry
        password_frame = tk.Frame(login_frame, bg=self.secondary_color)
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = tk.Label(
            password_frame,
            text="Password",
            font=("Helvetica", 10, "bold"),
            fg=self.text_color,
            bg=self.secondary_color,
            anchor="w"
        )
        password_label.pack(fill=tk.X)
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Helvetica", 12),
            bd=0,
            relief=tk.FLAT,
            show="*"  # Hide password input
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Add an underline
        tk.Frame(
            password_frame,
            height=2,
            bg=self.primary_color
        ).pack(fill=tk.X, pady=(0, 5))
        
        # Buttons frame
        button_frame = tk.Frame(login_frame, bg=self.secondary_color)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Login button with hover effect
        login_button = tk.Button(
            button_frame,
            text="Login",
            font=("Helvetica", 12, "bold"),
            fg=self.secondary_color,
            bg=self.primary_color,
            activebackground=self.accent_color,
            activeforeground=self.secondary_color,
            bd=0,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.login
        )
        login_button.pack(fill=tk.X, pady=(0, 10))
        
        # Create account button
        create_account_button = tk.Button(
            button_frame,
            text="Create New Account",
            font=("Helvetica", 12),
            fg=self.primary_color,
            bg=self.secondary_color,
            activeforeground=self.accent_color,
            activebackground=self.secondary_color,
            bd=0,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.show_create_account_page
        )   
        create_account_button.pack(fill=tk.X)

    def calculate_days_remaining(self, next_cycle_date_str):
        next_cycle_date = datetime.strptime(next_cycle_date_str, "%Y-%m-%d")
        current_date = datetime.now()
        days_remaining = (next_cycle_date - current_date).days
        return max(0, days_remaining)
            
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()  # Get password from the entry field
        
        if username in self.users:
            stored_password = self.users[username]["password"]
            
            if password == stored_password:
                self.current_user = username
                self.load_user_data()

                # Verify and update cycle dates if needed
                next_cycle_date = self.users[self.current_user]["next_cycle_date"]
                days_remaining = self.calculate_days_remaining(next_cycle_date)
                self.days_left.set(days_remaining)

                # Set frequency from saved data
                self.selected_frequency.set(self.users[self.current_user]["frequency"])

                # Check if cycle has completed while app was closed
                if days_remaining == 0:
                    self.complete_cycle()
                else:
                    self.create_main_page()
            else:
                messagebox.showerror("Login Error", "Incorrect password. Please try again.")
        else:
            messagebox.showerror("Login Error", "User does not exist. Please create an account.")

    def show_create_account_page(self):
        """Display a modern, simplified create account page."""
        self.clear_window()

        # Main container with a light background
        main_container = tk.Frame(self.root, bg="#f4f4f9")  # Light gray background
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header with light design
        header_frame = tk.Frame(main_container, bg="#f4f4f9", pady=15)
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text="Create Your Account",
            font=("Helvetica", 26, "bold"),  # Slightly increased font size
            fg="#1976d2",  # Bright blue for a modern look
            bg="#f4f4f9"
        ).pack()

        # Form container with soft light gray background
        form_frame = tk.Frame(main_container, bg="#f4f4f9", padx=40)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Basic Info Section
        def create_entry(parent, label_text, show=None):
            frame = tk.Frame(parent, bg="#f4f4f9", pady=8)
            frame.pack(fill=tk.X)

            tk.Label(
                frame,
                text=label_text,
                font=("Helvetica", 12),  # Slightly increased font size
                fg="#333333",  # Darker text for readability
                bg="#f4f4f9"
            ).pack(anchor="w")

            entry = tk.Entry(
                frame,
                font=("Helvetica", 12),  # Slightly increased font size
                bg="#ffffff",  # White background for inputs
                fg="#333333",  # Dark text for inputs
                insertbackground="#1976d2",  # Blue cursor color
                relief="flat",
                show=show
            )
            entry.pack(fill=tk.X, pady=(5, 0))

            # Accent line
            tk.Frame(
                frame,
                height=2,
                bg="#1976d2"  # Bright blue accent line
            ).pack(fill=tk.X, pady=(2, 0))

            return entry

        # Create the basic info entries
        self.new_username_entry = create_entry(form_frame, "USERNAME")
        self.password_entry = create_entry(form_frame, "PASSWORD", show="•")
        self.income_entry = create_entry(form_frame, "MONTHLY INCOME")

        # Categories Section
        categories_frame = tk.Frame(form_frame, bg="#f4f4f9", pady=15)
        categories_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            categories_frame,
            text="BUDGET CATEGORIES",
            font=("Helvetica", 16, "bold"),  # Slightly increased font size
            fg="#1976d2",  # Bright blue for category title
            bg="#f4f4f9"
        ).pack(pady=(0, 10))

        # Category list frame with scrollbar (Centering the categories)
        list_frame = tk.Frame(categories_frame, bg="#f4f4f9", pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, anchor='center')

        # Canvas for scrolling
        canvas = tk.Canvas(list_frame, bg="#f4f4f9", bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#f4f4f9")

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Default categories
        self.default_categories = ["Food", "Transport", "Entertainment", "Utilities", "Healthcare", "Education"]
        self.category_entries = {}

        # Create category entries
        for category in self.default_categories:
            cat_frame = tk.Frame(self.scrollable_frame, bg="#f4f4f9", pady=5)
            cat_frame.pack(fill=tk.X)

            tk.Label(
                cat_frame,
                text=category,
                font=("Helvetica", 12),  # Slightly increased font size
                fg="#333333",  # Dark text for categories
                bg="#f4f4f9",
                width=15,
                anchor="w"
            ).pack(side=tk.LEFT, padx=(10, 0))

            entry = tk.Entry(
                cat_frame,
                font=("Helvetica", 12),  # Slightly increased font size
                bg="#ffffff",  # White background for inputs
                fg="#333333",  # Dark text for inputs
                insertbackground="#1976d2",  # Blue cursor color
                relief="flat",
                width=15
            )
            entry.pack(side=tk.RIGHT, padx=10)
            entry.insert(0, "0")
            self.category_entries[category] = entry

        # Custom category entry
        custom_frame = tk.Frame(form_frame, bg="#f4f4f9", pady=15)
        custom_frame.pack(fill=tk.X)

        # Create and assign the custom category entry widget
        self.custom_category_entry = tk.Entry(
            custom_frame,
            font=("Helvetica", 12),
            bg="#ffffff",
            fg="#333333",
            insertbackground="#1976d2",
            relief="flat",
        )
        self.custom_category_entry.pack(fill=tk.X, pady=(5, 0), padx=(0, 10))

        # Accent line
        tk.Frame(
            custom_frame,
            height=2,
            bg="#1976d2"  # Bright blue accent line
        ).pack(fill=tk.X, pady=(2, 0), padx=(0, 10))

        # Add Custom Category Button
        add_category_btn = tk.Button(
            custom_frame,
            text="Add Custom Category",
            font=("Helvetica", 12, "bold"),  # Slightly increased font size
            fg="#ffffff",  # White text for button
            bg="#1976d2",  # Bright blue button color
            activebackground="#1565C0",  # Darker blue on hover
            activeforeground="#ffffff",  # White text on hover
            relief="flat",
            command=self.add_custom_category
        )
        add_category_btn.pack(side=tk.RIGHT, padx=10)

        # Buttons Frame
        button_frame = tk.Frame(form_frame, bg="#f4f4f9", pady=15)
        button_frame.pack(fill=tk.X)

        def create_button(parent, text, command, is_primary=True):
            btn = tk.Button(
                parent,
                text=text,
                font=("Helvetica", 12, "bold"),  # Slightly increased font size
                fg="#ffffff" if is_primary else "#1976d2",  # White text for primary, blue for secondary
                bg="#1976d2" if is_primary else "#ffffff",  # Blue for primary, white for secondary
                activebackground="#1565C0" if is_primary else "#f4f4f9",  # Darker blue for primary, lighter for secondary
                activeforeground="#ffffff" if is_primary else "#1976d2",  # White for primary, blue for secondary
                relief="flat",
                command=command,
                height=2
            )
            btn.pack(fill=tk.X, padx=20, pady=10)

        create_button(button_frame, "Create Account", self.create_account)

        # Go to Login button with updated color
        go_to_login_btn = tk.Button(
            button_frame,
            text="Go to Login",
            font=("Helvetica", 12, "bold"),  # Slightly increased font size
            fg="#ffffff",  # White text for button
            bg="#ff5722",  # Vibrant orange color for the button
            activebackground="#e64a19",  # Darker shade on hover
            activeforeground="#ffffff",  # White text on hover
            relief="flat",
            command=self.show_login_page
        )
        go_to_login_btn.pack(fill=tk.X, padx=20, pady=10)


    def add_custom_category(self):
        custom_category = self.custom_category_entry.get().strip()
        if custom_category:
            if custom_category not in self.category_entries:
                cat_frame = tk.Frame(self.scrollable_frame, bg="#f4f4f9", pady=5)
                cat_frame.pack(fill=tk.X)
                
                tk.Label(
                    cat_frame,
                    text=custom_category,
                    font=("Helvetica", 12),
                    fg="#333333",
                    bg="#f4f4f9",
                    width=15,
                    anchor="w"
                ).pack(side=tk.LEFT, padx=(10, 0))
                
                entry = tk.Entry(
                    cat_frame,
                    font=("Helvetica", 12),
                    bg="#ffffff",
                    fg="#333333",
                    insertbackground="#1976d2",
                    relief="flat",
                    width=15
                )
                entry.pack(side=tk.RIGHT, padx=10)
                entry.insert(0, "0")
                self.category_entries[custom_category] = entry
                
                self.custom_category_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Category already exists!")
        else:
            messagebox.showerror("Error", "Please enter a category name.")



    def create_account(self):
        username = self.new_username_entry.get()
        password = self.password_entry.get()  # Get password from the entry field
        try:
            income = float(self.income_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid income.")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists. Please choose another one.")
            return

        # Create categories dictionary
        categories = {}
        total_allocated = 0
        for category, allocation_entry in self.category_entries.items():
            try:
                allocation = float(allocation_entry.get())
                total_allocated += allocation
                categories[category] = {"allocated": allocation, "spent": 0}
            except ValueError:
                messagebox.showerror("Input Error", f"Please enter a valid amount for {category}.")
                return

        # Calculate initial savings
        initial_savings = income - total_allocated
        if initial_savings < 0:
            messagebox.showerror("Error", "Total allocations exceed income!")
            return

        # Add savings category
        categories["Savings"] = {"allocated": initial_savings, "spent": 0}

        # Set up cycle tracking
        current_date = datetime.now()
        frequency = "Monthly"  # Default frequency
        next_cycle_date = self.get_next_cycle_date(current_date, frequency)

        # Create user data (include password here)
        self.users[username] = {
            "password": password,  # Store password in the users dictionary
            "income": income,
            "categories": categories,
            "expenses": [],
            "frequency": frequency,
            "cycle_start_date": current_date.strftime("%Y-%m-%d"),
            "next_cycle_date": next_cycle_date.strftime("%Y-%m-%d"),
            "initial_savings": initial_savings,
            "current_savings": initial_savings
        }

        self.save_data()
        messagebox.showinfo("Account Created", f"Account for {username} created successfully!")
        self.show_login_page()

    
    def load_user_data(self):
        """Load current user's data."""
        self.expense_entries = self.users[self.current_user]["expenses"]
        self.categories = self.users[self.current_user]["categories"]
        self.original_allocations = {k: v["allocated"] for k, v in self.categories.items()}
        self.selected_frequency = tk.StringVar(value=self.users[self.current_user].get("frequency", "Monthly"))

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_page(self):
        """Create the main budgeting page with modern styling."""
        self.clear_window()
        
        # Define colors and styles
        COLORS = {
            'bg': '#f0f2f5',
            'card_bg': '#ffffff',
            'primary': '#1976d2',
            'success': '#4caf50',
            'warning': '#ff9800',
            'info': '#03a9f4',
            'purple': '#9c27b0',
            'text': '#2c3e50',
            'light_text': '#707070'
        }
        
        # Configure styles for ttk widgets
        style = ttk.Style()
        style.configure('Modern.TFrame', background=COLORS['bg'])
        style.configure('Card.TFrame', background=COLORS['card_bg'], relief='flat')
        style.configure('Modern.TLabel', background=COLORS['bg'], foreground=COLORS['text'])
        style.configure('Card.TLabel', background=COLORS['card_bg'], foreground=COLORS['text'])
        style.configure('Header.TLabel', background=COLORS['bg'], foreground=COLORS['text'], font=('Helvetica', 24, 'bold'))
        
        # Main container with modern background
        self.root.configure(bg=COLORS['bg'])
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_container, style='Modern.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        welcome_label = ttk.Label(header_frame, text=f"Welcome, {self.current_user}", style='Header.TLabel')
        welcome_label.pack(side=tk.LEFT)
        
        # Summary Cards
        summary_frame = ttk.Frame(main_container, style='Card.TFrame')
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        summary_frame.configure(padding=(20, 20))
        
        # Card data
        total_budget = self.users[self.current_user]["income"]
        total_spent = sum(cat["spent"] for cat in self.categories.values())
        total_remaining = total_budget - total_spent
        current_savings = self.users[self.current_user]["current_savings"]
        
        summary_items = [
            ("Total Budget", total_budget, COLORS['primary']),
            ("Total Spent", total_spent, COLORS['warning']),
            ("Remaining", total_remaining, COLORS['success']),
            ("Savings", current_savings, COLORS['purple'])
        ]
        
        for i, (label, value, color) in enumerate(summary_items):
            card_frame = ttk.Frame(summary_frame, style='Card.TFrame')
            card_frame.grid(row=0, column=i, padx=10, sticky='nsew')
            summary_frame.grid_columnconfigure(i, weight=1)
            
            # Label for the card title
            ttk.Label(card_frame, text=label, style='Card.TLabel', font=('Helvetica', 12)).pack(anchor='w', pady=(0, 5))
            
            # Value label with the correct background
            value_label = ttk.Label(
                card_frame, 
                text=f"₹{value:,.2f}", 
                font=('Helvetica', 16, 'bold'),
                background=COLORS['card_bg'],  # Ensure the background matches the card
                foreground=COLORS['text']      # Text color
            )
            value_label.pack(anchor='w')
            
            if label == "Total Budget":
                self.total_budget_label = value_label
            elif label == "Total Spent":
                self.total_spent_label = value_label
            elif label == "Remaining":
                self.total_remaining_label = value_label
            else:
                self.current_savings_label = value_label
            
            # Indicator bar
            canvas = tk.Canvas(card_frame, height=3, bg=color, highlightthickness=0)
            canvas.pack(fill=tk.X, pady=(10, 0))
        
        # Details Frame
        details_frame = ttk.Frame(main_container, style='Card.TFrame')
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        details_frame.configure(padding=(20, 20))
        
        ttk.Label(details_frame, text="Category Details", font=('Helvetica', 16, 'bold'), style='Card.TLabel').pack(anchor='w', pady=(0, 15))
        
        # Table Frame
        self.table_frame = ttk.Frame(details_frame, style='Card.TFrame')
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        self.load_table_data()
        
        # Timer Frame
        timer_frame = ttk.Frame(main_container, style='Card.TFrame')
        timer_frame.pack(fill=tk.X, pady=(0, 20))
        timer_frame.configure(padding=(20, 15))
        
        ttk.Label(timer_frame, text="Days Remaining:", style='Card.TLabel').pack(side=tk.LEFT)
        ttk.Label(timer_frame, textvariable=self.days_left, font=('Helvetica', 14, 'bold'), style='Card.TLabel').pack(side=tk.LEFT, padx=(5, 0))
        
        # Action Buttons
        button_frame = ttk.Frame(main_container, style='Modern.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        def create_custom_button(parent, text, command, bg_color):
            """Create a modern button with hover effect"""
            button = tk.Button(
                parent, text=text, command=command, bg=bg_color, fg='white',
                font=('Helvetica', 11), relief='flat', padx=15, pady=8, cursor='hand2'
            )
            button.bind('<Enter>', lambda e: button.configure(bg=self.adjust_color(bg_color, -20)))
            button.bind('<Leave>', lambda e: button.configure(bg=bg_color))
            return button
        
        buttons = [
            ("Add Expense", self.add_expense_form, COLORS['success']),
            ("Edit Categories", self.edit_categories, COLORS['warning']),
            ("Display Chart", self.display_chart, COLORS['purple']),
            ("View Entries", self.show_entries, COLORS['info']),
            ("Logout", self.show_login_page, COLORS['primary'])  # Logout Button
        ]
        
        for text, command, color in buttons:
            btn = create_custom_button(button_frame, text, command, color)
            btn.pack(side=tk.LEFT, padx=(0, 10))


    def load_table_data(self):
        """Load category data into a styled table."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        COLORS = {
        'bg': '#f0f2f5',
        'card_bg': '#ffffff',
        'primary': '#1976d2',
        'success': '#4caf50',
        'warning': '#ff9800',
        'info': '#03a9f4',
        'purple': '#9c27b0',
        'text': '#2c3e50',
        'light_text': '#707070'
        }   
        headers = ["Category", "Allocated", "Spent", "Remaining"]
        for col, header in enumerate(headers):
            tk.Label(
                self.table_frame,
                text=header,
                font=("Arial", 10, "bold"),
                bg=COLORS['card_bg'],  # Set to match card background
                fg=COLORS['text']       # Ensure text color is consistent
            ).grid(row=0, column=col, padx=10)

        for i, (category, data) in enumerate(self.categories.items()):
            tk.Label(
                self.table_frame,
                text=category,
                bg=COLORS['card_bg'],
                fg=COLORS['text']
            ).grid(row=i + 1, column=0)
            tk.Label(
                self.table_frame,
                text=f"{data['allocated']:.2f}",
                bg=COLORS['card_bg'],
                fg=COLORS['text']
            ).grid(row=i + 1, column=1)
            tk.Label(
                self.table_frame,
                text=f"{data['spent']:.2f}",
                bg=COLORS['card_bg'],
                fg=COLORS['text']
            ).grid(row=i + 1, column=2)
            remaining_amount = data['allocated'] - data['spent']
            tk.Label(
                self.table_frame,
                text=f"{remaining_amount:.2f}",
                bg=COLORS['card_bg'],
                fg=COLORS['text']
            ).grid(row=i + 1, column=3)

    def add_expense_form(self):
        """Improved and modernized expense form with better layout and validation."""
        self.clear_window()

        # Define colors and styles
        COLORS = {
            'bg': '#f0f2f5',  # Background color
            'card_bg': '#ffffff',  # Card background
            'primary': '#1976d2',  # Primary color (blue)
            'success': '#4caf50',  # Success color (green)
            'danger': '#f44336',  # Danger color (red)
            'text': '#2c3e50',  # Text color (dark gray)
            'input_bg': '#ffffff',  # Input background
            'button_hover': '#388e3c',  # Hover color for buttons
            'button_active': '#2c6c34'  # Active color for buttons
        }

        # Configure styles for ttk widgets
        style = ttk.Style()
        style.configure('Modern.TFrame', background=COLORS['bg'])
        style.configure('Modern.TLabel', background=COLORS['bg'], foreground=COLORS['text'], font=('Arial', 12, 'bold'))
        style.configure('Modern.TButton', font=('Arial', 12, 'bold'), relief="flat", anchor="center")
        style.configure('Modern.TLabelframe', background=COLORS['bg'], foreground=COLORS['text'], font=('Arial', 14, 'bold'))

        # Main frame with modern styling
        main_frame = ttk.Labelframe(self.root, text="Add New Expense", style='Modern.TLabelframe')
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Form frame for better spacing
        form_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        form_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Category selection
        category_label = ttk.Label(form_frame, text="Category:", style='Modern.TLabel')
        category_label.grid(row=0, column=0, pady=10, sticky="e")

        self.category_var = tk.StringVar()
        categories = list(self.categories.keys())
        self.category_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            values=categories,
            width=38,
            state="readonly"
        )
        self.category_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Amount entry (use tk.Entry instead of ttk.Entry)
        amount_label = ttk.Label(form_frame, text="Amount (₹):", style='Modern.TLabel')
        amount_label.grid(row=1, column=0, pady=10, sticky="e")
        self.amount_entry = tk.Entry(form_frame, width=30, font=('Arial', 12), bd=1, relief="solid", fg=COLORS['text'])
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Comments entry (use tk.Entry instead of ttk.Entry)
        comments_label = ttk.Label(form_frame, text="Comments:", style='Modern.TLabel')
        comments_label.grid(row=2, column=0, pady=10, sticky="e")
        self.comments_entry = tk.Entry(form_frame, width=30, font=('Arial', 12), bd=1, relief="solid", fg=COLORS['text'])
        self.comments_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Date entry (use tk.Entry instead of ttk.Entry)
        date_label = ttk.Label(form_frame, text="Date:", style='Modern.TLabel')
        date_label.grid(row=3, column=0, pady=10, sticky="e")
        self.date_entry = tk.Entry(form_frame, width=30, font=('Arial', 12), bd=1, relief="solid", fg=COLORS['text'])
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Buttons frame for action buttons
        button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        button_frame.pack(pady=20)

        # Modern Save button with hover effect
        save_button = tk.Button(
            button_frame,
            text="Save Expense",
            command=self.save_expense,
            bg=COLORS['success'],
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            relief="flat",
            cursor="hand2",
            bd=0,
            activebackground=COLORS['button_active']
        )
        save_button.pack(side=tk.LEFT, padx=10)
        save_button.bind('<Enter>', lambda e: save_button.configure(bg=self.adjust_color(COLORS['success'], -20)))
        save_button.bind('<Leave>', lambda e: save_button.configure(bg=COLORS['success']))

        # Modern Cancel button with hover effect
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            command=self.create_main_page,
            bg=COLORS['danger'],
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            relief="flat",
            cursor="hand2",
            bd=0,
            activebackground=COLORS['button_active']
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        cancel_button.bind('<Enter>', lambda e: cancel_button.configure(bg=self.adjust_color(COLORS['danger'], -20)))
        cancel_button.bind('<Leave>', lambda e: cancel_button.configure(bg=COLORS['danger']))

    def adjust_color(self, color, delta):
        """Adjusts the brightness of a given color."""
        r, g, b = self.hex_to_rgb(color)
        r = min(255, max(0, r + delta))
        g = min(255, max(0, g + delta))
        b = min(255, max(0, b + delta))
        return self.rgb_to_hex(r, g, b)

    def hex_to_rgb(self, hex_color):
        """Converts a hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, r, g, b):
        """Converts an RGB tuple to a hex color."""
        return f'#{r:02x}{g:02x}{b:02x}'

    def save_expense(self):
        """Save the new expense to the user's data with date of entry."""
        category = self.category_var.get()
        try:
            amount_spent = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return
        
        comments = self.comments_entry.get()
        date = self.date_entry.get()  # Use the date entered by the user

        # Update spent amount for the selected category
        self.categories[category]["spent"] += amount_spent
        self.expense_entries.append({
            "category": category,
            "amount": amount_spent,
            "comments": comments,
            "date": date  # Store the date
        })
        
        # Save data and return to main page
        self.save_data()
        self.create_main_page()

    def get_next_cycle_date(self, current_date, frequency):
        """Calculate the next cycle date based on the selected frequency."""
        if frequency == "Monthly":
            # For Monthly, add 1 month to the current date
            next_cycle_date = current_date.replace(day=1) + timedelta(days=32)
            next_cycle_date = next_cycle_date.replace(day=1)  # Adjust to next month's 1st day
        elif frequency == "Weekly":
            # For Weekly, add 7 days
            next_cycle_date = current_date + timedelta(weeks=1)
        elif frequency == "Yearly":
            # For Yearly, add 1 year
            next_cycle_date = current_date.replace(year=current_date.year + 1)
        else:
            next_cycle_date = current_date  # Default to current date if no frequency match

        return next_cycle_date

    def show_entries(self):
        """Create the All Expenses page with a table, filters, and download options."""
        self.clear_window()

        # New color scheme for a futuristic, vibrant look
        primary_color = "#9c27b0"  # Soft purple
        secondary_color = "#f0f0f0"  # Light gray background
        accent_color = "#00e676"  # Neon green for accents
        text_color = "#333333"  # Dark gray text for readability
        button_color1 = "#2196F3"  # Soft purple for the "Back to Main Page" button
        button_color2 = "#0D47A1"  # Pink for "Apply Filters"
        button_color3 = "#4A90E2"  # Cyan for "Download CSV"
        button_color4 = "#4A90E2"  # Orange for "Download PDF"

        # Main container for the All Expenses page
        main_container = tk.Frame(self.root, bg=secondary_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header frame with title and back button
        header_frame = tk.Frame(main_container, bg=secondary_color)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Back button
        back_button = tk.Button(
            header_frame,
            text="Back to Main Page",
            command=self.create_main_page,  # Assuming you have a show_main_menu method
            bg=button_color1,
            fg="white",
            activebackground=accent_color,
            activeforeground="white",
            relief=tk.FLAT,
            padx=15,
            font=("Arial", 10, "bold")
        )
        back_button.pack(side=tk.LEFT, pady=(0, 10))

        # Title
        tk.Label(
            header_frame,
            text="All Expenses",
            font=("Arial", 18, "bold"),
            bg=secondary_color,
            fg=text_color
        ).pack(side=tk.LEFT, pady=(0, 10), padx=(20, 0))

        # Frame for filters
        filter_frame = tk.Frame(main_container, bg=secondary_color)
        filter_frame.pack(fill=tk.X, pady=15)

        # Date range filters
        tk.Label(filter_frame, text="Start Date:", bg=secondary_color, fg=text_color).pack(side=tk.LEFT, padx=5)
        self.start_date = tk.Entry(filter_frame, width=15, font=("Arial", 12))
        self.start_date.pack(side=tk.LEFT, padx=5)
        self.start_date.insert(0, "YYYY-MM-DD")
        self.start_date.bind("<FocusIn>", self.clear_date_placeholder)
        self.start_date.bind("<FocusOut>", self.restore_date_placeholder)

        tk.Label(filter_frame, text="End Date:", bg=secondary_color, fg=text_color).pack(side=tk.LEFT, padx=5)
        self.end_date = tk.Entry(filter_frame, width=15, font=("Arial", 12))
        self.end_date.pack(side=tk.LEFT, padx=5)
        self.end_date.insert(0, "YYYY-MM-DD")
        self.end_date.bind("<FocusIn>", self.clear_date_placeholder)
        self.end_date.bind("<FocusOut>", self.restore_date_placeholder)

        # Category filter
        tk.Label(filter_frame, text="Category:", bg=secondary_color, fg=text_color).pack(side=tk.LEFT, padx=5)
        self.category_filter = tk.StringVar()
        category_options = ["All"] + list(self.categories.keys())
        category_menu = ttk.Combobox(filter_frame, textvariable=self.category_filter, values=category_options, state="readonly", font=("Arial", 12))
        category_menu.set("All")
        category_menu.pack(side=tk.LEFT, padx=5)

        # Sort by amount
        tk.Label(filter_frame, text="Sort by Amount:", bg=secondary_color, fg=text_color).pack(side=tk.LEFT, padx=5)
        self.sort_var = tk.StringVar()
        sort_options = ["None", "Ascending", "Descending"]
        sort_menu = ttk.Combobox(filter_frame, textvariable=self.sort_var, values=sort_options, state="readonly", font=("Arial", 12), width=12)
        sort_menu.set("None")
        sort_menu.pack(side=tk.LEFT, padx=5)

        # Button to apply filters
        apply_filter_button = tk.Button(
            filter_frame,
            text="Apply Filters",
            command=self.refresh_table,
            bg=button_color2,
            fg="white",
            activebackground=accent_color,
            activeforeground="white",
            relief=tk.FLAT,
            font=("Arial", 12, "bold"),
            padx=10
        )
        apply_filter_button.pack(side=tk.LEFT, padx=5)

        # Table frame with scrollbar
        table_frame = tk.Frame(main_container, bg=secondary_color)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Style configuration for the treeview (futuristic look)
        style = ttk.Style()
        style.configure(
            "Treeview",
            background=secondary_color,
            foreground=text_color,
            fieldbackground=secondary_color,
            font=("Arial", 12)
        )
        style.configure("Treeview.Heading", background=primary_color, foreground="black", font=("Arial", 12, "bold"))

        # Scrollbar for the table
        table_scrollbar = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview table to display expenses
        self.expenses_table = ttk.Treeview(table_frame, yscrollcommand=table_scrollbar.set)
        self.expenses_table["columns"] = ("date", "category", "amount", "comments")
        self.expenses_table.heading("#0", text="", anchor=tk.W)
        self.expenses_table.column("#0", width=0, stretch=tk.NO)
        self.expenses_table.heading("date", text="Date", anchor=tk.W)
        self.expenses_table.heading("category", text="Category", anchor=tk.W)
        self.expenses_table.heading("amount", text="Amount", anchor=tk.W)
        self.expenses_table.heading("comments", text="Comments", anchor=tk.W)

        # Set column widths
        self.expenses_table.column("date", width=120)
        self.expenses_table.column("category", width=150)
        self.expenses_table.column("amount", width=120)
        self.expenses_table.column("comments", width=250)

        self.expenses_table.pack(fill=tk.BOTH, expand=True)
        table_scrollbar.config(command=self.expenses_table.yview)

        # Buttons for downloading CSV and PDF
        download_frame = tk.Frame(main_container, bg=secondary_color)
        download_frame.pack(fill=tk.X, pady=10)

        download_csv_button = tk.Button(
            download_frame,
            text="Download CSV",
            command=self.download_csv,
            bg=button_color3,
            fg="white",
            activebackground=accent_color,
            activeforeground="white",
            relief=tk.FLAT,
            font=("Arial", 12, "bold"),
            padx=10
        )
        download_csv_button.pack(side=tk.LEFT, padx=5)

        download_pdf_button = tk.Button(
            download_frame,
            text="Download PDF",
            command=self.download_pdf,
            bg=button_color4,
            fg="white",
            activebackground=accent_color,
            activeforeground="white",
            relief=tk.FLAT,
            font=("Arial", 12, "bold"),
            padx=10
        )
        download_pdf_button.pack(side=tk.LEFT, padx=5)

        # Initially populate the table
        self.refresh_table()

    def refresh_table(self):
        """Refresh the table with filtered and sorted data."""
        # Clear existing items
        for item in self.expenses_table.get_children():
            self.expenses_table.delete(item)

        try:
            # Get filtered data
            filtered_data = self.get_filtered_data()

            # Apply sorting if selected
            sort_option = self.sort_var.get()
            if sort_option != "None":
                filtered_data = sorted(
                    filtered_data,
                    key=lambda x: float(x['amount']),
                    reverse=(sort_option == "Descending")
                )

            # Insert filtered and sorted data into table
            for expense in filtered_data:
                self.expenses_table.insert(
                    "",
                    tk.END,
                    values=(
                        expense["date"],
                        expense["category"],
                        f"₹{float(expense['amount']):.2f}",
                        expense["comments"]
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error refreshing table: {str(e)}")

    def get_filtered_data(self):
        """Retrieve filtered expense data based on selected filters."""
        try:
            # Get filter values
            category = self.category_filter.get()
            start_date_str = self.start_date.get().strip()
            end_date_str = self.end_date.get().strip()

            # Initialize filtered expenses with all expenses
            filtered_expenses = self.expense_entries

            # Apply date filters if dates are provided and valid
            if start_date_str and start_date_str != "YYYY-MM-DD":
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                filtered_expenses = [
                    expense for expense in filtered_expenses 
                    if datetime.strptime(expense["date"], "%Y-%m-%d") >= start_date
                ]

            if end_date_str and end_date_str != "YYYY-MM-DD":
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                filtered_expenses = [
                    expense for expense in filtered_expenses 
                    if datetime.strptime(expense["date"], "%Y-%m-%d") <= end_date
                ]

            # Apply category filter
            if category != "All":
                filtered_expenses = [
                    expense for expense in filtered_expenses 
                    if expense["category"] == category
                ]

            return filtered_expenses

        except ValueError as e:
            messagebox.showerror("Error", "Please enter dates in YYYY-MM-DD format")
            return self.expense_entries
        except Exception as e:
            messagebox.showerror("Error", f"Error filtering data: {str(e)}")
            return self.expense_entries
        
    def clear_date_placeholder(self, event):
        """Clear placeholder text when the field is focused."""
        if event.widget.get() == "YYYY-MM-DD":
            event.widget.delete(0, tk.END)

    def restore_date_placeholder(self, event):
        """Restore placeholder text if the field is empty."""
        if event.widget.get() == "":
            event.widget.insert(0, "YYYY-MM-DD")

    def download_csv(self):
        """Download the filtered expenses as a CSV file."""
        # Get the filtered data
        filtered_data = self.get_filtered_data()

        # Prompt the user to choose a file location
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            # Create a DataFrame and save to CSV
            df = pd.DataFrame(filtered_data)
            df.to_csv(file_path, index=False)
            tk.messagebox.showinfo("Success", "CSV file has been saved successfully!")

    def download_pdf(self):
        """Download the filtered expenses as a PDF file."""
        # Get the filtered data
        filtered_data = self.get_filtered_data()

        # Prompt the user to choose a file location
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            # Create a PDF and save the data
            c = canvas.Canvas(file_path)
            c.drawString(100, 800, "All Expenses Report")
            y_position = 750
            for expense in filtered_data:
                c.drawString(100, y_position, f"{expense['date']} - {expense['category']} - ₹{expense['amount']}: {expense['comments']}")
                y_position -= 20
                if y_position < 50:  # Start a new page if running out of space
                    c.showPage()
                    y_position = 750
            c.save()
            tk.messagebox.showinfo("Success", "PDF file has been saved successfully!")

    def filter_and_sort_entries(self, start_date, end_date, category, sort_order):
        """Filter entries based on date range, category, and sort them by amount."""
        filtered_entries = self.expense_entries

        # Filter by date range if provided
        if start_date:
            filtered_entries = [entry for entry in filtered_entries if datetime.strptime(entry['date'], '%Y-%m-%d') >= datetime.strptime(start_date, '%Y-%m-%d')]
        if end_date:
            filtered_entries = [entry for entry in filtered_entries if datetime.strptime(entry['date'], '%Y-%m-%d') <= datetime.strptime(end_date, '%Y-%m-%d')]

        # Filter by category if provided
        if category != "All Categories":
            filtered_entries = [entry for entry in filtered_entries if entry['category'] == category]

        # Sort entries by amount
        if sort_order == "Amount Ascending":
            filtered_entries.sort(key=lambda x: x['amount'])
        elif sort_order == "Amount Descending":
            filtered_entries.sort(key=lambda x: x['amount'], reverse=True)

        return filtered_entries

    def apply_filters(self, start_date, end_date, category, sort_order):
        """Apply filters and update the entries table."""
        # Save filter values to persist across function calls
        self.filter_values = {
            "start_date": start_date,
            "end_date": end_date,
            "category": category,
            "sort_order": sort_order
        }

        # Filter and sort the entries
        self.filtered_entries = self.filter_and_sort_entries(start_date, end_date, category, sort_order)

        # Refresh the entries (redraw the UI with filtered entries)
        self.show_entries()


    def edit_categories(self):
        """Create the Edit Categories page for modifying income and category details."""
        self.clear_window()

        # Define modern colors
        COLORS = {
            'bg': '#f4f6f9',  # Light background color
            'header': '#1976d2',  # Blue header color
            'success': '#4caf50',  # Green success button color
            'danger': '#f44336',  # Red danger button color
            'text': '#2c3e50',  # Dark text color
            'input_bg': '#ffffff',  # White input fields
            'input_fg': '#2c3e50',  # Dark text for inputs
        }

        # Main container for the Edit Categories page
        main_container = tk.Frame(self.root, bg=COLORS['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header for the Edit Categories page
        tk.Label(main_container, text="Edit Categories and Total Income", font=("Arial", 16, "bold"), fg=COLORS['header'], bg=COLORS['bg']).pack(pady=(0, 20))

        # Frame for editing total income
        income_frame = ttk.LabelFrame(main_container, text="Edit Total Income", padding=(10, 5))
        income_frame.pack(fill=tk.X, pady=10)

        # Entry for total income
        tk.Label(income_frame, text="Total Income:", font=("Arial", 12), fg=COLORS['text'], bg=COLORS['bg']).pack(side=tk.LEFT, padx=10)
        self.income_entry = tk.Entry(income_frame, font=("Arial", 12), bg=COLORS['input_bg'], fg=COLORS['input_fg'], width=25)
        self.income_entry.insert(0, str(self.users[self.current_user]["income"]))
        self.income_entry.pack(side=tk.LEFT, padx=10)

        # Frame for category management (use tk.Frame instead of ttk.Frame for bg support)
        category_frame = tk.Frame(main_container, bg=COLORS['bg'])
        category_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Listbox to display categories
        self.category_listbox = tk.Listbox(category_frame, font=("Arial", 12), bg=COLORS['input_bg'], fg=COLORS['input_fg'], height=10)
        self.category_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for category in self.categories:
            self.category_listbox.insert(tk.END, category)

        # Frame for category management buttons (use tk.Frame for bg support)
        button_frame = tk.Frame(category_frame, bg=COLORS['bg'])
        button_frame.pack(fill=tk.X, pady=10)

        # Add category button
        add_category_button = tk.Button(button_frame, text="Add Category", command=self.add_category, bg=COLORS['header'], fg="white", font=("Arial", 12), relief="flat", width=20)
        add_category_button.pack(side=tk.LEFT, padx=10)

        # Remove selected category button
        remove_category_button = tk.Button(button_frame, text="Remove Selected", command=self.remove_selected_category, bg=COLORS['danger'], fg="white", font=("Arial", 12), relief="flat", width=20)
        remove_category_button.pack(side=tk.LEFT, padx=10)

        # Edit allocated money button
        edit_alloc_button = tk.Button(button_frame, text="Edit Allocated Money", command=self.edit_allocated_money, bg=COLORS['success'], fg="white", font=("Arial", 12), relief="flat", width=20)
        edit_alloc_button.pack(side=tk.LEFT, padx=10)

        # Bottom button frame for Save and Back buttons (use tk.Frame for bg support)
        bottom_button_frame = tk.Frame(main_container, bg=COLORS['bg'])
        bottom_button_frame.pack(fill=tk.X, pady=20)

        # Save changes button
        save_button = tk.Button(bottom_button_frame, text="Save Changes", command=self.save_category_changes, bg=COLORS['success'], fg="white", font=("Arial", 12, "bold"), width=20)
        save_button.pack(side=tk.LEFT, padx=10)

        # Back button
        back_button = tk.Button(bottom_button_frame, text="Back", command=self.back_to_main_page, bg=COLORS['danger'], fg="white", font=("Arial", 12, "bold"), width=20)
        back_button.pack(side=tk.LEFT, padx=10)

    def add_category(self):
        """Add a new category to the list."""
        new_category = simpledialog.askstring("Add Category", "Enter category name:")
        if new_category:
            # Check if category already exists
            if new_category in self.categories:
                messagebox.showerror("Error", "Category already exists!")
                return
                
            # Add to new categories list
            self.new_categories.append(new_category)
            
            # Add to categories dict with initial values
            self.categories[new_category] = {"allocated": 0, "spent": 0}
            
            # Update the listbox
            self.category_listbox.insert(tk.END, new_category)
            
            # Show confirmation
            messagebox.showinfo("Success", f"Added new category: {new_category}")

    def remove_selected_category(self):
        """Remove the selected category."""
        selected_index = self.category_listbox.curselection()
        if selected_index:
            category_name = self.category_listbox.get(selected_index)
            if category_name == "Savings":
                messagebox.showerror("Error", "Cannot remove the Savings category!")
                return
                
            if category_name in self.categories:
                # Calculate remaining money in the category
                remaining_money = self.categories[category_name]["allocated"] - self.categories[category_name]["spent"]
                
                # Add remaining money to savings
                self.users[self.current_user]["current_savings"] += remaining_money
                if "Savings" in self.categories:
                    self.categories["Savings"]["allocated"] += remaining_money
                
                # Remove the category
                del self.categories[category_name]
                self.category_listbox.delete(selected_index)
                
                # Show confirmation message
                messagebox.showinfo("Success", f"Removed category {category_name} and transferred remaining funds to Savings")

    def edit_allocated_money(self):
        """Edit allocated money for the selected category."""
        selected_index = self.category_listbox.curselection()
        if selected_index:
            category_name = self.category_listbox.get(selected_index)
            if category_name in self.categories:  # Verify category exists
                current_allocated = self.categories[category_name]["allocated"]
                new_allocated = simpledialog.askfloat(
                    "Edit Allocated Money", 
                    f"Current allocated: ₹{current_allocated:.2f}\nEnter new amount:",
                    initialvalue=current_allocated
                )
                
                if new_allocated is not None:
                    # Calculate the difference in allocation
                    allocation_difference = new_allocated - current_allocated
                    
                    # Update savings based on change in allocated money
                    spent = self.categories[category_name]["spent"]
                    
                    # Update the category's allocated amount
                    self.categories[category_name]["allocated"] = new_allocated
                    
                    # Update current savings
                    self.users[self.current_user]["current_savings"] -= allocation_difference
                    
                    # Update the savings category if it exists
                    if "Savings" in self.categories:
                        self.categories["Savings"]["allocated"] = self.users[self.current_user]["current_savings"]
                    
                    # Show confirmation message
                    messagebox.showinfo("Success", f"Updated allocation for {category_name} to ₹{new_allocated:.2f}")

    def adjust_allocation(self, category, amount):
        """Adjust the allocation amount for a category."""
        self.categories[category]["allocated"] += amount
        self.allocated_entries[category].config(text=f"Allocated: {self.categories[category]['allocated']:.2f}")
    
    def back_to_main_page(self):
        """Return to the main page without saving changes."""
        # Show confirmation dialog before discarding changes
        if messagebox.askyesno("Confirm", "Any unsaved changes will be lost. Return to main page?"):
            self.create_main_page()

    def save_category_changes(self):
        """Save changes made in the Edit Categories page and update the main page."""
        try:
            # 1. Update total income if modified
            new_income = float(self.income_entry.get())
            if new_income != self.users[self.current_user]["income"]:
                self.users[self.current_user]["income"] = new_income

            # 2. Add new categories if specified
            for category in self.new_categories:
                if category not in self.categories:
                    self.categories[category] = {"allocated": 0, "spent": 0}
            
            # Clear the new categories list after processing
            self.new_categories.clear()

            # 3. Update the categories in the user data
            self.users[self.current_user]["categories"] = self.categories

            # 4. Save all changes to file
            self.save_data()

            # 5. Show success message
            messagebox.showinfo("Success", "Changes saved successfully!")

            # 6. Return to main page
            self.create_main_page()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for income.")
            return

    def update_main_page_budget_summary(self):
        """Update the total budget, spent, remaining, and current savings on the main page."""
        total_budget = self.users[self.current_user]["income"]
        total_spent = sum(cat["spent"] for cat in self.categories.values())
        total_remaining = total_budget - total_spent
        current_savings = self.users[self.current_user]["current_savings"]

        # Check if the label exists before updating
        if hasattr(self, 'total_budget_label'):
            self.total_budget_label.config(text=f"₹{total_budget:.2f}")

        if hasattr(self, 'total_spent_label'):
            self.total_spent_label.config(text=f"₹{total_spent:.2f}")

        if hasattr(self, 'total_remaining_label'):
            self.total_remaining_label.config(text=f"₹{total_remaining:.2f}")

        if hasattr(self, 'current_savings_label'):
            self.current_savings_label.config(text=f"₹{current_savings:.2f}")


    def display_chart(self):
        """Display charts in the main window based on category selection."""
        self.clear_window()

        # Create main container with a title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, text="Expense Analytics Dashboard", 
                            font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=5)

        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create filter frame
        filter_frame = ttk.LabelFrame(main_container, text="Analysis Controls", padding=10)
        filter_frame.pack(fill=tk.X, pady=5)

        # Create left frame for filters
        left_filter_frame = ttk.Frame(filter_frame)
        left_filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Category filter
        category_frame = ttk.Frame(left_filter_frame)
        category_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(category_frame, text="Category:", width=10).pack(side=tk.LEFT, padx=5)
        self.category_filter = ttk.Combobox(category_frame, 
                                        values=["All"] + list(self.categories.keys()),
                                        width=30)
        self.category_filter.set("All")
        self.category_filter.pack(side=tk.LEFT, padx=5)

        # Date range filters
        date_frame = ttk.Frame(left_filter_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        # Start date
        ttk.Label(date_frame, text="Start Date:", width=10).pack(side=tk.LEFT, padx=5)
        self.start_date = ttk.Entry(date_frame, width=15)
        self.start_date.insert(0, "YYYY-MM-DD")
        self.start_date.pack(side=tk.LEFT, padx=5)
        
        # End date
        ttk.Label(date_frame, text="End Date:", width=10).pack(side=tk.LEFT, padx=5)
        self.end_date = ttk.Entry(date_frame, width=15)
        self.end_date.insert(0, "YYYY-MM-DD")
        self.end_date.pack(side=tk.LEFT, padx=5)

        # Create right frame for chart controls
        right_filter_frame = ttk.Frame(filter_frame)
        right_filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)

        # Graph type selection
        graph_frame = ttk.LabelFrame(right_filter_frame, text="Chart Type", padding=5)
        graph_frame.pack(fill=tk.X, pady=5)
        
        self.graph_type = tk.StringVar(value="bar")
        
        chart_types = [("bar", "Bar Chart"), 
                    ("pie", "Pie Chart"), 
                    ("line", "Line Graph")]
        
        for value, text in chart_types:
            ttk.Radiobutton(graph_frame, 
                        text=text, 
                        variable=self.graph_type,
                        value=value).pack(side=tk.LEFT, padx=10)

        # Button frame
        button_frame = ttk.Frame(right_filter_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Generate charts button
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))
        
                # Generate Charts Button with tk.Button for better color control
        generate_btn = tk.Button(button_frame, 
                                text="Generate Charts", 
                                command=self.update_charts,
                                font=('Helvetica', 10, 'bold'),
                                bg="#4CAF50",  # Green color
                                fg="white",  # White text
                                activebackground="#45a049",  # Lighter green on hover
                                relief="flat",  # Removes the border for a modern look
                                padx=10, pady=5)
        generate_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Back to Dashboard Button with tk.Button for better color control
        back_btn = tk.Button(button_frame, 
                            text="Back to Dashboard", 
                            command=self.create_main_page,
                            font=('Helvetica', 10, 'bold'),
                            bg="#2196F3",  # Blue color
                            fg="white",  # White text
                            activebackground="#1976D2",  # Darker blue on hover
                            relief="flat",  # Removes the border for a modern look
                            padx=10, pady=5)
        back_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")




        # Create charts container
        charts_container = ttk.LabelFrame(main_container, text="Visualization", padding=10)
        charts_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.charts_frame = ttk.Frame(charts_container)
        self.charts_frame.pack(fill=tk.BOTH, expand=True)

        # Add hint label
        hint_label = ttk.Label(self.root, 
                            text="Tip: Select dates and category, then click 'Generate Charts' to update the visualization",
                            font=('Helvetica', 9, 'italic'))
        hint_label.pack(pady=5)

        # Add date validation and placeholder behavior
        def on_entry_click(event, default_text):
            """Clear placeholder text when entry is clicked."""
            widget = event.widget
            if widget.get() == default_text:
                widget.delete(0, tk.END)
                widget.config(foreground='black')

        def on_focus_out(event, default_text):
            """Restore placeholder text if entry is empty."""
            widget = event.widget
            if not widget.get():
                widget.insert(0, default_text)
                widget.config(foreground='gray')

        # Configure date entry fields
        for entry, default_text in [(self.start_date, "YYYY-MM-DD"), 
                                (self.end_date, "YYYY-MM-DD")]:
            entry.config(foreground='gray')
            entry.bind('<FocusIn>', lambda e, dt=default_text: on_entry_click(e, dt))
            entry.bind('<FocusOut>', lambda e, dt=default_text: on_focus_out(e, dt))

        # Initial chart creation
        self.update_charts()

        # Add keyboard shortcuts
        self.root.bind('<Control-g>', lambda e: self.update_charts())
        self.root.bind('<Escape>', lambda e: self.create_main_page())


    def update_charts(self):
        """Update charts based on selected category and filters."""
        try:
            # Clear existing charts
            for widget in self.charts_frame.winfo_children():
                widget.destroy()

            # Get filtered data
            filtered_expenses = self.get_filtered_data()
            
            if not filtered_expenses:
                messagebox.showinfo("No Data", "No expenses found for the selected filters.")
                return

            selected_category = self.category_filter.get()

            # Create single frame for selected graph type
            graph_frame = ttk.Frame(self.charts_frame)
            graph_frame.pack(fill=tk.BOTH, expand=True, pady=5)

            # Prepare category spending data
            category_spending = {}
            date_spending = {}  # For line graph
            
            if selected_category == "All":
                # Process data for all categories
                for expense in filtered_expenses:
                    category = expense["category"]
                    amount = float(expense["amount"])
                    date = expense["date"]

                    # For category totals (bar and pie charts)
                    if category not in category_spending:
                        category_spending[category] = 0
                    category_spending[category] += amount

                    # For daily totals (line graph)
                    if date not in date_spending:
                        date_spending[date] = 0
                    date_spending[date] += amount
            else:
                # Process data for single category
                for expense in filtered_expenses:
                    if expense["category"] == selected_category:
                        date = expense["date"]
                        amount = float(expense["amount"])
                        
                        # For daily spending (line graph)
                        if date not in date_spending:
                            date_spending[date] = 0
                        date_spending[date] += amount
                        
                        # For monthly aggregation (pie and bar charts)
                        month = date[:7]  # Get YYYY-MM
                        if month not in category_spending:
                            category_spending[month] = 0
                        category_spending[month] += amount

            selected_graph = self.graph_type.get()
            
            if selected_graph == "bar":
                if selected_category == "All":
                    self.create_bar_chart(graph_frame, category_spending, "Category Distribution")
                else:
                    self.create_bar_chart(graph_frame, category_spending, f"Monthly Spending - {selected_category}", 
                                        is_monthly=True)
            elif selected_graph == "pie":
                if selected_category == "All":
                    self.create_pie_chart(graph_frame, category_spending, "Category Distribution")
                else:
                    self.create_pie_chart(graph_frame, category_spending, f"Monthly Distribution - {selected_category}", 
                                        is_monthly=True)
            else:  # line graph
                title = "All Categories" if selected_category == "All" else selected_category
                self.create_line_graph(graph_frame, date_spending, title)

        except Exception as e:
            messagebox.showerror("Error", f"Error updating charts: {str(e)}")
            print(f"Detailed error: {e}")


    def create_bar_chart(self, frame, data, title, is_monthly=False):
        """Create a bar chart comparing allocated vs spent amounts."""
        fig_bar = Figure(figsize=(10, 6))
        ax_bar = fig_bar.add_subplot(111)

        if is_monthly:
            # For single category monthly view
            months = list(data.keys())
            spent = list(data.values())
            x = range(len(months))

            ax_bar.bar(x, spent, color='lightcoral')
            ax_bar.set_ylabel('Amount Spent (₹)')
            ax_bar.set_title(title)
            ax_bar.set_xticks(x)
            ax_bar.set_xticklabels(months, rotation=45)

            # Annotate each bar with the spent amount
            for i, amount in enumerate(spent):
                ax_bar.text(i, amount, f'₹{amount}', ha='center', va='bottom', fontsize=9, color='black')

        else:
            # For all categories view
            categories = list(data.keys())
            spent = list(data.values())

            # Ensure categories have valid data
            if not categories:
                ax_bar.text(0.5, 0.5, 'No categories to display', ha='center', va='center', fontsize=12, color='gray')
                ax_bar.set_axis_off()
            else:
                allocated = [
                    float(self.categories[cat]["allocated"]) if cat in self.categories else 0 for cat in categories
                ]
                x = range(len(categories))
                width = 0.35

                # Draw the bars
                ax_bar.bar([i - width / 2 for i in x], allocated, width, label='Allocated', color='lightblue')
                ax_bar.bar([i + width / 2 for i in x], spent, width, label='Spent', color='lightcoral')

                ax_bar.set_ylabel('Amount (₹)')
                ax_bar.set_title(title)
                ax_bar.set_xticks(x)
                ax_bar.set_xticklabels(categories, rotation=45)
                ax_bar.legend()

                # Annotate each bar with the allocated and spent amounts
                for i, (alloc, amount) in enumerate(zip(allocated, spent)):
                    ax_bar.text(i - width / 2, alloc, f'₹{alloc}', ha='center', va='bottom', fontsize=9, color='black')
                    ax_bar.text(i + width / 2, amount, f'₹{amount}', ha='center', va='bottom', fontsize=9, color='black')

        # Format y-axis to show integers
        ax_bar.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))

        fig_bar.tight_layout()

        canvas_bar = FigureCanvasTkAgg(fig_bar, frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().pack(fill=tk.BOTH, expand=True)



    def create_pie_chart(self, frame, data, title, is_monthly=False):
        """Create a pie chart showing spending distribution."""
        fig_pie = Figure(figsize=(10, 6))
        ax_pie = fig_pie.add_subplot(111)
        
        labels = list(data.keys())
        values = list(data.values())
        
        if sum(values) > 0:
            patches, texts, autotexts = ax_pie.pie(values, labels=labels, autopct='%1.1f%%')
            ax_pie.set_title(title)
            
            # Rotate labels for better readability if monthly view
            if is_monthly:
                plt.setp(texts, rotation=30)
        
        fig_pie.tight_layout()
        
        canvas_pie = FigureCanvasTkAgg(fig_pie, frame)
        canvas_pie.draw()
        canvas_pie.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_line_graph(self, frame, date_spending, category=None):
        """Create a line graph showing spending trends over time."""
        fig_line = Figure(figsize=(10, 6))
        ax_line = fig_line.add_subplot(111)
        
        # Sort dates and prepare data
        sorted_dates = sorted(date_spending.keys())
        amounts = [date_spending[date] for date in sorted_dates]
        
        if sorted_dates:
            # Convert dates to datetime objects
            dates = [datetime.strptime(date, "%Y-%m-%d") for date in sorted_dates]
            
            # Plot the line
            ax_line.plot(dates, amounts, marker='o')
            
            # Set labels
            ax_line.set_xlabel('Date')
            ax_line.set_ylabel('Amount Spent (₹)')
            
            title = 'Daily Spending Trend'
            if category:
                title += f' - {category}'
            ax_line.set_title(title)
            
            # Format x-axis dates
            from matplotlib.dates import DateFormatter
            date_formatter = DateFormatter('%Y-%m-%d')
            ax_line.xaxis.set_major_formatter(date_formatter)
            
            # Rotate and align the tick labels so they look better
            plt.setp(ax_line.get_xticklabels(), rotation=45, ha='right')
            
            # Add gridlines
            ax_line.grid(True, linestyle='--', alpha=0.7)
            
            # Format y-axis to show integers
            ax_line.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
            
            # Adjust layout to prevent label cutoff
            fig_line.tight_layout()
        
        canvas_line = FigureCanvasTkAgg(fig_line, frame)
        canvas_line.draw()
        canvas_line.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def get_all_entries(self):
        """Retrieve all entries from the database."""
        try:
            with open('entries.json', 'r') as f:
                entries = json.load(f)
            return entries.get(self.current_user, [])
        except FileNotFoundError:
            return []

    def clear_window(self):
        """Clear the current content in the window."""
        for widget in self.root.winfo_children():
            widget.destroy()


    def complete_cycle(self):
        """Resets the cycle and updates values at the end of the month."""
        # Get the current date
        current_date = datetime.now()
        
        # Retrieve next cycle date
        next_cycle_date = datetime.strptime(self.users[self.current_user]["next_cycle_date"], "%Y-%m-%d")
        
        # Check if the current date has surpassed the next cycle date (end of the month)
        if current_date >= next_cycle_date:
            # Calculate total remaining for all categories excluding savings
            total_remaining = sum(
                cat["allocated"] - cat["spent"]
                for cat_name, cat in self.categories.items()
                if cat_name != "Savings"
            )
            
            # Update current savings (add the remaining balance to savings)
            current_savings = self.users[self.current_user]["current_savings"]
            new_savings = current_savings + total_remaining
            self.users[self.current_user]["current_savings"] = new_savings
            self.categories["Savings"]["allocated"] = new_savings
            
            # Reset spent amounts for all categories
            for category in self.categories.values():
                category["spent"] = 0
            
            # Update total spent and total remaining for the summary
            total_spent = sum(cat["spent"] for cat in self.categories.values())
            total_remaining = self.users[self.current_user]["income"] - total_spent
            
            # Update the user data with the reset totals
            self.users[self.current_user]["total_spent"] = total_spent
            self.users[self.current_user]["total_remaining"] = total_remaining

            # Update cycle date
            next_cycle_date = next_cycle_date + timedelta(days=30)  # Move to the next month
            self.users[self.current_user]["next_cycle_date"] = next_cycle_date.strftime("%Y-%m-%d")
            
            # Save the updated data
            self.save_data()

            # Refresh or reload main page to reflect changes
            self.create_main_page()

root = tk.Tk()
#root.attributes("-fullscreen",True)
root.tk.call('tk', 'scaling', 1.75)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print(f"Failed to set DPI awareness: {e}")

app = PersonalBudgetApp(root)
root.mainloop()
