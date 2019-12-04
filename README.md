# TEST ROAD_ROUTER PROJECT AND CREATE INSTALLER

# Download and install VS Code: https://code.visualstudio.com/download

# Download and install Python 3.x: https://www.python.org/downloads/
# (select Add Python 3.x to PATH)

# Create folder in MS Explorer --> "Hello"
# Run VSCode
# Select VS Code --> File --> Add Folder to Workspace --> "Hello"
# Create file "hello.py" in folder Hello containing 'print("Hello World")'
# Press Ctrl-S to save file
# Right-click in file editor and select Run Python File in Terminal
# If Hello World does not appear in terminal see: https://code.visualstudio.com/docs/languages/python

# Open example project (road_router) folder in VSCode

# Download and install Git within VS Code when prompted
# Install the Python extension when prompted
# Status bar --> Select Python Interpreter --> Python 3.7.x 64-bit
# Install Linter pylint when prompted

# Install Python packages for road_router
pip install matplotlib
pip install dijkstar

# Run main.py in VSCode

# Create executable
pip install pyinstaller
pyinstaller --clean --onefile --windowed --distpath . --name road_router.exe main.py
# road_router.exe needs Input Data and Output Data as subfolders to work

# Install and run NSIS
# Compile road_router.nsi to install files to Desktop
