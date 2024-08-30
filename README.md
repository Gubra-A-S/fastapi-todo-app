# FastAPI Todo Application

![Python 3](https://img.shields.io/badge/Python-3-green.svg?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009485?style=for-the-badge&logo=fastapi&logoColor=white)

This is a basic API for a todo application made with FastAPI. You can use any frontend framework with this. I am using SQLite in this project. Other databases can also be used easily. <a href="https://fastapi.tiangolo.com/tutorial/sql-databases/">Refer to this</a> for more information on how to use other databases with FastAPI.

## Clone the project

```
git clone https://github.com/Gubra-A-S/fastapi-todo-app.git
```

## Run locally

Running locally requires python3 and pip

### Install dependencies

```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Start server

```
uvicorn main:app --reload
```

Track changes is enabled, so the server is automatically restarted whenever the code is updated.

## Run with docker

### Run server

```
docker compose up --build
```

Track changes is enabled, so the server is automatically restarted whenever the code is updated.

## API endpoints:

- Get all the todo items present in the database, send a get request on the following endpoint:

```
http://127.0.0.1:8000/todos
```

- To post a todo item in the database, send a post request on the following endpoint:

```
http://127.0.0.1:8000/todos
```

- To update a specific todo item as completed/pending, send a put request on the following endpoint:

```
http://127.0.0.1:8000/todos/<todoItemID>
```

For further details, you can refer to <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a> after starting the server. It will give you an auto generated and very detailed documentation.

### Changes Made in this Fork

**Authorization**

- A security layer has been added to the endpoints, requiring a JWT token generated via a unique username and password.

**Token Generation Endpoint**

- A POST action has been created on the `/token` endpoint, allowing for session validation and tokenization. The session will be stored in the local storage managed by the Front End.

**Unique Username and Password**

- A general username and password are registered in the `.env` file. These can be easily changed directly in the file.

**API Data Access**

- To verify the data, you can use Postman with the endpoint `http://127.0.0.1:8000/todos`, adding the Bearer Token in the authorization tab with the session token.

- The session token can be obtained using Postman or http://127.0.0.1:8000/docs by making a POST request to the endpoint `http://127.0.0.1:8000/token`, including the following JSON in the Body:

  ```json
  {
    "username": "*******",
    "password": "*******"
  }
