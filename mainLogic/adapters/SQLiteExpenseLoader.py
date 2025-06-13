import sqlite3
from mainLogic.adapters.abstract.ExpenseLoader import ExpenseLoader
from mainLogic.expensesMonitor.Expense import Expense
from datetime import date
import os

class SQLiteExpenseLoader(ExpenseLoader):
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(base_dir, '..', '..', 'data', 'expenses.db')
            self.db_path = os.path.abspath(self.db_path)
        else:
            self.db_path = db_path

        # Tworzenie folderu, jeśli nie istnieje
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self._create_table_if_not_exists()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table_if_not_exists(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            ''')
            conn.commit()

    def load_expenses(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, amount, category, description, date FROM expenses")
            rows = cursor.fetchall()
            return [
                Expense(
                    amount,
                    category,
                    description,
                    date.fromisoformat(date_str),  # <-- bezpieczne i spójne
                    id
                )
                for id, amount, category, description, date_str in rows
            ]

    def save_expenses(self, expenses):
        with self._connect() as conn:
            cursor = conn.cursor()
            for exp in expenses:
                if exp.id is not None:
                    cursor.execute(
                        """
                        UPDATE expenses
                        SET amount      = ?,
                            category    = ?,
                            description = ?,
                            date        = ?
                        WHERE id = ?
                        """,
                        (exp.amount, exp.category, exp.description, exp.date.isoformat(), exp.id)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                        (exp.amount, exp.category, exp.description, exp.date.isoformat())
                    )
                    exp.id = cursor.lastrowid
            conn.commit()

    def save_expense(self, expense):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                (expense.amount, expense.category, expense.description, expense.date.isoformat())
            )
            expense.id = cursor.lastrowid
            conn.commit()

    def delete_expense_by_id(self, id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
            conn.commit()