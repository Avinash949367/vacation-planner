#!/usr/bin/env python3
"""
Main application runner for development
Choose to run backend, frontend, or both
"""
import subprocess
import sys
import os
import platform
import threading
import time


def get_venv_python(directory: str) -> str:
    """Return the venv python if it exists, else current interpreter."""
    if platform.system() == 'Windows':
        candidate = os.path.join(directory, '.venv', 'Scripts', 'python.exe')
    else:
        candidate = os.path.join(directory, '.venv', 'bin', 'python')
    return candidate if os.path.exists(candidate) else sys.executable


def run_backend():
    """Run the backend server"""
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    python_exec = get_venv_python(backend_dir)
    
    print("🚀 Starting backend server...")
    try:
        subprocess.run([python_exec, 'run_backend.py'], cwd=backend_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running backend server: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped.")


def run_frontend():
    """Run the frontend app"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    python_exec = get_venv_python(frontend_dir)
    
    print("📱 Starting frontend app...")
    try:
        subprocess.run([python_exec, 'run_frontend.py'], cwd=frontend_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running frontend app: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Frontend app stopped.")


def main():
    """Main application runner"""
    print("🌟 TravelMate Application Runner")
    print("=" * 40)
    print("1. Run Backend Only")
    print("2. Run Frontend Only") 
    print("3. Run Both (Backend + Frontend)")
    print("4. Exit")
    print("=" * 40)
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                run_backend()
                break
            elif choice == '2':
                run_frontend()
                break
            elif choice == '3':
                print("\n🚀 Starting both backend and frontend...")
                print("Backend will start first, then frontend in 3 seconds...")
                
                # Start backend in a separate thread
                backend_thread = threading.Thread(target=run_backend, daemon=True)
                backend_thread.start()
                
                # Wait a bit for backend to start
                time.sleep(3)
                
                # Start frontend
                run_frontend()
                break
            elif choice == '4':
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == '__main__':
    main()
