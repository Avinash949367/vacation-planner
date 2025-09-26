#!/usr/bin/env python3
"""
Frontend app runner script
"""
import subprocess
import sys
import os
import platform


def get_venv_python(frontend_dir: str) -> str:
    """Return the frontend venv python if it exists, else current interpreter."""
    if platform.system() == 'Windows':
        candidate = os.path.join(frontend_dir, '.venv', 'Scripts', 'python.exe')
    else:
        candidate = os.path.join(frontend_dir, '.venv', 'bin', 'python')
    return candidate if os.path.exists(candidate) else sys.executable


def main():
    """Run the KivyMD frontend app"""
    project_root = os.path.dirname(__file__)
    frontend_dir = os.path.join(project_root, 'frontend')

    # Choose interpreter (prefer frontend venv)
    python_exec = get_venv_python(frontend_dir)

    # Change to frontend directory
    os.chdir(frontend_dir)

    # Run the app
    try:
        subprocess.run([python_exec, 'main.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running frontend app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nFrontend app stopped.")
        sys.exit(0)


if __name__ == '__main__':
    main()
