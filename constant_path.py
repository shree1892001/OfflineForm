from pathlib import Path
import sys
from pathlib import Path

# Determine the base directory based on whether the code is running as an executable
if getattr(sys, 'frozen', False):
    # If running as a packaged executable
    BASE_DIR = Path(sys._MEIPASS)
else:
    # If running as a .py file
    BASE_DIR = Path(__file__).resolve().parent

api_key_file_path = BASE_DIR / "KEYFILE.txt"
log_file_path = BASE_DIR / "Logging_file"
intents_file_path = BASE_DIR / "files"/"intents.json"
token_file_dir = BASE_DIR / "Token_file"
template_folder_path = BASE_DIR /"Templates"
offline_form_templates = BASE_DIR /"OfflineFormTemplates"
token_file_dir.mkdir(parents=True, exist_ok=True)

MS_GRAPH_JSON_PATH = token_file_dir / "ms_graph_api_token.json"
