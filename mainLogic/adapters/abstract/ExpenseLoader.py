from abc import ABC, abstractmethod

class ExpenseLoader(ABC):
    @abstractmethod
    def load_expenses(self):
        """Zwraca listę obiektów Expense pobranych z bazy danych."""
        pass
    @abstractmethod
    def save_expenses(self, expenses):
        """Zapisuje listę obiektów Expense do bazy danych."""
        pass

    @abstractmethod
    def save_expense(self, expense):
        pass
    @abstractmethod
    def delete_expense_by_id(self, id):
        pass