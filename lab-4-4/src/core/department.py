from src.utils.exceptions import DuplicateIdError, EmployeeNotFoundError, DeletionError

class Department:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
        self.__employees = []  # List[AbstractEmployee]

    def add_employee(self, employee):
        if any(e.emp_id == employee.emp_id for e in self.__employees):
            raise DuplicateIdError(f"Employee ID {employee.emp_id} already exists in {self.name}")
        self.__employees.append(employee)

    def remove_employee(self, emp_id: int):
        for i, emp in enumerate(self.__employees):
            if emp.emp_id == emp_id:
                del self.__employees[i]
                return
        raise EmployeeNotFoundError(f"Employee {emp_id} not found in {self.name}")

    def get_employees(self):
        return self.__employees

    def get_employee_by_id(self, emp_id: int):
        for emp in self.__employees:
            if emp.emp_id == emp_id:
                return emp
        return None

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "employees": [e.to_dict() for e in self.__employees]
        }