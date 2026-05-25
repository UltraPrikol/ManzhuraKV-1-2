import pytest
import os
from employee import (
    Company, Project, Department, Employee, 
    Manager, Developer, Salesperson,
    InvalidStatusError
)

class TestProjectCompany:
    
    # --- Тестирование Project ---
    def test_project_team_management(self):
        project = Project(1, "AI Platform", "Desc", "2024-12-31", "planning")
        dev = Developer(1, "John", "DEV", 5000, ["Python"], "senior")
        
        project.add_team_member(dev)
        assert len(project.get_team()) == 1
        assert project.get_team_size() == 1
        
        project.remove_team_member(1)
        assert len(project.get_team()) == 0

    def test_project_total_salary(self):
        project = Project(1, "AI", "Desc", "2024", "planning")
        manager = Manager(1, "Alice", "DEV", 7000, 2000) # 9000
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior") # 10000
        
        project.add_team_member(manager)
        project.add_team_member(developer)
        
        assert project.calculate_total_salary() == 19000

    def test_project_invalid_status_raises_error(self):
        with pytest.raises(InvalidStatusError):
            Project(1, "Test", "Test", "2024", "invalid_status")

    # --- Тестирование Company ---
    def test_company_department_management(self):
        company = Company("TechCorp")
        dept = Department("Development")
        
        company.add_department(dept)
        assert len(company.get_departments()) == 1
        
        company.remove_department("Development")
        assert len(company.get_departments()) == 0

    def test_company_find_employee(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)
        
        dept.add_employee(emp)
        company.add_department(dept)
        
        found = company.find_employee_by_id(1)
        assert found is not None
        assert found.name == "John"

    def test_cannot_delete_department_with_employees(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)
        
        dept.add_employee(emp)
        company.add_department(dept)
        
        with pytest.raises(ValueError, match="Cannot delete department with employees"):
            company.remove_department("Development")

    # --- Сериализация компании (Полный цикл) ---
    def test_company_serialization_roundtrip(self):
        filename = "test_company.json"
        try:
            # Создание
            company = Company("TechCorp")
            dept = Department("Development")
            emp = Employee(1, "John", "DEV", 5000)
            dept.add_employee(emp)
            company.add_department(dept)
            
            # Сохранение
            company.save_to_json(filename)
            
            # Загрузка
            loaded_company = Company.load_from_json(filename)
            
            assert loaded_company.name == "TechCorp"
            assert len(loaded_company.get_departments()) == 1
            loaded_emp = loaded_company.find_employee_by_id(1)
            assert loaded_emp.name == "John"
            
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    # --- Комплексный тест ---
    def test_complex_company_structure(self):
        company = Company("TechInnovations")
        
        # Создание отделов
        dev_department = Department("Development")
        sales_department = Department("Sales")
        
        # Создание сотрудников
        manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
        developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
        salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000)
        
        # Добавление в отделы
        dev_department.add_employee(manager)
        dev_department.add_employee(developer)
        sales_department.add_employee(salesperson)
        
        # Добавление отделов в компанию
        company.add_department(dev_department)
        company.add_department(sales_department)
        
        # Проверки
        assert company.calculate_total_monthly_cost() > 0
        assert len(company.get_all_employees()) == 3
        stats = company.get_department_stats()
        assert stats["Development"]["employee_count"] == 2