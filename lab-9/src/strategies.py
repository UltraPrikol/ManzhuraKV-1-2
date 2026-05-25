from abc import ABC, abstractmethod

class BonusStrategy(ABC):
    @abstractmethod
    def calculate(self, base_salary: float) -> float:
        pass

class NoBonusStrategy(BonusStrategy):
    def calculate(self, base_salary: float) -> float:
        return 0.0

class PerformanceBonusStrategy(BonusStrategy):
    def __init__(self, percent: float, performance_score: int):
        self.percent = percent
        self.performance_score = performance_score

    def calculate(self, base_salary: float) -> float:
        if self.performance_score > 8:
            return base_salary * (self.percent * 2)
        return base_salary * self.percent

class SeniorityBonusStrategy(BonusStrategy):
    def __init__(self, years: int):
        self.years = years

    def calculate(self, base_salary: float) -> float:
        return 1000.0 * self.years