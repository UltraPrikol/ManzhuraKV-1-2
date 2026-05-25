from datetime import datetime
from typing import List, Dict, Any
from src.core.abstract_employee import AbstractEmployee
from src.utils.exceptions import InvalidStatusError, DuplicateIdError, EmployeeNotFoundError

class Project:
    VALID_STATUSES = {"planning", "active", "completed", "cancelled"}

    def __init__(self, project_id: int, name: str, description: str, deadline: str, status: str):
        self.project_id = project_id
        self.name = name
        self.description = description
        
        # Validate Date
        if isinstance(deadline, str):
            self.deadline = datetime.strptime(deadline, "%Y-%m-%d")
        else:
            self.deadline = deadline
            
        # Validate Status
        if status not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Status must be one of {self.VALID_STATUSES}")
        self.status = status
        
        self.__team: List[AbstractEmployee] = []

    def add_team_member(self, employee: AbstractEmployee) -> None:
        if any(e.emp_id == employee.emp_id for e in self.__team):
            raise DuplicateIdError(f"Employee {employee.emp_id} is already in the project team.")
        self.__team.append(employee)

    def remove_team_member(self, employee_id: int) -> None:
        for i, member in enumerate(self.__team):
            if member.emp_id == employee_id:
                del self.__team[i]
                return
        raise EmployeeNotFoundError(f"Employee {employee_id} not found in project team.")

    def get_team(self) -> List[AbstractEmployee]:
        return self.__team

    def get_team_size(self) -> int:
        return len(self.__team)

    def calculate_total_salary(self) -> float:
        """Calculates sum of salaries of people working on this project."""
        return sum(member.calculate_salary() for member in self.__team)

    def get_project_info(self) -> str:
        return (f"Project: {self.name} (ID: {self.project_id})\n"
                f"Status: {self.status} | Deadline: {self.deadline.date()}\n"
                f"Team Size: {self.get_team_size()}")

    def change_status(self, new_status: str) -> None:
        if new_status not in self.VALID_STATUSES:
            raise InvalidStatusError(f"Invalid status: {new_status}")
        self.status = new_status

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialization Strategy:
        We serialize ID references for team members to avoid massive duplication 
        if saving the whole company, or serialize full objects if saving just the project.
        For this lab, we will serialize minimal info to reconstruct.
        """
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "status": self.status,
            "team_ids": [e.emp_id for e in self.__team]
        }