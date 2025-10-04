# FastAPI Todo Server with MCP Integration
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import subprocess
import threading
import time
from contextlib import asynccontextmanager

# Import shared data from MCP server
from mcp_server import todos, next_id

# ---- Todo Schema ----
class Todo(BaseModel):
    id: int
    title: str
    description: str = ""
    completed: bool = False

# ---- FastAPI App ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting MCP server in background...")
    # Start MCP server as a subprocess
    mcp_process = subprocess.Popen([
        "python", "mcp_server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"MCP server started with PID: {mcp_process.pid}")
    yield
    # Shutdown
    print("Shutting down MCP server...")
    mcp_process.terminate()
    mcp_process.wait()

app = FastAPI(
    title="Todo MCP Server", 
    description="A FastAPI app with MCP integration for todo management",
    lifespan=lifespan
)

# Regular FastAPI routes for direct API access
@app.get("/todos/")
def get_todos_api():
    return todos

class TodoCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

@app.post("/todos/")
def create_todo_api(todo: TodoCreate):
    global next_id
    todo_dict = {
        "id": next_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed
    }
    todos.append(todo_dict)
    next_id += 1
    return todo_dict

@app.get("/todos/{todo_id}")
def get_todo_api(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}")
def update_todo_api(todo_id: int, updated_todo: Todo):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todo["title"] = updated_todo.title
            todo["description"] = updated_todo.description
            todo["completed"] = updated_todo.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo_api(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            return todos.pop(i)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/")
def root():
    return {
        "message": "Todo MCP Server",
        "mcp_server": "Running on separate process",
        "api_docs": "/docs",
        "todos_api": "/todos/",
        "mcp_tools": [
            "get_todos", "create_todo", "get_todo", 
            "update_todo", "delete_todo", "complete_todo"
        ],
        "mcp_resources": [
            "todos://all", "todos://completed", "todos://pending"
        ]
    }

# Run with: uvicorn main:app --reload
