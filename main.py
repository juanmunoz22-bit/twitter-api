#Python
import json
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

#Pydantic
from pydantic import BaseModel, EmailStr, Field

#FastAPI
from fastapi import FastAPI, status, Body

app = FastAPI()

#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    birth_date: Optional[date] = Field(default=None)


class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
        )
    by: User = Field(...)

class CreateTweet(Tweet):
    created: datetime = Field(default=datetime.now())

class UpdateTweet(Tweet):
    updated: Optional[datetime] = Field(default=None)
# Path Ops


## Users

@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Register an User',
    tags=['User']
    )
def signup(
    user: UserRegister = Body(...)
    ):
    """
    **Signup**

    This path operation register a user in the app

    Parameters:
    - Request body parameter
        - user: UserRegister

    Returns a json with user's basic information:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    with open('users.json', 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Login an user',
    tags=['User']
    )
def login():
    pass

@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Show all users',
    tags=['User']
    )
def show_users():
    '''
    **Get Users**

    This path operation shows all users created in the app

    Parameters: None

    Returns a list with the basic user information of all users created in the app:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: date
    '''
    with open('users.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        return results

@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Show an user',
    tags=['User']
    )
def show_user():
    pass

@app.delete(
    path='/users/{user_id}/delete',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Delete an user',
    tags=['User']
    )
def delete_user():
    pass

@app.put(
    path='/users/{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update an user',
    tags=['User']
    )
def update_user():
    pass

## Tweets

@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='Show all tweets',
    tags=['Tweet'])
def home():
    with open('tweets.json', 'r', encoding='utf-8') as f:
        results = json.loads(f.read())
        return results


@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Post a tweet',
    tags=['Tweet']
    )
def post_tweet(
    tweet: CreateTweet = Body(...)
):
    """
    Post a Tweet

    This path operations post a tweet in the app

    Parameters:
    - Request body parameter
        - tweet: Tweet

    Return a json with the basic tweet information:
    - tweet_id: UUID
    - content:str
    - created: datetime
    - by: User
    """
    with open('tweets.json', 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created'] = str(tweet_dict['created'])
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict['by']['birth_date'])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a tweet',
    tags=['Tweet']
    )
def show_tweet():
    pass


@app.delete(
    path='/tweets/{tweet_id}/delete',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Delete a tweet',
    tags=['Tweet']
)
def delete_tweet():
    pass


@app.put(
    path='/tweets/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Update a tweet',
    tags=['Tweet']
)
def update_tweet():
    pass