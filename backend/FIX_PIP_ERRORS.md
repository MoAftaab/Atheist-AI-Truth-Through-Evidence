# Fixing pip Installation Errors on Windows

If you're encountering uvicorn installation errors, try these solutions:

## Solution 1: Close all Python processes
1. Close all running Python applications
2. Close your IDE/editor
3. Check Task Manager for any Python processes and end them
4. Try installing again

## Solution 2: Use --user flag
```powershell
pip install --user -r requirements.txt
```

## Solution 3: Reinstall uvicorn separately
```powershell
pip uninstall uvicorn -y
pip install uvicorn[standard]>=0.24.0,<0.35.0
```

## Solution 4: Use virtual environment (Recommended)
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Solution 5: Upgrade pip first
```powershell
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

## Solution 6: Manual cleanup
If uvicorn.exe is locked:
1. Close all terminals and IDEs
2. Delete `C:\Python312\Scripts\uvicorn.exe` manually (if it exists)
3. Delete `C:\Python312\Scripts\uvicorn.exe.deleteme` (if it exists)
4. Try installing again


