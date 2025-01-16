@echo off

REM Step 1: Create a virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

REM Step 2: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Step 3: Upgrade pip and install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Step 4: Run the Streamlit app
echo Starting the Streamlit app...
streamlit run app.py
