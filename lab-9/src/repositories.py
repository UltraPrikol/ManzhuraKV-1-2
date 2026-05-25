from typing import List
from interfaces import IEmployeeRepository, ISalaryCalculable

class InMemoryEmployeeRepository(IEmployeeRepository):
    def __init__(self):
        self._storage: List[ISalaryCalculable] = []

    def add(self, employee: ISalaryCalculable) -> None:
        self._storage.append(employee)

    def get_all(self) -> List[ISalaryCalculable]:
        return self._storage

