"""
Docker Setup Checker
Verify that Docker and Docker Compose are properly installed and configured.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return the result"""
    try:
        print(f"Checking {description}...")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}: OK")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description}: FAILED")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {str(e)}")
        return False

def check_docker_installation():
    """Check if Docker is installed and running"""
    print("=== Docker Setup Checker ===\n")
    
    # Check Docker version
    docker_version_ok = run_command("docker --version", "Docker installation")
    
    if not docker_version_ok:
        print("\nDocker is not installed or not in PATH.")
        print("Please install Docker Desktop from https://www.docker.com/products/docker-desktop")
        return False
    
    # Check Docker Compose version
    compose_version_ok = run_command("docker-compose --version", "Docker Compose installation")
    
    if not compose_version_ok:
        print("\nDocker Compose is not installed or not in PATH.")
        print("Docker Compose is usually included with Docker Desktop.")
        return False
    
    # Check if Docker daemon is running
    print("\nChecking if Docker daemon is running...")
    try:
        # Try a simple Docker command
        result = subprocess.run("docker info", shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker daemon: RUNNING")
            daemon_running = True
        else:
            print("❌ Docker daemon: NOT RUNNING")
            print("Please start Docker Desktop and wait for it to finish initializing.")
            daemon_running = False
    except subprocess.TimeoutExpired:
        print("❌ Docker daemon: NO RESPONSE (timeout)")
        print("Docker Desktop may still be starting up. Please wait and try again.")
        daemon_running = False
    except Exception as e:
        print(f"❌ Docker daemon: ERROR - {str(e)}")
        daemon_running = False
    
    if not daemon_running:
        return False
    
    # Check Docker Compose configuration
    print("\nChecking Docker Compose configuration...")
    compose_config_ok = run_command("docker-compose config", "Docker Compose configuration")
    
    if not compose_config_ok:
        print("\nDocker Compose configuration has errors.")
        print("Please check your docker-compose.yml file.")
        return False
    
    # All checks passed
    print("\n🎉 All Docker checks passed!")
    print("\nYou can now run the GuardianAI project with:")
    print("   docker-compose up --build")
    print("\nOr use the Makefile:")
    print("   make run-all")
    
    return True

def main():
    """Main function"""
    try:
        success = check_docker_installation()
        if not success:
            print("\n🔧 Troubleshooting tips:")
            print("1. Make sure Docker Desktop is installed and running")
            print("2. Check that Docker is in your system PATH")
            print("3. Wait for Docker Desktop to finish starting up")
            print("4. See DOCKER_TROUBLESHOOTING.md for detailed help")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()