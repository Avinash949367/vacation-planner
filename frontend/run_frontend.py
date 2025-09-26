#!/usr/bin/env python3
"""
Frontend app runner script for hosting
"""
import subprocess
import sys
import os
import platform


def get_venv_python() -> str:
    """Return the frontend venv python if it exists, else current interpreter."""
    if platform.system() == 'Windows':
        candidate = os.path.join('.venv', 'Scripts', 'python.exe')
    else:
        candidate = os.path.join('.venv', 'bin', 'python')
    return candidate if os.path.exists(candidate) else sys.executable


def main():
    """Run the KivyMD frontend app"""
    # We're already in the frontend directory for hosting
    python_exec = get_venv_python()

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
