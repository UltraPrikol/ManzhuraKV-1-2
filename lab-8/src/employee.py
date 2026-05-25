import json
from abc import ABC, abstractmethod
from typing import List, Dict

# --- Исключения ---
class DuplicateIdError(Exception):
    pass

class InvalidStatusError(Exception):
    pass

# --- Абстрактный класс ---
class AbstractEmployee(ABC):
    @abstractmethod
    def calculate_salary(self) -> float:
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        pass

# --- Базовый класс Employee ---
class Employee(AbstractEmployee):
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID должен быть положительным целым числом")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Имя не может быть пустым")
        self._name = value

    @property
    def base_salary(self):
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value):
        if value < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        self._base_salary = value

    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return f"Сотрудник: {self.name}, ЗП: {self.calculate_salary()}"

    def __str__(self):
        return f"Сотрудник [id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата: {self.base_salary}]"

    def __eq__(self, other):
        if isinstance(other, Employee):
            return self.id == other.id
        return False

    def __lt__(self, other):
        if isinstance(other, Employee):
            return self.calculate_salary() < other.calculate_salary()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Employee):
            return self.calculate_salary() > other.calculate_salary()
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Employee):
            return self.calculate_salary() + other.calculate_salary()
        if isinstance(other, (int, float)):
            return self.calculate_salary() + other
        return NotImplemented

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["department"], data["base_salary"])

# --- Наследники ---
class Manager(Employee):
    def __init__(self, emp_id, name, department, base_salary, bonus):
        super().__init__(emp_id, name, department, base_salary)
        self.bonus = bonus

    @property
    def bonus(self):
        return self._bonus

    @bonus.setter
    def bonus(self, value):
        if value < 0:
            raise ValueError("Бонус не может быть отрицательным")
        self._bonus = value

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        return f"{super().get_info()}, бонус: {self.bonus}, итоговая зарплата: {self.calculate_salary()}"
    
    def to_dict(self):
        data = super().to_dict()
        data["bonus"] = self.bonus
        return data

class Developer(Employee):
    LEVELS = {"junior": 1.0, "middle": 1.5, "senior": 2.0}

    def __init__(self, emp_id, name, department, base_salary, tech_stack: List[str], level: str):
        super().__init__(emp_id, name, department, base_salary)
        self.tech_stack = tech_stack
        self.level = level

    def add_skill(self, skill: str):
        self.tech_stack.append(skill)

    def calculate_salary(self) -> float:
        multiplier = self.LEVELS.get(self.level, 1.0)
        return self.base_salary * multiplier
    
    def get_info(self) -> str:
        return f"{super().get_info()}, стек: {self.tech_stack}, уровень: {self.level}"

    def __iter__(self):
        return iter(self.tech_stack)

    def to_dict(self):
        data = super().to_dict()
        data["tech_stack"] = self.tech_stack
        data["level"] = self.level
        return data

class Salesperson(Employee):
    def __init__(self, emp_id, name, department, base_salary, commission_rate, sales_volume=0):
        super().__init__(emp_id, name, department, base_salary)
        self.commission_rate = commission_rate
        self.sales_volume = sales_volume

    def update_sales(self, amount):
        self.sales_volume += amount

    def calculate_salary(self) -> float:
        return self.base_salary + (self.sales_volume * self.commission_rate)

    def get_info(self) -> str:
        return f"{super().get_info()}, продажи: {self.sales_volume}, комиссия: {self.commission_rate}"

    def to_dict(self):
        data = super().to_dict()
        data["commission_rate"] = self.commission_rate
        data["sales_volume"] = self.sales_volume
        return data

# --- Фабрика ---
class EmployeeFactory:
    @staticmethod
    def create_employee(emp_type, **kwargs):
        if emp_type == "Manager":
            return Manager(**kwargs)
        elif emp_type == "Developer":
            return Developer(**kwargs)
        elif emp_type == "Salesperson":
            return Salesperson(**kwargs)
        elif emp_type == "Employee":
            return Employee(**kwargs)
        else:
            raise ValueError(f"Unknown employee type: {emp_type}")

# --- Отдел ---
class Department:
    def __init__(self, name):
        self.name = name
        self._employees: List[Employee] = []

    def add_employee(self, employee: Employee):
        if any(e.id == employee.id for e in self._employees):
            raise DuplicateIdError(f"Сотрудник с ID {employee.id} уже существует")
        self._employees.append(employee)

    def remove_employee(self, emp_id: int):
        self._employees = [e for e in self._employees if e.id != emp_id]

    def get_employees(self):
        return self._employees

    def find_employee_by_id(self, emp_id: int):
        for emp in self._employees:
            if emp.id == emp_id:
                return emp
        return None

    def calculate_total_salary(self):
        return sum(emp.calculate_salary() for emp in self._employees)

    def get_employee_count(self):
        counts = {}
        for emp in self._employees:
            type_name = emp.__class__.__name__
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    def __len__(self):
        return len(self._employees)

    def __getitem__(self, index):
        return self._employees[index]

    def __contains__(self, item):
        if isinstance(item, Employee):
            return item in self._employees
        return False

    def __iter__(self):
        return iter(self._employees)
    
    def to_dict(self):
        return {
            "name": self.name,
            "employees": [e.to_dict() for e in self._employees]
        }

# --- Проект ---
class Project:
    VALID_STATUSES = ["planning", "active", "finished"]

    def __init__(self, proj_id, name, description, deadline, status):
        self.id = proj_id
        self.name = name
        self.description = description
        self.deadline = deadline
        if status not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Статус должен быть: {self.VALID_STATUSES}")
        self.status = status
        self._team: List[Employee] = []

    def add_team_member(self, employee: Employee):
        if employee not in self._team:
            self._team.append(employee)

    def remove_team_member(self, emp_id: int):
        self._team = [e for e in self._team if e.id != emp_id]

    def get_team(self):
        return self._team
    
    def get_team_size(self):
        return len(self._team)

    def calculate_total_salary(self):
        return sum(e.calculate_salary() for e in self._team)

# --- Компания ---
class Company:
    def __init__(self, name):
        self.name = name
        self._departments: Dict[str, Department] = {}

    def add_department(self, department: Department):
        self._departments[department.name] = department

    def remove_department(self, dept_name: str):
        if dept_name in self._departments:
            if len(self._departments[dept_name]) > 0:
                 raise ValueError("Cannot delete department with employees")
            del self._departments[dept_name]

    def get_departments(self):
        return list(self._departments.values())
    
    def find_employee_by_id(self, emp_id):
        for dept in self._departments.values():
            found = dept.find_employee_by_id(emp_id)
            if found: return found
        return None
    
    def get_all_employees(self):
        all_emps = []
        for dept in self._departments.values():
            all_emps.extend(dept.get_employees())
        return all_emps

    def get_department_stats(self):
        stats = {}
        for name, dept in self._departments.items():
            stats[name] = {
                "employee_count": len(dept),
                "total_salary": dept.calculate_total_salary()
            }
        return stats
    
    def calculate_total_monthly_cost(self):
        return sum(dept.calculate_total_salary() for dept in self._departments.values())

    def find_overloaded_employees(self):
        return []

    def save_to_json(self, filename):
        data = {
            "name": self.name,
            "departments": [dept.to_dict() for dept in self._departments.values()]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_from_json(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        company = cls(data["name"])
        for dept_data in data["departments"]:
            dept = Department(dept_data["name"])
            for emp_data in dept_data["employees"]:
                e_type = emp_data.pop("type")
                emp = EmployeeFactory.create_employee(e_type, 
                                                      emp_id=emp_data["id"], 
                                                      name=emp_data["name"], 
                                                      department=emp_data["department"], 
                                                      base_salary=emp_data["base_salary"],
                                                      **{k:v for k,v in emp_data.items() 
                                                         if k not in ["id", "name", "department", "base_salary"]}
                                                      )
                dept.add_employee(emp)
            company.add_department(dept)
        return company    


# --- Singleton ---
class DatabaseConnection:
    _instance = None
    def __init__(self):
        if DatabaseConnection._instance is not None:
            raise Exception("This class is a singleton!")
    @staticmethod
    def get_instance():
        if DatabaseConnection._instance is None:
            DatabaseConnection._instance = DatabaseConnection()
        return DatabaseConnection._instance

# --- Builder ---
class EmployeeBuilder:
    def __init__(self):
        self.reset()
    def reset(self):
        self._data = {"tech_stack": [], "level": "junior"}
        return self
    def set_id(self, emp_id):
        self._data["emp_id"] = emp_id
        return self
    def set_name(self, name):
        self._data["name"] = name
        return self
    def set_department(self, dept):
        self._data["department"] = dept
        return self
    def set_base_salary(self, salary):
        self._data["base_salary"] = salary
        return self
    def set_skills(self, skills):
        self._data["tech_stack"] = skills
        return self
    def set_seniority(self, level):
        self._data["level"] = level
        return self
    def set_bonus(self, bonus):
        self._data["bonus"] = bonus
        return self
    def build(self):
        from employee import Developer, Manager # Локальный импорт во избежание циклов
        if "bonus" in self._data:
            return Manager(self._data["emp_id"], self._data["name"], 
                           self._data["department"], self._data["base_salary"], self._data["bonus"])
        return Developer(self._data["emp_id"], self._data["name"], 
                         self._data["department"], self._data["base_salary"], 
                         self._data["tech_stack"], self._data["level"])

# --- Adapter ---
class ExternalSalaryService:
    def get_external_salary(self, emp_name):
        return 5000 # Имитация внешней логики

class SalaryCalculatorAdapter:
    def __init__(self, service):
        self.service = service
    def calculate_salary(self, employee):
        return self.service.get_external_salary(employee.name)

# --- Decorator ---
class BonusDecorator:
    def __init__(self, employee, bonus):
        self.employee = employee
        self.bonus = bonus
    def calculate_salary(self):
        return self.employee.calculate_salary() + self.bonus
    def get_info(self):
        return f"{self.employee.get_info()}, бонус: {self.bonus}"

# --- Observer ---
class ObservableEmployee:
    def __init__(self):
        self._observers = []
    def add_observer(self, observer):
        self._observers.append(observer)
    def notify_observers(self, message):
        for obs in self._observers:
            obs.update(self, message)

# Добавьте в основной класс Employee (в начало файла) наследование от ObservableEmployee
# И в сеттер salary добавьте: self.notify_observers("salary_changed")

# --- Strategy ---
class BonusStrategy:
    def calculate(self, salary): pass

class PerformanceBonusStrategy(BonusStrategy):
    def calculate(self, salary): return 1000

class SeniorityBonusStrategy(BonusStrategy):
    def calculate(self, salary): return 1500

# --- Command ---
class HireEmployeeCommand:
    def __init__(self, employee, company):
        self.employee = employee
        self.company = company
    def execute(self):
        # Логика добавления в какой-то отдел компании
        if not self.company.get_departments():
            from employee import Department
            self.company.add_department(Department("General"))
        self.company.get_departments()[0].add_employee(self.employee)
    def undo(self):
        for dept in self.company.get_departments():
            dept.remove_employee(self.employee.id)

# --- Repository & Specification ---
class EmployeeNotFoundError(Exception): pass

class EmployeeRepository:
    def __init__(self):
        self._employees = {}
    def add(self, employee):
        self._employees[employee.id] = employee
    def find_by_id(self, emp_id):
        if emp_id not in self._employees:
            raise EmployeeNotFoundError()
        return self._employees[emp_id]
    def find_by_specification(self, spec):
        return [e for e in self._employees.values() if spec.is_satisfied_by(e)]

class SalarySpecification:
    def __init__(self, min_salary):
        self.min_salary = min_salary
    def is_satisfied_by(self, employee):
        return employee.calculate_salary() >= self.min_salary
    def __and__(self, other):
        return CombinedSpecification(self, other)

class DepartmentSpecification:
    def __init__(self, department):
        self.department = department
    def is_satisfied_by(self, employee):
        return employee.department == self.department

class CombinedSpecification:
    def __init__(self, spec1, spec2):
        self.spec1 = spec1
        self.spec2 = spec2
    def is_satisfied_by(self, employee):
        return self.spec1.is_satisfied_by(employee) and self.spec2.is_satisfied_by(employee)

class NotificationSystem:
    def __init__(self):
        self.notifiers = []
    def add_notifier(self, notifier):
        self.notifiers.append(notifier)
    def update(self, employee, message):
        for n in self.notifiers:
            n.notify(employee, message)