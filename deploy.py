#!/usr/bin/env python3
"""
Deployment script for TravelMate
"""
import subprocess
import sys
import os
import platform


def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"✅ {command}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running: {command}")
        print(f"Error: {e.stderr}")
        return False


def deploy_backend():
    """Deploy backend to Heroku"""
    print("🚀 Deploying Backend to Heroku...")
    
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # Check if git is initialized
    if not os.path.exists(os.path.join(backend_dir, '.git')):
        print("📁 Initializing git repository...")
        if not run_command("git init", cwd=backend_dir):
            return False
    
    # Add all files
    if not run_command("git add .", cwd=backend_dir):
        return False
    
    # Commit changes
    if not run_command('git commit -m "Deploy backend"', cwd=backend_dir):
        return False
    
    # Check if Heroku app exists
    result = subprocess.run("heroku apps", shell=True, capture_output=True, text=True)
    if "travelmate-backend" not in result.stdout:
        print("📱 Creating Heroku app...")
        if not run_command("heroku create travelmate-backend", cwd=backend_dir):
            return False
    
    # Set environment variables
    print("🔧 Setting environment variables...")
    env_vars = [
        "MONGODB_URL=mongodb+srv://parkproplus_db_user:vacation@vacation-planner.tvg1alp.mongodb.net/?retryWrites=true&w=majority&appName=vacation-planner",
        "SECRET_KEY=your-super-secret-key-change-in-production-12345",
        "CORS_ORIGINS=https://travelmate-backend.herokuapp.com,http://localhost:3000"
    ]
    
    for env_var in env_vars:
        if not run_command(f"heroku config:set {env_var}", cwd=backend_dir):
            print(f"⚠️  Warning: Failed to set {env_var}")
    
    # Deploy
    print("🚀 Deploying to Heroku...")
    if not run_command("git push heroku main", cwd=backend_dir):
        return False
    
    print("✅ Backend deployed successfully!")
    print("🌐 Backend URL: https://travelmate-backend.herokuapp.com")
    return True


def build_frontend():
    """Build frontend for distribution"""
    print("📱 Building Frontend...")
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # Install buildozer if not present
    print("📦 Installing buildozer...")
    if not run_command("pip install buildozer cython", cwd=frontend_dir):
        print("⚠️  Warning: Could not install buildozer")
        return False
    
    # Initialize buildozer if not present
    if not os.path.exists(os.path.join(frontend_dir, 'buildozer.spec')):
        print("📋 Creating buildozer.spec...")
        if not run_command("buildozer init", cwd=frontend_dir):
            return False
    
    # Build APK
    print("🔨 Building Android APK...")
    if not run_command("buildozer android debug", cwd=frontend_dir):
        print("⚠️  Warning: APK build failed")
        return False
    
    print("✅ Frontend build completed!")
    print("📱 APK location: frontend/bin/")
    return True


def main():
    """Main deployment function"""
    print("🌟 TravelMate Deployment Script")
    print("=" * 40)
    print("1. Deploy Backend Only")
    print("2. Build Frontend Only")
    print("3. Deploy Both")
    print("4. Exit")
    print("=" * 40)
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                deploy_backend()
                break
            elif choice == '2':
                build_frontend()
                break
            elif choice == '3':
                print("\n🚀 Deploying both backend and frontend...")
                deploy_backend()
                print("\n" + "="*50)
                build_frontend()
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
