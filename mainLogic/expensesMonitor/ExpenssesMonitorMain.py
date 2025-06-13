from unittest import loader
from enum import Enum


from mainLogic.adapters.abstract import ExpenseLoader
from mainLogic.utilis.loggerConfig import setup_logger

logger = setup_logger(__name__)

class ExpenseCategory(Enum):
    FOOD = "Jedzenie"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Rozrywka"
    SHOPPING = "Zakupy"
    EDUCATION = "Edukacja"
    HEALTH = "Zdrowie"
    OTHER = "Inne"

class ExpensesMonitorMain:
    def __init__(self, loader: ExpenseLoader):
        self.expenses = []
        self.loadFromDatabase(loader)

    def addExpense(self, expense, loader: ExpenseLoader):
        self.expenses.append(expense)
        self.saveSingleExpenseToDatabase(loader, expense)
    def getExpenses(self):
        return self.expenses

    def removeExpenseById(self, id, loader: ExpenseLoader):
        found = False
        for i, e in enumerate(self.expenses):
            if e.id == id:
                self.expenses.pop(i)
                loader.delete_expense_by_id(id)
                found = True
                break

        if not found:
            logger.warning(f"Nie znaleziono wydatku o ID: {id}")

    def getExpensesByDate(self, date):
        return [e for e in self.expenses if e.date == date]

    def getExpensesByDescription(self, description):
        return [e for e in self.expenses if e.description == description]

    def getExpensesByCategory(self, category):
        return [e for e in self.expenses if e.category == category]

    def getExpensesByAmount(self, amount):
        return [e for e in self.expenses if e.amount == amount]

    def getExpensesByAmountRange(self, min_amount, max_amount):
        return [e for e in self.expenses if min_amount <= e.amount <= max_amount]

    def getExpensesByID(self, id):
        return [e for e in self.expenses if e.id == id]

    def getExpensesByDateRange(self, start_date, end_date):
        return [e for e in self.expenses if start_date <= e.date <= end_date]

    def loadFromDatabase(self, loader: ExpenseLoader):
        self.expenses = loader.load_expenses()
    def saveToDatabase(self, loader: ExpenseLoader):
        loader.save_expenses(self.expenses)
        self.expenses = loader.load_expenses()

    def saveSingleExpenseToDatabase(self, loader: ExpenseLoader, expense):
        loader.save_expense(expense)

    def getExpensesByDescriptionContains(self, text):
        return [e for e in self.expenses if text.lower() in e.description.lower()]
