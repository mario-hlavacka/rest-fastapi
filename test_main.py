from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, Session, StaticPool, create_engine

from database import get_session
from main import app
from models import Post


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_session] = get_session_override  
    client = TestClient(app)  

    yield client  

    app.dependency_overrides.clear()  


def test_create_post(client: TestClient):
    response = client.post(
        "/posts/",
        json={"user_id": 1, "title": "Bazz", "body": "Drop the bazz"},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["id"] is not None
    assert data["user_id"] == 1
    assert data["title"] == "Bazz"
    assert data["body"] == "Drop the bazz"

def test_create_post_missing_param(client: TestClient):
    response = client.post(
        "/posts/",
        json={"user_id": 2, "body": "Missing title"},
    )

    assert response.status_code == 422

def test_create_post_invalid_user_id(client: TestClient):
    response = client.post(
        "/posts/",
        json={"user_id": 30, "title": "Non existing user", "body": "Test"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
    

def test_read_post(session: Session, client: TestClient):
    post = Post(user_id=3, title="Reading a post", body="Body")
    session.add(post)
    session.commit()
    session.refresh(post)

    response = client.get(f"/posts/{post.id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] is not None
    assert data["user_id"] == 3
    assert data["title"] == "Reading a post"
    assert data["body"] == "Body"

def test_read_post_from_external(client: TestClient):
    response = client.get("/posts/40")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] is not None
    assert data["user_id"] == 4
    assert data["title"] == "enim quo cumque"
    assert data["body"] == "ut voluptatum aliquid illo tenetur nemo sequi quo facilis\nipsum rem optio mollitia quas\nvoluptatem eum voluptas qui\nunde omnis voluptatem iure quasi maxime voluptas nam"

def test_read_post_not_found(client: TestClient):
    response = client.get("/posts/752")

    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
    
def test_read_posts(session: Session, client: TestClient):
    post1 = Post(user_id=3, title="Getting post list", body="For user who has id=3")
    post2 = Post(user_id=3, title="2nd post", body="For user who has id=3")
    session.add(post1)
    session.add(post2)
    session.commit()
    session.refresh(post1)
    session.refresh(post2)

    response = client.get(f"/posts?user_id=3")

    assert response.status_code == 200
    assert response.json() == [
        {"id": post1.id, "user_id": 3, "title": "Getting post list", "body": "For user who has id=3"},
        {"id": post2.id, "user_id": 3, "title": "2nd post", "body": "For user who has id=3"}
    ]

def test_read_posts_empty(client: TestClient):
    response = client.get(f"/posts?user_id=17")

    assert response.status_code == 200
    assert response.json() == []

def test_delete_post(session: Session, client: TestClient):
    post = Post(user_id=5, title="Deleting a post", body="Random text")
    session.add(post)
    session.commit()
    session.refresh(post)

    response = client.delete(f"/posts/{post.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Post has been successfully deleted"}

def test_delete_post_not_found(client: TestClient):
    response = client.delete("/posts/1501")

    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

def test_update_post(session: Session, client: TestClient):
    post = Post(user_id=5, title="Updating post...", body="Random")
    session.add(post)
    session.commit()
    session.refresh(post)

    response = client.put(
        f"/posts/{post.id}",
        json={"user_id": 10, "title": "Updating post...", "body": "qwerty  "}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Post has been successfully updated"}

def test_update_post_missing_param(session: Session, client: TestClient):
    post = Post(user_id=3, title="Updating post", body="1234 5")
    session.add(post)
    session.commit()
    session.refresh(post)

    response = client.put(
        f"/posts/{post.id}",
        json={"title": "Missing User ID", "body": "ABC"}
    )

    assert response.status_code == 422

def test_update_post_invalid_user_id(session: Session, client: TestClient):
    post = Post(user_id=7, title="Updating post again", body="Body")
    session.add(post)
    session.commit()
    session.refresh(post)

    response = client.put(
        f"/posts/{post.id}",
        json={"user_id": 20, "title": "QWERTY", "body": "Invalid user ID"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_update_post_not_found(client: TestClient):
    response = client.put(
        "/posts/1510",
        json={"user_id": 2, "title": "Non existent post", "body": "Test"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}