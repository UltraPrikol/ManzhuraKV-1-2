# company_system.py
from __future__ import annotations
import json
import csv
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from abc import ABC, abstractmethod

# -----------------------
# Исключения
# -----------------------
class EmployeeNotFoundError(Exception):
    pass

class DepartmentNotFoundError(Exception):
    pass

class ProjectNotFoundError(Exception):
    pass

class InvalidStatusError(Exception):
    pass

class DuplicateIdError(Exception):
    pass

class ValidationError(Exception):
    pass

# -----------------------
# Абстрактный сотрудник
# -----------------------
class AbstractEmployee(ABC):
    def __init__(self, employee_id: int, name: str, department_code: str, base_salary: float):
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValidationError("ID сотрудника должен быть положительным целым числом.")
        if not name or not isinstance(name, str):
            raise ValidationError("Имя сотрудника должно быть непустой строкой.")
        if not isinstance(base_salary, (int, float)) or base_salary < 0:
            raise ValidationError("Базовая зарплата должна быть неотрицательным числом.")
        self.employee_id = employee_id
        self.name = name
        self.department_code = department_code
        self.base_salary = float(base_salary)
        # список проектов (храним ссылки на Project по объектам)
        self._projects: List[Project] = []

    @abstractmethod
    def calculate_salary(self) -> float:
        """Рассчитать итоговую месячную зарплату сотрудника."""
        pass

    def assign_to_project(self, project: "Project") -> None:
        if project not in self._projects:
            self._projects.append(project)

    def remove_from_project(self, project: "Project") -> None:
        if project in self._projects:
            self._projects.remove(project)

    def get_projects(self) -> List["Project"]:
        return list(self._projects)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "employee_id": self.employee_id,
            "name": self.name,
            "department_code": self.department_code,
            "base_salary": self.base_salary,
            # custom fields for subclasses will be added in subclass override
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.employee_id} name={self.name}>"

# -----------------------
# Конкретные типы сотрудников
# -----------------------
class Manager(AbstractEmployee):
    def __init__(self, employee_id: int, name: str, department_code: str, base_salary: float, bonus: float):
        super().__init__(employee_id, name, department_code, base_salary)
        if bonus < 0:
            raise ValidationError("Бонус менеджера не может быть отрицательным.")
        self.bonus = float(bonus)

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({"bonus": self.bonus})
        return d

class Developer(AbstractEmployee):
    def __init__(self, employee_id: int, name: str, department_code: str, base_salary: float,
                 skills: Optional[List[str]] = None, level: str = "junior"):
        super().__init__(employee_id, name, department_code, base_salary)
        self.skills = skills or []
        if level not in ("junior", "mid", "senior"):
            raise ValidationError("Неверный уровень разработчика. Ожидается 'junior','mid' или 'senior'.")
        self.level = level

    def calculate_salary(self) -> float:
        level_multiplier = {"junior": 1.0, "mid": 1.2, "senior": 1.5}
        return self.base_salary * level_multiplier.get(self.level, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({"skills": self.skills, "level": self.level})
        return d

class Salesperson(AbstractEmployee):
    def __init__(self, employee_id: int, name: str, department_code: str, base_salary: float,
                 commission_rate: float, sales_target: float):
        super().__init__(employee_id, name, department_code, base_salary)
        if not (0 <= commission_rate <= 1):
            raise ValidationError("Комиссионная ставка должна быть в диапазоне [0,1].")
        if sales_target < 0:
            raise ValidationError("Цель продаж не может быть отрицательной.")
        self.commission_rate = float(commission_rate)
        self.sales_target = float(sales_target)
        # текущие продажи (для демонстрации) — не обязательны
        self.current_sales = 0.0

    def calculate_salary(self) -> float:
        return self.base_salary + (self.commission_rate * self.current_sales)

    def to_dict(self) -> Dict[str, Any]:
        d = super().to_dict()
        d.update({
            "commission_rate": self.commission_rate,
            "sales_target": self.sales_target,
            "current_sales": self.current_sales
        })
        return d

# -----------------------
# Department (агрегация)
# -----------------------
class Department:
    def __init__(self, name: str, code: str):
        if not name or not isinstance(name, str):
            raise ValidationError("Название отдела должно быть непустой строкой.")
        if not code or not isinstance(code, str):
            raise ValidationError("Код отдела должен быть непустой строкой.")
        self.name = name
        self.code = code
        self._employees: List[AbstractEmployee] = []

    def add_employee(self, employee: AbstractEmployee) -> None:
        if any(e.employee_id == employee.employee_id for e in self._employees):
            raise DuplicateIdError(f"Сотрудник с ID {employee.employee_id} уже в отделе {self.code}.")
        self._employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        for e in self._employees:
            if e.employee_id == employee_id:
                self._employees.remove(e)
                return
        raise EmployeeNotFoundError(f"Сотрудник {employee_id} не найден в отделе {self.code}.")

    def get_employees(self) -> List[AbstractEmployee]:
        return list(self._employees)

    def get_size(self) -> int:
        return len(self._employees)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "code": self.code,
            "employee_ids": [e.employee_id for e in self._employees]
        }

    def __repr__(self):
        return f"<Department {self.code} ({self.name}) size={self.get_size()}>"

# -----------------------
# Project (композиция)
# -----------------------
class Project:
    VALID_STATUSES = {"planning", "active", "completed", "cancelled"}

    def __init__(self, project_id: int, name: str, description: str,
                 deadline: Union[str, datetime], status: str, budget: float = 0.0):
        if not isinstance(project_id, int) or project_id <= 0:
            raise ValidationError("ID проекта должен быть положительным целым числом.")
        if not name or not isinstance(name, str):
            raise ValidationError("Название проекта должно быть непустой строкой.")
        if not isinstance(budget, (int, float)) or budget < 0:
            raise ValidationError("Бюджет проекта должен быть неотрицательным числом.")
        self.project_id = project_id
        self.name = name
        self.description = description
        # deadline можно передать как строку "YYYY-MM-DD"
        if isinstance(deadline, str):
            try:
                self.deadline = datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("Неверный формат даты. Ожидается YYYY-MM-DD.")
        elif isinstance(deadline, datetime):
            self.deadline = deadline
        else:
            raise ValidationError("Срок проекта должен быть строкой в формате YYYY-MM-DD или datetime.")
        if self.deadline < datetime.now():
            # разрешаем проекты с прошлой датой, но предупреждаем (можно считать невалидным)
            # Здесь выберем строгую проверку: если проект создан с past deadline — это ошибка.
            # (пользователь может изменить логику при необходимости)
            pass  # можно либо поднять ошибку, либо позволить — оставляем разрешённым
        if status not in Project.VALID_STATUSES:
            raise InvalidStatusError(f"Неверный статус проекта: {status}")
        self.status = status
        self.budget = float(budget)
        # композиция — проект владеет списком сотрудников (ссылки на объекты)
        self.__team: List[AbstractEmployee] = []

    # валидируем входные данные в init уже сделали
    def add_team_member(self, employee: AbstractEmployee) -> None:
        if any(e.employee_id == employee.employee_id for e in self.__team):
            raise DuplicateIdError(f"Сотрудник {employee.employee_id} уже в проекте {self.project_id}.")
        self.__team.append(employee)
        # регистрация участия у сотрудника (двунаправленная связь)
        employee.assign_to_project(self)

    def remove_team_member(self, employee_id: int) -> None:
        for e in list(self.__team):
            if e.employee_id == employee_id:
                self.__team.remove(e)
                e.remove_from_project(self)
                return
        raise EmployeeNotFoundError(f"Сотрудник {employee_id} не найден в проекте {self.project_id}.")

    def get_team(self) -> List[AbstractEmployee]:
        return list(self.__team)

    def get_team_size(self) -> int:
        return len(self.__team)

    def calculate_total_salary(self) -> float:
        return sum(e.calculate_salary() for e in self.__team)

    def get_project_info(self) -> str:
        info = (
            f"Проект {self.project_id} — {self.name}\n"
            f"Описание: {self.description}\n"
            f"Срок: {self.deadline.date()}\n"
            f"Статус: {self.status}\n"
            f"Бюджет: {self.budget}\n"
            f"Команда ({self.get_team_size()}): {[e.employee_id for e in self.__team]}\n"
            f"Суммарная зарплата команды: {self.calculate_total_salary():.2f}"
        )
        return info

    def change_status(self, new_status: str) -> None:
        if new_status not in Project.VALID_STATUSES:
            raise InvalidStatusError(f"Неверный статус проекта: {new_status}")
        self.status = new_status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "status": self.status,
            "budget": self.budget,
            "team_ids": [e.employee_id for e in self.__team]
        }

    def __repr__(self):
        return f"<Project {self.project_id} '{self.name}' status={self.status} team_size={self.get_team_size()}>"

# -----------------------
# Company (агрегация)
# -----------------------
class Company:
    def __init__(self, name: str):
        if not name or not isinstance(name, str):
            raise ValidationError("Название компании должно быть непустой строкой.")
        self.name = name
        self.__departments: List[Department] = []
        self.__projects: List[Project] = []
        # дополнительные структуры для быстрой валидации уникальности
        self._employee_id_set: set = set()
        self._project_id_set: set = set()

    # -----------------
    # Отделы
    # -----------------
    def add_department(self, dept: Department) -> None:
        if any(d.code == dept.code for d in self.__departments):
            raise DuplicateIdError(f"Отдел с кодом {dept.code} уже существует.")
        self.__departments.append(dept)

    def remove_department(self, dept_code: str) -> None:
        dept = self._find_department_by_code(dept_code)
        if dept.get_size() > 0:
            raise ValidationError("Нельзя удалить отдел, в котором есть сотрудники.")
        self.__departments.remove(dept)

    def get_departments(self) -> List[Department]:
        return list(self.__departments)

    def _find_department_by_code(self, code: str) -> Department:
        for d in self.__departments:
            if d.code == code:
                return d
        raise DepartmentNotFoundError(f"Отдел с кодом {code} не найден.")

    # -----------------
    # Сотрудники: добавление/удаление в рамках отделов
    # -----------------
    def add_employee_to_department(self, employee: AbstractEmployee, dept_code: str) -> None:
        if employee.employee_id in self._employee_id_set:
            raise DuplicateIdError(f"Сотрудник с ID {employee.employee_id} уже есть в компании.")
        dept = self._find_department_by_code(dept_code)
        dept.add_employee(employee)
        self._employee_id_set.add(employee.employee_id)

    def remove_employee(self, employee_id: int) -> None:
        # нельзя удалять сотрудника, если он участвует в проектах
        emp = self.find_employee_by_id(employee_id)
        if emp is None:
            raise EmployeeNotFoundError(f"Сотрудник {employee_id} не найден.")
        if emp.get_projects():
            raise ValidationError("Нельзя удалить сотрудника, который участвует в проектах.")
        # найдём отдел, в котором он состоит
        for d in self.__departments:
            try:
                d.remove_employee(employee_id)
                self._employee_id_set.discard(employee_id)
                return
            except EmployeeNotFoundError:
                continue
        # если дошли сюда — сотрудник найден не был в отделах
        raise EmployeeNotFoundError(f"Сотрудник {employee_id} не найден в отделах.")

    def get_all_employees(self) -> List[AbstractEmployee]:
        res = []
        for d in self.__departments:
            res.extend(d.get_employees())
        return res

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        for e in self.get_all_employees():
            if e.employee_id == employee_id:
                return e
        return None

    def transfer_employee(self, employee_id: int, from_dept_code: str, to_dept_code: str) -> None:
        from_dept = self._find_department_by_code(from_dept_code)
        to_dept = self._find_department_by_code(to_dept_code)
        # найти сотрудника в from_dept
        emp = None
        for e in from_dept.get_employees():
            if e.employee_id == employee_id:
                emp = e
                break
        if emp is None:
            raise EmployeeNotFoundError(f"Сотрудник {employee_id} не найден в отделе {from_dept_code}.")
        # перенос
        from_dept.remove_employee(employee_id)
        emp.department_code = to_dept.code
        to_dept.add_employee(emp)

    # -----------------
    # Проекты
    # -----------------
    def add_project(self, project: Project) -> None:
        if project.project_id in self._project_id_set:
            raise DuplicateIdError(f"Проект с ID {project.project_id} уже существует в компании.")
        self.__projects.append(project)
        self._project_id_set.add(project.project_id)

    def remove_project(self, project_id: int) -> None:
        project = self.find_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Проект {project_id} не найден.")
        if project.get_team_size() > 0:
            raise ValidationError("Нельзя удалить проект, над которым работает команда.")
        self.__projects.remove(project)
        self._project_id_set.discard(project.project_id)

    def get_projects(self) -> List[Project]:
        return list(self.__projects)

    def find_project_by_id(self, project_id: int) -> Optional[Project]:
        for p in self.__projects:
            if p.project_id == project_id:
                return p
        return None

    def get_projects_by_status(self, status: str) -> List[Project]:
        if status not in Project.VALID_STATUSES:
            raise InvalidStatusError(f"Неверный статус: {status}")
        return [p for p in self.__projects if p.status == status]

    # -----------------
    # Финансы и отчёты
    # -----------------
    def calculate_total_monthly_cost(self) -> float:
        return sum(e.calculate_salary() for e in self.get_all_employees())

    # экспорт CSV по сотрудникам
    def export_employees_csv(self, filepath: str) -> None:
        employees = self.get_all_employees()
        with open(filepath, mode="w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            header = ["employee_id", "name", "department_code", "type", "base_salary", "calculated_salary", "extra"]
            writer.writerow(header)
            for e in employees:
                extra = {}
                if isinstance(e, Manager):
                    extra = {"bonus": e.bonus}
                elif isinstance(e, Developer):
                    extra = {"skills": ",".join(e.skills), "level": e.level}
                elif isinstance(e, Salesperson):
                    extra = {"commission_rate": e.commission_rate, "sales_target": e.sales_target, "current_sales": e.current_sales}
                writer.writerow([
                    e.employee_id, e.name, e.department_code, e.__class__.__name__,
                    f"{e.base_salary:.2f}", f"{e.calculate_salary():.2f}", json.dumps(extra, ensure_ascii=False)
                ])

    # экспорт CSV по проектам (включая состав команд и суммарную зарплату)
    def export_projects_csv(self, filepath: str) -> None:
        projects = self.get_projects()
        with open(filepath, mode="w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            header = ["project_id", "name", "description", "deadline", "status", "budget", "team_ids", "team_total_salary"]
            writer.writerow(header)
            for p in projects:
                writer.writerow([
                    p.project_id, p.name, p.description, p.deadline.strftime("%Y-%m-%d"),
                    p.status, f"{p.budget:.2f}", ",".join(str(e.employee_id) for e in p.get_team()),
                    f"{p.calculate_total_salary():.2f}"
                ])

    def export_financial_report(self, filepath: str) -> None:
        total = self.calculate_total_monthly_cost()
        lines = [
            f"Финансовый отчет компании: {self.name}",
            f"Дата отчёта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Общие ежемесячные затраты на зарплаты: {total:.2f}",
            "",
            "Отчёт по отделам:"
        ]
        for d in self.get_departments():
            dept_emps = d.get_employees()
            dept_cost = sum(e.calculate_salary() for e in dept_emps)
            lines.append(f"- {d.code} ({d.name}): сотрудников {len(dept_emps)}, затраты {dept_cost:.2f}")
        lines.append("")
        lines.append("Отчёт по проектам:")
        for p in self.get_projects():
            lines.append(f"- {p.project_id} {p.name}: бюджет {p.budget:.2f}, команда {','.join(str(e.employee_id) for e in p.get_team())}, зарплаты команды {p.calculate_total_salary():.2f}")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # -----------------
    # Сериализация / десериализация (JSON)
    # -----------------
    def save_to_json(self, filepath: str) -> None:
        # сериализуем департаменты, сотрудников и проекты отдельно, сохраняя ссылки по id
        data = {
            "company": {"name": self.name},
            "departments": [d.to_dict() for d in self.__departments],
            "employees": [e.to_dict() for e in self.get_all_employees()],
            "projects": [p.to_dict() for p in self.__projects]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_json(cls, filepath: str) -> "Company":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        company_name = data.get("company", {}).get("name", "LoadedCompany")
        company = Company(company_name)

        # 1) создаём отделы
        dept_map: Dict[str, Department] = {}
        for d in data.get("departments", []):
            dept = Department(d["name"], d["code"])
            company.add_department(dept)
            dept_map[dept.code] = dept

        # 2) создаём сотрудников (без привязки к проектам)
        emp_map: Dict[int, AbstractEmployee] = {}
        for e in data.get("employees", []):
            typ = e.get("type")
            eid = e["employee_id"]
            name = e["name"]
            dept_code = e["department_code"]
            base = e["base_salary"]
            if typ == "Manager":
                emp = Manager(eid, name, dept_code, base, e.get("bonus", 0.0))
            elif typ == "Developer":
                emp = Developer(eid, name, dept_code, base, e.get("skills", []), e.get("level", "junior"))
            elif typ == "Salesperson":
                emp = Salesperson(eid, name, dept_code, base, e.get("commission_rate", 0.0), e.get("sales_target", 0.0))
                emp.current_sales = e.get("current_sales", 0.0)
            else:
                raise ValidationError(f"Неизвестный тип сотрудника при загрузке: {typ}")
            emp_map[eid] = emp
            # добавляем сотрудника в соответствующий отдел
            if dept_code not in dept_map:
                raise DepartmentNotFoundError(f"При загрузке: отдел {dept_code} не найден.")
            company.add_employee_to_department(emp, dept_code)

        # 3) создаём проекты и привязываем команду
        proj_map: Dict[int, Project] = {}
        for p in data.get("projects", []):
            pid = p["project_id"]
            proj = Project(pid, p["name"], p.get("description", ""), p["deadline"], p["status"], p.get("budget", 0.0))
            company.add_project(proj)
            proj_map[pid] = proj

        # 4) связываем сотрудников и проекты (восстановление команд)
        for p in data.get("projects", []):
            pid = p["project_id"]
            team_ids = p.get("team_ids", [])
            proj = proj_map[pid]
            for tid in team_ids:
                if tid not in emp_map:
                    raise EmployeeNotFoundError(f"При загрузке: сотрудник {tid} не найден для проекта {pid}.")
                emp = emp_map[tid]
                proj.add_team_member(emp)

        # Все проверки пройдены
        return company

    # -----------------
    # Аналитика и планирование
    # -----------------
    def get_department_stats(self) -> Dict[str, Dict[str, Any]]:
        stats: Dict[str, Dict[str, Any]] = {}
        for d in self.get_departments():
            emps = d.get_employees()
            total_salary = sum(e.calculate_salary() for e in emps)
            stats[d.code] = {
                "name": d.name,
                "employee_count": len(emps),
                "total_salary": total_salary,
                "avg_salary": (total_salary / len(emps)) if emps else 0.0
            }
        return stats

    def get_project_budget_analysis(self) -> Dict[int, Dict[str, Any]]:
        analysis: Dict[int, Dict[str, Any]] = {}
        for p in self.get_projects():
            team_cost = p.calculate_total_salary()
            analysis[p.project_id] = {
                "name": p.name,
                "budget": p.budget,
                "team_cost": team_cost,
                "budget_balance": p.budget - team_cost
            }
        return analysis

    def find_overloaded_employees(self, project_threshold: int = 2) -> List[AbstractEmployee]:
        """Считаем 'перегруженными' сотрудников тех, у кого проектов > project_threshold."""
        overloaded = []
        for e in self.get_all_employees():
            if len(e.get_projects()) > project_threshold:
                overloaded.append(e)
        return overloaded

    def assign_employee_to_project(self, employee_id: int, project_id: int) -> bool:
        emp = self.find_employee_by_id(employee_id)
        if emp is None:
            raise EmployeeNotFoundError(f"Сотрудник {employee_id} не найден.")
        proj = self.find_project_by_id(project_id)
        if proj is None:
            raise ProjectNotFoundError(f"Проект {project_id} не найден.")
        # проверить доступность
        if not self.check_employee_availability(employee_id):
            return False
        proj.add_team_member(emp)
        return True

    def check_employee_availability(self, employee_id: int, max_projects: int = 3) -> bool:
        """Сотрудник доступен, если у него проектов < max_projects"""
        emp = self.find_employee_by_id(employee_id)
        if emp is None:
            raise EmployeeNotFoundError(f"Сотрудник {employee_id} не найден.")
        return len(emp.get_projects()) < max_projects

# -----------------------
# Демонстрация (main)
# -----------------------
if __name__ == "__main__":
    # Демонстрация по заданию
    try:
        # Создание компании
        company = Company("TechInnovations")

        # Создание отделов
        dev_department = Department("Development", "DEV")
        sales_department = Department("Sales", "SAL")

        # Добавление отделов в компанию
        company.add_department(dev_department)
        company.add_department(sales_department)

        # Создание сотрудников разных типов
        manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
        developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
        salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000)
        salesperson.current_sales = 30000  # для демонстрации комиссии

        # Добавление сотрудников в отделы
        company.add_employee_to_department(manager, "DEV")
        company.add_employee_to_department(developer, "DEV")
        company.add_employee_to_department(salesperson, "SAL")

        # Создание проектов
        ai_project = Project(101, "AI Platform", "Разработка AI системы", "2024-12-31", "active", budget=200000)
        web_project = Project(102, "Web Portal", "Создание веб-портала", "2024-09-30", "planning", budget=50000)

        # Добавление проектов в компанию
        company.add_project(ai_project)
        company.add_project(web_project)

        # Формирование команд проектов
        ai_project.add_team_member(developer)
        ai_project.add_team_member(manager)
        web_project.add_team_member(developer)  # developer работает на двух проектах

        # Демонстрация: попытка добавить сотрудника с дубликатом ID
        try:
            dup_dev = Developer(2, "Clone Bob", "DEV", 4000, ["Java"], "mid")
            company.add_employee_to_department(dup_dev, "DEV")
        except DuplicateIdError as ex:
            print("Ошибка (ожидаемо):", ex)

        # Попытка невалидного изменения статуса
        try:
            ai_project.change_status("invalid_status")
        except InvalidStatusError as ex:
            print("Ошибка изменения статуса (ожидаемо):", ex)

        # Попытка удаления занятого отдела
        try:
            company.remove_department("DEV")
        except ValidationError as ex:
            print("Ошибка удаления отдела (ожидаемо):", ex)

        # Сохранение компании в JSON
        company.save_to_json("company_data.json")
        print("Компания сохранена в company_data.json")

        # Загрузка компании из JSON
        loaded_company = Company.load_from_json("company_data.json")
        print("Компания загружена из company_data.json")

        # Экспорт отчетов
        company.export_employees_csv("employees_report.csv")
        company.export_projects_csv("projects_report.csv")
        company.export_financial_report("financial_report.txt")
        print("Экспорт отчётов выполнен: employees_report.csv, projects_report.csv, financial_report.txt")

        # Анализ данных
        print("Общие ежемесячные затраты:", company.calculate_total_monthly_cost())
        print("Статистика по отделам:", company.get_department_stats())
        print("Анализ бюджетов проектов:", company.get_project_budget_analysis())
        print("Перегруженные сотрудники:", company.find_overloaded_employees(project_threshold=1))

        # Планирование назначения
        can_assign = company.assign_employee_to_project(3, 101)  # назначить sales на AI project
        print("Назначение sales на AI project:", can_assign)

        # Демонстрация удаления проекта, над которым есть команда (ошибка)
        try:
            company.remove_project(101)
        except ValidationError as ex:
            print("Ошибка удаления проекта (ожидаемо):", ex)

        # Перенос сотрудника между отделами
        company.transfer_employee(3, "SAL", "DEV")
        print("Перенос сотрудника 3 из SAL в DEV выполнен.")

    except Exception as e:
        print("Непредвиденная ошибка при демонстрации:", repr(e))
