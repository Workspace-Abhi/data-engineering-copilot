"""Automated setup script for Data Engineering Copilot."""
import os
import subprocess
import sys
import shutil
from pathlib import Path

# Fix encoding issue on Windows terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass



def run_command(command, description):
    """Run a shell command and print status."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Success")
        if result.stdout:
            print(result.stdout[:500])
        return True
    else:
        print(f"❌ Failed")
        print(result.stderr[:500])
        return False


def setup():
    """Run full setup."""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           Data Engineering Copilot - Setup                  ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)

    # Create virtual environment
    if not Path("venv").exists():
        run_command("python -m venv venv", "Creating virtual environment")

    # Activate and install dependencies
    if os.name == 'nt':  # Windows
        pip_path = "venv\Scripts\pip"
    else:  # Unix/Mac
        pip_path = "venv/bin/pip"

    run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies")

    # Create directories
    dirs = ["chroma_db", "logs", "samples/adf", "samples/jira", "samples/meetings", "samples/sql", "samples/databricks"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {d}")

    # Check Ollama
    print(f"\n{'='*60}")
    print("🔍 Checking Ollama installation")
    print(f"{'='*60}")

    result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Ollama installed: {result.stdout.strip()}")

        # Pull recommended models
        models = ["llama3.2", "nomic-embed-text"]
        for model in models:
            run_command(f"ollama pull {model}", f"Pulling model: {model}")
    else:
        print("⚠️  Ollama not found. Please install from https://ollama.ai")

    # Create .env file
    if not Path(".env").exists():
        shutil.copy(".env.example", ".env")
        print("📝 Created .env file from .env.example")

    print(f"\n{'='*60}")
    print("✅ Setup complete!")
    print(f"{'='*60}")
    print("\nTo start the application:")
    if os.name == 'nt':
        print("    venv\Scripts\streamlit run app.py")
    else:
        print("    source venv/bin/activate && streamlit run app.py")
    print("\nMake sure Ollama is running: ollama serve")


if __name__ == "__main__":
    setup()
