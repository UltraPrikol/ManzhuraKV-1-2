import pytest
from employee import Employee

class TestEmployee:
    def test_employee_creation_valid_data(self):
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)

        # Assert
        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000

    def test_employee_invalid_id_raises_error(self):
        # Assert
        with pytest.raises(ValueError):
            Employee(-1, "Alice", "IT", 5000)

    def test_employee_invalid_name_raises_error(self):
        with pytest.raises(ValueError):
            Employee(1, "", "IT", 5000)

    def test_employee_negative_salary_raises_error(self):
        with pytest.raises(ValueError):
            Employee(1, "Alice", "IT", -5000)

    def test_employee_calculate_salary(self):
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        # Act
        salary = emp.calculate_salary()
        # Assert
        assert salary == 5000

    def test_employee_str_representation(self):
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        # Act
        result = str(emp)
        # Assert
        expected = "Сотрудник [id: 1, имя: Alice, отдел: IT, базовая зарплата: 5000]"
        assert result == expected