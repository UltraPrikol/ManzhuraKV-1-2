import abc
from typing import List, Any, Dict, Optional
import sqlite3

# --- Базовая сущность (Subject для Observer) ---
class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self, message: str):
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, message: str):
        for observer in self._observers:
            observer.update(message)

# Интерфейс стратегии (нужен классу Employee)
class BonusStrategy(abc.ABC):
    @abc.abstractmethod
    def calculate_bonus(self, base_salary: float) -> float:
        pass

# Базовый класс Сотрудника
class Employee(Subject):
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, skills: List[str] = None):
        super().__init__()
        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary
        self.skills = skills if skills else []
        self.bonus_strategy: Optional[BonusStrategy] = None
        self._seniority = "Junior"

    def set_bonus_strategy(self, strategy: BonusStrategy):
        self.bonus_strategy = strategy

    def get_salary(self) -> float:
        bonus = 0
        if self.bonus_strategy:
            bonus = self.bonus_strategy.calculate_bonus(self.base_salary)
        return self.base_salary + bonus

    def set_salary(self, new_salary: float):
        old_salary = self.base_salary
        self.base_salary = new_salary
        self.notify_observers(f"Salary changed for {self.name}: {old_salary} -> {new_salary}")

    def __str__(self):
        return f"[{self.department}] {self.name} (${self.get_salary()})"
    
# --- 1.1 Singleton ---
class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating new Database Connection instance...")
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # Эмуляция подключения (в памяти)
            cls._connection = sqlite3.connect(':memory:') 
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def get_connection(self):
        return self._connection
    
    def close_connection(self):
        if self._connection:
            self._connection.close()

# --- 1.2 Factory Method ---
class EmployeeFactory(abc.ABC):
    @abc.abstractmethod
    def create_employee(self, name: str) -> Employee:
        pass

class DeveloperFactory(EmployeeFactory):
    def create_employee(self, name: str) -> Employee:
        return Employee(id=0, name=name, department="DEV", base_salary=5000, skills=["Python"])

class ManagerFactory(EmployeeFactory):
    def create_employee(self, name: str) -> Employee:
        return Employee(id=0, name=name, department="HR", base_salary=6000, skills=["Management"])

# --- 1.3 Abstract Factory ---
class CompanyFactory(abc.ABC):
    @abc.abstractmethod
    def create_employee(self, name: str) -> Employee:
        pass
    
    @abc.abstractmethod
    def create_department_config(self) -> str:
        pass

class TechCompanyFactory(CompanyFactory):
    def create_employee(self, name: str) -> Employee:
        return Employee(0, name, "TECH_DEPT", 7000, ["Coding"])
    
    def create_department_config(self) -> str:
        return "Open Space Layout + High End Laptops"

class SalesCompanyFactory(CompanyFactory):
    def create_employee(self, name: str) -> Employee:
        return Employee(0, name, "SALES_DEPT", 4000, ["Negotiation"])
    
    def create_department_config(self) -> str:
        return "Cubicles + Phones"

# --- 1.4 Builder ---
class EmployeeBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._id = 0
        self._name = "Unknown"
        self._department = "General"
        self._salary = 0.0
        self._skills = []
        self._seniority = "Junior"

    def set_id(self, emp_id):
        self._id = emp_id
        return self

    def set_name(self, name):
        self._name = name
        return self

    def set_department(self, dept):
        self._department = dept
        return self

    def set_base_salary(self, salary):
        self._salary = salary
        return self

    def set_skills(self, skills):
        self._skills = skills
        return self

    def set_seniority(self, seniority):
        self._seniority = seniority
        return self

    def build(self) -> Employee:
        emp = Employee(self._id, self._name, self._department, self._salary, self._skills)
        emp._seniority = self._seniority
        self.reset()
        return emp

# --- 2.1 Adapter ---
class ExternalPayrollSystem:
    def calculate_complex_salary_net(self, gross_amount: float, tax_rate: float) -> float:
        # Сложная внешняя логика
        return gross_amount * (1 - tax_rate)

class PayrollAdapter:
    def __init__(self, external_system: ExternalPayrollSystem):
        self.external = external_system

    def calculate_net_salary(self, employee: Employee) -> float:
        # Адаптируем интерфейс к нашей системе (например, фиксируем налог 13%)
        return self.external.calculate_complex_salary_net(employee.get_salary(), 0.13)

# --- 2.2 Decorator ---
class EmployeeDecorator(Employee):
    def __init__(self, wrapped_employee: Employee):
        self._wrapped = wrapped_employee
    
    # Делегируем вызовы
    def get_salary(self) -> float:
        return self._wrapped.get_salary()
    
    @property
    def skills(self):
        return self._wrapped.skills
    
    @property
    def name(self):
        return self._wrapped.name

class BonusDecorator(EmployeeDecorator):
    def __init__(self, employee, bonus_amount):
        super().__init__(employee)
        self.bonus_amount = bonus_amount

    def get_salary(self) -> float:
        return super().get_salary() + self.bonus_amount

class TrainingDecorator(EmployeeDecorator):
    def __init__(self, employee, new_skill):
        super().__init__(employee)
        self.new_skill = new_skill

    @property
    def skills(self):
        current_skills = super().skills
        if self.new_skill not in current_skills:
            return current_skills + [self.new_skill]
        return current_skills

# --- 2.3 Facade ---
class CompanyFacade:
    def __init__(self, repo, db_conn):
        self.repo = repo
        self.db = db_conn
        self.payroll_adapter = PayrollAdapter(ExternalPayrollSystem())

    def hire_employee(self, employee: Employee):
        print(f"FACADE: Hiring {employee.name}...")
        self.repo.add(employee)
        # Логика БД скрыта
        cursor = self.db.get_connection().cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS logs (msg text)")
        cursor.execute("INSERT INTO logs VALUES (?)", (f"Hired {employee.name}",))

    def get_net_salary(self, emp_id: int):
        emp = self.repo.get(emp_id)
        if emp:
            return self.payroll_adapter.calculate_net_salary(emp)
        return 0

# --- 3.1 Observer (реализация) ---
class NotificationSystem(Observer):
    def update(self, message: str):
        print(f"!!! NOTIFICATION: {message} !!!")

# --- 3.2 Strategy (реализация) ---
class PerformanceBonusStrategy(BonusStrategy):
    def calculate_bonus(self, base_salary: float) -> float:
        return base_salary * 0.20  # +20%

class SeniorityBonusStrategy(BonusStrategy):
    def calculate_bonus(self, base_salary: float) -> float:
        return 1000.0  # Фикс $1000

# --- 3.3 Command ---
class Command(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass

class HireEmployeeCommand(Command):
    def __init__(self, employee, repository):
        self.employee = employee
        self.repo = repository

    def execute(self):
        self.repo.add(self.employee)
        print(f"COMMAND: Hired {self.employee.name}")

    def undo(self):
        self.repo.remove(self.employee)
        print(f"COMMAND UNDO: Removed {self.employee.name}")

class UpdateSalaryCommand(Command):
    def __init__(self, employee, new_salary):
        self.employee = employee
        self.new_salary = new_salary
        self.old_salary = employee.base_salary

    def execute(self):
        self.employee.set_salary(self.new_salary)

    def undo(self):
        self.employee.set_salary(self.old_salary)
    
# --- 4.3 Specification Pattern (определяем первым для использования в репозитории) ---
class Specification(abc.ABC):
    @abc.abstractmethod
    def is_satisfied_by(self, candidate: Employee) -> bool:
        pass

    def __and__(self, other):
        return AndSpecification(self, other)

class AndSpecification(Specification):
    def __init__(self, spec1, spec2):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, candidate: Employee) -> bool:
        return self.spec1.is_satisfied_by(candidate) and self.spec2.is_satisfied_by(candidate)

class SalarySpecification(Specification):
    def __init__(self, min_salary):
        self.min_salary = min_salary

    def is_satisfied_by(self, candidate: Employee) -> bool:
        return candidate.get_salary() >= self.min_salary

class DepartmentSpecification(Specification):
    def __init__(self, department):
        self.department = department

    def is_satisfied_by(self, candidate: Employee) -> bool:
        return candidate.department == self.department

# --- 4.1 Repository Pattern ---
class EmployeeRepository:
    def __init__(self):
        self._storage: Dict[int, Employee] = {}

    def add(self, employee: Employee):
        self._storage[employee.id] = employee

    def get(self, emp_id: int) -> Optional[Employee]:
        return self._storage.get(emp_id)

    def remove(self, employee: Employee):
        if employee.id in self._storage:
            del self._storage[employee.id]
    
    def find_by_specification(self, spec: Specification) -> List[Employee]:
        return [emp for emp in self._storage.values() if spec.is_satisfied_by(emp)]

# --- 4.2 Unit of Work ---
class UnitOfWork:
    def __init__(self, repository):
        self.repository = repository
        self.new_objects = []
        self.dirty_objects = []
        self.deleted_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_deleted(self, obj):
        self.deleted_objects.append(obj)

    def commit(self):
        print("\n--- UoW Committing Transaction ---")
        for obj in self.new_objects:
            self.repository.add(obj)
            print(f"UoW: Inserted {obj.name}")
        
        for obj in self.deleted_objects:
            self.repository.remove(obj)
            print(f"UoW: Deleted {obj.name}")
        
        # Для dirty просто логируем, так как объекты мутабельны и уже в памяти
        for obj in self.dirty_objects:
            print(f"UoW: Updated {obj.name}")
            
        self.new_objects.clear()
        self.dirty_objects.clear()
        self.deleted_objects.clear()
    
# --- 5.1 Комплексный пример ---

def demonstrate_patterns():
    print("=== ЗАПУСК ДЕМОНСТРАЦИИ ПАТТЕРНОВ ===\n")

    # 1. Singleton: Проверка БД
    print("--- 1. Singleton ---")
    db1 = DatabaseConnection.get_instance()
    db2 = DatabaseConnection.get_instance()
    print(f"db1 is db2: {db1 is db2}")  # True
    
    # 2. Abstract Factory: Создание компании
    print("\n--- 2. Abstract Factory ---")
    tech_factory = TechCompanyFactory()
    # Создаем сотрудника через фабрику компании (без конкретного имени класса)
    tech_emp = tech_factory.create_employee("Tech Lead")
    print(f"Created via Abstract Factory: {tech_emp}")

    # 3. Builder: Сложный объект
    print("\n--- 3. Builder ---")
    developer = (EmployeeBuilder()
                .set_id(101)
                .set_name("John Doe")
                .set_department("DEV")
                .set_base_salary(5000)
                .set_skills(["Python", "Java"])
                .set_seniority("Senior")
                .build())
    print(f"Built Developer: {developer}, Skills: {developer.skills}")
    
    # 4. Observer: Подписка на изменения
    print("\n--- 4. Observer ---")
    notification_system = NotificationSystem()
    developer.add_observer(notification_system)
    
    # 5. Strategy: Смена стратегии бонусов
    print("\n--- 5. Strategy ---")
    print(f"Base Salary: {developer.base_salary}")
    
    # Стратегия производительности (+20%)
    developer.set_bonus_strategy(PerformanceBonusStrategy())
    print(f"With Performance Bonus: {developer.get_salary()}")
    
    # Смена на стратегию стажа (фиксированно +1000)
    developer.set_bonus_strategy(SeniorityBonusStrategy())
    print(f"With Seniority Bonus: {developer.get_salary()}")
    
    # 6. Command: Выполнение команд и отмена
    print("\n--- 6. Command ---")
    employee_repo = EmployeeRepository()
    
    hire_cmd = HireEmployeeCommand(developer, employee_repo)
    hire_cmd.execute() # Добавляем в репозиторий
    
    salary_cmd = UpdateSalaryCommand(developer, 8000)
    salary_cmd.execute() # Зарплата меняется -> срабатывает Observer
    
    print("Undoing salary update...")
    salary_cmd.undo() # Откат зарплаты -> снова срабатывает Observer
    
    # 7. Decorator: Динамическое добавление возможностей
    print("\n--- 7. Decorator ---")
    # Добавляем супер-навык
    decorated_dev = TrainingDecorator(developer, "Docker")
    # Добавляем временный бонус "Лучший сотрудник месяца"
    decorated_dev = BonusDecorator(decorated_dev, 500)
    
    print(f"Decorated Salary: {decorated_dev.get_salary()}")
    print(f"Decorated Skills: {decorated_dev.skills}")
    
    # 8. Facade & Adapter: Упрощение сложного + работа с "внешней" системой
    print("\n--- 8. Facade & Adapter ---")
    facade = CompanyFacade(employee_repo, db1)
    
    # Фасад использует адаптер внутри
    net_salary = facade.get_net_salary(101)
    print(f"Net Salary (via Facade->Adapter): {net_salary}")
    
    # 9. Unit of Work: Транзакционность
    print("\n--- 9. Unit of Work ---")
    uow = UnitOfWork(employee_repo)
    
    new_dev = Employee(102, "Alice Junior", "DEV", 3000)
    uow.register_new(new_dev)
    uow.commit() # Только здесь Alice попадет в репозиторий
    
    # 10. Specification: Сложный поиск
    print("\n--- 10. Specification ---")
    # Создаем условия: Зарплата > 4000 И Отдел == DEV
    high_salary_spec = SalarySpecification(min_salary=4000)
    dev_spec = DepartmentSpecification("DEV")
    combined_spec = high_salary_spec & dev_spec
    
    # В репозитории сейчас John (5000, DEV) и Alice (3000, DEV)
    # Alice не должна попасть в выборку по зарплате
    results = employee_repo.find_by_specification(combined_spec)
    
    print(f"Found employees (Salary > 4000 & Dept == DEV):")
    for emp in results:
        print(f" - {emp.name} (${emp.get_salary()})")

    # Закрываем ресурсы
    db1.close_connection()

if __name__ == "__main__":
    demonstrate_patterns()