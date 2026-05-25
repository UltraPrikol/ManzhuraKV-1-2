from abc import ABC, abstractmethod
from typing import Dict, Any

class AbstractEmployee(ABC):
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "emp_id": self.emp_id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary
        }


class Manager(AbstractEmployee):
    def __init__(self, emp_id, name, department, base_salary, bonus):
        super().__init__(emp_id, name, department, base_salary)
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.bonus

    def to_dict(self):
        data = super().to_dict()
        data["bonus"] = self.bonus
        return data

class Developer(AbstractEmployee):
    def __init__(self, emp_id, name, department, base_salary, tech_stack, level):
        super().__init__(emp_id, name, department, base_salary)
        self.tech_stack = tech_stack
        self.level = level

    def calculate_salary(self):
        return self.base_salary

    def to_dict(self):
        data = super().to_dict()
        data["tech_stack"] = self.tech_stack
        data["level"] = self.level
        return data

class Salesperson(AbstractEmployee):
    def __init__(self, emp_id, name, department, base_salary, commission, sales):
        super().__init__(emp_id, name, department, base_salary)
        self.commission = commission
        self.sales = sales

    def calculate_salary(self):
        return self.base_salary + (self.sales * self.commission)

    def to_dict(self):
        data = super().to_dict()
        data["commission"] = self.commission
        data["sales"] = self.sales
        return data