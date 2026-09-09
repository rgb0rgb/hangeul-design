import os
import subprocess
import sys


def _project_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _python_path(here: str) -> str:
    if os.name == "nt":
        candidate = os.path.join(here, "venv", "Scripts", "python.exe")
    else:
        candidate = os.path.join(here, "venv", "bin", "python")
    if os.path.exists(candidate):
        return candidate
    if not getattr(sys, "frozen", False):
        return sys.executable
    raise RuntimeError("Python virtual environment not found. Run run.bat first to create venv.")


def main():
    here = _project_dir()
    app = os.path.join(here, "app_cinematic.py")
    if not os.path.exists(app):
        raise FileNotFoundError(f"App entry point not found: {app}")
    python_exe = _python_path(here)
    cmd = [
        python_exe,
        "-m",
        "streamlit",
        "run",
        app,
        "--server.address",
        "localhost",
        "--server.port",
        "8504",
        "--server.headless",
        "true",
    ]
    subprocess.Popen(cmd, cwd=here)


if __name__ == "__main__":
    main()
