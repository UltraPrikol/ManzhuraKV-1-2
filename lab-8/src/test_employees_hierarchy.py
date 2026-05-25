import pytest
from employee import (
    Manager, Developer, Salesperson, 
    AbstractEmployee, EmployeeFactory
)

class TestEmployeesHierarchy:
    
    # 1. Тестирование абстрактного класса
    def test_cannot_instantiate_abstract_employee(self):
        with pytest.raises(TypeError):
            AbstractEmployee()

    # 2. Тестирование класса Manager
    def test_manager_salary_calculation(self):
        # Arrange
        manager = Manager(1, "John", "Management", 5000, 1000)
        # Act
        salary = manager.calculate_salary()
        # Assert
        assert salary == 6000

    def test_manager_get_info_includes_bonus(self):
        manager = Manager(1, "John", "Management", 5000, 1000)
        info = manager.get_info()
        assert "бонус: 1000" in info
        assert "итоговая зарплата: 6000" in info

    def test_manager_negative_bonus_error(self):
        with pytest.raises(ValueError):
            Manager(1, "John", "Mgmt", 5000, -100)

    # 3. Тестирование класса Developer (Параметризованные тесты)
    @pytest.mark.parametrize("level,expected_salary", [
        ("junior", 5000),   # 5000 * 1.0
        ("middle", 7500),   # 5000 * 1.5
        ("senior", 10000)   # 5000 * 2.0
    ])
    def test_developer_salary_by_level(self, level, expected_salary):
        # Arrange
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], level)
        # Act & Assert
        assert dev.calculate_salary() == expected_salary

    def test_developer_add_skill(self):
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")
        dev.add_skill("Docker")
        assert "Docker" in dev.tech_stack

    # 4. Тестирование класса Salesperson
    def test_salesperson_salary(self):
        # 4000 + (50000 * 0.15) = 4000 + 7500 = 11500
        sales = Salesperson(3, "Saly", "Sales", 4000, 0.15, 50000)
        assert sales.calculate_salary() == 11500

    def test_salesperson_update_sales(self):
        sales = Salesperson(3, "Saly", "Sales", 4000, 0.15, 0)
        sales.update_sales(1000)
        assert sales.sales_volume == 1000

    # 5. Тестирование фабрики
    def test_factory_creates_correct_class(self):
        mgr = EmployeeFactory.create_employee("Manager", emp_id=1, name="M", department="D", base_salary=100, bonus=10)
        assert isinstance(mgr, Manager)
        
        dev = EmployeeFactory.create_employee("Developer", emp_id=2, name="D", department="D", base_salary=100, tech_stack=[], level="junior")
        assert isinstance(dev, Developer)

    # 6. Полиморфное поведение
    def test_polymorphic_collection(self):
        employees = [
            Manager(1, "A", "D", 1000, 100),  # 1100
            Developer(2, "B", "D", 1000, [], "junior") # 1000
        ]
        
        total_salary = sum(emp.calculate_salary() for emp in employees)
        assert total_salary == 2100