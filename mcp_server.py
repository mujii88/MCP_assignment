# MCP Todo Server
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import json

# In-memory storage (shared with FastAPI app)
todos: List[Dict[str, Any]] = []
next_id = 1

# ---- MCP Server Setup ----
mcp_server = FastMCP(
    name="todo-mcp-server",
    instructions="A simple MCP server for managing todos with CRUD operations"
)

# ---- MCP Tools ----
@mcp_server.tool()
def get_todos() -> List[Dict[str, Any]]:
    """Get all todos"""
    return todos

@mcp_server.tool()
def create_todo(title: str, description: str = "") -> Dict[str, Any]:
    """Create a new todo"""
    global next_id
    todo = {
        "id": next_id,
        "title": title,
        "description": description,
        "completed": False
    }
    todos.append(todo)
    next_id += 1
    return todo

@mcp_server.tool()
def get_todo(todo_id: int) -> Dict[str, Any]:
    """Get a specific todo by ID"""
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise ValueError(f"Todo with ID {todo_id} not found")

@mcp_server.tool()
def update_todo(todo_id: int, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
    """Update a todo by ID"""
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            if title is not None:
                todo["title"] = title
            if description is not None:
                todo["description"] = description
            if completed is not None:
                todo["completed"] = completed
            return todo
    raise ValueError(f"Todo with ID {todo_id} not found")

@mcp_server.tool()
def delete_todo(todo_id: int) -> Dict[str, Any]:
    """Delete a todo by ID"""
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            return todos.pop(i)
    raise ValueError(f"Todo with ID {todo_id} not found")

@mcp_server.tool()
def complete_todo(todo_id: int) -> Dict[str, Any]:
    """Mark a todo as completed"""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = True
            return todo
    raise ValueError(f"Todo with ID {todo_id} not found")

# ---- MCP Resources ----
@mcp_server.resource("todos://all")
def get_all_todos_resource() -> str:
    """Resource that returns all todos as JSON"""
    return json.dumps(todos, indent=2)

@mcp_server.resource("todos://completed")
def get_completed_todos_resource() -> str:
    """Resource that returns only completed todos as JSON"""
    completed = [todo for todo in todos if todo["completed"]]
    return json.dumps(completed, indent=2)

@mcp_server.resource("todos://pending")
def get_pending_todos_resource() -> str:
    """Resource that returns only pending todos as JSON"""
    pending = [todo for todo in todos if not todo["completed"]]
    return json.dumps(pending, indent=2)

if __name__ == "__main__":
    # Run the MCP server
    mcp_server.run(transport="sse")
