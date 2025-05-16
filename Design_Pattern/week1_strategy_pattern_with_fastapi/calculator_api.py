from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Strategy Interface
class OperationStrategy:
    def calculate(self, a: float, b: float) -> float:
        raise NotImplementedError

# Concrete Strategies
class AddStrategy(OperationStrategy):
    def calculate(self, a: float, b: float) -> float:
        return a + b

class SubtractStrategy(OperationStrategy):
    def calculate(self, a: float, b: float) -> float:
        return a - b

class MultiplyStrategy(OperationStrategy):
    def calculate(self, a: float, b: float) -> float:
        return a * b

class DivideStrategy(OperationStrategy):
    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

# Context
class Calculator:
    def __init__(self, strategy: OperationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: OperationStrategy):
        self.strategy = strategy

    def calculate(self, a: float, b: float) -> float:
        return self.strategy.calculate(a, b)

# FastAPI app
app = FastAPI()

class CalcRequest(BaseModel):
    a: float
    b: float
    operation: str

strategies = {
    "add": AddStrategy(),
    "subtract": SubtractStrategy(),
    "multiply": MultiplyStrategy(),
    "divide": DivideStrategy(),
}

@app.post("/calculate")
def calculate(req: CalcRequest):
    strategy = strategies.get(req.operation)
    if not strategy:
        raise HTTPException(status_code=400, detail="Invalid operation")
    calculator = Calculator(strategy)
    try:
        result = calculator.calculate(req.a, req.b)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"result": result}