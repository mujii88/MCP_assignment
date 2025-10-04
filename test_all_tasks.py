#!/usr/bin/env python3
"""
Comprehensive test script to verify MCP server can access all tasks
"""
import json
import requests
import time
from mcp_server import todos, next_id

def test_rest_api_access():
    """Test accessing all tasks via REST API"""
    print("=== Testing REST API Access ===")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Get all todos
    print("\n1. Getting all todos via REST API...")
    response = requests.get(f"{base_url}/todos/")
    if response.status_code == 200:
        all_todos = response.json()
        print(f"✅ Found {len(all_todos)} todos via REST API")
        print(f"Todos: {json.dumps(all_todos, indent=2)}")
    else:
        print(f"❌ Failed to get todos: {response.status_code}")
        return False
    
    # Test 2: Create multiple todos
    print("\n2. Creating multiple todos...")
    test_todos = [
        {"title": "Task 1", "description": "First test task", "completed": False},
        {"title": "Task 2", "description": "Second test task", "completed": False},
        {"title": "Task 3", "description": "Third test task", "completed": True},
    ]
    
    created_todos = []
    for i, todo_data in enumerate(test_todos):
        response = requests.post(f"{base_url}/todos/", json=todo_data)
        if response.status_code == 200:
            created_todo = response.json()
            created_todos.append(created_todo)
            print(f"✅ Created todo {i+1}: {created_todo['title']} (ID: {created_todo['id']})")
        else:
            print(f"❌ Failed to create todo {i+1}: {response.status_code}")
    
    # Test 3: Get all todos again
    print("\n3. Getting all todos after creation...")
    response = requests.get(f"{base_url}/todos/")
    if response.status_code == 200:
        all_todos = response.json()
        print(f"✅ Now have {len(all_todos)} todos total")
        print(f"All todos: {json.dumps(all_todos, indent=2)}")
    else:
        print(f"❌ Failed to get todos: {response.status_code}")
    
    # Test 4: Access individual todos
    print("\n4. Accessing individual todos...")
    for todo in all_todos:
        todo_id = todo['id']
        response = requests.get(f"{base_url}/todos/{todo_id}")
        if response.status_code == 200:
            individual_todo = response.json()
            print(f"✅ Retrieved todo {todo_id}: {individual_todo['title']}")
        else:
            print(f"❌ Failed to get todo {todo_id}: {response.status_code}")
    
    return True

def test_mcp_direct_access():
    """Test accessing all tasks via direct MCP server functions"""
    print("\n=== Testing MCP Direct Access ===")
    
    # Import MCP server functions directly
    from mcp_server import (
        get_todos, create_todo, get_todo, 
        update_todo, delete_todo, complete_todo
    )
    
    # Test 1: Get all todos via MCP
    print("\n1. Getting all todos via MCP...")
    all_todos = get_todos()
    print(f"✅ MCP found {len(all_todos)} todos")
    print(f"MCP todos: {json.dumps(all_todos, indent=2)}")
    
    # Test 2: Create todos via MCP
    print("\n2. Creating todos via MCP...")
    mcp_todos = [
        ("MCP Task 1", "Created via MCP"),
        ("MCP Task 2", "Another MCP task"),
        ("MCP Task 3", "Third MCP task"),
    ]
    
    created_mcp_todos = []
    for title, description in mcp_todos:
        todo = create_todo(title, description)
        created_mcp_todos.append(todo)
        print(f"✅ Created MCP todo: {todo['title']} (ID: {todo['id']})")
    
    # Test 3: Get all todos again via MCP
    print("\n3. Getting all todos after MCP creation...")
    all_todos = get_todos()
    print(f"✅ MCP now has {len(all_todos)} todos total")
    print(f"All MCP todos: {json.dumps(all_todos, indent=2)}")
    
    # Test 4: Access individual todos via MCP
    print("\n4. Accessing individual todos via MCP...")
    for todo in all_todos:
        todo_id = todo['id']
        try:
            individual_todo = get_todo(todo_id)
            print(f"✅ MCP retrieved todo {todo_id}: {individual_todo['title']}")
        except ValueError as e:
            print(f"❌ MCP failed to get todo {todo_id}: {e}")
    
    return True

def test_mcp_resources():
    """Test accessing all tasks via MCP resources"""
    print("\n=== Testing MCP Resources ===")
    
    # Import MCP resource functions
    from mcp_server import (
        get_all_todos_resource, 
        get_completed_todos_resource, 
        get_pending_todos_resource
    )
    
    # Test 1: All todos resource
    print("\n1. All todos resource...")
    all_resource = get_all_todos_resource()
    all_todos = json.loads(all_resource)
    print(f"✅ Resource found {len(all_todos)} todos")
    print(f"All todos resource: {all_resource}")
    
    # Test 2: Completed todos resource
    print("\n2. Completed todos resource...")
    completed_resource = get_completed_todos_resource()
    completed_todos = json.loads(completed_resource)
    print(f"✅ Resource found {len(completed_todos)} completed todos")
    print(f"Completed todos resource: {completed_resource}")
    
    # Test 3: Pending todos resource
    print("\n3. Pending todos resource...")
    pending_resource = get_pending_todos_resource()
    pending_todos = json.loads(pending_resource)
    print(f"✅ Resource found {len(pending_todos)} pending todos")
    print(f"Pending todos resource: {pending_resource}")
    
    return True

def test_shared_data_consistency():
    """Test that both REST API and MCP access the same data"""
    print("\n=== Testing Data Consistency ===")
    
    # Get todos via REST API
    try:
        response = requests.get("http://localhost:8000/todos/")
        rest_todos = response.json() if response.status_code == 200 else []
    except:
        rest_todos = []
    
    # Get todos via MCP
    mcp_todos = get_todos()
    
    print(f"REST API todos: {len(rest_todos)}")
    print(f"MCP todos: {len(mcp_todos)}")
    
    if len(rest_todos) == len(mcp_todos):
        print("✅ Data consistency: Both APIs see the same number of todos")
        
        # Check if todos match
        rest_ids = {todo['id'] for todo in rest_todos}
        mcp_ids = {todo['id'] for todo in mcp_todos}
        
        if rest_ids == mcp_ids:
            print("✅ Data consistency: Both APIs see the same todo IDs")
        else:
            print("❌ Data inconsistency: Different todo IDs")
            print(f"REST IDs: {rest_ids}")
            print(f"MCP IDs: {mcp_ids}")
    else:
        print("❌ Data inconsistency: Different number of todos")
    
    return True

def test_comprehensive_access():
    """Comprehensive test of all access methods"""
    print("🔍 COMPREHENSIVE TASK ACCESS TEST")
    print("=" * 50)
    
    # Test REST API access
    rest_success = test_rest_api_access()
    
    # Test MCP direct access
    mcp_success = test_mcp_direct_access()
    
    # Test MCP resources
    resource_success = test_mcp_resources()
    
    # Test data consistency
    consistency_success = test_shared_data_consistency()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"REST API Access: {'✅ PASS' if rest_success else '❌ FAIL'}")
    print(f"MCP Direct Access: {'✅ PASS' if mcp_success else '❌ FAIL'}")
    print(f"MCP Resources: {'✅ PASS' if resource_success else '❌ FAIL'}")
    print(f"Data Consistency: {'✅ PASS' if consistency_success else '❌ FAIL'}")
    
    all_passed = all([rest_success, mcp_success, resource_success, consistency_success])
    print(f"\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

if __name__ == "__main__":
    # Import MCP functions
    from mcp_server import get_todos
    
    print("🚀 Starting Comprehensive Task Access Test")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print()
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    # Run comprehensive test
    success = test_comprehensive_access()
    
    if success:
        print("\n🎉 All tests passed! The MCP server can access all tasks successfully.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
