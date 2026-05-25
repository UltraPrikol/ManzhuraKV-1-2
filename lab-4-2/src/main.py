from abc import ABC, abstractmethod

# ============================================================
# 1. Абстрактный базовый класс
# ============================================================
class AbstractEmployee(ABC):
    """
    Абстрактный базовый класс для всех сотрудников.
    Определяет общие атрибуты и абстрактные методы.
    """

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
            raise ValueError("Имя не может быть пустой строкой.")
        self.__name = value.strip()

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название отдела не может быть пустой строкой.")
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
        """Вычисление итоговой зарплаты"""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Возврат полной информации о сотруднике"""
        pass

    def __str__(self):
        return (f"Сотрудник [id: {self.id}, имя: {self.name}, "
                f"отдел: {self.department}, базовая зарплата: {self.base_salary}]")

# ============================================================
# 2. Класс Employee (реализация абстрактных методов)
# ============================================================
class Employee(AbstractEmployee):
    """Обычный сотрудник компании"""

    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return f"{super().__str__()}, итоговая зарплата: {self.calculate_salary()}"

# ============================================================
# 3. Manager
# ============================================================
class Manager(Employee):
    """Менеджер с бонусом"""

    def __init__(self, emp_id, name, department, base_salary, bonus: float):
        super().__init__(emp_id, name, department, base_salary)
        self.bonus = bonus

    @property
    def bonus(self):
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Бонус должен быть неотрицательным числом.")
        self.__bonus = float(value)

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        return f"{super().__str__()}, бонус: {self.bonus}, итоговая зарплата: {self.calculate_salary()}"

# ============================================================
# 4. Developer
# ============================================================
class Developer(Employee):
    """Разработчик с уровнем и стеком технологий"""

    def __init__(self, emp_id, name, department, base_salary, tech_stack=None, seniority_level="junior"):
        super().__init__(emp_id, name, department, base_salary)
        self.tech_stack = tech_stack or []
        self.seniority_level = seniority_level

    @property
    def tech_stack(self):
        return self.__tech_stack

    @tech_stack.setter
    def tech_stack(self, value):
        if not isinstance(value, list):
            raise ValueError("tech_stack должен быть списком строк.")
        self.__tech_stack = value

    @property
    def seniority_level(self):
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value):
        if value not in ("junior", "middle", "senior"):
            raise ValueError("seniority_level должен быть 'junior', 'middle' или 'senior'.")
        self.__seniority_level = value

    def add_skill(self, new_skill: str) -> None:
        """Добавляет новую технологию в стек"""
        if new_skill not in self.__tech_stack:
            self.__tech_stack.append(new_skill)

    def calculate_salary(self) -> float:
        coef = {"junior": 1.0, "middle": 1.5, "senior": 2.0}[self.seniority_level]
        return self.base_salary * coef

    def get_info(self) -> str:
        return (f"{super().__str__()}, уровень: {self.seniority_level}, "
                f"технологии: {', '.join(self.tech_stack)}, итоговая зарплата: {self.calculate_salary()}")

# ============================================================
# 5. Salesperson
# ============================================================
class Salesperson(Employee):
    """Продавец с комиссией и объёмом продаж"""

    def __init__(self, emp_id, name, department, base_salary, commission_rate: float, sales_volume: float = 0.0):
        super().__init__(emp_id, name, department, base_salary)
        self.commission_rate = commission_rate
        self.sales_volume = sales_volume

    @property
    def commission_rate(self):
        return self.__commission_rate

    @commission_rate.setter
    def commission_rate(self, value):
        if not 0 <= value <= 1:
            raise ValueError("commission_rate должен быть числом от 0 до 1.")
        self.__commission_rate = float(value)

    @property
    def sales_volume(self):
        return self.__sales_volume

    @sales_volume.setter
    def sales_volume(self, value):
        if value < 0:
            raise ValueError("sales_volume не может быть отрицательным.")
        self.__sales_volume = float(value)

    def update_sales(self, new_sales: float) -> None:
        """Добавить сумму к объёму продаж"""
        if new_sales < 0:
            raise ValueError("Нельзя добавить отрицательный объём продаж.")
        self.__sales_volume += new_sales

    def calculate_salary(self) -> float:
        return self.base_salary + (self.sales_volume * self.commission_rate)

    def get_info(self) -> str:
        return (f"{super().__str__()}, комиссия: {self.commission_rate*100}%, "
                f"объём продаж: {self.sales_volume}, итоговая зарплата: {self.calculate_salary()}")

# ============================================================
# 6. Фабрика сотрудников
# ============================================================
class EmployeeFactory:
    """Фабрика для создания сотрудников по типу"""

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        emp_type = emp_type.lower()
        if emp_type == "employee":
            return Employee(**kwargs)
        elif emp_type == "manager":
            return Manager(**kwargs)
        elif emp_type == "developer":
            return Developer(**kwargs)
        elif emp_type == "salesperson":
            return Salesperson(**kwargs)
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {emp_type}")

# ============================================================
# 7. Тестирование и демонстрация
# ============================================================
if __name__ == "__main__":
    emp = Employee(1, "Иван Иванов", "Бухгалтерия", 50000)
    mgr = Manager(2, "Анна Смирнова", "Управление", 80000, 15000)
    dev = Developer(3, "Петр Петров", "IT", 90000, ["Python", "Django"], "senior")
    sal = Salesperson(4, "Олег Сидоров", "Продажи", 40000, 0.1, 250000)

    employees = [emp, mgr, dev, sal]

    for e in employees:
        print(e.get_info())
        print("-" * 80)

    # Фабричный метод
    print("Демонстрация фабричного метода:\n")
    new_dev = EmployeeFactory.create_employee(
        "developer",
        emp_id=5,
        name="Мария Ковалева",
        department="IT",
        base_salary=70000,
        tech_stack=["JavaScript", "React"],
        seniority_level="middle"
    )
    print(new_dev.get_info())