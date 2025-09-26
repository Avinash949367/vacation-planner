#!/usr/bin/env python3
"""
Backend server runner script
"""
import subprocess
import sys
import os
import platform


def get_venv_python(backend_dir: str) -> str:
    """Return the backend venv python if it exists, else current interpreter."""
    if platform.system() == 'Windows':
        candidate = os.path.join(backend_dir, '.venv', 'Scripts', 'python.exe')
    else:
        candidate = os.path.join(backend_dir, '.venv', 'bin', 'python')
    return candidate if os.path.exists(candidate) else sys.executable


def main():
    """Run the FastAPI backend server"""
    project_root = os.path.dirname(__file__)
    backend_dir = os.path.join(project_root, 'backend')

    # Prefer backend venv interpreter
    python_exec = get_venv_python(backend_dir)

    # Change to backend directory
    os.chdir(backend_dir)

    # Run the server
    try:
        subprocess.run([python_exec, 'main.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running backend server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
        sys.exit(0)


if __name__ == '__main__':
    main()
