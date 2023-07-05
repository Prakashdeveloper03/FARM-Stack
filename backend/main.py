from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Todo
from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/todo")
async def get_todo():
    """
    Get all todos.

    Returns:
        List[Dict]: List of all todos.
    """
    response = await fetch_all_todos()
    return response


@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title: str):
    """
    Get a specific todo by title.

    Args:
        title (str): Title of the todo.

    Returns:
        Todo: Todo item with the given title.

    Raises:
        HTTPException: If no todo is found with the given title (status code 404).
    """
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.post("/api/todo/", response_model=Todo)
async def post_todo(todo: Todo):
    """
    Create a new todo.

    Args:
        todo (Todo): Todo item to be created.

    Returns:
        Todo: Newly created todo item.

    Raises:
        HTTPException: If something goes wrong during creation (status code 400).
    """
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")


@app.put("/api/todo/{title}/", response_model=Todo)
async def put_todo(title: str, desc: str):
    """
    Update a todo's description by title.

    Args:
        title (str): Title of the todo.
        desc (str): New description for the todo.

    Returns:
        Todo: Updated todo item.

    Raises:
        HTTPException: If no todo is found with the given title (status code 404).
    """
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.delete("/api/todo/{title}")
async def delete_todo(title: str):
    """
    Delete a todo by title.

    Args:
        title (str): Title of the todo to be deleted.

    Returns:
        str: Success message if the deletion is successful.

    Raises:
        HTTPException: If no todo is found with the given title (status code 404).
    """
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {title}")
