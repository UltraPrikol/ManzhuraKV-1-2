from dataclasses import dataclass, field
from typing import List, Optional
from interfaces import ISalaryCalculable, IInfoProvidable, ISkillManageable
from strategies import BonusStrategy, NoBonusStrategy

# Валидатор (SRP - отдельный класс для проверок)
class EmployeeValidator:
    @staticmethod
    def validate(name: str, salary: float) -> None:
        if not name:
            raise ValueError("Name cannot be empty")
        if salary < 0:
            raise ValueError("Salary cannot be negative")

# Базовый класс
class Employee(ISalaryCalculable, IInfoProvidable):
    def __init__(self, emp_id: int, name: str, base_salary: float, 
                 bonus_strategy: Optional[BonusStrategy] = None):
        EmployeeValidator.validate(name, base_salary)
        self.id = emp_id
        self.name = name
        self.base_salary = base_salary
        # Внедрение зависимости через конструктор (Strategy)
        self.bonus_strategy = bonus_strategy if bonus_strategy else NoBonusStrategy()

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus_strategy.calculate(self.base_salary)

    def get_info(self) -> str:
        return f"ID: {self.id}, Name: {self.name}"

# Подклассы (LSP соблюден: Developer полностью заменяет Employee там, где это нужно)
class Developer(Employee, ISkillManageable):
    def __init__(self, emp_id: int, name: str, base_salary: float, 
                 bonus_strategy: Optional[BonusStrategy] = None):
        super().__init__(emp_id, name, base_salary, bonus_strategy)
        self.skills: List[str] = []

    def add_skill(self, skill: str) -> None:
        if skill not in self.skills:
            self.skills.append(skill)

    def get_info(self) -> str:
        base_info = super().get_info()
        return f"{base_info}, Skills: {', '.join(self.skills)}"

class Manager(Employee):
    def __init__(self, emp_id: int, name: str, base_salary: float, 
                 subordinates_count: int,
                 bonus_strategy: Optional[BonusStrategy] = None):
        super().__init__(emp_id, name, base_salary, bonus_strategy)
        self.subordinates_count = subordinates_count