#!/usr/bin/env python3
"""
Simple MCP server connection and interaction test
"""
import json
from mcp_server import mcp_server

def main():
    print("🔌 Simple MCP Server Test")
    print("=" * 30)
    
    # 1. Connect and show server info
    print(f"✅ Connected to: {mcp_server.name}")
    print(f"✅ Instructions: {mcp_server.instructions}")
    
    # 2. Show available tools
    print(f"\n🛠️  Available Tools:")
    for name, tool in mcp_server._tool_manager._tools.items():
        print(f"   - {name}")
    
    # 3. Show available resources  
    print(f"\n📚 Available Resources:")
    for uri, resource in mcp_server._resource_manager._resources.items():
        print(f"   - {uri}")
    
    # 4. Test creating a todo using direct function calls
    print(f"\n🧪 Testing Tools:")
    from mcp_server import create_todo, get_todos, complete_todo, get_all_todos_resource, get_completed_todos_resource
    
    todo = create_todo("Test Todo", "Testing MCP connection")
    print(f"✅ Created todo: {todo['title']} (ID: {todo['id']})")
    
    # 5. Test getting all todos
    all_todos = get_todos()
    print(f"✅ Found {len(all_todos)} todos total")
    
    # 6. Test completing the todo
    completed = complete_todo(todo['id'])
    print(f"✅ Completed: {completed['title']}")
    
    # 7. Test resources
    print(f"\n📚 Testing Resources:")
    all_resource = get_all_todos_resource()
    todos_data = json.loads(all_resource)
    print(f"✅ All Resource: {len(todos_data)} todos")
    
    completed_resource = get_completed_todos_resource()
    completed_data = json.loads(completed_resource)
    print(f"✅ Completed Resource: {len(completed_data)} completed")
    
    print(f"\n🎉 MCP server is working correctly!")

if __name__ == "__main__":
    main()
