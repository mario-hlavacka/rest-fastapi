from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    title: str = Field()
    body: str = Field()

class PostUpdate(SQLModel):
    user_id: int
    title: str
    body: str