import json

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from calculator import Calculator


class CalculateBody(BaseModel):
    a: float
    op: str
    b: float


class CalculatorServer:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.calculator = Calculator()

        with open("config.json", encoding="utf-8") as file:
            config = json.load(file)

        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=config["cors_origins"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.get("/")(self.index)
        self.app.get("/api/operations")(self.get_operations)
        self.app.post("/api/calculate")(self.calculate)
        self.app.get("/api/history")(self.get_history)
        self.app.delete("/api/history")(self.clear_history)

    def index(self):
        return FileResponse("index.html")

    def get_operations(self):
        operations = []
        for symbol, operation in self.calculator.operations.items():
            operations.append({"symbol": symbol, "name": operation.name})
        return operations

    def calculate(self, body: CalculateBody):
        try:
            result = self.calculator.calculate(body.a, body.op, body.b)
        except ZeroDivisionError as error:
            raise HTTPException(status_code=400, detail=str(error))
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error))
        return {"result": self.calculator.format_number(result)}

    def get_history(self):
        return self.calculator.history.get_all()

    def clear_history(self):
        self.calculator.history.clear()
        return {"ok": True}

    def start(self):
        print(f"Калькулятор запущен: http://{self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)
