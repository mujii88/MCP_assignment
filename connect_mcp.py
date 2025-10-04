#!/usr/bin/env python3
"""
Connect to MCP server and interact with it
"""
import asyncio
import json
import sys
from mcp.server.fastmcp import FastMCP
from mcp_server import mcp_server

def test_mcp_connection():
    """Test connecting to MCP server and listing available tools/resources"""
    print("🔌 Connecting to MCP Server")
    print("=" * 40)
    
    try:
        # Get server information
        print(f"✅ MCP Server Name: {mcp_server.name}")
        print(f"✅ Instructions: {mcp_server.instructions}")
        
        # List available tools
        print(f"\n🛠️  Available Tools ({len(mcp_server._tool_manager._tools)}):")
        for tool_name, tool in mcp_server._tool_manager._tools.items():
            print(f"   - {tool_name}: {tool.description}")
        
        # List available resources
        print(f"\n📚 Available Resources ({len(mcp_server._resource_manager._resources)}):")
        for resource_uri, resource in mcp_server._resource_manager._resources.items():
            print(f"   - {resource_uri}: {resource.description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        return False

def test_mcp_tools():
    """Test using MCP tools directly"""
    print("\n🧪 Testing MCP Tools")
    print("=" * 40)
    
    try:
        # Test creating todos
        print("\n1. Creating todos...")
        todo1 = mcp_server._tool_manager._tools["create_todo"].func("MCP Test 1", "Testing MCP connection")
        todo2 = mcp_server._tool_manager._tools["create_todo"].func("MCP Test 2", "Another MCP test")
        print(f"✅ Created: {todo1['title']} (ID: {todo1['id']})")
        print(f"✅ Created: {todo2['title']} (ID: {todo2['id']})")
        
        # Test getting all todos
        print("\n2. Getting all todos...")
        all_todos = mcp_server._tool_manager._tools["get_todos"].func()
        print(f"✅ Found {len(all_todos)} todos:")
        for todo in all_todos:
            status = "✅" if todo['completed'] else "⏳"
            print(f"   {status} {todo['id']}: {todo['title']}")
        
        # Test getting specific todo
        print("\n3. Getting specific todo...")
        todo = mcp_server._tool_manager._tools["get_todo"].func(1)
        print(f"✅ Retrieved: {todo['title']} - {todo['description']}")
        
        # Test updating todo
        print("\n4. Updating todo...")
        updated = mcp_server._tool_manager._tools["update_todo"].func(1, completed=True)
        print(f"✅ Updated: {updated['title']} (Completed: {updated['completed']})")
        
        # Test completing todo
        print("\n5. Completing todo...")
        completed = mcp_server._tool_manager._tools["complete_todo"].func(2)
        print(f"✅ Completed: {completed['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test MCP tools: {e}")
        return False

def test_mcp_resources():
    """Test accessing MCP resources"""
    print("\n📚 Testing MCP Resources")
    print("=" * 40)
    
    try:
        # Test all todos resource
        print("\n1. All todos resource...")
        all_resource = mcp_server._resource_manager._resources["todos://all"].func()
        all_todos = json.loads(all_resource)
        print(f"✅ All Resource: {len(all_todos)} todos")
        print(f"Content: {all_resource[:200]}...")
        
        # Test completed todos resource
        print("\n2. Completed todos resource...")
        completed_resource = mcp_server._resource_manager._resources["todos://completed"].func()
        completed_todos = json.loads(completed_resource)
        print(f"✅ Completed Resource: {len(completed_todos)} completed")
        print(f"Content: {completed_resource[:200]}...")
        
        # Test pending todos resource
        print("\n3. Pending todos resource...")
        pending_resource = mcp_server._resource_manager._resources["todos://pending"].func()
        pending_todos = json.loads(pending_resource)
        print(f"✅ Pending Resource: {len(pending_todos)} pending")
        print(f"Content: {pending_resource[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test MCP resources: {e}")
        return False

def interactive_mcp_chat():
    """Interactive chat with MCP server"""
    print("\n💬 Interactive MCP Chat")
    print("=" * 40)
    print("Available commands:")
    print("  - list: List all todos")
    print("  - create <title> [description]: Create a new todo")
    print("  - get <id>: Get a specific todo")
    print("  - update <id> [title] [description] [completed]: Update a todo")
    print("  - complete <id>: Mark a todo as completed")
    print("  - delete <id>: Delete a todo")
    print("  - resources: Show all resources")
    print("  - quit: Exit")
    print()
    
    while True:
        try:
            command = input("MCP> ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif command.lower() == 'list':
                todos = mcp_server._tool_manager._tools["get_todos"].func()
                print(f"📋 Found {len(todos)} todos:")
                for todo in todos:
                    status = "✅" if todo['completed'] else "⏳"
                    print(f"   {status} {todo['id']}: {todo['title']}")
            elif command.lower().startswith('create '):
                parts = command.split(' ', 2)
                title = parts[1] if len(parts) > 1 else "New Todo"
                description = parts[2] if len(parts) > 2 else ""
                todo = mcp_server._tool_manager._tools["create_todo"].func(title, description)
                print(f"✅ Created: {todo['title']} (ID: {todo['id']})")
            elif command.lower().startswith('get '):
                try:
                    todo_id = int(command.split()[1])
                    todo = mcp_server._tool_manager._tools["get_todo"].func(todo_id)
                    print(f"📄 {todo['title']}: {todo['description']} ({'✅' if todo['completed'] else '⏳'})")
                except (ValueError, IndexError):
                    print("❌ Invalid ID. Use: get <id>")
            elif command.lower().startswith('complete '):
                try:
                    todo_id = int(command.split()[1])
                    todo = mcp_server._tool_manager._tools["complete_todo"].func(todo_id)
                    print(f"✅ Completed: {todo['title']}")
                except (ValueError, IndexError):
                    print("❌ Invalid ID. Use: complete <id>")
            elif command.lower().startswith('delete '):
                try:
                    todo_id = int(command.split()[1])
                    todo = mcp_server._tool_manager._tools["delete_todo"].func(todo_id)
                    print(f"🗑️  Deleted: {todo['title']}")
                except (ValueError, IndexError):
                    print("❌ Invalid ID. Use: delete <id>")
            elif command.lower() == 'resources':
                print("📚 Available Resources:")
                for uri, resource in mcp_server._resource_manager._resources.items():
                    print(f"   - {uri}: {resource.description}")
            elif command.lower() == 'help':
                print("Available commands: list, create, get, complete, delete, resources, quit")
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function to test MCP connection and interaction"""
    print("🚀 MCP Server Connection Test")
    print("=" * 50)
    
    # Test connection
    if not test_mcp_connection():
        print("❌ Failed to connect to MCP server")
        return
    
    # Test tools
    if not test_mcp_tools():
        print("❌ Failed to test MCP tools")
        return
    
    # Test resources
    if not test_mcp_resources():
        print("❌ Failed to test MCP resources")
        return
    
    print("\n✅ All MCP tests passed!")
    
    # Ask if user wants interactive chat
    try:
        response = input("\n🤔 Would you like to start interactive chat? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_mcp_chat()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
