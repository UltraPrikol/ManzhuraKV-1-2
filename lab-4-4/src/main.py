from src.core.company import Company
from src.core.department import Department
from src.core.project import Project
from src.core.abstract_employee import Manager, Developer, Salesperson
from src.utils.exceptions import *

def main():
    print("=== 1. Creating Company Structure ===")
    company = Company("TechInnovations")
    
    dev_department = Department("Development", "DEV")
    sales_department = Department("Sales", "SAL")
    
    company.add_department(dev_department)
    company.add_department(sales_department)
    
    manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
    dev1 = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
    dev2 = Developer(3, "Eve Hacker", "DEV", 5200, ["Java", "Spring"], "senior")
    salesperson = Salesperson(4, "Charlie Brown", "SAL", 4000, 0.15, 50000)

    dev_department.add_employee(manager)
    dev_department.add_employee(dev1)
    dev_department.add_employee(dev2)
    sales_department.add_employee(salesperson)
    
    print(f"Total Employees: {len(company.get_all_employees())}")

    print("\n=== 2. Managing Projects (Composition) ===")
    ai_project = Project(101, "AI Platform", "AI System", "2024-12-31", "active")
    web_project = Project(102, "Web Portal", "Web Site", "2024-09-30", "active")
    
    company.add_project(ai_project)
    company.add_project(web_project)

    ai_project.add_team_member(dev1) # Bob
    ai_project.add_team_member(manager) # Alice

    web_project.add_team_member(dev1) # Bob
    web_project.add_team_member(dev2) # Eve
    
    print(f"AI Project Cost: ${ai_project.calculate_total_salary()}")

    print("\n=== 3. Validation & Dependency Management ===")
    try:
        ai_project.add_team_member(dev1)
    except DuplicateIdError as e:
        print(f"caught expected error: {e}")
    try:
        company.remove_department("DEV")
    except DeletionError as e:
        print(f"Caught expected error: {e}")
    try:
        company.remove_project(101)
    except DeletionError as e:
        print(f"Caught expected error: {e}")

    print("\n=== 4. Analysis & Stats ===")
    print(f"Total Monthly Cost: ${company.calculate_total_monthly_cost()}")
    
    overloaded = company.find_overloaded_employees()
    print("Overloaded Employees (Active in >1 projects):")
    for emp in overloaded:
        print(f"- {emp.name} (ID: {emp.emp_id})")

    print("\n=== 5. Serialization & Export ===")
    company.save_to_json("company_data.json")
    print("Company saved to JSON.")
    
    company.export_employees_csv("employees_report.csv")
    print("Employee CSV exported.")

    print("\n=== 6. Restoration ===")
    loaded_company = Company.load_from_json("company_data.json")
    print(f"Loaded Company: {loaded_company.name}")
    print(f"Loaded Employees: {len(loaded_company.get_all_employees())}")
    print(f"Loaded Projects: {len(loaded_company._Company__projects)}") 

    p = loaded_company._Company__projects[0]
    print(f"Project '{p.name}' team size: {p.get_team_size()}")

if __name__ == "__main__":
    main()