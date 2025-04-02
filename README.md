# rest-fastapi
Python version used - 3.13.2

## Installation:
1. Create virtual environment `python -m venv .venv`
2. Activate virtual environment (win) `.venv\Scripts\activate.bat`
3. Install required dependencies `pip install -r requirements.txt`
4. Run the API `fastapi dev main.py`

Once the API is running, you can access the documentation at localhost:8000/docs


## Task

Create a microservice in Python that will provide a RESTful API for managing user posts. The post format is as follows:
- id: integer
- user_id: integer
- title: string
- body: string

### Functional Requirements:
- Add a post - the user_id must be validated using an external API.
- View a post:
    - Based on id or user_id.
    - If the post is not found in the system, it must be fetched from an external API and saved (only for searching by post id).
- Delete a post.
- Edit a post - the ability to change the title and body.

The external API can be found at the link https://jsonplaceholder.typicode.com/ - use the users and posts endpoints.

### General Requirements:
- README with installation instructions and the first run guide.
- API documentation (e.g., Swagger).
- Input data validation.
- Use of ORM.

### The solution should demonstrate the ability to work with (the more, the better):
- ORM
- REST
- Third-party API integration
- Input validation
- Error handling
- Proper structuring of source code

Optional Tasks:
- Provide not only the API but also a simple frontend that supports these features.
- Containerization (e.g., with Docker).

When coding, focus primarily on clean code, using proper design patterns, styles, functions, and principles of the language.