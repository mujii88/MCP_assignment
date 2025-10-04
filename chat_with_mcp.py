#!/usr/bin/env python3
"""
Interactive chat with MCP server
"""
import json
from mcp_server import (
    get_todos, create_todo, get_todo, 
    update_todo, delete_todo, complete_todo,
    get_all_todos_resource, get_completed_todos_resource, get_pending_todos_resource
)

def show_help():
    """Show available commands"""
    print("""
🤖 MCP Todo Chat Commands:
========================
📋 list                    - List all todos
➕ create <title> [desc]   - Create a new todo
👁️  get <id>               - Get a specific todo
✏️  update <id> [options]  - Update a todo
✅ complete <id>           - Mark todo as completed
❌ delete <id>            - Delete a todo
📊 resources              - Show all resources
📈 stats                  - Show todo statistics
❓ help                   - Show this help
🚪 quit                   - Exit chat
""")

def show_stats():
    """Show todo statistics"""
    all_todos = get_todos()
    completed = [t for t in all_todos if t['completed']]
    pending = [t for t in all_todos if not t['completed']]
    
    print(f"""
📊 Todo Statistics:
==================
📝 Total todos: {len(all_todos)}
✅ Completed: {len(completed)}
⏳ Pending: {len(pending)}
📈 Completion rate: {len(completed)/len(all_todos)*100:.1f}% if len(all_todos) > 0 else 0
""")

def show_resources():
    """Show all MCP resources"""
    print("\n📚 MCP Resources:")
    print("================")
    
    # All todos resource
    all_resource = get_all_todos_resource()
    all_todos = json.loads(all_resource)
    print(f"📋 todos://all - {len(all_todos)} todos")
    
    # Completed todos resource
    completed_resource = get_completed_todos_resource()
    completed_todos = json.loads(completed_resource)
    print(f"✅ todos://completed - {len(completed_todos)} completed")
    
    # Pending todos resource
    pending_resource = get_pending_todos_resource()
    pending_todos = json.loads(pending_resource)
    print(f"⏳ todos://pending - {len(pending_todos)} pending")

def list_todos():
    """List all todos"""
    todos = get_todos()
    if not todos:
        print("📝 No todos found. Create one with: create <title>")
        return
    
    print(f"\n📋 All Todos ({len(todos)}):")
    print("=" * 30)
    for todo in todos:
        status = "✅" if todo['completed'] else "⏳"
        print(f"{status} {todo['id']}: {todo['title']}")
        if todo['description']:
            print(f"   📝 {todo['description']}")

def create_todo_interactive():
    """Interactive todo creation"""
    title = input("📝 Todo title: ").strip()
    if not title:
        print("❌ Title cannot be empty")
        return
    
    description = input("📄 Description (optional): ").strip()
    
    try:
        todo = create_todo(title, description)
        print(f"✅ Created: {todo['title']} (ID: {todo['id']})")
    except Exception as e:
        print(f"❌ Error creating todo: {e}")

def get_todo_interactive():
    """Interactive todo retrieval"""
    try:
        todo_id = int(input("🔍 Todo ID: ").strip())
        todo = get_todo(todo_id)
        status = "✅" if todo['completed'] else "⏳"
        print(f"\n📄 Todo {todo['id']}:")
        print(f"   {status} {todo['title']}")
        if todo['description']:
            print(f"   📝 {todo['description']}")
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")
    except Exception as e:
        print(f"❌ Error: {e}")

def complete_todo_interactive():
    """Interactive todo completion"""
    try:
        todo_id = int(input("✅ Complete todo ID: ").strip())
        todo = complete_todo(todo_id)
        print(f"✅ Completed: {todo['title']}")
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")
    except Exception as e:
        print(f"❌ Error: {e}")

def delete_todo_interactive():
    """Interactive todo deletion"""
    try:
        todo_id = int(input("❌ Delete todo ID: ").strip())
        todo = delete_todo(todo_id)
        print(f"🗑️  Deleted: {todo['title']}")
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main chat loop"""
    print("🤖 Welcome to MCP Todo Chat!")
    print("Type 'help' for commands or 'quit' to exit")
    print("=" * 40)
    
    while True:
        try:
            command = input("\n🤖 MCP> ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Thanks for using MCP Todo Chat!")
                break
            elif command == 'help':
                show_help()
            elif command == 'list':
                list_todos()
            elif command == 'create':
                create_todo_interactive()
            elif command == 'get':
                get_todo_interactive()
            elif command == 'complete':
                complete_todo_interactive()
            elif command == 'delete':
                delete_todo_interactive()
            elif command == 'resources':
                show_resources()
            elif command == 'stats':
                show_stats()
            elif command.startswith('create '):
                # Handle inline creation
                parts = command.split(' ', 1)
                if len(parts) > 1:
                    title = parts[1]
                    try:
                        todo = create_todo(title)
                        print(f"✅ Created: {todo['title']} (ID: {todo['id']})")
                    except Exception as e:
                        print(f"❌ Error: {e}")
            elif command.startswith('get '):
                # Handle inline retrieval
                try:
                    todo_id = int(command.split()[1])
                    todo = get_todo(todo_id)
                    status = "✅" if todo['completed'] else "⏳"
                    print(f"📄 {todo['title']}: {todo['description']} ({status})")
                except (ValueError, IndexError):
                    print("❌ Usage: get <id>")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif command.startswith('complete '):
                # Handle inline completion
                try:
                    todo_id = int(command.split()[1])
                    todo = complete_todo(todo_id)
                    print(f"✅ Completed: {todo['title']}")
                except (ValueError, IndexError):
                    print("❌ Usage: complete <id>")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif command.startswith('delete '):
                # Handle inline deletion
                try:
                    todo_id = int(command.split()[1])
                    todo = delete_todo(todo_id)
                    print(f"🗑️  Deleted: {todo['title']}")
                except (ValueError, IndexError):
                    print("❌ Usage: delete <id>")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif command == '':
                continue
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using MCP Todo Chat!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
