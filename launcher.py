import subprocess, sys, os
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    app = os.path.join(here, "app.py")
    cmd = [sys.executable, "-m", "streamlit", "run", app, "--server.address", "localhost", "--server.port", "8504"]
    subprocess.Popen(cmd, cwd=here)
if __name__ == "__main__":
    main()
