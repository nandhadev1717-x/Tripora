# Tripora — AI-Powered Travel Agency

A college project built with Python, Flask, SQLite, Flask-SQLAlchemy, and Flask-Login.
It includes destination browsing, preference-based recommendations, customer accounts,
booking requests, booking history, and an admin dashboard.

## Requirements
- Python 3.10+
- VS Code (recommended)

## Run on Windows
1. Extract the ZIP and open the `Tripora` folder in VS Code.
2. Open Terminal → New Terminal.
3. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt and run:
   `venv\Scripts\activate.bat`
4. Install packages:
   `python -m pip install -r requirements.txt`
5. Start the app:
   `python run.py`
6. Open http://127.0.0.1:5000

## Demo admin
On first run, the app creates a demo admin:
- Email: `admin@tripora.local`
- Password: `TriporaAdmin123!`

Change this password and the `SECRET_KEY` before any public deployment. This is a college/demo project, not a production-ready booking/payment platform.

## AI recommendation note
The current recommender uses explainable preference scoring (budget, trip length, activities, and travel style). It does not call a paid AI API or claim to be a trained ML model. You can later extend it with real travel data and evaluated ML methods.

## Main features
- Responsive homepage and destination catalogue
- Register/login/logout
- Preference-based destination recommendations with match explanations
- Booking request form and customer booking history
- Admin dashboard for destinations and booking status
- SQLite database auto-created on first launch
