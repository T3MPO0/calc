import os

from server import CalculatorServer


if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    app = CalculatorServer(host, 8000)
    app.start()
