from datetime import datetime, date

from mainLogic.expensesMonitor.ExpenssesMonitorMain import ExpenseCategory


def prompt_float():
    while True:
        try:
            value = input("Podaj kwotę: ")
            return float(value)
        except ValueError:
            print("Błędna wartość. Wpisz liczbę.")

def prompt_text():
    return input("Podaj opis (ENTER = brak): ").strip()

def prompt_date():
    while True:
        value = input("Podaj datę (dd-mm-rrrr, ENTER = dzisiaj): ").strip()
        if not value:
            return date.today()
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            print("Błędny format. Użyj formatu dd-mm-rrrr.")

def prompt_category():
    categories = list(ExpenseCategory)
    print("Wybierz kategorię:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat.value}")
    while True:
        try:
            choice = int(input("Numer kategorii: "))
            if 1 <= choice <= len(categories):
                return categories[choice - 1].value
            else:
                print("Wybierz numer z listy.")
        except ValueError:
            print("Wpisz poprawny numer.")

def print_expense(expense):
    print(f"ID: {expense.id} | Kwota: {expense.amount:.2f} | Data: {expense.date.strftime('%d-%m-%Y')} | Kategoria: {expense.category} | Opis: {expense.description}")