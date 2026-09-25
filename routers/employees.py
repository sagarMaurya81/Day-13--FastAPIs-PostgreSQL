from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    status
)

from sqlalchemy.orm import Session

from database.db import get_db

from schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeePartialUpdate,
    EmployeeResponse
)

from services.employee import (
    create_employee,
    get_employees,
    get_employee,
    update_employee,
    update_employee_partial,
    delete_employee
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# =========================================================
# CREATE EMPLOYEE
# =========================================================

@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create employee"
)
def create_employee_api(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    try:

        return create_employee(
            db=db,
            employee_data=employee_data
        )

    except ValueError as e:

        message = str(e)

        if "already exists" in message:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


# =========================================================
# GET EMPLOYEES
# =========================================================

@router.get(
    "/",
    response_model=list[EmployeeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get employees"
)
def get_all_employees(
    department: str | None = Query(
        default=None,
        min_length=2,
        max_length=100,
        description="Filter employees by department"
    ),

    search: str | None = Query(
        default=None,
        min_length=2,
        max_length=100,
        description="Search by first name, last name or email"
    ),

    db: Session = Depends(get_db)
):

    try:

        return get_employees(
            db=db,
            department=department,
            search=search
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =========================================================
# GET EMPLOYEE BY ID
# =========================================================

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get employee by ID"
)
def get_employee_api(
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    ),

    db: Session = Depends(get_db)
):

    try:

        employee = get_employee(
            db=db,
            employee_id=employee_id
        )

        if employee is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        return employee

    except HTTPException:
        raise

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =========================================================
# FULL UPDATE
# =========================================================

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Full update employee"
)
def update_employee_api(
    employee_data: EmployeeUpdate,

    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    ),

    db: Session = Depends(get_db)
):

    employee = get_employee(
        db=db,
        employee_id=employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    try:

        return update_employee(
            db=db,
            employee=employee,
            employee_data=employee_data
        )

    except ValueError as e:

        message = str(e)

        if "already exists" in message:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


# =========================================================
# PARTIAL UPDATE
# =========================================================

@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Partial update employee"
)
def partial_update_employee_api(
    employee_data: EmployeePartialUpdate,

    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    ),

    db: Session = Depends(get_db)
):

    employee = get_employee(
        db=db,
        employee_id=employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    try:

        return update_employee_partial(
            db=db,
            employee=employee,
            employee_data=employee_data
        )

    except ValueError as e:

        message = str(e)

        if "already exists" in message:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


# =========================================================
# DELETE
# =========================================================

@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete employee"
)
def delete_employee_api(
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    ),

    db: Session = Depends(get_db)
):

    employee = get_employee(
        db=db,
        employee_id=employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    try:

        delete_employee(
            db=db,
            employee=employee
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    return None