import json
from abc import ABC, abstractmethod
from typing import Optional
from functools import cmp_to_key

# ============================================================
# Абстрактный базовый класс
# ============================================================
class AbstractEmployee(ABC):
    """Абстрактный базовый класс для сотрудников"""

    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary

    # --- Геттеры и сеттеры ---
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID должен быть положительным целым числом.")
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя не может быть пустым.")
        self.__name = value.strip()

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название отдела не может быть пустым.")
        self.__department = value.strip()

    @property
    def base_salary(self):
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Базовая зарплата должна быть положительным числом.")
        self.__base_salary = float(value)

    # --- Абстрактные методы ---
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'AbstractEmployee':
        pass

    def __str__(self):
        return (f"[{self.__class__.__name__} | id: {self.id}, имя: {self.name}, "
                f"отдел: {self.department}, базовая: {self.base_salary}]")

    # --- Магические методы сравнения и арифметики ---
    def __eq__(self, other):
        return isinstance(other, AbstractEmployee) and self.id == other.id

    def __lt__(self, other):
        return self.calculate_salary() < other.calculate_salary()

    def __add__(self, other):
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.calculate_salary() + other.calculate_salary()

    def __radd__(self, other):
        if other == 0:
            return self.calculate_salary()
        elif isinstance(other, (int, float)):
            return other + self.calculate_salary()
        return NotImplemented


# ============================================================
# Обычный сотрудник
# ============================================================
class Employee(AbstractEmployee):
    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return f"{super().__str__()}, зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        return {
            "type": "employee",
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Employee':
        return cls(data["id"], data["name"], data["department"], data["base_salary"])


# ============================================================
# Менеджер
# ============================================================
class Manager(Employee):
    def __init__(self, emp_id, name, department, base_salary, bonus: float):
        super().__init__(emp_id, name, department, base_salary)
        self.bonus = bonus

    @property
    def bonus(self):
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        if value < 0:
            raise ValueError("Бонус не может быть отрицательным.")
        self.__bonus = float(value)

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        return f"{super().__str__()}, бонус: {self.bonus}, зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"type": "manager", "bonus": self.bonus})
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Manager':
        return cls(data["id"], data["name"], data["department"], data["base_salary"], data["bonus"])


# ============================================================
# Разработчик
# ============================================================
class Developer(Employee):
    def __init__(self, emp_id, name, department, base_salary, tech_stack=None, seniority_level="junior"):
        super().__init__(emp_id, name, department, base_salary)
        self.tech_stack = tech_stack or []
        self.seniority_level = seniority_level

    def __iter__(self):
        """Итерирование по стеку технологий"""
        return iter(self.tech_stack)

    @property
    def seniority_level(self):
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value):
        if value not in ("junior", "middle", "senior"):
            raise ValueError("Неверный уровень seniority.")
        self.__seniority_level = value

    @property
    def tech_stack(self):
        return self.__tech_stack

    @tech_stack.setter
    def tech_stack(self, value):
        if not isinstance(value, list):
            raise ValueError("tech_stack должен быть списком строк.")
        self.__tech_stack = value

    def calculate_salary(self) -> float:
        coef = {"junior": 1.0, "middle": 1.5, "senior": 2.0}[self.seniority_level]
        return self.base_salary * coef

    def get_info(self) -> str:
        return f"{super().__str__()}, уровень: {self.seniority_level}, стек: {', '.join(self.tech_stack)}, зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "type": "developer",
            "tech_stack": self.tech_stack,
            "seniority_level": self.seniority_level
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Developer':
        return cls(data["id"], data["name"], data["department"], data["base_salary"],
                   data["tech_stack"], data["seniority_level"])


# ============================================================
# Продавец
# ============================================================
class Salesperson(Employee):
    def __init__(self, emp_id, name, department, base_salary, commission_rate, sales_volume=0.0):
        super().__init__(emp_id, name, department, base_salary)
        self.commission_rate = commission_rate
        self.sales_volume = sales_volume

    @property
    def commission_rate(self):
        return self.__commission_rate

    @commission_rate.setter
    def commission_rate(self, value):
        if not (0 <= value <= 1):
            raise ValueError("Комиссия должна быть между 0 и 1.")
        self.__commission_rate = value

    @property
    def sales_volume(self):
        return self.__sales_volume

    @sales_volume.setter
    def sales_volume(self, value):
        if value < 0:
            raise ValueError("Объём продаж не может быть отрицательным.")
        self.__sales_volume = value

    def calculate_salary(self) -> float:
        return self.base_salary + self.sales_volume * self.commission_rate

    def get_info(self) -> str:
        return f"{super().__str__()}, продажи: {self.sales_volume}, комиссия: {self.commission_rate}, зарплата: {self.calculate_salary()}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "type": "salesperson",
            "commission_rate": self.commission_rate,
            "sales_volume": self.sales_volume
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Salesperson':
        return cls(data["id"], data["name"], data["department"], data["base_salary"],
                   data["commission_rate"], data["sales_volume"])


# ============================================================
# Отдел (Department)
# ============================================================
class Department:
    """Класс отдела, содержащего сотрудников"""

    def __init__(self, name: str):
        self.name = name
        self.__employees: list[AbstractEmployee] = []

    def add_employee(self, employee: AbstractEmployee) -> None:
        self.__employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        self.__employees = [e for e in self.__employees if e.id != employee_id]

    def get_employees(self) -> list[AbstractEmployee]:
        return list(self.__employees)

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        return next((e for e in self.__employees if e.id == employee_id), None)

    def calculate_total_salary(self) -> float:
        return sum(e.calculate_salary() for e in self.__employees)

    def get_employee_count(self) -> dict[str, int]:
        counts = {}
        for e in self.__employees:
            counts[e.__class__.__name__] = counts.get(e.__class__.__name__, 0) + 1
        return counts

    # --- Магические методы ---
    def __len__(self):
        return len(self.__employees)

    def __getitem__(self, index):
        return self.__employees[index]

    def __contains__(self, employee: AbstractEmployee):
        return employee in self.__employees

    def __iter__(self):
        return iter(self.__employees)

    # --- Сериализация ---
    def save_to_file(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            data = [e.to_dict() for e in self.__employees]
            json.dump({"department": self.name, "employees": data}, f, ensure_ascii=False, indent=4)

    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        dept = cls(data["department"])
        for emp_data in data["employees"]:
            emp_type = emp_data["type"]
            if emp_type == "manager":
                dept.add_employee(Manager.from_dict(emp_data))
            elif emp_type == "developer":
                dept.add_employee(Developer.from_dict(emp_data))
            elif emp_type == "salesperson":
                dept.add_employee(Salesperson.from_dict(emp_data))
            else:
                dept.add_employee(Employee.from_dict(emp_data))
        return dept


# ============================================================
# Компараторы
# ============================================================
def compare_by_name(e1, e2):
    return (e1.name > e2.name) - (e1.name < e2.name)

def compare_by_salary(e1, e2):
    return (e1.calculate_salary() > e2.calculate_salary()) - (e1.calculate_salary() < e2.calculate_salary())

def compare_by_department_then_name(e1, e2):
    if e1.department == e2.department:
        return compare_by_name(e1, e2)
    return (e1.department > e2.department) - (e1.department < e2.department)


# ============================================================
# Демонстрация
# ============================================================
if __name__ == "__main__":
    dev = Developer(1, "Иван", "IT", 80000, ["Python", "Django"], "senior")
    mgr = Manager(2, "Мария", "IT", 90000, 15000)
    sales = Salesperson(3, "Олег", "Продажи", 50000, 0.1, 200000)
    emp = Employee(4, "Татьяна", "HR", 40000)

    dept = Department("IT & Sales")
    for e in [dev, mgr, sales, emp]:
        dept.add_employee(e)

    print("Всего сотрудников:", len(dept))
    print("Список сотрудников отдела:")
    for e in dept:
        print(" •", e.get_info())

    print("\nОбщая зарплата отдела:", dept.calculate_total_salary())
    print("Количество по типам:", dept.get_employee_count())

    # Проверка магических методов
    print("\nСравнение зарплат:", dev < mgr)
    print("Сумма зарплат dev + mgr =", dev + mgr)
    print("Сумма всех сотрудников:", sum(dept))

    print("\nИтерация по стеку технологий разработчика:")
    for skill in dev:
        print(" -", skill)

    # Сохранение и загрузка
    dept.save_to_file("department.json")
    new_dept = Department.load_from_file("department.json")
    print("\nЗагружено из файла:")
    for e in new_dept:
        print(" •", e.get_info())

    # Сортировки
    print("\nСортировка по имени:")
    for e in sorted(dept, key=lambda x: x.name):
        print(" •", e.name)

    print("\nСортировка по зарплате:")
    for e in sorted(dept, key=lambda x: x.calculate_salary(), reverse=True):
        print(" •", e.name, "-", e.calculate_salary())

    print("\nСортировка по отделу и имени:")
    for e in sorted(dept, key=cmp_to_key(compare_by_department_then_name)):
        print(" •", e.name, "(", e.department, ")")