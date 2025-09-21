VENV_DIR=".venv"

if [[ -d "$VENV_DIR" ]]; then
  echo "Virtual environment '$VENV_DIR' exists."
else
  echo "Creating virtual environment '$VENV_DIR'."
  python3 -m venv "$VENV_DIR"
  echo "Virtual environment created."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Dependencies installed."
fi