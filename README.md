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

pip install -r requirements_dev.txt
```