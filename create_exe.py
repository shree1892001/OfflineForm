import os
import sys
from pathlib import Path

# Base directory of your project
project_dir = Path(__file__).parent.resolve()

# Virtual environment paths
venv_dir = project_dir / "env" / "Lib" / "site-packages"

# Dependencies with dynamic paths
dependencies = [
    {
        "src": venv_dir / "en_core_web_sm" / "en_core_web_sm-3.8.0",
        "dest": "en_core_web_sm",
    },
    {
        "src": venv_dir / "contractions" / "data",
        "dest": "contractions/data",
    },
    {
        "src": venv_dir / "autocorrect" / "data",
        "dest": "autocorrect/data",
    },
    {
        "src": project_dir / "KEYFILE.txt",
        "dest": ".",
    },
    {
        "src": project_dir / "Logging_file",
        "dest": ".",
    },
    {
        "src": project_dir / "files",
        "dest": "files",
    },
]

# Main script
main_script = project_dir / "Main.py"

# Construct the pyinstaller command
pyinstaller_command = [
    "pyinstaller",
    "--onefile",
]

for dep in dependencies:
    pyinstaller_command.append(
        f'--add-data "{dep["src"]};{dep["dest"]}"'
    )

# Add the main script
pyinstaller_command.append(str(main_script))

# Print the generated command for debugging
command_str = " ".join(pyinstaller_command)
print("Generated PyInstaller command:")
print(command_str)
os.system(command_str)
