from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


class SkillCreate(BaseModel):
    title: str


class SkillResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    description: str


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True


class MembershipCreate(BaseModel):
    user_id: int
    skill_id: int
    role: str


class MembershipResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    skill_id: int
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    details: str
    assignee_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    details: str
    project_id: int
    assignee_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    body: str


class CommentResponse(BaseModel):
    id: int
    body: str
    task_id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
