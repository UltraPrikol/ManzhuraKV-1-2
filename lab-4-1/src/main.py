class Employee:
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        # приватные атрибуты
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    #Геттеры и сеттеры

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
        if not (isinstance(value, int) or isinstance(value, float)) or value <= 0:
            raise ValueError("Базовая зарплата должна быть положительным числом.")
        self.__base_salary = float(value)

    #Строковое представление
    def __str__(self):
        return (f"Сотрудник [id: {self.__id}, имя: {self.__name}, "
                f"отдел: {self.__department}, базовая зарплата: {self.__base_salary}]")

#Проверка работы
if __name__ == "__main__":
    # Корректное создание объектов
    emp1 = Employee(1, "Иван Иванов", "Отдел продаж", 75000.0)
    emp2 = Employee(2, "Мария Петрова", "Бухгалтерия", 82000.5)

    print(emp1)
    print(emp2)

    # Получение и изменение значений
    print("Имя сотрудника 1:", emp1.name)
    emp1.name = "Иван Сергеевич Иванов"
    print("Новое имя сотрудника 1:", emp1.name)

    # Попытка установить некорректные значения
    try:
        emp1.base_salary = -5000
    except ValueError as e:
        print("Ошибка при установке base_salary:", e)

    try:
        emp2.name = ""
    except ValueError as e:
        print("Ошибка при установке name:", e)