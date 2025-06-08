## Setup Instructions

### 1. Install Python
- Download from [python.org](https://www.python.org/).
- Verify: `python --version`.

### 2. Clone or Set Up Project
- Place files in a directory (e.g., `C:\Users\bharg\OneDrive\Desktop\SVC Projects\two-factor-auth-system`).

### 3. Create Virtual Environment

python -m venv venv
.venv\Scripts\activate

### 4. Install Dependencies

-pip install -r requirements.txt

### 5. Configure Twilio
Sign up at twilio.com.
Get:
Account SID
Auth Token
Twilio Phone Number (e.g., +1234567890).

### Create .env in the project root:

TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
SECRET_KEY=your_random_secret_key  # e.g., "mysecret123"

### 6. Verify Phone Number (Trial Mode)
Go to twilio.com/user/account/phone-numbers/verified.
Add your number (e.g., +91868827XXXX) and verify it with the SMS code.

## How to Run
### Step 1: Activate Virtual Environment
.venv\Scripts\activate

### Step 2: Run the Application
python app.py

### Output:
Open http://127.0.0.1:5000 in your browser.