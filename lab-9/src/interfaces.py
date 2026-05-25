from abc import ABC, abstractmethod
from typing import List

class ISalaryCalculable(ABC):
    """Интерфейс для объектов, имеющих зарплату."""
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

class IInfoProvidable(ABC):
    """Интерфейс для предоставления информации."""
    @abstractmethod
    def get_info(self) -> str:
        pass

class ISkillManageable(ABC):
    """Интерфейс для управления навыками (например, для разработчиков)."""
    @abstractmethod
    def add_skill(self, skill: str) -> None:
        pass

class IEmployeeRepository(ABC):
    """Интерфейс репозитория (DIP)."""
    @abstractmethod
    def add(self, employee: ISalaryCalculable) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[ISalaryCalculable]:
        pass