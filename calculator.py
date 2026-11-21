import os
import sqlite3


class Operation:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name

    def calculate(self, a, b):
        raise NotImplementedError("Операция не реализована")


class Addition(Operation):
    def __init__(self):
        super().__init__("+", "Сложение")

    def calculate(self, a, b):
        return a + b


class Subtraction(Operation):
    def __init__(self):
        super().__init__("-", "Вычитание")

    def calculate(self, a, b):
        return a - b


class Multiplication(Operation):
    def __init__(self):
        super().__init__("*", "Умножение")

    def calculate(self, a, b):
        return a * b


class Division(Operation):
    def __init__(self):
        super().__init__("/", "Деление")

    def calculate(self, a, b):
        if b == 0:
            raise ZeroDivisionError("На ноль делить нельзя")
        return a / b


class History:
    def __init__(self, max_size=10, db_path="data/history.db"):
        self.max_size = max_size
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.__connection = sqlite3.connect(db_path, check_same_thread=False)
        self.__connection.execute(
            "CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)"
        )

    def add(self, text):
        self.__connection.execute("INSERT INTO history (text) VALUES (?)", (text,))
        self.__connection.commit()

    def get_all(self):
        rows = self.__connection.execute(
            "SELECT text FROM history ORDER BY id DESC LIMIT ?", (self.max_size,)
        ).fetchall()
        return [row[0] for row in rows]

    def clear(self):
        self.__connection.execute("DELETE FROM history")
        self.__connection.commit()


class Calculator:
    def __init__(self):
        self.operations = {}
        self.history = History()

        self.add_operation(Addition())
        self.add_operation(Subtraction())
        self.add_operation(Multiplication())
        self.add_operation(Division())

    def add_operation(self, operation):
        self.operations[operation.symbol] = operation

    def get_operations(self):
        return self.operations

    def format_number(self, number):
        if number == int(number):
            return str(int(number))
        return str(round(number, 10))

    def calculate(self, a, symbol, b):
        if symbol not in self.operations:
            raise ValueError("Неизвестная операция")

        operation = self.operations[symbol]
        result = operation.calculate(a, b)

        text = self.format_number(a) + " " + symbol + " " + self.format_number(b)
        text = text + " = " + self.format_number(result)
        self.history.add(text)

        return result
