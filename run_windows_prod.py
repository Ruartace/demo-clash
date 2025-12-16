import os
import sys
import threading
import webbrowser
import time
from waitress import serve
from clashflow.wsgi import application

def run_backend():
    print("Starting Backend on port 8000...")
    # Setup environment variables for production simulation
    os.environ.setdefault("DJANGO_DEBUG", "False")
    # Add localhost to allowed hosts
    os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1 [::1]")
    
    # Run waitress server
    serve(application, host='0.0.0.0', port=8000)

def run_frontend():
    print("Starting Frontend (Vite Preview) on port 5173...")
    # This assumes you have run 'npm run build' first
    # We use 'npm run preview' to serve the built files
    os.system("cd frontend && npm run preview")

if __name__ == "__main__":
    print("=== Windows Production Simulator ===")
    print("1. Make sure you have run: cd frontend && npm run build")
    print("2. Make sure your PostgreSQL database is running")
    print("=======================================")

    # Start Backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Give backend a moment to start
    time.sleep(2)

    # Start Frontend (this will block the main thread usually, or we can run it in parallel)
    # Since 'npm run preview' is a long running process, we run it here.
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        sys.exit(0)
