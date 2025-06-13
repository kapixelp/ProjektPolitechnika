from datetime import datetime
from mainLogic.adapters.SQLiteExpenseLoader import SQLiteExpenseLoader
from mainLogic.expensesMonitor.Expense import Expense
from consoleApp.consoleUtils import print_expense, prompt_category, prompt_date, prompt_float, prompt_text
from mainLogic.expensesMonitor.ExpenssesMonitorMain import ExpensesMonitorMain

loader = SQLiteExpenseLoader()
monitor = ExpensesMonitorMain(loader)


def main_menu():
    while True:
        print("""
========= MENU =========
1. Dodaj wydatek
2. Pokaż wszystkie
3. Usuń po ID
4. Szukaj po opisie
5. Filtruj po dacie (zakres)
6. Filtruj po kwocie (zakres)
7. Filtruj po kategorii
8. Zapisz i zakończ
========================
        """)
        choice = input("Wybierz opcję: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            show_all()
        elif choice == '3':
            remove_by_id()
        elif choice == '4':
            search_by_description()
        elif choice == '5':
            filter_by_date_range()
        elif choice == '6':
            filter_by_amount_range()
        elif choice == '7':
            filter_by_category()
        elif choice == '8':
            monitor.saveToDatabase(loader)
            print("Zapisano. Do zobaczenia!")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")


def add_expense():
    print("Dodawanie nowego wydatku:")
    amount = prompt_float()
    category = prompt_category()
    description = prompt_text() or "brak opisu"
    date = prompt_date()
    expense = Expense(amount, category, description, date)
    monitor.addExpense(expense, loader)
    print("Dodano wydatek.")


def show_all():
    for e in monitor.getExpenses():
        print_expense(e)


def remove_by_id():
    try:
        id = int(input("Podaj ID do usunięcia: "))
        monitor.removeExpenseById(id, loader)
    except ValueError:
        print("Błędny ID")


def search_by_description():
    text = input("Szukany fragment opisu: ")
    results = monitor.getExpensesByDescriptionContains(text)
    for e in results:
        print_expense(e)


def filter_by_date_range():
    print("Zakres dat:")
    start = prompt_date()
    end = prompt_date()
    results = monitor.getExpensesByDateRange(start, end)
    for e in results:
        print_expense(e)


def filter_by_amount_range():
    print("Zakres kwot:")
    min_val = prompt_float()
    max_val = prompt_float()
    results = monitor.getExpensesByAmountRange(min_val, max_val)
    for e in results:
        print_expense(e)


def filter_by_category():
    print("Filtruj po kategorii:")
    category = prompt_category()
    results = monitor.getExpensesByCategory(category)
    for e in results:
        print_expense(e)


if __name__ == '__main__':
    main_menu()
