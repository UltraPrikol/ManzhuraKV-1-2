from typing import List
from interfaces import IEmployeeRepository, ISalaryCalculable

# Сервис для работы с финансами (выделен из Company)
class FinancialCalculator:
    def calculate_total_payroll(self, employees: List[ISalaryCalculable]) -> float:
        return sum(emp.calculate_salary() for emp in employees)

# Фасад для управления компанией (Delegation)
class CompanyService:
    def __init__(self, repository: IEmployeeRepository, calculator: FinancialCalculator):
        self.repo = repository
        self.calculator = calculator

    def hire_employee(self, employee) -> None:
        self.repo.add(employee)
        print(f"Hired: {employee.get_info()}")

    def get_total_costs(self) -> float:
        employees = self.repo.get_all()
        return self.calculator.calculate_total_payroll(employees)