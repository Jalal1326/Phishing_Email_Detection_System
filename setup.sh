# for mac and linux only
echo "[SETUP] Starting the project setup..."

# Create virtual environment if missing
if [ ! -d "venv" ]; then
    echo "[SETUP] Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "[SETUP] Virtual environment already exists."
fi

source venv/bin/activate

echo "[SETUP] Installing dependencies..."
pip install -r requirements.txt

echo "[SETUP] Training the model..."
python train_model.py

echo ""
echo "[SETUP] --- Setup Complete! ---"
echo "Model saved to 'models/' directory."
echo "Activate with: source venv/bin/activate"
echo "Then run:"
echo "python detect_phishing.py --email \"Your email text here\""
