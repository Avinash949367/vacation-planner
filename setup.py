#!/usr/bin/env python3
"""
TravelMate Vacation Planner Setup Script
"""
import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_backend():
    """Setup backend environment"""
    print("\n🚀 Setting up Backend...")
    
    backend_dir = "backend"
    if not os.path.exists(backend_dir):
        print(f"❌ Backend directory not found: {backend_dir}")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing backend dependencies"):
        return False
    
    print("✅ Backend setup completed successfully")
    return True

def setup_frontend():
    """Setup frontend environment"""
    print("\n📱 Setting up Frontend...")
    
    # Go back to root directory
    os.chdir("..")
    
    frontend_dir = "frontend"
    if not os.path.exists(frontend_dir):
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return False
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing frontend dependencies"):
        return False
    
    print("✅ Frontend setup completed successfully")
    return True

def create_run_scripts():
    """Create convenient run scripts"""
    print("\n📝 Creating run scripts...")
    
    # Go back to root directory
    os.chdir("..")
    
    # Create run_backend.py
    backend_script = '''#!/usr/bin/env python3
"""
Backend server runner script
"""
import subprocess
import sys
import os

def main():
    """Run the FastAPI backend server"""
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Run the server
    try:
        subprocess.run([sys.executable, 'main.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running backend server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\\nBackend server stopped.")
        sys.exit(0)

if __name__ == '__main__':
    main()
'''
    
    with open("run_backend.py", "w") as f:
        f.write(backend_script)
    
    # Create run_frontend.py
    frontend_script = '''#!/usr/bin/env python3
"""
Frontend app runner script
"""
import subprocess
import sys
import os

def main():
    """Run the KivyMD frontend app"""
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Run the app
    try:
        subprocess.run([sys.executable, 'main.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running frontend app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\\nFrontend app stopped.")
        sys.exit(0)

if __name__ == '__main__':
    main()
'''
    
    with open("run_frontend.py", "w") as f:
        f.write(frontend_script)
    
    # Make scripts executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("run_backend.py", 0o755)
        os.chmod("run_frontend.py", 0o755)
    
    print("✅ Run scripts created successfully")

def main():
    """Main setup function"""
    print("🌟 TravelMate Vacation Planner Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        sys.exit(1)
    
    # Create run scripts
    create_run_scripts()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update MongoDB connection string in backend/config.py")
    print("2. Get OpenWeather API key and update backend/services/weather_service.py")
    print("3. Run backend: python run_backend.py")
    print("4. Run frontend: python run_frontend.py")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()




