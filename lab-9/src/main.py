from models import Developer, Manager
from strategies import PerformanceBonusStrategy, SeniorityBonusStrategy
from repositories import InMemoryEmployeeRepository
from services import CompanyService, FinancialCalculator
from utils import Logger, JsonSerializer

def main():
    Logger.log("Starting application refactoring demo...")

    # 1. Setup Dependencies (DIP в действии)
    # Мы создаем зависимости снаружи и "внедряем" их внутрь
    repository = InMemoryEmployeeRepository()
    calculator = FinancialCalculator()
    company_service = CompanyService(repository, calculator)

    # 2. Setup Strategies (OCP в действии)
    # Мы конфигурируем поведение "на лету"
    high_perf_bonus = PerformanceBonusStrategy(percent=0.10, performance_score=9)
    seniority_bonus = SeniorityBonusStrategy(years=5)

    # 3. Create Employees
    dev = Developer(1, "Alice", 5000, bonus_strategy=high_perf_bonus)
    dev.add_skill("Python")
    dev.add_skill("Docker")

    manager = Manager(2, "Bob", 8000, subordinates_count=10, bonus_strategy=seniority_bonus)

    # 4. Use Service
    company_service.hire_employee(dev)
    company_service.hire_employee(manager)

    # 5. Calculate Logic
    total_cost = company_service.get_total_costs()
    
    Logger.log(f"Total Monthly Cost: ${total_cost}")
    
    # 6. Serialization
    print("\nSerialized Developer Data:")
    print(JsonSerializer.to_json(dev))

if __name__ == "__main__":
    main()