# Medical Transcript Assistant

Example Project to demonstrate LLM to summarize medical exam transcription into a patient record

# Getting Started

```bash
# load .env vars (optional)
[ -f .env ] && while IFS= read -r line; do [[ $line =~ ^[^#]*= ]] && eval "export $line"; done < .env

# Create and activate a python virtual environment
# virtualenv \path\to\.venv -p path\to\specific_version_python.exe
python3 -m venv .venv
source .venv/bin/activate
# deactivate

# Install dependencies
pip install -r requirements_dev.txt
pre-commit install

# Run the tool
python main.py


# Testing
# Use pre-commit scripts to run all linting
pre-commit run --all-files

# Run a specific linter via pre-commit
pre-commit run --all-files codespell

# Run linters outside of pre-commit
codespell .
```
