import json
import csv
from typing import List, Optional, Dict
from src.core.department import Department
from src.core.project import Project
from src.core.abstract_employee import AbstractEmployee, Manager, Developer, Salesperson
from src.utils.exceptions import *

class Company:
    def __init__(self, name: str):
        self.name = name
        self.__departments: List[Department] = [] # Aggregation
        self.__projects: List[Project] = []       # Aggregation


    def add_department(self, department: Department):
        if any(d.code == department.code for d in self.__departments):
            raise DuplicateIdError(f"Department {department.code} already exists.")
        self.__departments.append(department)

    def remove_department(self, code: str):
        dept = next((d for d in self.__departments if d.code == code), None)
        if not dept:
            raise DepartmentNotFoundError(f"Department {code} not found.")

        if len(dept.get_employees()) > 0:
            raise DeletionError(f"Cannot delete department {code}: it contains employees.")
        
        self.__departments.remove(dept)


    def add_project(self, project: Project):
        if any(p.project_id == project.project_id for p in self.__projects):
            raise DuplicateIdError(f"Project ID {project.project_id} already exists.")
        self.__projects.append(project)

    def remove_project(self, project_id: int):
        proj = next((p for p in self.__projects if p.project_id == project_id), None)
        if not proj:
            raise ProjectNotFoundError(f"Project {project_id} not found.")
        

        if proj.get_team_size() > 0:
            raise DeletionError(f"Cannot delete project {project_id}: it has an active team.")
            
        self.__projects.remove(proj)


    def get_all_employees(self) -> List[AbstractEmployee]:
        all_emps = []
        for dept in self.__departments:
            all_emps.extend(dept.get_employees())
        return all_emps

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        for dept in self.__departments:
            emp = dept.get_employee_by_id(employee_id)
            if emp:
                return emp
        return None

    def calculate_total_monthly_cost(self) -> float:
        return sum(e.calculate_salary() for e in self.get_all_employees())


    def find_overloaded_employees(self) -> List[AbstractEmployee]:
        """Identifies employees working on more than 1 active project."""
        participation_count = {}
        
        for project in self.__projects:
            if project.status == "active":
                for member in project.get_team():
                    participation_count[member.emp_id] = participation_count.get(member.emp_id, 0) + 1
        
        overloaded = []
        for emp_id, count in participation_count.items():
            if count > 1:
                overloaded.append(self.find_employee_by_id(emp_id))
        return overloaded


    def save_to_json(self, filename: str):
        data = {
            "name": self.name,
            "departments": [d.to_dict() for d in self.__departments],
            "projects": [p.to_dict() for p in self.__projects]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def load_from_json(cls, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        company = cls(data["name"])
        
        for dept_data in data["departments"]:
            dept = Department(dept_data["name"], dept_data["code"])
            for emp_data in dept_data["employees"]:
                e_type = emp_data.pop("type")
                if e_type == "Manager":
                    emp = Manager(**emp_data)
                elif e_type == "Developer":
                    emp = Developer(**emp_data)
                elif e_type == "Salesperson":
                    emp = Salesperson(**emp_data)
                else:
                    continue # Unknown type
                dept.add_employee(emp)
            company.add_department(dept)
            
        for proj_data in data["projects"]:
            team_ids = proj_data.pop("team_ids")
            project = Project(**proj_data)
            
            for emp_id in team_ids:
                emp = company.find_employee_by_id(emp_id)
                if emp:
                    project.add_team_member(emp)
            
            company.add_project(project)
            
        return company

    def export_employees_csv(self, filename: str):
        employees = self.get_all_employees()
        if not employees:
            return
            
        fieldnames = ["emp_id", "name", "department", "base_salary", "calculated_salary"]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for emp in employees:
                row = {
                    "emp_id": emp.emp_id,
                    "name": emp.name,
                    "department": emp.department,
                    "base_salary": emp.base_salary,
                    "calculated_salary": emp.calculate_salary()
                }
                writer.writerow(row)