#!/usr/bin/env python3
"""
Test script to demonstrate MCP server functionality
"""
import json
from mcp_server import todos

def test_todo_operations():
    """Test the todo operations directly"""
    print("=== Testing Todo Operations ===")
    
    # Test creating todos
    print("\n1. Creating todos...")
    todo1 = {
        "id": 1,
        "title": "Learn MCP",
        "description": "Study Model Context Protocol",
        "completed": False
    }
    todos.append(todo1)
    
    todo2 = {
        "id": 2,
        "title": "Build API",
        "description": "Create FastAPI integration",
        "completed": False
    }
    todos.append(todo2)
    
    print(f"Created todo 1: {json.dumps(todo1, indent=2)}")
    print(f"Created todo 2: {json.dumps(todo2, indent=2)}")
    
    # Test getting all todos
    print("\n2. Getting all todos...")
    print(f"All todos: {json.dumps(todos, indent=2)}")
    
    # Test updating todo
    print("\n3. Updating todo 1...")
    for todo in todos:
        if todo["id"] == 1:
            todo["completed"] = True
            break
    print(f"Updated todo 1: {json.dumps(todo, indent=2)}")
    
    # Test filtering completed todos
    print("\n4. Completed todos:")
    completed = [todo for todo in todos if todo["completed"]]
    print(f"Completed: {json.dumps(completed, indent=2)}")
    
    # Test filtering pending todos
    print("\n5. Pending todos:")
    pending = [todo for todo in todos if not todo["completed"]]
    print(f"Pending: {json.dumps(pending, indent=2)}")
    
    print("\n=== MCP Server Information ===")
    print("MCP Server Name: todo-mcp-server")
    print("Available Tools:")
    print("  - get_todos: Get all todos")
    print("  - create_todo: Create a new todo")
    print("  - get_todo: Get a specific todo by ID")
    print("  - update_todo: Update a todo by ID")
    print("  - delete_todo: Delete a todo by ID")
    print("  - complete_todo: Mark a todo as completed")
    print("\nAvailable Resources:")
    print("  - todos://all: All todos as JSON")
    print("  - todos://completed: Completed todos as JSON")
    print("  - todos://pending: Pending todos as JSON")

if __name__ == "__main__":
    print("MCP Server Test")
    print("===============")
    test_todo_operations()
