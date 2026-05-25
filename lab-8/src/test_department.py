import pytest
from employee import Employee, Department, Manager, Developer, DuplicateIdError

class TestDepartmentAndMagicMethods:
    
    # --- Тесты магических методов сотрудников ---
    def test_employee_equality(self):
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(1, "Jane", "HR", 4000) # Тот же ID
        emp3 = Employee(2, "Bob", "IT", 5000)
        
        assert emp1 == emp2  # ID совпадают
        assert emp1 != emp3

    def test_employee_salary_comparison(self):
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        
        assert emp1 < emp2
        assert emp2 > emp1

    def test_employee_addition(self):
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        
        assert emp1 + emp2 == 11000

    # --- Тесты методов Отдела ---
    def test_department_add_remove_employee(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        
        dept.add_employee(emp)
        assert len(dept.get_employees()) == 1
        
        dept.remove_employee(1)
        assert len(dept.get_employees()) == 0

    def test_duplicate_employee_id_raises_error(self):
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp1)
        
        # Пытаемся добавить сотрудника с тем же ID
        with pytest.raises(DuplicateIdError):
            dept.add_employee(Employee(1, "Clone", "IT", 5000))

    # --- Тесты магических методов Отдела ---
    def test_department_magic_methods(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        
        dept.add_employee(emp)
        
        assert len(dept) == 1
        assert dept[0] == emp
        assert emp in dept

    def test_department_iteration(self):
        dept = Department("IT")
        employees = [Employee(i, f"Emp{i}", "IT", 5000) for i in range(3)]
        
        for emp in employees:
            dept.add_employee(emp)
        
        count = 0
        for employee in dept:
            count += 1
        
        assert count == 3

    # --- Тесты итерации по навыкам (Developer) ---
    def test_developer_skills_iteration(self):
        dev = Developer(1, "John", "DEV", 5000, ["Python", "Java", "SQL"], "senior")
        
        skills = []
        for skill in dev:
            skills.append(skill)
        
        assert skills == ["Python", "Java", "SQL"]

    # --- Тесты сериализации ---
    def test_employee_serialization(self):
        emp = Employee(1, "John", "IT", 5000)
        data = emp.to_dict()
        new_emp = Employee.from_dict(data)
        
        assert new_emp.id == emp.id
        assert new_emp.name == emp.name

    # --- Интеграционный тест ---
    def test_department_integration_salary(self):
        dept = Department("Development")
        manager = Manager(1, "Alice", "DEV", 7000, 2000) # 9000
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior") # 10000
        
        dept.add_employee(manager)
        dept.add_employee(developer)
        
        total_salary = dept.calculate_total_salary()
        assert total_salary == 19000
        
        stats = dept.get_employee_count()
        assert stats["Manager"] == 1
        assert stats["Developer"] == 1