import motor.motor_asyncio
from model import Todo

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
database = client.TodoList
collection = database.todo


async def fetch_one_todo(title: str):
    """
    Fetch a todo by title.

    Args:
        title (str): Title of the todo to be fetched.

    Returns:
        dict: Todo document from the database if found, None otherwise.
    """
    document = await collection.find_one({"title": title})
    return document


async def fetch_all_todos():
    """
    Fetch all todos.

    Returns:
        List[Todo]: List of all todo objects from the database.
    """
    todos = []
    cursor = collection.find({})
    async for document in cursor:
        todos.append(Todo(**document))
    return todos


async def create_todo(todo: dict):
    """
    Create a new todo.

    Args:
        todo (dict): Dictionary representation of the todo to be created.

    Returns:
        dict: Created todo document from the database.
    """
    document = todo
    result = await collection.insert_one(document)
    return document


async def update_todo(title: str, desc: str):
    """
    Update a todo's description by title.

    Args:
        title (str): Title of the todo to be updated.
        desc (str): New description for the todo.

    Returns:
        dict: Updated todo document from the database.
    """
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    return document


async def remove_todo(title: str):
    """
    Remove a todo by title.

    Args:
        title (str): Title of the todo to be removed.

    Returns:
        bool: True if the deletion is successful.

    """
    await collection.delete_one({"title": title})
    return True
