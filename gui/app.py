import tkinter as tk
from tkinter import ttk, messagebox
from database.db_setup import create_connection, setup_database
from models.transaction import Transaction
from utils.helpers import format_currency

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget App")
        self.root.geometry("600x600")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Apply some custom styling for a prettier UI
        self.style.configure('TLabel', font=('Helvetica', 12))
        self.style.configure('TButton', font=('Helvetica', 12), background='#4CAF50', foreground='white')
        self.style.configure('TEntry', font=('Helvetica', 12))
        self.style.configure('TFrame', background='#f5f5f5')
        
        # Initialize database
        setup_database()

        self.create_widgets()

    def create_widgets(self):
        # Frame for balance
        self.frame_balance = ttk.Frame(self.root, padding="10")
        self.frame_balance.pack(fill="x", padx=10, pady=5)
        
        self.balance_label = ttk.Label(self.frame_balance, text="Current Balance: $0.00", font=('Helvetica', 16, 'bold'))
        self.balance_label.pack(side="left")

        # Add transaction section
        self.frame_add = ttk.LabelFrame(self.root, text="Add Transaction", padding="10")
        self.frame_add.pack(fill="x", padx=10, pady=5)

        self.amount_label = ttk.Label(self.frame_add, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.frame_add)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        self.desc_label = ttk.Label(self.frame_add, text="Description:")
        self.desc_label.grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.frame_add)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        self.type_label = ttk.Label(self.frame_add, text="Type:")
        self.type_label.grid(row=2, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="Expense")
        self.type_expense = ttk.Radiobutton(self.frame_add, text="Expense", variable=self.type_var, value="Expense")
        self.type_income = ttk.Radiobutton(self.frame_add, text="Income", variable=self.type_var, value="Income")
        self.type_expense.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.type_income.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        self.add_button = ttk.Button(self.frame_add, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=3, columnspan=3, pady=10)

        # Recurring transaction section
        self.frame_recurring = ttk.LabelFrame(self.root, text="Add Recurring Transaction", padding="10")
        self.frame_recurring.pack(fill="x", padx=10, pady=5)

        self.rec_amount_label = ttk.Label(self.frame_recurring, text="Amount:")
        self.rec_amount_label.grid(row=0, column=0, padx=5, pady=5)
        self.rec_amount_entry = ttk.Entry(self.frame_recurring)
        self.rec_amount_entry.grid(row=0, column=1, padx=5, pady=5)

        self.rec_desc_label = ttk.Label(self.frame_recurring, text="Description:")
        self.rec_desc_label.grid(row=1, column=0, padx=5, pady=5)
        self.rec_desc_entry = ttk.Entry(self.frame_recurring)
        self.rec_desc_entry.grid(row=1, column=1, padx=5, pady=5)

        self.rec_type_label = ttk.Label(self.frame_recurring, text="Type:")
        self.rec_type_label.grid(row=2, column=0, padx=5, pady=5)
        self.rec_type_var = tk.StringVar(value="Expense")
        self.rec_type_expense = ttk.Radiobutton(self.frame_recurring, text="Expense", variable=self.rec_type_var, value="Expense")
        self.rec_type_income = ttk.Radiobutton(self.frame_recurring, text="Income", variable=self.rec_type_var, value="Income")
        self.rec_type_expense.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.rec_type_income.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        self.frequency_label = ttk.Label(self.frame_recurring, text="Frequency:")
        self.frequency_label.grid(row=3, column=0, padx=5, pady=5)
        self.frequency_var = tk.StringVar(value="Monthly")
        self.frequency_menu = ttk.Combobox(self.frame_recurring, textvariable=self.frequency_var, values=["Daily", "Weekly", "Monthly"])
        self.frequency_menu.grid(row=3, column=1, padx=5, pady=5)

        self.add_recurring_button = ttk.Button(self.frame_recurring, text="Add Recurring Transaction", command=self.add_recurring_transaction)
        self.add_recurring_button.grid(row=4, columnspan=3, pady=10)

        # Transaction history section with drop-down
        self.frame_history = ttk.LabelFrame(self.root, text="Transaction History", padding="10")
        self.frame_history.pack(fill="x", padx=10, pady=5)

        self.history_combobox = ttk.Combobox(self.frame_history, height=10, width=60)
        self.history_combobox.pack(fill="x", padx=10, pady=5)
        self.history_combobox.bind("<<ComboboxSelected>>", self.show_transaction_detail)

        self.transaction_detail_text = tk.Text(self.frame_history, height=10, width=60)
        self.transaction_detail_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.transaction_detail_text.config(state=tk.DISABLED)

        self.load_transactions()

    def add_transaction(self):
        amount = self.amount_entry.get()
        description = self.desc_entry.get()
        transaction_type = self.type_var.get()

        if not amount or not description:
            messagebox.showwarning("Input Error", "Please enter all fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount")
            return

        conn = create_connection()
        c = conn.cursor()
        transaction = Transaction(description, amount, transaction_type)
        c.execute("INSERT INTO transactions (date, description, amount, type) VALUES (?, ?, ?, ?)", 
                  (transaction.date, transaction.description, transaction.amount, transaction.type))
        conn.commit()
        conn.close()

        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

        self.load_transactions()

    def add_recurring_transaction(self):
        amount = self.rec_amount_entry.get()
        description = self.rec_desc_entry.get()
        transaction_type = self.rec_type_var.get()
        frequency = self.frequency_var.get()

        if not amount or not description:
            messagebox.showwarning("Input Error", "Please enter all fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount")
            return

        conn = create_connection()
        c = conn.cursor()
        c.execute("INSERT INTO recurring_transactions (start_date, description, amount, type, frequency) VALUES (datetime('now'), ?, ?, ?, ?)", 
                  (description, amount, transaction_type, frequency))
        conn.commit()
        conn.close()

        self.rec_amount_entry.delete(0, tk.END)
        self.rec_desc_entry.delete(0, tk.END)

        self.load_transactions()

    def load_transactions(self):
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT date, description, amount, type FROM transactions")
        transactions = c.fetchall()
        conn.close()

        self.history_combobox['values'] = [f"{date} - {description}" for (date, description, _, _) in transactions]

        balance = 0
        for transaction in transactions:
            date, description, amount, transaction_type = transaction
            if transaction_type == "Expense":
                amount = -amount
            balance += amount

        self.balance_label.config(text=f"Current Balance: {format_currency(balance)}")

    def show_transaction_detail(self, event):
        selected_index = self.history_combobox.current()
        if selected_index == -1:
            return

        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM transactions")
        transactions = c.fetchall()
        conn.close()

        transaction = transactions[selected_index]
        date, description, amount, transaction_type = transaction[1], transaction[2], transaction[3], transaction[4]

        detail = f"Date: {date}\nDescription: {description}\nAmount: {format_currency(amount)}\nType: {transaction_type}"
        self.transaction_detail_text.config(state=tk.NORMAL)
        self.transaction_detail_text.delete('1.0', tk.END)
        self.transaction_detail_text.insert(tk.END, detail)
        self.transaction_detail_text.config(state=tk.DISABLED)
