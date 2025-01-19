import tkinter as tk
from tkinter import messagebox
import csv
import os
import datetime

import  re
# BankAccount class to handle basic banking operations
class BankAccount:
    def __init__(self, account_id, name, dob, address, balance=0):
        self.account_id = account_id
        self.name = name
        self.dob = dob
        self.address = address
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    @staticmethod
    def to_dict(account):
        return {
            "account_id": account.account_id,
            "name": account.name,
            "dob": account.dob,
            "address": account.address,
            "balance": account.balance
        }


# BankApp class to handle the UI logic
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("money Bank - Banking System")

        self.accounts = {}  # Dictionary to store accounts by account ID

        # Load accounts from CSV
        self.load_accounts()

        # Home page frame
        self.home_frame = tk.Frame(root)
        self.home_frame.pack()

        self.home_label = tk.Label(self.home_frame, text="Welcome to money Bank", font=("Arial", 18))
        self.home_label.pack(pady=20)

        self.create_account_button = tk.Button(self.home_frame, text="Create Account", width=20,
                                               command=self.show_create_account_page)
        self.create_account_button.pack(pady=10)

        self.deposit_button = tk.Button(self.home_frame, text="Deposit Money", width=20, command=self.show_deposit_page)
        self.deposit_button.pack(pady=10)

        self.withdraw_button = tk.Button(self.home_frame, text="Withdraw Money", width=20,
                                         command=self.show_withdraw_page)
        self.withdraw_button.pack(pady=10)

        self.delete_account_button = tk.Button(self.home_frame, text="Delete Account", width=20,
                                               command=self.show_delete_account_page)
        self.delete_account_button.pack(pady=10)

        self.check_balance_button = tk.Button(self.home_frame, text="Check Balance", width=20,
                                              command=self.show_check_balance_page)
        self.check_balance_button.pack(pady=10)

        # Create Account Page
        self.create_account_frame = tk.Frame(root)

        self.account_id_label = tk.Label(self.create_account_frame, text="Account ID:")
        self.account_id_label.pack()
        self.account_id_entry = tk.Entry(self.create_account_frame)
        self.account_id_entry.pack()

        self.name_label = tk.Label(self.create_account_frame, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.create_account_frame)
        self.name_entry.pack()

        self.dob_label = tk.Label(self.create_account_frame, text="Date of Birth (DD/MM/YYYY):")
        self.dob_label.pack()
        self.dob_entry = tk.Entry(self.create_account_frame)
        self.dob_entry.pack()

        self.address_label = tk.Label(self.create_account_frame, text="Address:")
        self.address_label.pack()
        self.address_entry = tk.Entry(self.create_account_frame)
        self.address_entry.pack()

        self.initial_deposit_label = tk.Label(self.create_account_frame, text="Initial Deposit ($):")
        self.initial_deposit_label.pack()
        self.initial_deposit_entry = tk.Entry(self.create_account_frame)
        self.initial_deposit_entry.pack()

        self.create_account_button_in_page = tk.Button(self.create_account_frame, text="Create Account",
                                                       command=self.create_account)
        self.create_account_button_in_page.pack()

        self.back_to_home_button_from_create = tk.Button(self.create_account_frame, text="Back to Home",
                                                         command=self.show_home_page)
        self.back_to_home_button_from_create.pack()

        # Deposit Page
        self.deposit_frame = tk.Frame(root)

        self.deposit_account_id_label = tk.Label(self.deposit_frame, text="Account ID:")
        self.deposit_account_id_label.pack()
        self.deposit_account_id_entry = tk.Entry(self.deposit_frame)
        self.deposit_account_id_entry.pack()

        self.deposit_amount_label = tk.Label(self.deposit_frame, text="Deposit Amount ($):")
        self.deposit_amount_label.pack()
        self.deposit_amount_entry = tk.Entry(self.deposit_frame)
        self.deposit_amount_entry.pack()

        self.deposit_button_in_page = tk.Button(self.deposit_frame, text="Deposit", command=self.deposit)
        self.deposit_button_in_page.pack()

        self.back_to_home_button_from_deposit = tk.Button(self.deposit_frame, text="Back to Home",
                                                          command=self.show_home_page)
        self.back_to_home_button_from_deposit.pack()

        # Withdraw Page
        self.withdraw_frame = tk.Frame(root)

        self.withdraw_account_id_label = tk.Label(self.withdraw_frame, text="Account ID:")
        self.withdraw_account_id_label.pack()
        self.withdraw_account_id_entry = tk.Entry(self.withdraw_frame)
        self.withdraw_account_id_entry.pack()

        self.withdraw_amount_label = tk.Label(self.withdraw_frame, text="Withdraw Amount ($):")
        self.withdraw_amount_label.pack()
        self.withdraw_amount_entry = tk.Entry(self.withdraw_frame)
        self.withdraw_amount_entry.pack()

        self.withdraw_button_in_page = tk.Button(self.withdraw_frame, text="Withdraw", command=self.withdraw)
        self.withdraw_button_in_page.pack()

        self.back_to_home_button_from_withdraw = tk.Button(self.withdraw_frame, text="Back to Home",
                                                           command=self.show_home_page)
        self.back_to_home_button_from_withdraw.pack()

        # Delete Account Page
        self.delete_account_frame = tk.Frame(root)

        self.delete_account_id_label = tk.Label(self.delete_account_frame, text="Account ID:")
        self.delete_account_id_label.pack()
        self.delete_account_id_entry = tk.Entry(self.delete_account_frame)
        self.delete_account_id_entry.pack()

        self.delete_account_button_in_page = tk.Button(self.delete_account_frame, text="Delete Account",
                                                       command=self.delete_account)
        self.delete_account_button_in_page.pack()

        self.back_to_home_button_from_delete = tk.Button(self.delete_account_frame, text="Back to Home",
                                                         command=self.show_home_page)
        self.back_to_home_button_from_delete.pack()

        # Check Balance Page
        self.check_balance_frame = tk.Frame(root)

        self.check_balance_account_id_label = tk.Label(self.check_balance_frame, text="Account ID:")
        self.check_balance_account_id_label.pack()
        self.check_balance_account_id_entry = tk.Entry(self.check_balance_frame)
        self.check_balance_account_id_entry.pack()

        self.check_balance_button_in_page = tk.Button(self.check_balance_frame, text="Check Balance",
                                                      command=self.check_balance)
        self.check_balance_button_in_page.pack()

        self.back_to_home_button_from_check_balance = tk.Button(self.check_balance_frame, text="Back to Home",
                                                                command=self.show_home_page)
        self.back_to_home_button_from_check_balance.pack()

    def load_accounts(self):
        """ Load accounts from CSV file into the dictionary """
        if os.path.exists('accounts.csv'):
            with open('accounts.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # To avoid empty rows
                        account_id, name, dob, address, balance = row
                        balance = float(balance)
                        self.accounts[account_id] = BankAccount(account_id, name, dob, address, balance)

    def save_accounts(self):
        """ Save all accounts in the dictionary back to the CSV file """
        with open('accounts.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for account in self.accounts.values():
                writer.writerow([account.account_id, account.name, account.dob, account.address, account.balance])

    def show_home_page(self):
        """ Show the home page frame """
        self.clear_frames()
        self.home_frame.pack()

    def show_create_account_page(self):
        """ Show the create account page frame """
        self.clear_frames()
        self.create_account_frame.pack()

    def show_deposit_page(self):
        """ Show the deposit page frame """
        self.clear_frames()
        self.deposit_frame.pack()

    def show_withdraw_page(self):
        """ Show the withdraw page frame """
        self.clear_frames()
        self.withdraw_frame.pack()

    def show_delete_account_page(self):
        """ Show the delete account page frame """
        self.clear_frames()
        self.delete_account_frame.pack()

    def show_check_balance_page(self):
        """ Show the check balance page frame """
        self.clear_frames()
        self.check_balance_frame.pack()

    def clear_frames(self):
        """ Clear all frames from the window """
        for frame in [self.home_frame, self.create_account_frame, self.deposit_frame, self.withdraw_frame,
                      self.delete_account_frame, self.check_balance_frame]:
            frame.pack_forget()

    def create_account(self):
        account_id = self.account_id_entry.get().strip()
        name = self.name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        if not self.is_valid_dob(dob):
            messagebox.showwarning("Invalid DOB", "Please enter a valid Date of Birth in the format DD/MM/YYYY.")
            return
        address = self.address_entry.get().strip()
        try:
            initial_deposit = float(self.initial_deposit_entry.get())
            if name == "" or dob == "" or address == "" or initial_deposit < 0 or account_id == "":
                messagebox.showwarning("Invalid Input", "Please fill all fields with valid data.")
                return

            if account_id in self.accounts:
                messagebox.showwarning("Account ID Exists", f"Account ID '{account_id}' already exists.")
                return

            # Create a new bank account with the user-provided Account ID
            new_account = BankAccount(account_id, name, dob, address, initial_deposit)
            self.accounts[account_id] = new_account

            # Save updated accounts to CSV
            self.save_accounts()

            messagebox.showinfo("Success", f"Account created successfully!\nAccount ID: {account_id}")
            self.show_home_page()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number for the deposit amount.")

    def get_selected_account(self):
        account_id = self.deposit_account_id_entry.get().strip()
        if not account_id or account_id not in self.accounts:
            messagebox.showwarning("Invalid Account", "Please enter a valid Account ID.")
            return None
        return self.accounts.get(account_id)

    def is_valid_dob(self, dob):
        """ Validate the Date of Birth format and value """
        try:
            # Check if the date matches the format DD/MM/YYYY
            dob_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
            if not dob_pattern.match(dob):
                return False

            # Convert string to date object to check if it is a valid date
            dob_obj = datetime.strptime(dob, "%d/%m/%Y")

            # Check if the user is at least 18 years old
            today = datetime.today()
            age = today.year - dob_obj.year - ((today.month, today.day) < (dob_obj.month, dob_obj.day))
            if age < 18:
                messagebox.showwarning("Age Restriction", "You must be at least 18 years old to open an account.")
                return False

            return True
        except ValueError:
            # If the date conversion fails, it's an invalid date
            return False

    def deposit(self):
        account = self.get_selected_account()
        if account:
            try:
                amount = float(self.deposit_amount_entry.get())
                if account.deposit(amount):
                    messagebox.showinfo("Success", f"Deposited ${amount:.2f} successfully!")
                    self.save_accounts()  # Save updated accounts
                    self.show_home_page()
                else:
                    messagebox.showwarning("Invalid Amount", "Deposit amount must be greater than 0.")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number for the deposit amount.")

    def withdraw(self):
        account = self.get_selected_account()
        if account:
            try:
                amount = float(self.withdraw_amount_entry.get())
                if account.withdraw(amount):
                    messagebox.showinfo("Success", f"Withdrew ${amount:.2f} successfully!")
                    self.save_accounts()  # Save updated accounts
                    self.show_home_page()
                else:
                    messagebox.showwarning("Insufficient Funds", "Not enough balance to withdraw.")
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid number for the withdrawal amount.")

    def delete_account(self):
        account_id = self.delete_account_id_entry.get().strip()
        if account_id not in self.accounts:
            messagebox.showwarning("Invalid Account", "Account ID does not exist.")
            return

        confirmation = messagebox.askyesno("Delete Account",
                                           f"Are you sure you want to delete Account ID: {account_id}?")
        if confirmation:
            del self.accounts[account_id]
            self.save_accounts()  # Save updated accounts
            messagebox.showinfo("Deleted", f"Account ID {account_id} deleted successfully.")
            self.show_home_page()

    def check_balance(self):
        account_id = self.check_balance_account_id_entry.get().strip()
        if not account_id or account_id not in self.accounts:
            messagebox.showwarning("Invalid Account", "Please enter a valid Account ID.")
            return

        account = self.accounts[account_id]
        balance = account.get_balance()
        messagebox.showinfo("Account Balance", f"Account ID: {account_id}\nBalance: ${balance:.2f}")
        self.show_home_page()


# Initialize the main Tkinter window
def main():
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
