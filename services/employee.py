from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeePartialUpdate
)

from models.employee import Employee


# =========================================================
# DATABASE VALIDATION
# =========================================================

def validate_unique_employee(
    db: Session,
    email: str | None = None,
    phone_number: str | None = None,
    exclude_employee_id: int | None = None
) -> None:

    # -----------------------------------------------------
    # Email validation
    # -----------------------------------------------------

    if email is not None:

        query = db.query(Employee).filter(
            Employee.email == email
        )

        if exclude_employee_id is not None:

            query = query.filter(
                Employee.employee_id != exclude_employee_id
            )

        existing_employee = query.first()

        if existing_employee:

            raise ValueError(
                "Email already exists"
            )

    # -----------------------------------------------------
    # Phone validation
    # -----------------------------------------------------

    if phone_number is not None:

        query = db.query(Employee).filter(
            Employee.phone_number == phone_number
        )

        if exclude_employee_id is not None:

            query = query.filter(
                Employee.employee_id != exclude_employee_id
            )

        existing_employee = query.first()

        if existing_employee:

            raise ValueError(
                "Phone number already exists"
            )


# =========================================================
# CREATE
# =========================================================

def create_employee(
    db: Session,
    employee_data: EmployeeCreate
) -> Employee:

    email = str(employee_data.email)

    # Database validation
    validate_unique_employee(
        db=db,
        email=email,
        phone_number=employee_data.phone_number
    )

    employee = Employee(
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=email,
        phone_number=employee_data.phone_number,
        department=employee_data.department
    )

    try:

        db.add(employee)

        db.commit()

        db.refresh(employee)

        return employee

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Email or phone number already exists"
        ) from e

    except SQLAlchemyError as e:

        db.rollback()

        raise ValueError(
            "Database error while creating employee"
        ) from e


# =========================================================
# GET ALL EMPLOYEES
# =========================================================

def get_employees(
    db: Session,
    department: str | None = None,
    search: str | None = None
) -> list[Employee]:

    try:

        # Start query
        query = db.query(Employee)

        # -------------------------------------------------
        # Department filter
        #
        # GET /employees?department=IT
        # -------------------------------------------------

        if department:

            query = query.filter(
                Employee.department.ilike(department)
            )

        # -------------------------------------------------
        # Search filter
        #
        # GET /employees?search=rahul
        #
        # Searches:
        # first_name
        # last_name
        # email
        # -------------------------------------------------

        if search:

            search_value = f"%{search}%"

            query = query.filter(
                (Employee.first_name.ilike(search_value))
                |
                (Employee.last_name.ilike(search_value))
                |
                (Employee.email.ilike(search_value))
            )

        # -------------------------------------------------
        # Return employees
        # -------------------------------------------------

        return (
            query
            .order_by(Employee.employee_id)
            .all()
        )

    except SQLAlchemyError as e:

        raise ValueError(
            "Database error while fetching employees"
        ) from e


# =========================================================
# GET ONE EMPLOYEE
# =========================================================

def get_employee(
    db: Session,
    employee_id: int
) -> Employee | None:

    try:

        return (
            db.query(Employee)
            .filter(
                Employee.employee_id == employee_id
            )
            .first()
        )

    except SQLAlchemyError as e:

        raise ValueError(
            "Database error while fetching employee"
        ) from e


# =========================================================
# FULL UPDATE
# =========================================================

def update_employee(
    db: Session,
    employee: Employee,
    employee_data: EmployeeUpdate
) -> Employee:

    email = str(employee_data.email)

    # Validate unique email and phone
    # Exclude current employee

    validate_unique_employee(
        db=db,
        email=email,
        phone_number=employee_data.phone_number,
        exclude_employee_id=employee.employee_id
    )

    # -----------------------------------------------------
    # Update fields
    # -----------------------------------------------------

    employee.first_name = employee_data.first_name

    employee.last_name = employee_data.last_name

    employee.email = email

    employee.phone_number = employee_data.phone_number

    employee.department = employee_data.department

    try:

        db.commit()

        db.refresh(employee)

        return employee

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Email or phone number already exists"
        ) from e

    except SQLAlchemyError as e:

        db.rollback()

        raise ValueError(
            "Database error while updating employee"
        ) from e


# =========================================================
# PARTIAL UPDATE
# =========================================================

def update_employee_partial(
    db: Session,
    employee: Employee,
    employee_data: EmployeePartialUpdate
) -> Employee:

    # Get only fields provided by client
    update_data = employee_data.model_dump(
        exclude_unset=True
    )

    # -----------------------------------------------------
    # Check empty PATCH request
    # -----------------------------------------------------

    if not update_data:

        raise ValueError(
            "At least one field is required for update"
        )

    # -----------------------------------------------------
    # Email validation
    # -----------------------------------------------------

    if "email" in update_data:

        email = update_data["email"]

        if email is not None:

            email = str(email)

            validate_unique_employee(
                db=db,
                email=email,
                exclude_employee_id=employee.employee_id
            )

            update_data["email"] = email

    # -----------------------------------------------------
    # Phone validation
    # -----------------------------------------------------

    if "phone_number" in update_data:

        phone_number = update_data["phone_number"]

        if phone_number is not None:

            validate_unique_employee(
                db=db,
                phone_number=phone_number,
                exclude_employee_id=employee.employee_id
            )

    # -----------------------------------------------------
    # Update only provided fields
    # -----------------------------------------------------

    for field, value in update_data.items():

        setattr(
            employee,
            field,
            value
        )

    try:

        db.commit()

        db.refresh(employee)

        return employee

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Email or phone number already exists"
        ) from e

    except SQLAlchemyError as e:

        db.rollback()

        raise ValueError(
            "Database error while partially updating employee"
        ) from e


# =========================================================
# DELETE
# =========================================================

def delete_employee(
    db: Session,
    employee: Employee
) -> None:

    try:

        db.delete(employee)

        db.commit()

    except IntegrityError as e:

        db.rollback()

        raise ValueError(
            "Employee cannot be deleted because "
            "related records exist"
        ) from e

    except SQLAlchemyError as e:

        db.rollback()

        raise ValueError(
            "Database error while deleting employee"
        ) from e