# Two-Factor Authentication System Using Flask and Twilio ![Flask-2FA System](https://img.shields.io/badge/Flask-2FA%2520System-blue)

A secure Two-Factor Authentication (2FA) system for web applications built with Flask and Twilio's SMS API. This project implements an additional security layer by requiring users to verify their login attempts with a one-time password (OTP) delivered to their mobile phones.

## Features

- **User Registration & Login**: Secure user accounts with username/password  
- **SMS-based 2FA**: One-Time Passwords sent via Twilio API  
- **reCAPTCHA Protection**: Google reCAPTCHA integration to prevent bot attacks  
- **Secure Password Storage**: Password hashing using Werkzeug security  
- **Session Management**: Secure handling of user sessions  
- **Profile Management**: Update password and phone number  
- **OTP Resend with Cooldown**: Prevent OTP spamming with 30-second cooldown  
---
## 🧱 System Architecture

![System Architecture](https://i.imgur.com/xyz123.png)

---

## ⚙️ Installation

### Prerequisites

- Python 3.8+
- A [Twilio](https://www.twilio.com/) account (for sending SMS OTPs)
- [Google reCAPTCHA](https://www.google.com/recaptcha/about/) site and secret keys
## 🔧 Setup
### Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Clone the repository:

```bash
git clone https://github.com/yourusername/flask-2fa-system.git
cd flask-2fa-system
```
### Install dependencies:

```bash
pip install -r requirements.txt
```
### Create a `.env` file and add your credentials:

```env
SECRET_KEY=your_secret_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
RECAPTCHA_SECRET_KEY=your_recaptcha_secret_key
```
### Initialize the database:

```bash
python
>>> from app import db, app
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```
### Run the application:

```bash
python app.py

