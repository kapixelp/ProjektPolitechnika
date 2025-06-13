from datetime import date

class Expense:
    def __init__(self, amount, category, description, date, id=None):
        self.id = id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date
    def __str__(self):
        return f"{self.amount} {self.category} {self.description}"