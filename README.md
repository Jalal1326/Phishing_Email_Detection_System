# Phishing Email Detection System

This project is a machine learning-based tool designed to detect phishing emails. It uses Python and the Scikit-learn library to analyze the text content of an email and classify it as either "Phishing" or "Legitimate".

## Project Structure

The project directory should be set up as follows:

```
.
├── data/
│   └── Phishing_Email.csv
├── models/
│   ├── model.pkl
│   └── vectorizer.pkl
├── .gitignore
├── database.py
├── detect_phishing.py
├── README.md
├── requirements.txt
└── train_model.py
```

## Features

-   **Text Analysis**: Utilizes TF-IDF and n-grams to analyze email content.
-   **Machine Learning Model**: Employs a Random Forest Classifier for robust detection.
-   **Database Logging**: Saves every analysis result to an SQLite database for auditing.
-   **Command-Line Interface**: Easy-to-use CLI for analyzing emails in real-time.

---

## Setup and Installation

### Prerequisites

-   Python 3.8 or newer
-   `pip` and `venv` (usually included with Python)

### Step 1: Get the Code

Clone the repository to your local machine:

### Step 2: Download the Dataset

The model's performance depends entirely on the quality of its training data.

1.  **Download the dataset**: Go to the [Phishing Email Dataset on Kaggle](https://www.kaggle.com/datasets/subhajournal/phishingemails ).
2.  **Unzip the file**: The downloaded file will be `archive.zip`. Unzip it to find `Phishing_Email.csv`.
3.  **Place the dataset**: Move the `Phishing_Email.csv` file into the `data/` directory within your project folder.

### Step 3: Set Up Environment and Train the Model

Follow the instructions for your operating system.

#### For Windows (Using PowerShell)

Open PowerShell and navigate to the project's root directory. Run these commands one by one.

1.  **Create a virtual environment:**
    ```powershell
    python -m venv venv
    ```

2.  **Activate the virtual environment:**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
    *Note: If you get an error about script execution being disabled, run `Set-ExecutionPolicy Unrestricted -Scope Process` and try again.*

3.  **Install the required libraries:**
    ```powershell
    pip install -r requirements.txt
    ```

4.  **Run the training script:** This will train the model and save the necessary files in the `models/` directory.
    ```powershell
    python train_model.py
    ```

#### For Linux / macOS (Using Bash Terminal)

The `setup.sh` script automates the entire process.

1.  **Make the script executable (only needs to be done once):**
    ```bash
    chmod +x setup.sh
    ```

2.  **Run the setup script:**
    ```bash
    ./setup.sh
    ```
    This will create the virtual environment, install dependencies, and train the model automatically.

---

## How to Use the Detector

After a successful setup, you can use the `detect_phishing.py` script to analyze any email text.

**1. Activate the Virtual Environment (if not already active):**
   - On Windows: `.\venv\Scripts\Activate.ps1`
   - On Linux/macOS: `source venv/bin/activate`

**2. Run the Detector:**

Use the `--email` argument to pass the email text. Remember to enclose the text in double quotes.

#### Phishing Examples

```bash
python detect_phishing.py --email "urgent action required click here to secure your account and win a prize"

python detect_phishing.py --email "Security Alert: We noticed a suspicious sign-in from a new IP. Please verify your identity now by clicking here to prevent account lockout."

python detect_phishing.py --email "There was a problem with your last payment to Netflix. Your account is on hold. To avoid service interruption, please update your billing information now."
```

#### Legitimate Email Examples

```bash
python detect_phishing.py --email "Hi team, thanks for the productive meeting earlier. I've attached my notes as promised."

python detect_phishing.py --email "Hey Mike, are you going to be in the office tomorrow afternoon? I wanted to ask you a quick question about the new software update."
```

---

## Viewing Stored Results

Every analysis is logged to the `phishing_analysis.db` file. You can inspect its contents using any SQLite viewer or via the command line.

```bash
sqlite3 phishing_analysis.db "SELECT * FROM analysis_results;"
```

## File Descriptions

-   **`train_model.py`**: Loads the dataset, preprocesses the text, trains the Random Forest model, and saves the trained model and vectorizer to the `models/` directory.
-   **`detect_phishing.py`**: The main application script. Loads the saved model and provides a command-line interface for classifying new emails.
-   **`database.py`**: Contains functions to create and interact with the SQLite database for logging analysis results.
-   **`requirements.txt`**: A list of all the Python libraries required for the project.
-   **`setup.sh`**: A shell script to automate the setup process for Linux/macOS users.
