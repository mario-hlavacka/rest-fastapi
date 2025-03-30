
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, SQLModel, create_engine, select
from typing import Annotated

from external_api import get_external_post, is_valid_user
from models import Post, PostUpdate


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/posts/")
async def create_post(post: PostUpdate, session: SessionDep) -> Post:
    if not is_valid_user(post.user_id):
        raise HTTPException(status_code=404, detail='User not found')

    post = Post(user_id=post.user_id, title=post.title, body=post.body)

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@app.get("/posts/{post_id}")
async def read_post(post_id: int, session: SessionDep) -> Post:
    post = session.get(Post, post_id)

    if not post:
        post = get_external_post(post_id)

        if not post:
            raise HTTPException(status_code=404, detail='Post not found')

        session.add(post)
        session.commit()
        session.refresh(post)

    return post


@app.get("/posts")
async def read_posts(user_id: int, session: SessionDep) -> list[Post]:
    if user_id is None:
        raise HTTPException(status_code=404, detail='user_id has not been provided')

    statement = select(Post).where(Post.user_id == user_id)
    posts = session.exec(statement)

    return [ post for post in posts ]


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    
    session.delete(post)
    session.commit()

    return {'message': 'Post has been successfully deleted'}


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post_updated: PostUpdate, session: SessionDep):
    if not is_valid_user(post_updated.user_id):
        raise HTTPException(status_code=404, detail='User not found')

    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')

    post.user_id = post_updated.user_id
    post.title = post_updated.title
    post.body = post_updated.body
    session.commit()

    return {'message': 'Post has been successfully updated'}
