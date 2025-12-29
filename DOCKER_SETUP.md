# Docker Installation & Setup Guide

## Issue: Docker Not Found

If you see `docker : The term 'docker' is not recognized`, Docker is not installed on your system.

## Step 1: Install Docker Desktop

### For Windows:

1. **Download Docker Desktop for Windows:**
   - Visit: https://docs.docker.com/desktop/install/windows-install/
   - Download Docker Desktop Installer
   - Run the installer and follow the setup wizard

2. **Requirements:**
   - Windows 10 64-bit: Pro, Enterprise, or Education (Build 15063 or later)
   - WSL 2 feature enabled
   - Virtualization enabled in BIOS

3. **After Installation:**
   - Restart your computer
   - Launch Docker Desktop
   - Wait for Docker to start (whale icon in system tray)
   - Verify installation:
     ```powershell
     docker --version
     docker-compose --version
     ```

### Alternative: Install via Winget (Windows Package Manager)

```powershell
winget install Docker.DockerDesktop
```

## Step 2: Verify Docker Installation

After installing Docker Desktop, verify it's working:

```powershell
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker with hello-world
docker run hello-world
```

## Step 3: Build Your Backend

**Important:** Run Docker commands from the **project root**, not from the `backend` directory.

```powershell
# Navigate to project root
cd C:\Users\Mohd Aftaab\atheist_rag

# Build the Docker image
docker build -f backend/Dockerfile -t atheist-ai-backend .

# Or use Docker Compose (recommended)
docker-compose up -d --build
```

## Common Issues

### Issue 1: "Docker daemon is not running"

**Solution:**
- Make sure Docker Desktop is running
- Check the system tray for Docker icon
- Click "Start" if Docker Desktop shows it's stopped

### Issue 2: WSL 2 not installed

**Solution:**
```powershell
# Enable WSL 2
wsl --install

# Restart computer, then verify
wsl --status
```

### Issue 3: Virtualization not enabled

**Solution:**
1. Restart computer
2. Enter BIOS/UEFI settings (usually F2, F10, or Del during boot)
3. Enable "Virtualization Technology" or "Intel VT-x" / "AMD-V"
4. Save and exit

### Issue 4: Permission denied

**Solution:**
- Make sure you're running PowerShell as Administrator (if needed)
- Docker Desktop should handle permissions automatically

## Quick Start After Installation

Once Docker is installed:

```powershell
# 1. Navigate to project root
cd C:\Users\Mohd Aftaab\atheist_rag

# 2. Create .env file (if not exists)
# Copy backend/.env.example or create manually

# 3. Build and run with Docker Compose
docker-compose up -d

# 4. Check logs
docker-compose logs -f backend

# 5. Test the API
curl http://localhost:8000/api/v1/health
```

## Using Docker Without Installation (Alternative)

If you can't install Docker Desktop, you can:

1. **Use WSL 2 with Linux:**
   - Install Ubuntu from Microsoft Store
   - Install Docker inside WSL 2
   - Run commands from WSL terminal

2. **Use Cloud Services:**
   - GitHub Codespaces
   - GitPod
   - Replit (with Docker support)

3. **Use venv for local development:**
   - Skip Docker for now
   - Use Python virtual environment instead
   - See backend setup instructions in README.md

## Next Steps

After Docker is installed and running:

1. ✅ Verify Docker is working: `docker --version`
2. ✅ Build your image: `docker build -f backend/Dockerfile -t atheist-ai-backend .`
3. ✅ Run with compose: `docker-compose up -d`
4. ✅ Check health: `curl http://localhost:8000/api/v1/health`

## Need Help?

- Docker Desktop Docs: https://docs.docker.com/desktop/
- Docker Desktop Troubleshooting: https://docs.docker.com/desktop/troubleshoot/
- Windows WSL 2 Setup: https://docs.microsoft.com/en-us/windows/wsl/install


