from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TaskCreate(BaseModel):
    title: str
    priority: str


class TaskUpdate(BaseModel):
    title: str
    priority: str


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    user_id: int

    class Config:
        from_attributes = True