from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import Comment, Project, ProjectMembership, Skill, Task, User
from app.db.session import get_db
from app.schemas.entities import (
    CommentCreate,
    CommentResponse,
    LoginRequest,
    MembershipCreate,
    MembershipResponse,
    PasswordChangeRequest,
    ProjectCreate,
    ProjectResponse,
    SkillCreate,
    SkillResponse,
    TaskCreate,
    TaskResponse,
    TokenResponse,
    UserCreate,
    UserResponse,
)

router = APIRouter()


@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    existing_user = db.scalar(select(User).where(User.email == payload.email))
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong email or password")
    return TokenResponse(access_token=create_access_token(user.id))


@router.get("/users/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[User]:
    return list(db.scalars(select(User).order_by(User.id)).all())


@router.post("/users/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    if not verify_password(payload.old_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
    current_user.password_hash = hash_password(payload.new_password)
    db.commit()


@router.post("/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(payload: SkillCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> Skill:
    skill = Skill(title=payload.title)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.get("/skills", response_model=list[SkillResponse])
def list_skills(db: Session = Depends(get_db)) -> list[Skill]:
    return list(db.scalars(select(Skill).order_by(Skill.id)).all())


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> Project:
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)) -> list[Project]:
    return list(db.scalars(select(Project).order_by(Project.id)).all())


@router.post("/projects/{project_id}/memberships", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
def add_membership(
    project_id: int,
    payload: MembershipCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ProjectMembership:
    project = db.get(Project, project_id)
    user = db.get(User, payload.user_id)
    skill = db.get(Skill, payload.skill_id)
    if not project or not user or not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project, user or skill not found")

    membership = ProjectMembership(
        project_id=project_id,
        user_id=payload.user_id,
        skill_id=payload.skill_id,
        role=payload.role,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get("/projects/{project_id}/memberships", response_model=list[MembershipResponse])
def list_memberships(project_id: int, db: Session = Depends(get_db)) -> list[ProjectMembership]:
    return list(
        db.scalars(
            select(ProjectMembership).where(ProjectMembership.project_id == project_id).order_by(ProjectMembership.id)
        ).all()
    )


@router.post("/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Task:
    if db.get(Project, project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if payload.assignee_id is not None and db.get(User, payload.assignee_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignee not found")

    task = Task(
        title=payload.title,
        details=payload.details,
        project_id=project_id,
        assignee_id=payload.assignee_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/projects/{project_id}/tasks", response_model=list[TaskResponse])
def list_tasks(project_id: int, db: Session = Depends(get_db)) -> list[Task]:
    return list(db.scalars(select(Task).where(Task.project_id == project_id).order_by(Task.id)).all())


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    task_id: int,
    payload: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Comment:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    comment = Comment(body=payload.body, task_id=task_id, author_id=current_user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def list_comments(task_id: int, db: Session = Depends(get_db)) -> list[Comment]:
    return list(db.scalars(select(Comment).where(Comment.task_id == task_id).order_by(Comment.id)).all())
