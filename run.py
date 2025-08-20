import subprocess
import time
import requests
import sys
import os

# Paths
VENV_PATH = r"C:\Users\thapa\Desktop\FootballHg\.venv\Scripts\activate.bat"
BACKEND_PATH = r"C:\Users\thapa\Desktop\FootballHg\FOOTECH--Football-Highlights-Generator-via-Commentary-Analysis\backend\app.py"
FRONTEND_PATH = r"C:\Users\thapa\Desktop\FootballHg\FOOTECH--Football-Highlights-Generator-via-Commentary-Analysis\frontend\main.py"

BACKEND_URL = "http://127.0.0.1:8000"
WAIT_TIME = 1  # seconds between retries
MAX_RETRIES = 30  # max wait 30 seconds

print(f"Backend script: {BACKEND_PATH}")
print(f"Frontend script: {FRONTEND_PATH}")

# Activate venv
print("Activating virtual environment...")
activate_command = f'cmd /k "{VENV_PATH}"'
# No need to run separately, just ensure python from venv is used
python_executable = os.path.join(os.path.dirname(VENV_PATH), "python.exe")

# Start backend
print("Starting backend...")
backend_process = subprocess.Popen(
    [python_executable, BACKEND_PATH],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Wait for backend to be ready
for i in range(MAX_RETRIES):
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            print("Backend is ready!")
            break
    except requests.exceptions.RequestException:
        pass
    print(f"Backend not ready, waiting {WAIT_TIME}s...")
    time.sleep(WAIT_TIME)
else:
    print("Backend did not start in time. Exiting.")
    backend_process.terminate()
    sys.exit(1)

# Print backend output in real-time
def print_output(proc):
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        print(f"[BACKEND] {line.strip()}")

import threading
threading.Thread(target=print_output, args=(backend_process,), daemon=True).start()

# Start frontend
print("Starting frontend...")
frontend_process = subprocess.Popen(
    [python_executable, FRONTEND_PATH],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

def print_frontend_output(proc):
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        print(f"[FRONTEND] {line.strip()}")

threading.Thread(target=print_frontend_output, args=(frontend_process,), daemon=True).start()

# Keep main script alive until both processes are running
try:
    while True:
        if backend_process.poll() is not None:
            print("Backend stopped.")
            frontend_process.terminate()
            break
        if frontend_process.poll() is not None:
            print("Frontend stopped.")
            backend_process.terminate()
            break
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping both processes...")
    backend_process.terminate()
    frontend_process.terminate()
