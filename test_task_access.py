#!/usr/bin/env python3
"""
Simple test script to verify MCP server can access all tasks
"""
import json
import requests
import time

def test_task_access():
    """Test that we can access all tasks through different methods"""
    print("🧪 Testing Task Access Methods")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # Method 1: REST API - Get all todos
    print("\n1️⃣ REST API - Get all todos")
    try:
        response = requests.get(f"{base_url}/todos/")
        if response.status_code == 200:
            todos = response.json()
            print(f"✅ REST API: Found {len(todos)} todos")
            for todo in todos:
                print(f"   - {todo['id']}: {todo['title']} ({'✅' if todo['completed'] else '⏳'})")
        else:
            print(f"❌ REST API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ REST API error: {e}")
    
    # Method 2: MCP Direct Access
    print("\n2️⃣ MCP Direct Access")
    try:
        from mcp_server import get_todos
        todos = get_todos()
        print(f"✅ MCP Direct: Found {len(todos)} todos")
        for todo in todos:
            print(f"   - {todo['id']}: {todo['title']} ({'✅' if todo['completed'] else '⏳'})")
    except Exception as e:
        print(f"❌ MCP Direct error: {e}")
    
    # Method 3: MCP Resources
    print("\n3️⃣ MCP Resources")
    try:
        from mcp_server import (
            get_all_todos_resource,
            get_completed_todos_resource, 
            get_pending_todos_resource
        )
        
        # All todos resource
        all_resource = get_all_todos_resource()
        all_todos = json.loads(all_resource)
        print(f"✅ All Resource: {len(all_todos)} todos")
        
        # Completed todos resource
        completed_resource = get_completed_todos_resource()
        completed_todos = json.loads(completed_resource)
        print(f"✅ Completed Resource: {len(completed_todos)} completed")
        
        # Pending todos resource
        pending_resource = get_pending_todos_resource()
        pending_todos = json.loads(pending_resource)
        print(f"✅ Pending Resource: {len(pending_todos)} pending")
        
    except Exception as e:
        print(f"❌ MCP Resources error: {e}")
    
    # Method 4: Server Info
    print("\n4️⃣ Server Information")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            info = response.json()
            print(f"✅ Server: {info['message']}")
            print(f"✅ MCP Tools: {', '.join(info['mcp_tools'])}")
            print(f"✅ MCP Resources: {', '.join(info['mcp_resources'])}")
        else:
            print(f"❌ Server info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Server info error: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Task access test completed!")

def create_test_tasks():
    """Create some test tasks to work with"""
    print("\n🔧 Creating test tasks...")
    
    base_url = "http://localhost:8000"
    test_tasks = [
        {"title": "Learn MCP", "description": "Study Model Context Protocol", "completed": False},
        {"title": "Build API", "description": "Create FastAPI integration", "completed": True},
        {"title": "Test Integration", "description": "Verify MCP + FastAPI works", "completed": False},
    ]
    
    for i, task in enumerate(test_tasks):
        try:
            response = requests.post(f"{base_url}/todos/", json=task)
            if response.status_code == 200:
                created = response.json()
                print(f"✅ Created task {i+1}: {created['title']} (ID: {created['id']})")
            else:
                print(f"❌ Failed to create task {i+1}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error creating task {i+1}: {e}")

if __name__ == "__main__":
    print("🚀 MCP Task Access Test")
    print("Make sure the server is running: uvicorn main:app --reload")
    print()
    
    # Wait for server to be ready
    time.sleep(2)
    
    # Create some test tasks first
    create_test_tasks()
    
    # Test accessing all tasks
    test_task_access()
    
    print("\n🎯 Test completed! Check the output above to verify task access.")
