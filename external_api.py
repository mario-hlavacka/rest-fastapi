import json
import requests

from models import Post


USERS_URL = "https://jsonplaceholder.typicode.com/users/"
POSTS_URL = "https://jsonplaceholder.typicode.com/posts/"


def is_valid_user(user_id: int):
    users = USERS_URL + str(user_id)
    response = requests.get(users)

    return response.status_code == 200

def get_external_post(post_id):
    post_url = POSTS_URL + str(post_id)

    response = make_request(post_url)

    if response.status_code == 200:
        post_dict = json.loads(response.content)
        user_id = post_dict['userId']
        title = post_dict['title']
        body = post_dict['body']

        return Post(user_id=user_id, title=title, body=body)
    return None

def make_request(endpoint_url: str):
    response = requests.get(endpoint_url)

    return response