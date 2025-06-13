from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QHBoxLayout, QListWidget, QMessageBox, QComboBox, QDateEdit, QFormLayout
)
from PyQt6.QtCore import QDate
from datetime import datetime, date
import sys

from mainLogic.adapters.SQLiteExpenseLoader import SQLiteExpenseLoader
from mainLogic.expensesMonitor.Expense import Expense
from mainLogic.expensesMonitor.ExpenssesMonitorMain import ExpensesMonitorMain, ExpenseCategory


class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitor wydatków")
        self.loader = SQLiteExpenseLoader()
        self.monitor = ExpensesMonitorMain(self.loader)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Filtry
        filter_layout = QFormLayout()
        self.filter_start_date = QDateEdit()
        self.filter_start_date.setCalendarPopup(True)
        self.filter_start_date.setDate(QDate(2000, 1, 1))

        self.filter_end_date = QDateEdit()
        self.filter_end_date.setCalendarPopup(True)
        self.filter_end_date.setDate(QDate.currentDate())

        self.filter_min_amount = QLineEdit()
        self.filter_max_amount = QLineEdit()
        self.filter_description = QLineEdit()
        self.filter_category = QComboBox()
        self.filter_category.addItem("Wszystkie")
        self.filter_category.addItems([c.value for c in ExpenseCategory])

        filter_layout.addRow("Data od:", self.filter_start_date)
        filter_layout.addRow("Data do:", self.filter_end_date)
        filter_layout.addRow("Kwota od:", self.filter_min_amount)
        filter_layout.addRow("Kwota do:", self.filter_max_amount)
        filter_layout.addRow("Opis zawiera:", self.filter_description)
        filter_layout.addRow("Kategoria:", self.filter_category)

        filter_button = QPushButton("Zastosuj filtry")
        filter_button.clicked.connect(self.load_filtered_expenses)
        filter_layout.addRow(filter_button)

        layout.addLayout(filter_layout)

        # Lista wydatków
        self.expense_list = QListWidget()
        layout.addWidget(QLabel("Lista wydatków:"))
        layout.addWidget(self.expense_list)
        self.total_label = QLabel("Suma: 0.00 PLN")
        layout.addWidget(self.total_label)

        # Formularz dodawania
        form_layout = QFormLayout()
        self.amount_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems([c.value for c in ExpenseCategory])
        self.description_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        form_layout.addRow("Kwota:", self.amount_input)
        form_layout.addRow("Kategoria:", self.category_input)
        form_layout.addRow("Opis:", self.description_input)
        form_layout.addRow("Data:", self.date_input)

        layout.addLayout(form_layout)

        # Przyciski
        button_layout = QHBoxLayout()
        add_button = QPushButton("Dodaj")
        delete_button = QPushButton("Usuń zaznaczony")
        refresh_button = QPushButton("Odśwież")

        add_button.clicked.connect(self.add_expense)
        delete_button.clicked.connect(self.delete_selected_expense)
        refresh_button.clicked.connect(self.load_expenses_to_list)

        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(refresh_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.load_expenses_to_list()

    def load_expenses_to_list(self):
        self.expense_list.clear()
        self.monitor.loadFromDatabase(self.loader)
        for expense in self.monitor.getExpenses():
            self.expense_list.addItem(
                f"ID: {expense.id} | {expense.amount:.2f} PLN | {expense.date.strftime('%d-%m-%Y')} | {expense.category} | {expense.description}"
            )
        self.update_total(self.monitor.getExpenses())

    def update_total(self, expense_list):
        total = sum(e.amount for e in expense_list)
        self.total_label.setText(f"Suma: {total:.2f} PLN")

    def load_filtered_expenses(self):
        try:
            start = self.filter_start_date.date().toPyDate()
            end = self.filter_end_date.date().toPyDate()
            min_amt = float(self.filter_min_amount.text()) if self.filter_min_amount.text() else None
            max_amt = float(self.filter_max_amount.text()) if self.filter_max_amount.text() else None
            category = self.filter_category.currentText()
            description = self.filter_description.text()

            results = self.monitor.getFilteredExpenses(
                start_date=start,
                end_date=end,
                min_amount=min_amt,
                max_amount=max_amt,
                category=category,
                description_contains=description
            )

            self.expense_list.clear()
            for e in results:
                self.expense_list.addItem(
                    f"ID: {e.id} | {e.amount:.2f} PLN | {e.date.strftime('%d-%m-%Y')} | {e.category} | {e.description}"
                )
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Nieprawidłowe dane w filtrach.")
        self.update_total(results)

    def add_expense(self):
        try:
            amount = float(self.amount_input.text())
            category = self.category_input.currentText()
            description = self.description_input.text() or "brak opisu"
            parsed_date = self.date_input.date().toPyDate()

            new_expense = Expense(amount, category, description, parsed_date)
            self.monitor.addExpense(new_expense, self.loader)
            self.load_expenses_to_list()
            self.clear_form()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Nieprawidłowa kwota.")

    def delete_selected_expense(self):
        selected = self.expense_list.currentRow()
        if selected != -1:
            expense = self.monitor.getExpenses()[selected]
            self.monitor.removeExpenseById(expense.id, self.loader)
            self.load_expenses_to_list()
        else:
            QMessageBox.information(self, "Info", "Nie wybrano elementu do usunięcia.")

    def clear_form(self):
        self.amount_input.clear()
        self.description_input.clear()
        self.date_input.setDate(QDate.currentDate())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec())