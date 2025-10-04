# MCP Todo Server with FastAPI Integration

This project demonstrates how to create a Model Context Protocol (MCP) server and integrate it with a FastAPI application for todo management.

## Features

### MCP Server (`mcp_server.py`)
- **Tools**: 6 MCP tools for todo management
  - `get_todos`: Get all todos
  - `create_todo`: Create a new todo
  - `get_todo`: Get a specific todo by ID
  - `update_todo`: Update a todo by ID
  - `delete_todo`: Delete a todo by ID
  - `complete_todo`: Mark a todo as completed

- **Resources**: 3 MCP resources for data access
  - `todos://all`: All todos as JSON
  - `todos://completed`: Completed todos as JSON
  - `todos://pending`: Pending todos as JSON

### FastAPI Server (`main.py`)
- **REST API**: Full CRUD operations for todos
- **MCP Integration**: Runs MCP server as a subprocess
- **Shared Data**: Both servers share the same todo data
- **API Documentation**: Auto-generated Swagger docs at `/docs`

## Project Structure

```
assignment/
├── main.py              # FastAPI application
├── mcp_server.py        # MCP server implementation
├── test_mcp.py         # Test script for MCP functionality
├── README.md           # This documentation
└── venv/               # Virtual environment
```

## Installation

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies (already installed):**
   ```bash
   pip install fastapi uvicorn mcp
   ```

## Running the Application

### Option 1: Run FastAPI with MCP Integration
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

This will:
- Start the FastAPI server on port 8000
- Automatically start the MCP server as a subprocess
- Provide both REST API and MCP functionality

### Option 2: Run MCP Server Standalone
```bash
python mcp_server.py
```

This will start only the MCP server using SSE transport.

## API Endpoints

### FastAPI REST Endpoints

- `GET /` - Server information and available tools/resources
- `GET /todos/` - Get all todos
- `POST /todos/` - Create a new todo
- `GET /todos/{todo_id}` - Get a specific todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo
- `GET /docs` - API documentation (Swagger UI)

### MCP Tools

The MCP server provides the following tools:

1. **get_todos()** - Returns all todos
2. **create_todo(title, description="")** - Creates a new todo
3. **get_todo(todo_id)** - Gets a specific todo by ID
4. **update_todo(todo_id, title=None, description=None, completed=None)** - Updates a todo
5. **delete_todo(todo_id)** - Deletes a todo
6. **complete_todo(todo_id)** - Marks a todo as completed

### MCP Resources

The MCP server provides the following resources:

1. **todos://all** - All todos as JSON
2. **todos://completed** - Only completed todos as JSON
3. **todos://pending** - Only pending todos as JSON

## Usage Examples

### Using the REST API

```bash
# Get all todos
curl http://localhost:8000/todos/

# Create a new todo
curl -X POST "http://localhost:8000/todos/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn MCP", "description": "Study Model Context Protocol", "completed": false}'

# Get a specific todo
curl http://localhost:8000/todos/1

# Update a todo
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn MCP", "description": "Study Model Context Protocol", "completed": true}'

# Delete a todo
curl -X DELETE http://localhost:8000/todos/1
```

### Using MCP Tools

```python
from mcp_server import mcp_server

# Create a todo
todo = mcp_server.tools["create_todo"].func("Learn MCP", "Study MCP protocol")

# Get all todos
all_todos = mcp_server.tools["get_todos"].func()

# Complete a todo
completed = mcp_server.tools["complete_todo"].func(1)
```

### Testing the Implementation

Run the test script to see the MCP functionality in action:

```bash
python test_mcp.py
```

## Architecture

The application uses a hybrid architecture:

1. **FastAPI Server**: Provides REST API endpoints for direct HTTP access
2. **MCP Server**: Provides Model Context Protocol tools and resources
3. **Shared Data**: Both servers share the same in-memory todo storage
4. **Process Management**: FastAPI manages the MCP server as a subprocess

## Key Benefits

- **Dual Interface**: Both REST API and MCP protocol access
- **Shared State**: Data consistency between both interfaces
- **Extensible**: Easy to add new tools and resources
- **Standards Compliant**: Follows MCP specification
- **Developer Friendly**: Auto-generated API documentation

## MCP Protocol Benefits

- **Standardized**: Uses the Model Context Protocol standard
- **Tool Integration**: Can be used with MCP-compatible clients
- **Resource Access**: Provides structured data access
- **Extensible**: Easy to add new tools and resources
- **Type Safe**: Full type annotations and validation

## Development

To extend the application:

1. **Add new MCP tools**: Add functions decorated with `@mcp_server.tool()`
2. **Add new MCP resources**: Add functions decorated with `@mcp_server.resource("uri")`
3. **Add new API endpoints**: Add FastAPI route handlers
4. **Update shared data**: Modify the `todos` list and `next_id` counter

## Dependencies

- `fastapi`: Web framework for building APIs
- `uvicorn`: ASGI server
- `mcp`: Model Context Protocol implementation
- `pydantic`: Data validation and serialization
- `python-dotenv`: Environment variable management

## License

This project is for educational purposes and demonstrates MCP and FastAPI integration.
# MCP_assignment
