def transform_employee(record):

    employee_id = int(record["id"])
    name = record["name"].strip().title()
    salary = int(record["salary"])
    department = record["department"].strip().upper()

    if not name:
        raise ValueError("Employee name is empty")

    if salary < 0:
        raise ValueError("Salary cannot be negative")

    annual_salary = salary * 12

    return {
        "id": employee_id,
        "name": name,
        "salary": salary,
        "department": department,
        "annual_salary": annual_salary
    }