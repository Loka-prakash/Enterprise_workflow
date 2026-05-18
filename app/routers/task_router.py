from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.task import Task

from app.models.user import User

from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskAssign
)

from app.dependencies import get_current_user

from app.middleware.role_checker import (
    role_required
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    role_required(
        current_user["role"],
        ["admin", "manager"]
    )

    assigned_user = db.query(User).filter(
        User.id == task.assigned_to_id
    ).first()

    if not assigned_user:

        raise HTTPException(
            status_code=404,
            detail="Assigned user not found"
        )

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        assigned_to_id=task.assigned_to_id,
        created_by_id=current_user["user_id"]
    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return {
        "message": "Task created successfully"
    }


@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] == "admin":

        tasks = db.query(Task).all()

    elif current_user["role"] == "manager":

        tasks = db.query(Task).filter(
            Task.created_by_id == current_user["user_id"]
        ).all()

    else:

        tasks = db.query(Task).filter(
            Task.assigned_to_id == current_user["user_id"]
        ).all()

    return tasks


@router.put("/{task_id}")
def update_task(
    task_id: int,
    updated_task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if current_user["role"] == "employee":

        raise HTTPException(
            status_code=403,
            detail="Employees cannot update tasks"
        )

    for key, value in updated_task.dict(
        exclude_unset=True
    ).items():

        setattr(task, key, value)

    db.commit()

    return {
        "message": "Task updated successfully"
    }


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    role_required(
        current_user["role"],
        ["admin"]
    )

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)

    db.commit()

    return {
        "message": "Task deleted successfully"
    }


@router.patch("/{task_id}/assign")
def assign_task(
    task_id: int,
    data: TaskAssign,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    role_required(
        current_user["role"],
        ["admin", "manager"]
    )

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    user = db.query(User).filter(
        User.id == data.assigned_to_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    task.assigned_to_id = data.assigned_to_id

    db.commit()

    return {
        "message": "Task assigned successfully"
    }