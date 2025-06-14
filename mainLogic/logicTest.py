from mainLogic.adapters.SQLiteExpenseLoader import SQLiteExpenseLoader
from mainLogic.expensesMonitor.Expense import Expense
from mainLogic.expensesMonitor.ExpenssesMonitorMain import ExpensesMonitorMain

if __name__ == '__main__':
    loader = SQLiteExpenseLoader()
    x = ExpensesMonitorMain(loader)
    # x.addExpense(Expense(30,"jedzenie", "brak opisu","30-05-2025" ))
    # x.addExpense(Expense(50,"jedzenie", "brak opisu","30-05-2025" ))
    # x.addExpense(Expense(40,"jedzenie", "brak opisu","30-05-2025" ))
    # x.addExpense(Expense(70,"jedzenie", "ad opisu","30-05-2025" ))
    # x.addExpense(Expense(85,"jedzenie", "brsadak opisu","30-05-2025" ))
    x.saveToDatabase(loader)

