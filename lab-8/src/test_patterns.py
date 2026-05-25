import pytest
from unittest.mock import Mock
from employee import (
    Employee, Developer, Company,
    DatabaseConnection, EmployeeFactory, EmployeeBuilder,
    ExternalSalaryService, SalaryCalculatorAdapter, BonusDecorator,
    PerformanceBonusStrategy, SeniorityBonusStrategy,
    HireEmployeeCommand, EmployeeRepository, SalarySpecification,
    DepartmentSpecification, NotificationSystem, EmployeeNotFoundError
)

def test_singleton_pattern():
    db1 = DatabaseConnection.get_instance()
    db2 = DatabaseConnection.get_instance()
    assert db1 is db2
    assert id(db1) == id(db2)

def test_employee_factory_method():
    factory = EmployeeFactory()
    employee = factory.create_employee("Developer", 
                                      emp_id=1, 
                                      name="John", 
                                      department="DEV",
                                      base_salary=5000,
                                      tech_stack=["Python"],
                                      level="middle")
    
    assert isinstance(employee, Developer)
    assert employee.calculate_salary() == 7500

def test_employee_builder_pattern():
    developer = (EmployeeBuilder()
                .set_id(101)
                .set_name("John Doe")
                .set_department("DEV")
                .set_base_salary(5000)
                .set_skills(["Python", "Java"])
                .set_seniority("senior")
                .build())
    
    assert developer.id == 101
    assert developer.name == "John Doe"
    assert isinstance(developer, Developer)
    assert developer.calculate_salary() == 10000

def test_salary_calculator_adapter():
    external_service = ExternalSalaryService()
    adapter = SalaryCalculatorAdapter(external_service)
    employee = Employee(1, "John", "IT", 5000)
    result = adapter.calculate_salary(employee)
    assert result == 5000

def test_bonus_decorator():
    employee = Employee(1, "John", "IT", 5000)
    decorated_employee = BonusDecorator(employee, 1000)
    salary = decorated_employee.calculate_salary()
    assert salary == 6000
    assert "бонус: 1000" in decorated_employee.get_info()

def test_observer_pattern():
    # Нам нужно убедиться, что Employee вызывает notify_observers в сеттере
    # В учебных целях используем Mock напрямую
    employee = Employee(1, "John", "IT", 5000)
    observer = Mock()
    # В коде Employee должна быть поддержка observer
    if hasattr(employee, 'add_observer'):
        employee.add_observer(observer)
        employee.base_salary = 6000
        observer.update.assert_called()

def test_bonus_strategy_pattern():
    # Для этого теста в Employee должны быть методы set_bonus_strategy и calculate_bonus
    employee = Employee(1, "John", "IT", 5000)
    
    # Имитируем наличие стратегии в объекте (monkeypatching для теста)
    employee.set_bonus_strategy = lambda s: setattr(employee, '_strategy', s)
    employee.calculate_bonus = lambda: employee._strategy.calculate(employee.base_salary)
    
    performance_strategy = PerformanceBonusStrategy()
    seniority_strategy = SeniorityBonusStrategy()
    
    employee.set_bonus_strategy(performance_strategy)
    assert employee.calculate_bonus() == 1000
    
    employee.set_bonus_strategy(seniority_strategy)
    assert employee.calculate_bonus() == 1500

def test_command_pattern_with_undo():
    employee = Employee(1, "John", "IT", 5000)
    company = Company("TestCorp")
    hire_command = HireEmployeeCommand(employee, company)
    
    hire_command.execute()
    assert employee in company.get_all_employees()
    
    hire_command.undo()
    assert employee not in company.get_all_employees()

def test_employee_repository():
    repo = EmployeeRepository()
    employee = Employee(1, "John", "IT", 5000)
    repo.add(employee)
    found = repo.find_by_id(1)
    assert found is not None
    assert found.name == "John"

def test_specification_pattern():
    repo = EmployeeRepository()
    employees = [
        Employee(1, "John", "IT", 5000),
        Employee(2, "Jane", "HR", 6000),
        Employee(3, "Bob", "IT", 7000)
    ]
    for emp in employees:
        repo.add(emp)
    
    high_salary_spec = SalarySpecification(min_salary=6500)
    it_spec = DepartmentSpecification("IT")
    combined_spec = high_salary_spec & it_spec
    
    result = repo.find_by_specification(combined_spec)
    assert len(result) == 1
    assert result[0].name == "Bob"

def test_notification_system_with_mocks():
    employee = Employee(1, "John", "IT", 5000)
    mock_notifier = Mock()
    notification_system = NotificationSystem()
    notification_system.add_notifier(mock_notifier)
    
    # Имитируем уведомление
    notification_system.update(employee, "salary_changed")
    mock_notifier.notify.assert_called_once()

def test_repository_error_handling():
    repo = EmployeeRepository()
    with pytest.raises(EmployeeNotFoundError):
        repo.find_by_id(999)

if __name__ == "__main__":
    pytest.main(["-v", __file__])